# NexaHome – Avaliação de Segurança do NexaSense (IoT)

> **Preencha os trechos marcados com `[ ]` depois de executar os testes. Não deixe nada que você não tenha executado.**

## 1. Objetivo
Avaliar a superfície de ataque do protótipo NexaSense (ESP32 + sensor de temperatura/umidade + Wi-Fi/MQTT), cobrindo hardware, firmware, comunicação e acesso físico, e propor mitigações e hardening para uma versão comercial.

## 2. Dispositivo analisado
- Plataforma: ESP32 DevKit C (Xtensa LX6) com sensor DHT22 no GPIO4.
- Firmware: `simulation/wokwi/sketch.ino` (firmware educacional v0.3.1-proto).
- **Ambiente: SIMULADO no Wokwi** (sem placa física). Ver seção 3.

## 3. Escopo e limitações
- O hardware foi **simulado** no Wokwi por indisponibilidade de equipamento físico. O firmware, o `.bin`, os hashes, o log serial e a captura `.pcap` são **reais**, gerados a partir da simulação.
- A análise das interfaces físicas (UART, JTAG, SPI flash, BOOT/EN) é **documental** (datasheet e esquemático da ESP32 DevKit C); não houve acesso a pinos reais.
- O tráfego foi gerado pelo dispositivo simulado para um broker MQTT público de testes, usando **apenas dados e credenciais fictícios**. Nenhum serviço de terceiros foi atacado ou sondado.
- O SSID da simulação é aberto (`Wokwi-GUEST`); a exposição no nível Wi-Fi não deve ser atribuída ao produto.
- Mecanismos irreversíveis (eFuses) foram analisados apenas conceitualmente.

## 4. Arquitetura
Ver `architecture/architecture-diagram.png`.

## 5. Ferramentas utilizadas
Wokwi (simulador), Wireshark, esptool, `strings`, `sha256sum`, binwalk (opcional). `[ ] ajuste conforme o que usou`

## 6. Organização das evidências
| Pasta | Conteúdo |
|---|---|
| `architecture/` | Diagrama da arquitetura |
| `firmware/` | Imagem original (somente leitura), `hashes.txt`, saídas de análise em `work/`, `analysis-notes.md` |
| `hardware/` | `interface-map.md` e capturas da UART em `evidence/` |
| `network/` | `protocol-analysis.md`, `.pcap` e capturas em `evidence/` |
| `findings/` | `findings.md` (tabela de achados e demonstração controlada) |
| `remediation/` | `hardening-plan.md` |
| `scripts/` | `analyze_firmware.sh` |

## 7. Resumos
- **Firmware:** `[ ] 3-5 linhas com o que encontrou (formato, strings relevantes, URL de OTA)`
- **Hardware:** `[ ] 3-5 linhas`
- **Protocolos:** `[ ] 3-5 linhas`

## 8. Principais achados e recomendações
`[ ] copie o resumo da tabela de findings/findings.md`

## 9. Como reproduzir
1. Criar um projeto ESP32 no Wokwi, montar o circuito (DHT22 → GPIO4) e colar `simulation/wokwi/sketch.ino` e `libraries.txt`.
2. Trocar `SEUNOME` nos tópicos MQTT e executar a simulação (capturar o log serial).
3. No editor: compilar e baixar o firmware (F1), salvar em `firmware/original/` e rodar `./scripts/analyze_firmware.sh firmware/original/<arquivo>.bin`.
4. Durante a simulação: ícone de Wi-Fi → *Download PCAP*; abrir no Wireshark (filtros `mqtt`, `mqtt.msgtype == 1`).

> Credenciais usadas são fictícias. Não publique segredos reais neste repositório.
