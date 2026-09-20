# Diário da aferidor

Registro append-only. **Nunca reescreva uma entrada antiga** — se mudou de
ideia, escreva uma entrada nova dizendo que mudou e por quê.

Isto parece burocracia até a primeira vez que você precisa responder "por que
paramos de comprar naquele mercado?" seis meses depois. A tabela de preços diz
*o que* aconteceu; o diário diz *por que* alguém decidiu aquilo.

Formato da seção: `## AAAA-MM-DD HH:mm — assunto`

---

## 2026-01-01 00:00 — repositório criado

Casa nova. Nenhuma observação ainda, nenhum mercado de referência definido.

Primeira meta: três semanas registrando preço de tudo que entra em casa, sem
mudar nada na rotina de compra. Sem essa linha de base não dá para afirmar que
qualquer coisa ficou mais barata — e "achei que economizei" não é um número.

Próxima ação: registrar a próxima compra com `aferidor record` ou, se veio nota
fiscal eletrônica, `aferidor nfce --importar`.
