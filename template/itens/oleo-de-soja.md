---
item: Óleo de soja
unidade_base: L
marca_padrao: Liza
marcas_substitutas: [Soya, Concordia, Coamo]
mercado_atual: mercado-do-bairro
ponto_de_recompra: 1
pode_substituir: sim
tags: [exemplo, mercearia]
---

# Óleo de soja

> Item de exemplo. Apague este arquivo quando começar a registrar os seus.

**Este é o item mais importante do template.** Ele existe para mostrar o erro
que o método inteiro foi construído para evitar.

Rode `aferidor compare oleo-de-soja` e olhe as duas colunas:

| | preço na etiqueta | preço por litro |
|---|---:|---:|
| Liza 900 ml, mercado do bairro | R$ 7,49 | **R$ 8,32** |
| Soya 1 L, atacarejo online | R$ 7,90 | **R$ 7,90** |

O óleo do bairro é 5% mais barato na etiqueta e 5% **mais caro** no litro. Quem
compara etiqueta com etiqueta escolhe errado, toda vez, e nunca descobre.

Isso não é um caso raro. A embalagem de 900 ml existe *exatamente* porque a
maioria das pessoas compara etiquetas. O mesmo vale para café de 500 g que
virou 450 g, papel higiênico de 30 m que virou 20 m, e iogurte de 1 L que virou
850 g. O nome técnico é redução de conteúdo — no varejo brasileiro é rotina, e
o Código de Defesa do Consumidor obriga a informar a mudança na embalagem por
um tempo, não para sempre.

A única defesa é normalizar antes de comparar. O `aferidor` faz isso sozinho: você
escreve `900ml` no campo `embalagem` e ele divide. É a coisa mais chata e mais
lucrativa do programa.

## Decisões

| Data | Decisão | Por quê |
|---|---|---|
| 2026-07-19 | investigar migração | a diferença por litro inverte o ranking da etiqueta |
