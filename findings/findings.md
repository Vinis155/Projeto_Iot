# Achados e demonstração controlada

> As colunas "Impacto", "Probabilidade" e "Risco" abaixo são **sugestões iniciais**. Ajuste justificando com o contexto. Só mantenha um achado se tiver a evidência correspondente.

| ID | Achado | Evidência (arquivo) | Impacto | Probabilidade | Risco | Recomendação |
|---|---|---|---|---|---|---|
| F01 | Credenciais MQTT fixas no firmware, iguais em todos os dispositivos | `firmware/work/strings_interesting.txt`; `hardware/evidence/E01` | Alto (comprometimento da frota se uma extração ocorrer) | Média | Alto | Credenciais únicas por dispositivo, armazenamento protegido, Flash Encryption |
| F02 | MQTT sem TLS; usuário/senha e telemetria em texto claro | `network/evidence/E05` (CONNECT), `E06` (PUBLISH) | Alto | Média | Alto | MQTT sobre TLS (8883), certificados por dispositivo |
| F03 | Console de debug na UART sem autenticação, comando `cfg` imprime segredos | `hardware/evidence/E01`, `E02` | Médio-Alto (exige acesso físico) | Média | Médio | Remover/desabilitar console em produção, exigir autenticação |
| F04 | Logs de boot verbosos expõem MAC, versão, host e credenciais | `hardware/evidence/E01` | Médio | Média | Médio | Reduzir nível de log, não imprimir segredos |
| F05 | Fluxo OTA via HTTP sem verificação de assinatura (observado no código/strings; execução simulada) | `firmware/work/strings_interesting.txt`, log `[OTA]` | Alto | Baixa-Média | Médio-Alto | OTA por HTTPS + assinatura de firmware + Secure Boot + rollback |
| F06 | Comandos remotos via MQTT sem validação de origem (análise de código) | `simulation/wokwi/sketch.ino` | Médio | Média | Médio | Autenticação/ACL por tópico, comandos assinados |
| F07 | Interfaces físicas (UART, JTAG, modo de download) potencialmente acessíveis | `hardware/interface-map.md` (documental) | Depende de eFuses | Baixa-Média | `[ ]` | Desabilitar JTAG e modo de download em produção |

## Cadeia por achado (exemplo F01)
Evidência → Fragilidade → Ameaça → Impacto → Risco → Mitigação
`[ ] escreva a cadeia completa de pelo menos F01, F02 e F03`

## Demonstração controlada
**Objetivo:** mostrar que um segredo do dispositivo é obtido por três caminhos independentes.
1. Serial: digitar `cfg` no monitor serial → imprime `mqtt_user/mqtt_pass` (E02).
2. Rede: no `.pcap`, pacote MQTT CONNECT mostra usuário e senha em texto claro (E05).
3. Firmware: `strings` no `.bin` encontra os mesmos valores (strings_interesting.txt).

**Reprodução:** ver README, seção 9. **Escopo:** dispositivo simulado, credenciais fictícias, sem acesso a sistemas de terceiros.
