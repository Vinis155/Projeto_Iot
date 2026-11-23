# Análise de comunicação (captura `wokwi.pcap`)

Fonte: `network/evidence/wokwi.pcap` (1.759 quadros 802.11, ~148 s de simulação) e `network/evidence/pcap-summary.txt`, gerado por `scripts/analyze_pcap.py`.
Prints do Wireshark 4.6.9: `network/evidence/E05-connect-wireshark.png` (filtro `mqtt.msgtype == 1`, 6 pacotes CONNECT) e `network/evidence/E06-publish-wireshark.png` (filtro `mqtt.msgtype == 3`, 28 pacotes PUBLISH).

| Item | Observação (verificada no PCAP) |
|---|---|
| Protocolos identificados | 802.11 (rede aberta simulada), ARP, DNS, TCP e **MQTT 3.1.1** (nível de protocolo 4) |
| Origem / destino | `10.10.0.2` (dispositivo) → IPs de `broker.hivemq.com`: `18.197.179.222`, `63.185.133.90`, `3.68.133.207` (o DNS devolveu 3 registros) |
| Porta | TCP **1883** (MQTT sem TLS) |
| Autenticação | Cada pacote **CONNECT** carrega `client_id=nexasense-001`, `user=nexasense` e `password=Nexa@2024-lab` **em texto claro**. Foram 6 CONNECT em 148 s |
| Criptografia (TLS) | Ausente: o conteúdo MQTT aparece legível |
| Informação transmitida | 28 PUBLISH no tópico `nexahome-lab/Vinis/nexasense-001/telemetry`, com JSON `{"device","mac","fw","temp","hum"}` a cada ~5 s |
| Identificadores expostos | device_id, **MAC** do dispositivo e **versão do firmware** no payload; client_id fixo |
| Mensagens de controle | SUBSCRIBE no tópico `nexahome-lab/Vinis/nexasense-001/cmd` (canal de comandos remotos `reboot`/`ota`) |
| Integridade/autenticidade das mensagens | Nada observado: sem assinatura ou HMAC no payload nem identificação da origem dos comandos |
| Consulta DNS | `broker.hivemq.com`, em texto claro |

## Identificar ≠ avaliar
Identificar MQTT só diz *qual* protocolo é usado. Para avaliar a segurança, o que importa é: sem TLS, as credenciais e a telemetria trafegam legíveis (F02); a credencial é a mesma em qualquer dispositivo com este firmware (F01); e o canal `cmd` não mostra autenticação da origem dos comandos (F06, **hipótese de projeto, não testada**).

## Observações
- **Reconexões:** houve 6 CONNECT em ~148 s, com troca de IP do broker. Possível causa: o `client_id` fixo `nexasense-001` pode colidir com outros clientes no broker público, ou a política do broker. **Não foi verificado**; registre como observação, não como achado.
- **Simulação:** o AP `Wokwi-GUEST` é aberto, então os quadros 802.11 aparecem sem cifra. Isso é característica do ambiente, **não** do produto; a análise se concentra em MQTT/TCP.
- Os timestamps do PCAP são relativos ao início da simulação.
