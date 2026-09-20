---
item: Papel higiênico folha dupla 30m
unidade_base: un
marca_padrao: Neve
marcas_substitutas: [Personal, Mili, Sublime]
mercado_atual: mercado-do-bairro
ponto_de_recompra: 4
pode_substituir: sim
tags: [exemplo, limpeza]
---

# Papel higiênico 30m

> Item de exemplo. Apague este arquivo quando começar a registrar os seus.

Este item está **de propósito** com dados insuficientes: uma observação em cada
mercado. Rode `aferidor compare papel-higienico-30m` e o programa se recusa a
opinar — ele responde `COLETAR`, não um vencedor.

Essa recusa é o comportamento correto, e é a parte que as pessoas mais tentam
desligar. Com uma amostra por mercado você não sabe se o rolo de R$ 32,90 é o
preço normal ou a promoção da semana. Recomendar uma migração em cima disso é
chutar com aparência de planilha.

Note também que os pacotes são diferentes — 12 e 16 rolos. O `aferidor` normaliza
para preço por rolo, então `c/12` e `c/16` são comparáveis. Metros por rolo,
não: um rolo de 30 m e um de 20 m contam igual aqui. Se a sua casa liga para
isso, mude `unidade_base` para `m` e escreva a metragem total na embalagem
(`12x30m`).

## Decisões

| Data | Decisão | Por quê |
|---|---|---|
| — | nenhuma | dados insuficientes, e isso está certo |
