# Análise do firmware

## 1. Identificação e integridade
Ver `firmware/hashes.txt` (gerado por `scripts/analyze_firmware.sh`).
- Nome / tamanho / data / origem: `[ ]`
- SHA-256: `[ ]`
- Cópia de trabalho idêntica ao original: `[ ]`

## 2. Estrutura da imagem (`work/image_info.txt`)
`[ ] chip alvo, número de segmentos, endereço de entrada, checksum/hash anexado, flash size`

## 3. Informações relevantes (`work/strings_interesting.txt`)
| Item encontrado | Trecho (censure se real) | Relevância para segurança |
|---|---|---|
| Credencial MQTT | `[ ]` | `[ ]` |
| Host/porta do broker | `[ ]` | `[ ]` |
| URL de OTA (http://) | `[ ]` | `[ ]` |
| Mensagens de debug (`[DBG]`) | `[ ]` | `[ ]` |
| Bibliotecas / versões | `[ ]` | `[ ]` |

## 4. Atualização (OTA)
`[ ] O que o firmware faz: protocolo (HTTP), há verificação de assinatura/hash? (O fluxo é simulado: declare isso.)`

## 5. Limites
Não foi feita descompilação nem reconstrução do código-fonte.
