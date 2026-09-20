# DESIGN.md — identidade visual do aferidor

Regras para qualquer imagem, diagrama ou peça deste repositório. Curto de
propósito: um sistema que ninguém consegue seguir não é um sistema.

## Para quem

| Público | O que precisa ver primeiro |
|---|---|
| Casa brasileira / professora | que dá pra entender e usar **sem instalar nada** |
| Pessoa técnica | uma demo real, o limite de privacidade, e o primeiro resultado em 2 min |
| Quem contribui | que as alegações têm teste, e onde encaixar a primeira mudança |

## A promessa

**Comparar o preço que a casa realmente pagou, por quilo — e só trocar de
mercado quando compensa.**

Não é "economize 20%". A ferramenta responde *"vale a pena mudar?"*, e na maioria
das semanas a resposta é não.

## Voz

Direta, concreta, sem hype. Números com fonte ou não entram. Uma limitação dita
na abertura vale mais que dez selos.

- **Sim:** "não paga a troca", "faltam 2 amostras", "não sei"
- **Não:** "revolucionário", "poderoso", "sem esforço", "10x", "IA de ponta"
- Português nas peças; inglês só no código e nos tópicos do repositório.
- Sem ponto de exclamação. Sem emoji decorativo em título.

## Paleta

Grafite sobre papel, um verde de feira, um vermelho só para alerta. Contraste
verificado por `scripts/check-assets.py` — **falha o CI se cair abaixo de AA**.

| Token | Hex | Uso | Contraste em `#FFFFFF` |
|---|---|---|---|
| `ink` | `#1F2328` | texto principal, traço do logo | 15.3:1 ✅ AAA |
| `paper` | `#FFFFFF` | fundo | — |
| `paper-2` | `#F6F8FA` | fundo de bloco, preenchimento leve | — |
| `verde` | `#1A7F37` | decisão boa, destaque de preço | 4.7:1 ✅ AA |
| `vermelho` | `#CF222E` | alerta, preço pior | 4.8:1 ✅ AA |
| `cinza` | `#57606A` | texto secundário | 5.9:1 ✅ AA |
| `borda` | `#D0D7DE` | traço de borda, linha de tabela | — (só borda, ≥3:1) |

São os tokens do GitHub Primer. Escolha deliberada: já são acessíveis, já
combinam com a interface onde o README vive, e ninguém precisa confiar no meu
gosto.

**Regra dura:** nunca use `verde` ou `vermelho` como **única** portadora de
significado. Sempre acompanhe de texto ou forma — daltonismo vermelho-verde
atinge ~8% dos homens, e a decisão do `aferidor` é literalmente verde/vermelho.

## Tipografia

Só fontes de sistema e abertas. **Nenhum arquivo de fonte entra no repositório**
— evita ambiguidade de licença e peso de download.

- Texto: pilha do sistema (`system-ui`, `-apple-system`, `Segoe UI`, `Roboto`, `sans-serif`)
- Números e terminal: monoespaçada do sistema (`ui-monospace`, `SFMono-Regular`, `Menlo`, `Consolas`, `monospace`)
- Em SVG, sempre declare a pilha inteira. Um SVG que depende de uma fonte
  instalada renderiza diferente na máquina de quem lê.
- Texto que importa vira **caminho vetorial** na peça final (OG image), senão
  quebra em quem não tem a fonte.

## Espaçamento e forma

- Escala de 4 px: 4, 8, 12, 16, 24, 32, 48, 64.
- Um raio por classe de superfície. Cartão `6px`, marca `2px`. Nada de raio
  diferente por elemento.
- Traço do logo: `2px` em grade de 32. Precisa sobreviver a 16 px.
- Sem sombra. Sem brilho. Sem bisel.

## Ilustração

- **SVG escrito à mão, versionado como fonte.** Qualquer pessoa pode ler o
  arquivo e ver do que é feito.
- Geometria simples: uma metáfora por peça.
- Diagrama: **Mermaid primeiro** (é texto, o GitHub renderiza, dá pra diff).
  Só vira SVG à mão quando o Mermaid não consegue dizer a coisa.
- Todo diagrama tem um **parágrafo em prosa ao lado** dizendo a mesma coisa —
  leitor de tela não lê caixa e seta.

## Movimento

- Só a demo de terminal se move. Mais nada.
- 10–20 s, sem piscar, sem corte rápido.
- **O GitHub não respeita `prefers-reduced-motion` em imagem de README.** Então
  o cuidado é no conteúdo: devagar, e sempre com equivalente estático + `.cast`
  em texto.

## Banidos (recusar na revisão)

1. Gradiente roxo→rosa, "orb" com brilho, glassmorphism
2. Faísca ✨, foguete 🚀, cérebro, robô — o vocabulário visual de "IA" 2024
3. Logo que morre a 32 px, ou que só existe em PNG
4. Parede de selos; selo que não carrega sinal (`PRs welcome`, `made with ❤`)
5. Captura de tela com dado real da casa — **só fixture**
6. Imagem de banco de imagens, mascote gerado, texto com glifo torto
7. Texto que só existe como pixel
8. Número sem fonte numa peça gráfica
9. Fonte proprietária embutida
10. Depoimento inventado, métrica inventada, "production-ready" na v0.1.0

## Onde as coisas ficam

```
docs/assets/
├── source/      fonte editável e versionada (SVG, .cast, .mmd)
├── rendered/    saída gerada (PNG, GIF) — regenerável pelo Makefile
└── MANIFEST.md  o que é cada peça, com ferramenta, licença e como refazer
```

Regenerar tudo: `make assets`. Conferir: `make check-assets` (dimensões, peso,
contraste, XML bem-formado). O check roda no CI.

**Nenhuma peça entra sem fonte.** Se não dá pra refazer com um comando, não entra.
