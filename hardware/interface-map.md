# Mapa de interfaces físicas – ESP32 DevKit C (análise documental)

> Fonte: datasheet do ESP32 e esquemático da DevKit C. **Não houve acesso físico à placa**; a coluna "Observado na simulação" só deve ser preenchida com o que foi de fato visto.

| Interface | Pinos / acesso | O que permite | Observado na simulação | Contexto e proteções | Risco se acessível em produto |
|---|---|---|---|---|---|
| UART0 (console/boot log) | TX=GPIO1, RX=GPIO3 | Ler logs de boot; no firmware educacional, console `help/cfg/ota/reboot` sem autenticação | **Observada** na simulação: log da ROM + firmware (E01), console `help/cfg` (E02) | Sem senha no console do firmware | Atacante com acesso físico lê configuração e segredos |
| Modo de download (UART ROM) | GPIO0 em nível baixo + reset/EN | Gravar/ler flash via bootloader da ROM | Não simulada | Depende de eFuses/Flash Encryption | Substituição ou extração do firmware |
| JTAG | MTDI=GPIO12, MTCK=GPIO13, MTMS=GPIO14, MTDO=GPIO15 | Depuração em baixo nível, leitura de memória | Não simulada | Pode ser desabilitado por eFuse | Acesso a memória e controle da execução |
| Flash SPI externa/interna | GPIO6-11 (flash do módulo) | Armazena firmware e configuração | `.bin` analisado (ver `firmware/`) | Sem Flash Encryption no protótipo | Extração de firmware e segredos |
| Botões EN / BOOT | EN, GPIO0 | Reset e entrada em modo de download | Não simulada | — | Facilita acesso ao modo de download |
| I²C / SPI periféricos | (não usados neste projeto) | — | — | — | Fora do escopo |

## Conclusão
Das interfaces físicas do ESP32 DevKit C, apenas a UART0 pôde ser observada na simulação. Ela expõe o log de boot da ROM e um console de depuração sem autenticação (help, cfg, ota, reboot); o comando cfg imprime usuário e senha MQTT, URL de OTA e MAC em texto claro. Um atacante com acesso físico ao conector lê a configuração sem ferramentas especiais. JTAG (GPIO12-15), modo de download (GPIO0 + EN) e flash SPI foram analisados apenas de forma documental. Sem Flash Encryption e sem desabilitar JTAG e modo de download por eFuse, essas interfaces permitiriam extrair ou substituir o firmware em um produto real, o que agravaria o achado F01. Em produção, o console de debug deve ser removido e essas interfaces desabilitadas ou protegidas.
