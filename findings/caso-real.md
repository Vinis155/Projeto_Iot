# Caso real

## CVE-2019-15894: falha no Secure Boot do ESP32 por injeção de falhas

Um atacante que use injeção de falhas para perturbar fisicamente a CPU do ESP32 consegue contornar a verificação do digest do Secure Boot na inicialização e executar código não verificado a partir da flash. Se o dispositivo não usa Flash Encryption, o ataque bem-sucedido permite execução arbitrária de código. O problema foi reportado à Espressif por analistas da Riscure e, de forma independente, por LimitedResults, e o aviso oficial saiu em 3 de setembro de 2019. A recomendação foi combinar Secure Boot com Flash Encryption e atualizar o firmware para habilitar a Flash Encryption de forma permanente.

## Relação com o projeto

O NexaSense v0.3.1 tem imagem sem assinatura (F05) e o estado dos eFuses não foi avaliado (F07). O caso mostra que o acesso físico é um vetor realista contra ESP32 e que o Secure Boot sozinho não basta: a defesa precisa de camadas (Secure Boot, Flash Encryption e redução das interfaces físicas), exatamente o que o plano de hardening propõe.

## Fontes
- Espressif Security Advisory Concerning Fault Injection and Secure Boot: https://www.espressif.com/en/news/Espressif_Security_Advisory_Concerning_Fault_Injection_and_Secure_Boot
- NVD, CVE-2019-15894: https://nvd.nist.gov/vuln/detail/cve-2019-15894
