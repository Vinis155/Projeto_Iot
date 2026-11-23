# NexaHome – Avaliação de Segurança do NexaSense (IoT)

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
Wokwi (simulador), `strings`, `sha256sum`, scripts Python próprios (`parse_esp_image.py`, `analyze_pcap.py`). esptool v5.6.0 (`image-info`). Wireshark 4.6.9 (prints E05 e E06).

## 6. Organização das evidências
| Pasta | Conteúdo |
|---|---|
| `architecture/` | Diagrama da arquitetura |
| `firmware/` | Imagem original (somente leitura), `hashes.txt`, saídas de análise em `work/`, `analysis-notes.md` |
| `hardware/` | `interface-map.md` e capturas da UART em `evidence/` |
| `network/` | `protocol-analysis.md`, `.pcap` e capturas em `evidence/` |
| `findings/` | `findings.md` (tabela de achados e demonstração controlada), `caso-real.md` (CVE-2019-15894) |
| `remediation/` | `hardening-plan.md` |
| `scripts/` | `analyze_firmware.sh` |

## 7. Resumos
- **Firmware:** imagem de aplicação ESP32 de 904.416 bytes (SHA-256 em `firmware/hashes.txt`), sem assinatura de Secure Boot. As strings revelam a credencial MQTT, o broker, a URL de OTA em HTTP e mensagens de debug.
- **Hardware:** só a UART foi observada na simulação (log da ROM e console `help/cfg` sem autenticação). JTAG, modo de download e flash foram analisados de forma documental.
- **Protocolos:** MQTT 3.1.1 na porta 1883, sem TLS. O PCAP mostra usuário e senha em texto claro nos pacotes CONNECT e a telemetria legível nos PUBLISH.

## 8. Principais achados e recomendações
F01 a F04 confirmados com evidência; F05 e F06 parciais (análise de código e strings, sem teste de ataque); F07 documental. Detalhes em `findings/findings.md`.

## 9. Como reproduzir
1. Criar um projeto ESP32 no Wokwi, montar o circuito (DHT22 → GPIO4) e colar `simulation/wokwi/sketch.ino` e `libraries.txt`.
2. Trocar `SEUNOME` nos tópicos MQTT e executar a simulação (capturar o log serial).
3. No editor: compilar e baixar o firmware (F1), salvar em `firmware/original/` e rodar `./scripts/analyze_firmware.sh firmware/original/<arquivo>.bin`.
4. Durante a simulação: ícone de Wi-Fi → *Download PCAP*; abrir no Wireshark (filtros `mqtt`, `mqtt.msgtype == 1`).

> Credenciais usadas são fictícias. Não publique segredos reais neste repositório.
