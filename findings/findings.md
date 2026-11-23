# Achados e demonstração controlada

> Impacto, probabilidade e risco são **sugestões iniciais**; ajuste justificando com o contexto do produto.

| ID | Achado | Evidência | Status | Impacto | Prob. | Risco | Recomendação |
|---|---|---|---|---|---|---|---|
| F01 | Credenciais MQTT fixas no firmware, iguais em todo dispositivo | `firmware/work/strings_interesting.txt` (senha no binário); `hardware/evidence/E02-comando-cfg.png`; `pcap-summary.txt` | **Confirmado** (3 fontes) | Alto | Média | Alto | Credenciais únicas por dispositivo, armazenamento protegido, Flash Encryption |
| F02 | MQTT sem TLS: usuário/senha e telemetria em texto claro | `network/evidence/wokwi.pcap`, `pcap-summary.txt` (6 CONNECT, 28 PUBLISH), `E05-connect-wireshark.png`, `E06-publish-wireshark.png` | **Confirmado** | Alto | Média | Alto | MQTT sobre TLS (8883), certificado por dispositivo |
| F03 | Console de debug na UART sem autenticação; `cfg` imprime segredos | `hardware/evidence/E02-comando-cfg.png`, `E01b-bloco-dbg.png` | **Confirmado** (na simulação) | Médio-Alto (exige acesso físico) | Média | Médio | Remover/proteger o console em produção |
| F04 | Logs verbosos expõem MAC, versão, host e **senha** (`[MQTT] Conectando ... pass=...`) | `hardware/evidence/E01-boot-serial.txt` | **Confirmado** | Médio | Média | Médio | Reduzir nível de log, não imprimir segredos |
| F05 | Fluxo OTA via HTTP sem verificação de assinatura | URL `http://` e mensagens `[OTA]` em `strings_interesting.txt`; imagem sem assinatura (`firmware/analysis-notes.md`, seção 2) | **Parcial**: fluxo simulado no código, nenhuma atualização real foi testada | Alto | Baixa-Média | Médio-Alto | OTA por HTTPS, firmware assinado, Secure Boot, rollback |
| F06 | Comandos remotos via MQTT sem validação de origem | `sketch.ino` (callback `onMessage`); SUBSCRIBE em `.../cmd` no PCAP | **Parcial**: análise de código, sem teste de envio | Médio | Média | Médio | ACL por tópico, comandos assinados |
| F07 | Interfaces físicas (UART, JTAG, modo de download) potencialmente acessíveis | `hardware/interface-map.md` (documental); UART observada em E01/E02 | **Documental** (só a UART foi observada) | Depende de eFuses | Baixa-Média | Médio (depende dos eFuses, não avaliados) | Desabilitar JTAG e modo de download em produção |

## Cadeia por achado (exemplo F02)
- **Evidência:** `pcap-summary.txt` mostra 6 CONNECT com `user='nexasense' password='Nexa@2024-lab'` e 28 PUBLISH legíveis na porta 1883.
- **Fragilidade:** MQTT sem TLS e sem proteção da credencial em trânsito.
- **Ameaça:** atacante com acesso ao caminho de rede captura as credenciais e a telemetria.
- **Impacto:** vazamento de dados e uso da credencial para se passar pelo dispositivo.
- **Risco:** alto, porque a credencial é fixa e idêntica em todos os dispositivos (F01).
- **Mitigação:** TLS com certificado por dispositivo e ACL por tópico no broker.

### Cadeia F01
- Evidência: a senha `Nexa@2024-lab` aparece em strings_interesting.txt, no E02-comando-cfg.png e no pacote CONNECT do PCAP.
- Fragilidade: credencial MQTT fixa no firmware, idêntica em todos os dispositivos, sem proteção de armazenamento.
- Ameaça: quem obtiver um único dispositivo ou binário (extração da flash, strings ou captura de tráfego) obtém a credencial de toda a frota.
- Impacto: acesso ao broker como se fosse qualquer dispositivo, com leitura e publicação de telemetria e comandos.
- Risco: alto.
- Mitigação: credencial única por dispositivo provisionada na fabricação, Flash Encryption e NVS cifrado, revogação individual.

### Cadeia F03
- Evidência: E02-comando-cfg.png e E01b-bloco-dbg.png.
- Fragilidade: console de debug na UART0 sem autenticação, que imprime segredos.
- Ameaça: pessoa com acesso físico ao dispositivo (instalação, descarte, revenda) conecta-se à serial.
- Impacto: obtém credenciais MQTT, URL de OTA e identificadores, o que facilita os ataques ligados a F01 e F02.
- Risco: médio (exige acesso físico, mas o ataque é trivial).
- Mitigação: remover o console em produção ou exigir autenticação, não imprimir segredos, reduzir o nível de log.

## Demonstração controlada
**Objetivo:** mostrar que o mesmo segredo do dispositivo é obtido por três caminhos independentes.
1. **Serial (UART):** os comandos `help` e `cfg` no monitor serial imprimem `mqtt_user` e `mqtt_pass` sem autenticação (`E02-comando-cfg.png`).
2. **Rede:** o `.pcap` mostra o pacote MQTT CONNECT com o mesmo usuário e senha em texto claro (`E05-connect-wireshark.png`, `pcap-summary.txt`).
3. **Firmware:** `strings` no `.bin` encontra os mesmos valores (`strings_interesting.txt`).

**Escopo:** dispositivo simulado, credenciais fictícias, broker MQTT público de testes, sem ataque a sistemas de terceiros.
**Reprodução:** README, seção 9.
