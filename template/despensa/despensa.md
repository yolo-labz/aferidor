# Despensa

O que existe em casa agora. Sem isto, a lista de compras é chute — e chute
compra o terceiro vidro de páprica enquanto o arroz acaba.

Não precisa ser perfeito nem contar tudo. Precisa cobrir os itens que a casa
compra sempre e que dói acabar. Vinte linhas bem mantidas valem mais que
duzentas abandonadas.

Regra prática: atualize na hora de guardar a compra, não depois. É o único
momento em que você já está com tudo na mão.

| Item | Quantidade | Ponto de recompra | Confirmado em | Validade | Nota |
|---|---:|---:|---|---|---|
| arroz-tio-joao-1kg | 10 | 2 | 2026-07-19 | — | exemplo — saco de 5 kg aberto, ainda com folga |
| oleo-de-soja | 1 | 1 | 2026-07-19 | — | exemplo — já estava no ponto |
| papel-higienico-30m | 8 | 4 | 2026-07-19 | — | exemplo |

**Quantidade e ponto de recompra vão na unidade base do item** — `kg` para o
arroz, `L` para o óleo, `un` para o papel. Um número solto (`3`) é lido nessa
unidade; se preferir ser explícito, escreva `3 kg` e o `aferidor` entende igual.

**`Confirmado em` é a coluna que faz o `aferidor falta` funcionar.** Sem ela o
número é só um número: o programa não tem como saber se você contou hoje ou em
março, então se recusa a opinar e devolve `COLETAR`. Com ela, ele mostra a
idade da contagem junto do palpite — "contou 3 há 21 dias" — e você julga se
ainda vale.

**Ponto de recompra** é quanto pode sobrar antes de o item entrar na lista.
Ele deve cobrir o prazo de entrega do mercado mais o tempo até a próxima
compra. Se o atacarejo demora 2 dias e você compra a cada 15, o ponto de
recompra precisa cobrir 17 dias de consumo — não zero.

Um ponto de recompra baixo demais é o que empurra a casa para o mercado da
esquina no preço cheio. É lá que a economia da planilha vai morrer.
