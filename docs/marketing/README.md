# Kit de lançamento

Textos e peças prontos para publicar. **Nada aqui foi publicado** — é material
preparado, aguardando decisão.

A regra que governa este diretório: **toda frase publicável tem que passar pela
[tabela de alegações](#tabela-de-alegações--evidência)**. Se uma afirmação não
tem linha lá, ela não sai. É assim que a cópia não vira propaganda sem ninguém
perceber.

| Arquivo | O que tem |
|---|---|
| `README.md` (aqui) | descrições, tabela de alegações, inventário de peças |
| [`posts.md`](posts.md) | os três textos de lançamento + roteiro de trailer |

## Descrições

### Uma linha (até 120 caracteres — descrição do repositório, bio)

> Um agente que pesquisa preço no app do mercado e monta o carrinho no seu celular — o pagamento continua seu.

Variante em inglês para os tópicos e a busca do GitHub:

> An agent that prices groceries inside the delivery apps on your own Android phone and builds the cart — you tap pay.

**Nas duas, a segunda metade não é opcional.** Cortar "o pagamento continua seu"
para caber num limite de caracteres transforma a descrição na promessa que o
projeto passou quatro revisões recusando fazer.

### Três frases (post curto, apresentação, README de diretório)

> O `aferidor` é um agente que lê preço **dentro dos aplicativos de entrega, no seu
> próprio celular**, decide comparando por quilo ou litro em vez da etiqueta, e
> monta o carrinho no aparelho. Aí ele para: tocar no botão de pagar é recusado
> em código, e no servidor MCP a ferramenta de pagar nem existe — quem finaliza
> é você, à mão, no app. A camada do celular é **experimental** e exige um
> Android físico homologado; abaixo dela, o método e o CLI decidem *o que
> comprar e onde* sozinhos, sem celular nenhum.

### Longa (página de projeto, submissão, e-mail)

> Comparador de preços olha o preço **anunciado**, na loja que paga o anúncio. O
> `aferidor` faz o contrário: parte da nota fiscal eletrônica que o mercado já
> emitiu para a sua casa, normaliza cada preço por quilo, litro ou unidade, e
> responde uma pergunta só — *vale a pena mudar alguma coisa?*
>
> A normalização é a parte que devolve dinheiro sozinha: uma garrafa de 900 ml a
> R$ 7,49 tem etiqueta menor e sai mais cara por litro que uma de 1 litro a
> R$ 7,90. A regra de decisão é a parte que evita perder dinheiro: só migrar com
> 8% de diferença e 3 observações, porque trocar de mercado custa frete, pedido
> mínimo e tempo.
>
> O método funciona numa planilha, sem instalar nada — e essa é a camada que
> mais importa. O software é Python de biblioteca padrão, sem dependência de
> runtime, sem chamada de rede, com os dados em texto puro que abre em qualquer
> editor. Há um servidor MCP para perguntar em português usando o cliente de IA
> que você já tem, e ele **não possui nenhuma ferramenta de pedido ou pagamento**
> — um teste falha se alguém adicionar uma.
>
> Roda numa casa em Recife desde maio de 2026. Nenhuma economia foi medida
> contra linha de base controlada, e o projeto não promete porcentagem.

## Tabela de alegações ↔ evidência

Cada linha é uma coisa que a gente pode dizer em público, e onde alguém confere.

| Alegação | Status | Evidência |
|---|---|---|
| Normaliza preço por kg/L/unidade | ✅ verificável | `aferidor compare oleo-de-soja`; `parse_package()` + casos no `aferidor selftest` |
| 900 ml a R$ 7,49 sai mais caro por litro que 1 L a R$ 7,90 | ✅ verificável | fixture `template/dados/observacoes.csv`; aritmética no `selftest` |
| Só migra com ≥8% e ≥3 amostras | ✅ verificável | `verdict()` em `bin/aferidor`; casos no `aferidor selftest` |
| Diz "não mude" quando não compensa | ✅ verificável | veredito `MANTER` na demo e no `advise` |
| Recusa opinar sem dados suficientes | ✅ verificável | veredito `COLETAR`; item `papel-higienico-30m` |
| Lê nota fiscal eletrônica (NFC-e modelo 65) | ✅ verificável | `aferidor nfce`; `parse_nfce()` em `bin/aferidor` |
| Zero dependência de runtime | ✅ verificável | só stdlib; `import` no fonte; CI sem `pip install` |
| Nenhuma chamada de rede no CLI | ✅ verificável | ausência de `urllib`/`socket`/`http` em `bin/aferidor` |
| MCP não tem ferramenta de pedido nem pagamento | ✅ verificável | `tests/test_mcp.py`, incluindo teste negativo |
| `aferidor-fone` recusa botão de pagamento | ✅ verificável | lista `PERIGO` + `tests/test_fone.py`; e a demo grava a recusa acontecendo |
| Lê preço e monta carrinho num Android físico | ✅ verificável, **com a ressalva da vitrine** | `demo-fone.cast` é uma gravação real; a loja é `vitrine-fixture.html`, não um app de entrega |
| `aferidor-fone` funciona no iFood / Rappi / app X | ❌ **NÃO AFIRMAR** | nenhum aplicativo de entrega real foi automatizado; não há lista de apps suportados |
| A camada do celular está pronta para usar | ❌ **NÃO AFIRMAR** | experimental: uma casa, um aparelho, sem release |
| Instalador não roda como root, instala só no `$HOME` | ✅ verificável | `install.sh`; teste ponta a ponta no CI |
| Emulador Android falha no pagamento (Play Integrity) | ⚠️ raciocinado, não testado por nós | `docs/pesquisa/harness-de-login.md`, aferido 25/08/2026 — **dizer sempre com a data** |
| Roda numa casa em Recife desde maio/2026 | ⚠️ relato do autor | `docs/01-o-caso.md` — não é prova pública |
| **Economia em reais ou %** | ❌ **NÃO AFIRMAR** | não há linha de base controlada; `docs/01-o-caso.md#o-que-ainda-não-está-provado` |
| **Quantas pessoas usam** | ❌ **NÃO AFIRMAR** | não há instalação externa conhecida |
| "Pronto para produção", "v1.0" | ❌ **NÃO AFIRMAR** | 0.1.0, sem release publicada |

### Frases proibidas

Estas foram testadas e reprovadas em duas revisões adversariais (25 e
26/08/2026), ambas de família de modelo diferente de quem escreveu a cópia.

- ❌ "Comprar mercado abaixo do preço que você pagaria sozinho" — promete
  resultado financeiro causal
- ❌ "Você não sabe se pagou caro. Ninguém sabe." — universal indefensável
- ❌ "O preço do arroz varia 40%" — número sem fonte apresentado como fato geral
- ❌ "A garrafa de 900 ml existe porque a de 1 litro existia antes" — conjectura
  histórica sem evidência
- ❌ "5% não paga o frete" — a regra de 8% é política configurada, não prova
  econômica. Diga: "a política padrão não recomenda trocar abaixo de 8%"
- ❌ "não exige chave de API de ninguém" — o `aferidor` não exige; o cliente de IA
  pode exigir
- ❌ "faz sua compra no iFood" / "compra sozinho no app do mercado" — nenhum
  aplicativo de entrega real foi automatizado, e o software não compra em
  lugar nenhum. Diga: "monta o carrinho; quem finaliza é você"
- ❌ Publicar o GIF do celular sem dizer que a vitrine é de exemplo — a imagem
  sozinha faz o espectador concluir que o app é real. (Desde 26/08 a tarja está
  queimada nos quadros, mas a legenda continua obrigatória em texto)
- ❌ **"comparador de preços"** como autodescrição — o README tem uma seção
  inteira explicando por que não é isso, e o texto de lançamento não pode dizer
  o contrário da página que ele linka. Diga o que ele faz: lê preço, decide por
  quilo/litro, monta o carrinho, para no pagamento
- ❌ **Pedir encaixe** — "caso de ensino?", "extensão?", "PIBIC?". Quem pediu o
  material pediu uma dica; entregue a dica e pare. Proposta que parte do outro
  lado vale mais que uma que a gente foi buscar (correção do Pedro, 26/08)
- ❌ Mandar um **apêndice técnico** para quem não é da computação — transforma um
  documento útil numa escada de três degraus
- ❌ Usar o GIF de tema claro sobre fundo escuro. Existe `-dark` de cada um
- ❌ "nunca foi instalado por outra pessoa" — indemonstrável. Diga: "não há
  instalação externa conhecida"

Da segunda revisão (26/08/2026) — estas são mais sutis, e todas passaram pela
primeira sem serem pegas:

- ❌ **"uma ferramenta que manda trocar de mercado toda semana faz você gastar
  mais"** — causalidade afirmada sobre a categoria inteira, sem medição. É a
  assimetria que mais machuca este projeto: recusar prometer economia própria e
  ao mesmo tempo afirmar prejuízo alheio. Diga o custo da troca (frete, pedido
  mínimo, tempo) como **razão de desenho**, não como lei de mercado.
- ❌ **"o preço que a sua casa realmente pagou"** — a entrada também é digitada, e
  digitação erra. Diga "o preço que a sua casa pagou, conforme você registra".
- ❌ **"não faz nenhuma chamada de rede"** sem escopo — o instalador baixa, a
  extensão lê página. Diga "o `aferidor` **instalado** não faz chamada de rede".
- ❌ **"nunca busca preço na internet"** sem escopo — contradiz a extensão. Diga
  "não consulta preço na internet por conta própria; a extensão lê só a página
  que você abriu, quando você clica".
- ❌ **"funciona com uma planilha e um caderno"** dito do repositório — isso é
  verdade do **método**. Atribua e linke, senão é uma promessa que o repo não
  demonstra.
- ❌ **"a maioria dos clientes de IA roda com assinatura de consumidor"** —
  afirmação sem fonte sobre um mercado que muda rápido, e que apodrece sozinha.
- ⚠️ **O resumo em inglês tem que carregar as mesmas ressalvas do português.**
  Na primeira versão ele omitia "sem release" e "economia não medida" — o leitor
  estrangeiro recebia a versão cor-de-rosa, que é exatamente o vazamento que este
  documento existe pra impedir.

## Inventário de peças

| Peça | Arquivo | Onde usar | Fatos |
|---|---|---|---|
| **Demo do celular** | `rendered/demo-fone.gif` · `demo-fone-dark.gif` | **herói do README**; qualquer peça sobre o produto | 921×684, 249 / 262 KB |
| Demo do celular, estática | `rendered/demo-fone.png` | onde GIF não roda; e-mail | 921×684, 25 KB |
| Preview social | `rendered/social-preview.png` | **só o unfurl de link** e o ajuste do repositório | 1280×640 (2:1), 71 KB; recorte central em X/Slack |
| Demo do CLI | `rendered/demo.gif` · `demo-dark.gif` | post técnico; seção do CLI | 921×628, 78 KB |
| Demo do CLI, estática | `rendered/demo.png` | onde GIF não roda | 921×628, 46 KB |
| Demo em texto | `source/demo-fone.cast`, `demo.cast` | leitor de tela; quem prefere texto | — |
| Marca | `source/logo.svg` | avatar da organização, favicon | quadrado, legível a 16 px |
| Diagrama | bloco Mermaid no README | README; slide | renderizado pelo GitHub |

**O cartão social não é o herói do README** — foi até 26/08 e deixou de ser. Em
modo escuro ele é um bloco branco, e o conteúdo dele era uma lista de bullets
desenhada como imagem: não seleciona, não traduz, não reflui, não é lida por
leitor de tela. O topo do README é a gravação; o cartão serve o *unfurl*, onde
é a única peça possível.

**Todo GIF tem par claro e escuro.** Ao republicar num lugar com fundo escuro,
use o `-dark`. No README quem escolhe é o `<picture media="(prefers-color-scheme: dark)">`.

Texto alternativo de cada uma: em [`MANIFEST.md`](../assets/MANIFEST.md) e nas
tags `alt` do próprio README. Não republique uma peça sem o texto alternativo
junto.

**A demo do celular vem com uma legenda obrigatória.** A gravação é real — o
aparelho, o `adb`, a leitura da tela e a recusa —, mas a loja é uma vitrine de
mentira. Toda republicação precisa dizer isso, com essas palavras ou parecidas:

> Gravação real num Android físico. A vitrine é uma página de exemplo, não um
> aplicativo de entrega — nenhuma conta real foi automatizada para esta peça.

Publicar o GIF sem essa linha deixa o espectador concluir que o `aferidor` já
dirige o iFood, que é exatamente a alegação que o projeto não sustenta hoje.

## Antes de publicar qualquer coisa

- [ ] Toda afirmação tem linha na tabela acima
- [ ] Nenhuma frase da lista de proibidas
- [ ] Nenhum dado real de casa em imagem — só fixture
- [ ] Texto alternativo em toda imagem
- [ ] Links apontam para `yolo-labz/aferidor`
- [ ] A afirmação sobre emulador vem com a data da aferição
- [ ] Sem ponto de exclamação, sem emoji em título, sem "🚀"
