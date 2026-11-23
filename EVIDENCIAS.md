# Índice de evidências

| ID | Arquivo | O que prova | Achado |
|---|---|---|---|
| E01 | `hardware/evidence/E01-boot-serial.txt` | Boot completo (log da ROM e do firmware), com a senha MQTT impressa no log | F04, F03 |
| E01b | `hardware/evidence/E01b-bloco-dbg.png` | Print do bloco `[DBG]` com `mqtt_user`, `mqtt_pass` e `ota_url` | F01, F04 |
| E02 | `hardware/evidence/E02-comando-cfg.png` | Comandos `help` e `cfg` na UART, sem autenticação, devolvendo a configuração | F03, F01 |
| E03 | `firmware/hashes.txt`, `firmware/work/image_info_esptool.txt`, prints `firmware/work/E03a-hash-esptool.png` e `E03b-esptool-completo.png`; conferência em `image_info_manual.txt` | SHA-256 do `.bin` conferido no Windows (PowerShell), estrutura validada pelo esptool v5.6.0, ausência de assinatura, `Secure version: 0` | F05 |
| E04 | `firmware/work/strings_interesting.txt` | Credencial, broker, URL de OTA e mensagens de debug dentro do binário | F01, F05 |
| E05 | `network/evidence/E05-connect-wireshark.png` | Wireshark 4.6.9: 6 pacotes CONNECT (filtro `mqtt.msgtype == 1`); client ID, usuário e senha visíveis em texto claro | F02, F01 |
| E06 | `network/evidence/E06-publish-wireshark.png` | Wireshark 4.6.9: 28 pacotes PUBLISH (filtro `mqtt.msgtype == 3`); tópico e JSON da telemetria legíveis | F02 |
| E07 | `network/evidence/wokwi.pcap` | Captura 802.11 original do Wokwi | F02 |
| E07r | `network/evidence/pcap-summary.txt` | Resumo decodificado: CONNECT com usuário/senha e PUBLISH legíveis | F02, F01 |
