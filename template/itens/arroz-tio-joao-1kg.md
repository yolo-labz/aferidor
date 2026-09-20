---
item: Arroz Branco Tio João Tipo 1
unidade_base: kg
marca_padrao: Tio João
marcas_substitutas: [Camil, Urbano, Prato Fino]
mercado_atual: mercado-do-bairro
ponto_de_recompra: 2
pode_substituir: sim
tags: [exemplo, graos, alta-frequencia]
---

# Arroz Tio João

> Item de exemplo. Apague este arquivo quando começar a registrar os seus.

`mercado_atual` é o mercado onde a casa compra este item **hoje**. É o
incumbente: `aferidor compare` mede todo mundo contra ele, e a regra de migração
só o destrona se outro for consistentemente e significativamente mais barato.

`ponto_de_recompra` é quantas embalagens sobrando na despensa disparam a
recompra. Dois pacotes de arroz é uma semana de folga — tempo suficiente para
esperar uma promoção em vez de comprar no susto pelo preço cheio.

## Observações

Este item existe para demonstrar duas coisas ao mesmo tempo:

1. **A regra de migração funcionando.** Rode `aferidor compare arroz-tio-joao-1kg`.
   O atacarejo online só aparece mais barato porque o preço foi normalizado: o
   pacote lá é de 5 kg, e comparar "R$ 27,45" com "R$ 6,99" sem dividir pelo
   peso não diz nada.
2. **Por que três amostras é o piso.** O app de entrega tem só duas
   observações, então ele não entra na disputa — mesmo que uma delas fosse a
   mais barata de todas. Um preço isolado é sorte, não é mercado.

## Decisões

| Data | Decisão | Por quê |
|---|---|---|
| 2026-07-19 | manter no mercado do bairro por ora | ainda faltava fechar o frete do atacarejo |
