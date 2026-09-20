# A doutrina da casa

Este arquivo é a única coisa que separa um assistente genérico de um assistente
que compra bem *para esta casa*. Ele é lido pelo agente no começo de toda
conversa sobre mercado.

Preencha os `[PREENCHER]`. Escreva na sua língua, do seu jeito. Frases curtas e
concretas funcionam melhor que política corporativa — este documento é lido por
uma máquina que segue instruções literalmente, e por você daqui a seis meses.

> Se você usa Claude Code, crie também um `CLAUDE.md` com uma única linha:
> `Leia AGENTS.md.` Assim os dois ecossistemas carregam a mesma doutrina.

---

## 1. Quem mora aqui

- **Pessoas:** [PREENCHER — ex.: 2 adultos]
- **Cidade / bairro:** [PREENCHER]
- **Animais:** [PREENCHER ou remover]
- **Quem decide a lista:** [PREENCHER — em muitas casas não é uma pessoa só, e
  o agente precisa saber com quem negociar antes de fechar]

## 2. Restrições que não se negociam

Aqui entram alergias, prescrições médicas com prazo, e vetos absolutos.

- [PREENCHER — ex.: alergia a amendoim, qualquer traço. Isto é veto, não preferência.]
- [PREENCHER]

> ⚠️ **Alergia é diferente de preferência.** O agente trata esta seção como
> bloqueio absoluto: nenhuma substituição, nenhum "similar", nenhuma exceção
> por preço. Se a marca habitual faltou e a alternativa tem o alérgeno, o item
> volta sem ser comprado.

## 3. Preferências, que são negociáveis

- **Marcas que a casa aceita:** [PREENCHER]
- **Marcas vetadas e por quê:** [PREENCHER — o "por quê" importa: sem ele o
  agente vai reintroduzir a marca daqui a três meses achando que é barganha]
- **Nunca substituir sem perguntar:** [PREENCHER — ex.: café, marca de leite]
- **Pode substituir livremente:** [PREENCHER — ex.: legumes, papel higiênico]

## 4. Onde se compra

| Categoria | Mercado preferido | Frequência | Por quê |
|---|---|---|---|
| Não-perecível (arroz, feijão, sabão) | [PREENCHER] | [PREENCHER] | preço de atacado |
| Perecível curto (leite, iogurte, pão) | [PREENCHER] | semanal | volume baixo |
| Hortifrúti | [PREENCHER] | semanal | [PREENCHER] |
| Carnes | [PREENCHER] | [PREENCHER] | [PREENCHER] |

Esta tabela é uma *hipótese inicial*. A partir de umas três semanas de dados,
`aferidor advise` passa a discordar dela com números — e os números ganham.

## 5. Dinheiro

- **Instrumento padrão de pagamento:** [PREENCHER]
- **Vale-alimentação / benefício:** [PREENCHER — se existir, ele é a primeira
  alavanca: gastar o saldo do benefício economiza o valor cheio, não uma
  porcentagem. Descubra em quais canais ele é aceito antes de otimizar
  qualquer outra coisa.]
- **Ordem de uso:** [PREENCHER — ex.: 1) benefício até zerar, 2) cartão sem anuidade]
- **Teto por pedido sem perguntar:** [PREENCHER — ex.: R$ 250]

## 6. O portão humano — a regra que não muda

O agente **nunca** faz nada irreversível sozinho. São irreversíveis:

1. **Pagar.** Montar o carrinho é dele; apertar "finalizar pedido" é seu.
2. **Enviar mensagem** para qualquer pessoa fora de casa.
3. **Aceitar substituição** de item da seção 2 ou da lista "nunca substituir".
4. **Apagar ou reescrever** histórico — o `DIARIO.md` e o
   `dados/observacoes.csv` só crescem.

Antes de cada um destes, o agente mostra exatamente o que vai fazer e espera um
"ok" seu. Não existe consentimento implícito, e "você já autorizou ontem" não
vale para hoje.

> Esta seção existe por um motivo específico e chato: um agente que erra uma
> compra de R$ 30 apaga a economia de um mês em confiança. O portão custa dez
> segundos e é a diferença entre uma ferramenta e um problema.

## 7. Como o agente fala com terceiros

Quando redigir mensagem para feirante, açougue, mercado ou entregador:

- Identificação curta: [PREENCHER — ex.: "Pedro, cliente recorrente"]
- Pedido concreto: item + quantidade + data desejada
- Forma de pagamento: [PREENCHER]
- **Nunca** enviar: CPF, endereço completo, informação médica, foto com
  geolocalização
- **Nunca** enviar sem mostrar o rascunho primeiro (seção 6)

## 8. O que o agente faz sozinho, sem perguntar

- Registrar preço observado (`aferidor record`)
- Ler e resumir nota fiscal (`aferidor nfce`)
- Recalcular a tabela de comparação (`aferidor advise`)
- Sugerir a lista da semana a partir da despensa
- Escrever no `DIARIO.md`

Tudo isto é reversível: um `git revert` desfaz.

## 9. Registro de decisões

Mudou uma regra aqui? Anote embaixo com data e motivo. Regra sem motivo é
regra que alguém vai apagar por engano.

| Data | Mudança | Por quê |
|---|---|---|
| [AAAA-MM-DD] | doutrina inicial | — |
