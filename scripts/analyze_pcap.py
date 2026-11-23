#!/usr/bin/env python3
"""Resume uma captura PCAP 802.11 do Wokwi (Wi-Fi aberto) sem depender do Wireshark.
Decodifica 802.11 -> LLC/SNAP -> IPv4 -> TCP/UDP -> DNS e MQTT 3.1.1.
Uso: python3 scripts/analyze_pcap.py network/evidence/wokwi.pcap
Complementa o Wireshark; a evidencia visual (prints) continua sendo do Wireshark."""
import sys, struct, collections, datetime

PKT_TYPES = {1: "CONNECT", 2: "CONNACK", 3: "PUBLISH", 4: "PUBACK", 8: "SUBSCRIBE",
             9: "SUBACK", 12: "PINGREQ", 13: "PINGRESP", 14: "DISCONNECT"}


def read_pcap(path):
    d = open(path, "rb").read()
    magic = d[:4]
    if magic == b"\x4d\x3c\xb2\xa1":
        endian, div = "<", 1e9      # nanosegundos
    elif magic == b"\xd4\xc3\xb2\xa1":
        endian, div = "<", 1e6      # microsegundos
    else:
        sys.exit("Formato de PCAP nao suportado (use .pcap, nao .pcapng)")
    linktype = struct.unpack(endian + "I", d[20:24])[0]
    off, pkts = 24, []
    while off + 16 <= len(d):
        s, f, cap, orig = struct.unpack(endian + "IIII", d[off:off + 16])
        pkts.append((s + f / div, d[off + 16:off + 16 + cap]))
        off += 16 + cap
    return linktype, pkts


def dot11_payload(fr):
    """Retorna (tipo, subtipo, addr1, addr2, addr3, payload_LLC) para quadros de dados."""
    if len(fr) < 24:
        return None
    fc = struct.unpack("<H", fr[:2])[0]
    ftype, sub = (fc >> 2) & 3, (fc >> 4) & 0xF
    if ftype != 2:
        return ftype, sub, None, None, None, None
    hdr = 24
    if sub & 0x8:       # QoS
        hdr += 2
    if fc & 0x8000:     # campo Order (HT control)
        hdr += 4
    mac = lambda b: ":".join(f"{x:02x}" for x in b)
    return ftype, sub, mac(fr[4:10]), mac(fr[10:16]), mac(fr[16:22]), fr[hdr:]


def dns_name(b, o):
    labels = []
    while o < len(b) and b[o]:
        if b[o] & 0xC0 == 0xC0:
            ptr = ((b[o] & 0x3F) << 8) | b[o + 1]
            n, _ = dns_name(b, ptr)
            labels.append(n)
            return ".".join(labels), o + 2
        ln = b[o]
        labels.append(b[o + 1:o + 1 + ln].decode(errors="replace"))
        o += 1 + ln
    return ".".join(labels), o + 1


def parse_mqtt(p):
    out = []
    while len(p) >= 2:
        t = p[0] >> 4
        mult, ln, i = 1, 0, 1
        while i < len(p):
            b = p[i]; ln += (b & 0x7F) * mult; i += 1
            if not b & 0x80:
                break
            mult *= 128
        body = p[i:i + ln]
        out.append((t, p[0] & 0xF, body))
        p = p[i + ln:]
    return out


def u16s(b, o):
    n = struct.unpack(">H", b[o:o + 2])[0]
    return b[o + 2:o + 2 + n].decode(errors="replace"), o + 2 + n


