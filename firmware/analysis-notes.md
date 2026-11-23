# Análise do firmware

## 1. Identificação e integridade
Gerado por `scripts/analyze_firmware.sh` (ver `firmware/hashes.txt`).
| Item | Valor |
|---|---|
| Arquivo | `firmware-esp32.bin` |
| Tamanho | 904.416 bytes |
| SHA-256 | `ab7c5a880988dd8fc9407f45904bf3bdf89ba1d26d8fd79ea84f67d160c2db13` |
| Origem | Wokwi (simulador online): F1 > Download Firmware, após compilar o projeto. Projeto: https://wokwi.com/projects/480483846150517761 |
| Cópia de trabalho idêntica | Sim (mesmo SHA-256) |
| Original preservado | `firmware/original/` (somente leitura) |

## 2. Estrutura da imagem
Fonte oficial: `firmware/work/image_info_esptool.txt` (comando `esptool image-info`, esptool v5.6.0; prints `E03a-hash-esptool.png` e `E03b-esptool-completo.png`, E03). Conferido contra a leitura manual do cabeçalho (`firmware/work/image_info_manual.txt`, `scripts/parse_esp_image.py`): entrada, número e tamanho dos segmentos, endereços de carga, flash e hash anexado coincidem. A única diferença é o rótulo de offset: o esptool mostra o início do cabeçalho de cada segmento e o script mostrava o início dos dados (8 bytes depois).
- Tipo: **imagem de aplicação** ESP32 (magic 0xE9), não a flash completa (sem bootloader nem tabela de partições).
- 6 segmentos; ponto de entrada `0x40081BCC`; chip_id 0x0000 (ESP32); flash DIO, 4 MB, 80 MHz.
- Maior segmento de código: ~676 KB em `0x400D0020` (IROM/código da aplicação).
- Descritor da aplicação: projeto `arduino-lib-builder`, versão `6671d0b`, IDF v5.5.5, compilado em 16/09/2026. **Esses valores descrevem o core Arduino-ESP32 usado, não o código do NexaSense.**
- Os 32 bytes finais são um SHA-256 de **integridade**, e confere com o recalculado. Não há nenhum dado depois dele; um bloco de assinatura do Secure Boot v2 deixaria ~1 KB adicional. **Conclusão: a imagem não está assinada.**
- O `esptool` confirma: checksum `0xe3` válido, *validation hash* válido, ELF SHA-256 `ceee7b9b…e49b3`, ESP-IDF v5.5.5 e 6 segmentos (DROM, DRAM, IROM, IRAM, RTC_DATA). Sua saída não lista nenhum bloco de assinatura de Secure Boot, o que confere com a conclusão acima.
- `Secure version: 0`: o descritor da aplicação não traz número de versão de segurança, compatível com a ausência de proteção anti-rollback na OTA. Isso **não prova** que o recurso esteja desabilitado na configuração do bootloader, que não foi analisado.

## 3. Informações relevantes (`firmware/work/strings_interesting.txt`)
| Item | Trecho encontrado | Relevância |
|---|---|---|
| Credencial MQTT | usuário `nexasense`, senha `Nexa@2024-lab` (fictícia) | Segredo em texto claro no binário, o mesmo em todos os dispositivos (F01) |
| Broker | `broker.hivemq.com` (porta 1883 no código) | Aponta o destino da telemetria; sem TLS (F02) |
| Rede Wi-Fi | `Wokwi-GUEST` | Característica da simulação |
| Identificadores | `nexasense-001`, tópicos `nexahome-lab/.../telemetry` e `.../cmd` | Identificação previsível do dispositivo e canal de comando (F06) |
| URL de OTA | `http://updates.nexahome.lab/nexasense/latest.bin` | Atualização por HTTP, sem TLS (F05) |
| Mensagens de debug | blocos `[DBG]` com `mqtt_pass = %s`, `ota_url = %s`, comandos `help/cfg/ota/reboot` | Console de debug e vazamento de segredos nos logs (F03, F04) |
| Mensagens de OTA | "sem verificar assinatura/hash (simulado)" | Fluxo sem verificação de integridade/autenticidade (F05) |
| Versão | `0.3.1-proto` | Build de desenvolvimento em uso |

## 4. Atualização (OTA)
O firmware contém a URL `http://` e mensagens indicando que a imagem seria gravada sem verificar assinatura ou hash. **O fluxo é simulado no código (nenhuma requisição real é feita).** A conclusão sobre o F05 vem da leitura das strings e do código-fonte, não de um teste de rede.

## 5. Limites
- Não foi feita descompilação nem reconstrução do código-fonte.
- Análise estática de uma imagem de aplicação; bootloader, partições e eFuses não foram avaliados.
- As strings `Nexa@2024-lab` etc. são fictícias, criadas para este exercício.
