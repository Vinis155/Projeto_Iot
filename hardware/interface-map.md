# Mapa de interfaces físicas – ESP32 DevKit C (análise documental)

> Fonte: datasheet do ESP32 e esquemático da DevKit C. **Não houve acesso físico à placa**; a coluna "Observado na simulação" só deve ser preenchida com o que foi de fato visto.

| Interface | Pinos / acesso | O que permite | Observado na simulação | Contexto e proteções | Risco se acessível em produto |
|---|---|---|---|---|---|
| UART0 (console/boot log) | TX=GPIO1, RX=GPIO3 | Ler logs de boot; no firmware educacional, console `help/cfg/ota/reboot` sem autenticação | `[ ] E01: log serial no Wokwi` | Sem senha no console do firmware | Atacante com acesso físico lê configuração e segredos |
| Modo de download (UART ROM) | GPIO0 em nível baixo + reset/EN | Gravar/ler flash via bootloader da ROM | `[ ] não simulado` | Depende de eFuses/Flash Encryption | Substituição ou extração do firmware |
| JTAG | MTDI=GPIO12, MTCK=GPIO13, MTMS=GPIO14, MTDO=GPIO15 | Depuração em baixo nível, leitura de memória | `[ ] não simulado` | Pode ser desabilitado por eFuse | Acesso a memória e controle da execução |
| Flash SPI externa/interna | GPIO6-11 (flash do módulo) | Armazena firmware e configuração | `[ ] .bin analisado` | Sem Flash Encryption no protótipo | Extração de firmware e segredos |
| Botões EN / BOOT | EN, GPIO0 | Reset e entrada em modo de download | `[ ]` | — | Facilita acesso ao modo de download |
| I²C / SPI periféricos | (não usados neste projeto) | — | — | — | Fora do escopo |

## Conclusão (escreva com suas palavras)
`[ ] Evite "UART existe, logo é inseguro". Descreva: interface acessível + o que expõe + qual proteção falta + impacto para atacante com acesso físico.`
