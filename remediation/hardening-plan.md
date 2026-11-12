# Plano de hardening – versão comercial do NexaSense

> Medidas com eFuse são **irreversíveis**; foram analisadas só conceitualmente. Confira os nomes e requisitos na documentação ESP-IDF da Espressif para a revisão de chip escolhida.

| Prioridade | Medida | Achado tratado | Referência |
|---|---|---|---|
| P1 | MQTT sobre TLS com certificado por dispositivo (mTLS) e ACL por tópico | F02, F06 | NIST IR 8259A (proteção de dados); ETSI EN 303 645 (comunicação segura) |
| P1 | Credenciais únicas por dispositivo, provisionadas na fabricação; sem segredos no código | F01 | ETSI EN 303 645 (sem senhas universais; armazenamento seguro de parâmetros) |
| P1 | Secure Boot + assinatura de firmware | F05 | ESP-IDF Security; ETSI (integridade de software) |
| P1 | OTA por HTTPS, imagem assinada, versionamento anti-rollback e recuperação em falha | F05 | NIST IR 8259A (atualização de software); ETSI (manter software atualizado) |
| P2 | Flash Encryption e armazenamento protegido de parâmetros (NVS cifrado) | F01, F07 | ESP-IDF Security; MITRE EMB3D (extração de firmware) |
| P2 | Desabilitar JTAG e restringir o modo de download UART em produção | F07 | MITRE EMB3D (interfaces privilegiadas expostas) |
| P2 | Remover console de debug ou protegê-lo; reduzir nível de log | F03, F04 | ETSI (minimizar superfície de ataque) |
| P3 | Processo de gestão de vulnerabilidades e documentação da superfície de ataque | — | ETSI EN 303 645; OWASP ISTG |

## Ordem de implantação sugerida
`[ ] justifique em 3-4 linhas por que P1 vem primeiro (impacto x esforço)`
