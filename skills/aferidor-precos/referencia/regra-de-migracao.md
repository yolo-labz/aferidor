# A regra de migração — por que 8% e 3 amostras

A regra existe para responder a uma pergunta que "qual está mais barato?" não
responde: **vale a pena mudar?**

Comparar preço é fácil. Trocar de mercado custa frete, pedido mínimo, cadastro,
o risco de o item vir errado, e o seu tempo. Uma recomendação que ignora esses
custos produz uma casa que persegue promoções e gasta mais.

## Os dois portões

Um mercado desafiante só rouba um item do incumbente se passar nos **dois**:

### Portão 1 — diferença mínima (padrão: 8%)

De onde vem o número, para uma compra típica de entrega:

| Custo da troca | Valor típico |
|---|---:|
| Frete do mercado novo | R$ 8 a R$ 15 |
| Risco de item faltando / substituído | ~3% do pedido |
| Seu tempo (cadastro, aprender o app, conferir) | 20 a 40 min |

Num item de R$ 30 comprado quinzenalmente, 8% são R$ 2,40 por compra, R$ 62 por
ano. Isso cobre o incômodo. 3% não cobre.

**Quando mudar o padrão:**

- **Suba para 12–15%** se a casa concentra quase tudo num mercado só. Aí cada
  item que sai enfraquece o carrinho principal e pode fazer você perder o frete
  grátis — o desconto do item vira prejuízo no pedido.
- **Desça para 5%** para itens de volume alto e recompra frequente (arroz,
  ração, fralda, sabão em pó), onde o mesmo percentual vale muito mais reais por
  ano e o item já é comprado em quantidade.
- **Nunca desça abaixo de 3%.** Abaixo disso você está dentro do ruído: a
  mesma loja varia mais que isso entre uma terça e um sábado.

### Portão 2 — amostras mínimas (padrão: 3)

Uma observação é um evento, não um preço. Pode ser promoção, pode ser erro de
etiqueta, pode ser o dia em que aquele mercado estava zerando estoque.

Três é o mínimo em que uma mediana começa a significar algo. Não é rigor
estatístico — com n=3 o intervalo de confiança ainda é largo. É o ponto onde o
custo de errar cai mais rápido que o custo de esperar.

Se a casa comprar semanalmente, três amostras levam três semanas. **Essas três
semanas não são tempo perdido, são o método funcionando.** Um sistema que
recomenda na primeira semana está inventando.

O `aferidor` usa **mediana**, não média, exatamente porque uma promoção isolada
não deve puxar o resultado. Com n=3, a mediana é o preço do meio: a promoção
fica visível na coluna `mín` e não contamina a decisão.

## A janela (padrão: 90 dias)

Preço de quatro meses atrás não descreve o mercado de hoje — inflação de
alimento no Brasil se move rápido, e o mix de promoção de cada rede muda por
temporada.

Noventa dias equilibra: longo o bastante para juntar três amostras num item
quinzenal, curto o bastante para não carregar o preço do trimestre passado.

Casas que compram mensalmente devem subir para 120–180 dias, senão nada nunca
acumula amostras suficientes.

## O que a regra não faz

- **Não considera qualidade.** Se a marca mais barata é pior, a decisão é sua.
  Registre em `marcas_substitutas` no arquivo do item quais marcas a casa aceita
  de fato, e só compare dentro desse conjunto.
- **Não considera frete automaticamente.** Ela recomenda item a item; agrupar as
  migrações num pedido só, respeitando pedido mínimo, é trabalho do
  `aferidor-lista`.
- **Não sabe de conveniência.** O mercado da esquina que entrega em 20 minutos
  tem valor que não aparece em R$/kg. Se a casa quer isso, suba o
  `delta_minimo_pct` — é literalmente quanto você está disposto a pagar pela
  conveniência, escrito como número.

## Onde mexer

`aferidor.toml`, seção `[comparacao]`:

```toml
[comparacao]
delta_minimo_pct = 8.0
amostras_minimas = 3
janela_dias      = 90
```

Mudou? Escreva no `DIARIO.md` **por que**. Um limiar sem motivo é um limiar que
alguém vai mexer de novo daqui a três meses sem saber o que está desfazendo.
