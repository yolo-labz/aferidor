# Unidades e embalagens — o que o normalizador entende

O campo `embalagem` decide toda a comparação. Ele descreve **uma** embalagem; a
quantidade de embalagens vai em `-q/--quantidade`.

`preço por unidade-base = preco_total / (quantidade × conteúdo_da_embalagem)`

## Formatos reconhecidos

| Você escreve | Vira | Base |
|---|---:|---|
| `1kg`, `1 kg`, `1KG` | 1,0 | kg |
| `500g`, `pct 500g`, `saco de 500 g` | 0,5 | kg |
| `1L`, `1 l`, `1 litro`* | 1,0 | L |
| `900ml`, `900 mL` | 0,9 | L |
| `1,25L` (vírgula) | 1,25 | L |
| `1.25L` (ponto) | 1,25 | L |
| `6x350ml`, `6 x 350 ml`, `fardo 6x350ml` | 2,1 | L |
| `12x1L`, `cx 12x1L` | 12,0 | L |
| `c/16`, `com 16`, `leve 16` | 16,0 | un |
| `un`, `1un`, `unidade` | 1,0 | un |
| vazio, `bandeja`, `pote` | 1,0 | un |

\* `litro` por extenso cai no caso `l` só se estiver colado num número
(`1 litro` → sim). Prefira a abreviação.

Regras:

- **Vírgula e ponto decimal funcionam.** `1,25` e `1.25` dão o mesmo número.
  `1.234,56` também é lido corretamente como mil duzentos e trinta e quatro.
- **A primeira medida encontrada vence.** `arroz 1kg promoção 2kg grátis` lê
  `1kg`. Escreva a embalagem no campo `embalagem` e a promoção no campo
  `observacao`.
- **Multiplicador precisa vir antes.** `6x350ml` funciona; `350ml x6` não.
- **Não reconheceu?** Vira `1 un`. Isso é silencioso de propósito — não dá para
  adivinhar. Rode `aferidor check`, que lista as linhas de onde não saiu preço
  unitário confiável.

## Escolhendo a unidade-base do item

No front matter do item, `unidade_base` documenta o que a casa considera
comparável. O normalizador deriva a base da embalagem, então os dois precisam
combinar:

| Item | `unidade_base` | Por quê |
|---|---|---|
| arroz, feijão, carne, café | `kg` | vendido por peso, embalagem varia |
| leite, óleo, refrigerante, sabão líquido | `L` | vendido por volume |
| ovo, papel higiênico, iogurte em pote, pilha | `un` | conta é o que importa |

**Não misture bases dentro de um item.** Se um mercado vende iogurte em pote de
170 g e outro em garrafa de 1,25 L, esses são produtos diferentes para efeito de
comparação, ainda que a marca seja a mesma. Crie dois itens.

## O caso que motiva tudo isto

```
Liza  900 ml   R$ 7,49   →  R$ 8,32 / L
Soya  1 L      R$ 7,90   →  R$ 7,90 / L
```

O de baixo tem etiqueta maior e é mais barato. A embalagem de 900 ml existe
porque a maioria compara etiquetas.

O mesmo padrão aparece em café que saiu de 500 g para 450 g e depois 400 g,
papel higiênico que saiu de 30 m para 20 m, e achocolatado que saiu de 400 g
para 370 g. Chama-se redução de conteúdo. É legal, e o Código de Defesa do
Consumidor exige avisar na embalagem — por um período, não para sempre.

Normalizar não é preciosismo. É a única defesa que não depende de você lembrar.