def main(path):
    linktype, pkts = read_pcap(path)
    print(f"arquivo: {path} | linktype={linktype} (105 = IEEE 802.11) | quadros={len(pkts)}")
    if pkts:
        t0, t1 = pkts[0][0], pkts[-1][0]
        print(f"duracao: {t1 - t0:.1f} s (timestamps do Wokwi sao relativos ao inicio da simulacao)")
    kinds = collections.Counter()
    ips, dns, mqtt_kinds = collections.Counter(), [], collections.Counter()
    connects, publishes, subs = [], [], []
    flows = collections.Counter()
    for ts, fr in pkts:
        r = dot11_payload(fr)
        if not r:
            kinds["curto/invalido"] += 1; continue
        ftype, sub, a1, a2, a3, llc = r
        kinds[{0: "gerenciamento", 1: "controle", 2: "dados"}.get(ftype, "?")] += 1
        if llc is None or len(llc) < 8 or llc[:3] != b"\xaa\xaa\x03":
            continue
        ethertype = struct.unpack(">H", llc[6:8])[0]
        ip = llc[8:]
        if ethertype != 0x0800 or len(ip) < 20:
            kinds[f"eth 0x{ethertype:04x}"] += 1; continue
        ihl = (ip[0] & 0xF) * 4
        proto = ip[9]
        src = ".".join(map(str, ip[12:16])); dst = ".".join(map(str, ip[16:20]))
        l4 = ip[ihl:]
        if proto == 6 and len(l4) >= 20:
            sp, dp = struct.unpack(">HH", l4[:4])
            doff = (l4[12] >> 4) * 4
            pl = l4[doff:]
            flows[f"TCP {src}:{sp} -> {dst}:{dp}"] += 1
            if 1883 in (sp, dp) and pl:
                for t, flags, body in parse_mqtt(pl):
                    mqtt_kinds[PKT_TYPES.get(t, str(t))] += 1
                    try:
                        if t == 1:
                            proto_name, o = u16s(body, 0)
                            level, cflags = body[o], body[o + 1]
                            o += 4
                            cid, o = u16s(body, o)
                            user = pwd = None
                            if cflags & 0x04:     # will
                                _, o = u16s(body, o); n = struct.unpack(">H", body[o:o + 2])[0]; o += 2 + n
                            if cflags & 0x80:
                                user, o = u16s(body, o)
                            if cflags & 0x40:
                                pwd, o = u16s(body, o)
                            connects.append((ts, src, dst, proto_name, level, cid, user, pwd))
                        elif t == 3:
                            topic, o = u16s(body, 0)
                            if (flags >> 1) & 3:
                                o += 2
                            publishes.append((ts, src, dst, topic, body[o:].decode(errors="replace")))
                        elif t == 8:
                            o = 2
                            topic, _ = u16s(body, o)
                            subs.append((ts, src, topic))
                    except Exception as e:
                        mqtt_kinds[f"erro_parse({e})"] += 1
        elif proto == 17 and len(l4) >= 8:
            sp, dp = struct.unpack(">HH", l4[:4])
            pl = l4[8:]
            flows[f"UDP {src}:{sp} -> {dst}:{dp}"] += 1
            if dp == 53 and len(pl) > 12:
                qn, _ = dns_name(pl, 12)
                dns.append((ts, src, qn))
            if sp == 53 and len(pl) > 12:
                qn, o = dns_name(pl, 12)
                an = struct.unpack(">H", pl[6:8])[0]
                ips[f"resposta DNS {qn} ({an} registros)"] += 1
        else:
            flows[f"IP proto {proto} {src} -> {dst}"] += 1

    print("\n== Tipos de quadro 802.11 ==")
    for k, v in kinds.most_common():
        print(f"  {k}: {v}")
    print("\n== Fluxos (top 12) ==")
    for k, v in flows.most_common(12):
        print(f"  {v:>4}  {k}")
    print("\n== DNS consultado ==")
    for n in sorted({n for _, _, n in dns}):
        print("  ", n)
    for k, v in ips.items():
        print("  ", k)
    print("\n== MQTT: contagem por tipo ==")
    for k, v in mqtt_kinds.most_common():
        print(f"  {k}: {v}")
    print("\n== MQTT CONNECT (texto claro) ==")
    for c in connects:
        print(f"  t={c[0] - pkts[0][0]:.1f}s {c[1]} -> {c[2]} proto={c[3]} v{c[4]} client_id={c[5]!r} user={c[6]!r} password={c[7]!r}")
    print("\n== MQTT SUBSCRIBE ==")
    for s in subs[:5]:
        print(f"  t={s[0] - pkts[0][0]:.1f}s {s[1]} topico={s[2]!r}")
    print(f"\n== MQTT PUBLISH (total {len(publishes)}; primeiros 3 e ultimo) ==")
    for p in publishes[:3] + publishes[-1:]:
        print(f"  t={p[0] - pkts[0][0]:.1f}s {p[1]} -> {p[2]} topico={p[3]!r}\n      payload={p[4]}")


if __name__ == "__main__":
    main(sys.argv[1])
