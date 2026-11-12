# Análise de comunicação (captura `.pcap` do Wokwi)

| Item | Observação |
|---|---|
| Protocolo(s) identificados | `[ ] ex.: DNS, TCP, MQTT 3.1.1` |
| Origem / destino | `[ ] IP do dispositivo (10.10.0.2 no gateway público) → broker` |
| Porta | `[ ] 1883` |
| Autenticação | `[ ] usuário/senha vão no pacote CONNECT?` |
| Criptografia (TLS) | `[ ]` |
| Informação transmitida | `[ ] JSON com device, mac, fw, temp, hum` |
| Identificadores expostos | `[ ] MAC, device_id, versão do firmware` |
| Mensagens de controle | `[ ] subscribe em .../cmd` |
| Integridade/autenticidade das mensagens | `[ ]` |

## Identificar ≠ avaliar
Identificar MQTT apenas diz *qual* protocolo é usado. Avaliar se é seguro exige verificar TLS, autenticação, autorização por tópico e proteção contra replay. `[ ] conclua para este caso`

## Nota sobre a simulação
O AP `Wokwi-GUEST` é aberto, então os quadros 802.11 aparecem sem cifra. Isso é característica do ambiente, **não** do produto; o foco da análise é a camada MQTT/TCP.

## Evidências
`network/evidence/`: `wokwi.pcap`, captura do pacote CONNECT, captura do PUBLISH.
