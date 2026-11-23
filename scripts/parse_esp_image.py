#!/usr/bin/env python3
"""Le o cabecalho de uma imagem de aplicacao ESP32 (.bin) sem depender do esptool.
Uso: python3 scripts/parse_esp_image.py firmware/original/<arquivo>.bin
Complementa (nao substitui) a saida oficial do esptool image-info."""
import sys, struct, hashlib
d = open(sys.argv[1], "rb").read()
modes = {0: "QIO", 1: "QOUT", 2: "DIO", 3: "DOUT"}
sizes = {0: "1MB", 1: "2MB", 2: "4MB", 3: "8MB", 4: "16MB"}
freqs = {0: "40MHz", 1: "26MHz", 2: "20MHz", 0xF: "80MHz"}
if d[0] != 0xE9:
    sys.exit("Magic byte != 0xE9: nao e uma imagem de aplicacao ESP (pode ser flash completa).")
nseg, fmode, fsf = d[1], d[2], d[3]
print(f"tamanho_arquivo     : {len(d)} bytes")
print(f"segmentos           : {nseg}")
print(f"flash_mode          : {modes.get(fmode, hex(fmode))}")
print(f"flash_size / freq   : {sizes.get(fsf >> 4, '?')} / {freqs.get(fsf & 0xF, '?')}")
print(f"entry_point         : 0x{struct.unpack('<I', d[4:8])[0]:08X}")
print(f"chip_id             : 0x{struct.unpack('<H', d[12:14])[0]:04X} (0x0000 = ESP32)")
print(f"digest_sha256_anexado: {'sim' if d[23] else 'nao'}")
off = 24
for i in range(nseg):
    addr, size = struct.unpack("<II", d[off:off + 8])
    print(f"  seg{i}: load=0x{addr:08X} tamanho={size:>7} offset_dados=0x{off + 8:X} (esptool mostra o do cabecalho do segmento: 0x{off:X})")
    off += 8 + size
print(f"fim_dos_segmentos   : {off}")
print(f"bytes_apos_segmentos: {len(d) - off} (padding+checksum 1-16 B + digest 32 B; se houvesse assinatura Secure Boot v2 haveria ~1 KB a mais)")
ok = hashlib.sha256(d[:-32]).digest() == d[-32:]
print(f"sha256_anexado      : {d[-32:].hex()}")
print(f"sha256_confere      : {'SIM' if ok else 'NAO'} (verifica integridade, NAO autenticidade)")
print(f"descritor_app       : projeto={d[0x50:0x70].split(b'\0')[0].decode(errors='replace')} versao={d[0x30:0x50].split(b'\0')[0].decode(errors='replace')}")
