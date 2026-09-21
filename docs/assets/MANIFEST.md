# Inventário de assets

Toda peça deste repositório é gerada a partir de fonte versionada. Nada aqui foi
desenhado à mão numa ferramenta e exportado sem origem — se você não consegue
refazer com um comando, não deveria estar aqui.

Regenerar tudo: `make assets`. Conferir: `make check-assets` (roda no CI).

## Fontes — `docs/assets/source/`

| Arquivo | O que é | Ferramenta | Licença |
|---|---|---|---|
| `logo.svg` | a marca: etiqueta de preço com a barra de fração vazada | escrito à mão | Apache-2.0 (deste repo) |
| `social-preview.svg` | cartão 1280×640 para o preview social do GitHub | escrito à mão | Apache-2.0 (deste repo) |
| `arquitetura.mmd` | diagrama das quatro camadas | Mermaid (o GitHub renderiza) | Apache-2.0 (deste repo) |
| `demo.sh` | roteiro da demo do CLI | escrito à mão | Apache-2.0 (deste repo) |
| `demo.cast` | gravação da demo do CLI, formato asciicast v3 | asciinema 3.2.1 | Apache-2.0 (deste repo) |
| `demo-fone.sh` | roteiro da demo do celular | escrito à mão | Apache-2.0 (deste repo) |
| `demo-fone.cast` | gravação da demo do celular, num aparelho real | asciinema 3.2.1 | Apache-2.0 (deste repo) |
| `vitrine-fixture.html` | vitrine de mentira que a demo do celular dirige | escrito à mão | Apache-2.0 (deste repo) |
| `portrait.py` | recomposição textual do cast existente em cinco cartões verticais; não executa comandos gravados | Python stdlib + Inkscape + FFmpeg | Apache-2.0 (deste repo) |

**Nenhuma fonte tipográfica está embutida.** Os SVGs declaram a pilha do sistema
(`DejaVu Sans, Inter, system-ui, sans-serif`) e o texto do preview social é
convertido em caminho vetorial na renderização (`inkscape -T`), então ele não
depende de nenhuma fonte instalada — e não há licença de fonte para auditar.

**Nada foi gerado por IA de imagem.** Todo desenho é geometria escrita à mão,
legível no `git diff`.

## Renderizados — `docs/assets/rendered/`

| Arquivo | Dimensões | Peso | Orçamento | Como refazer |
|---|---|---:|---:|---|
| `social-preview.png` | 1280×640 | ~71 KB | ≤ 1024 KB (teto do GitHub) | `make assets` |
| `demo.gif` | 921×628, 51 quadros | ~85 KB | ≤ 900 KB | `make demo` |
| `demo-dark.gif` | 921×628, 51 quadros | ~83 KB | ≤ 900 KB | `make assets` (mesmo cast, tema escuro) |
| `demo.png` | 921×628 | ~46 KB | ≤ 300 KB | `make assets` (último quadro do GIF) |
| `demo-fone.gif` | 921×684, 78 quadros | ~276 KB | ≤ 900 KB | `make demo-fone` (exige celular) |
| `demo-fone-dark.gif` | 921×684, 78 quadros | ~295 KB | ≤ 900 KB | `make assets` (mesmo cast, tema escuro) |
| `demo-fone.png` | 921×684 | ~25 KB | ≤ 300 KB | `make assets` (último quadro do GIF) |
| `portrait.mp4` | 1080×1920, 24 fps, 40 s | ~869 KiB | ≤ 8 MiB | `make portrait MEDIA_ENCODER=h264_vaapi` (ou `make portrait` para libx264) |
| `portrait.png` | 1080×1920, último cartão | ~233 KiB | ≤ 400 KiB | `make portrait` |

Os orçamentos são verificados por `scripts/check-assets.py`, que **quebra o CI**
se uma peça engordar. O do GIF é bem mais apertado que o formato permite porque
ele precisa carregar no celular, em dado móvel.

## Dados usados nas peças

As demos mostram **os dados de exemplo que acompanham o `template/`** — o óleo
de 900 ml contra o de 1 litro, do `template/dados/observacoes.csv`.

Isso é regra, não coincidência:

- **Nenhum dado real de casa nenhuma** aparece em imagem deste repositório.
  Nota fiscal tem CPF e a lista completa do que uma família consome.
- Como as peças usam a fixture, elas **não podem divergir** do que a ferramenta
  realmente imprime: `aferidor compare oleo-de-soja` produz exatamente os números
  que aparecem na gravação.

O cartão social não traz número nenhum, de propósito. Ele é lido a ~600 px numa
prévia de link, onde uma tabela de preços vira textura; ele carrega uma frase
só, e quem quiser o número clica.

A demo é gravada num diretório temporário que é apagado no fim, sem nome de
usuário, sem hostname e sem caminho da máquina que gravou.

### A demo do celular

`make demo-fone` é a única peça que precisa de hardware: um Android físico
ligado por `adb`. A gravação é real — o `aferidor-fone` lê a árvore de
acessibilidade do aparelho, toca de verdade e recusa o pagamento de verdade.

**O que é encenado é só a loja.** A demo dirige
`docs/assets/source/vitrine-fixture.html`, uma vitrine estática com os mesmos
itens do `template/`, servida na rede local e aberta no navegador do aparelho.
Gravar contra um aplicativo de entrega real significaria expor a conta de
alguém — endereço, histórico de pedidos, formas de pagamento — para produzir
material de divulgação, além de dirigir o app de um terceiro com essa
finalidade. A fixture mantém a demonstração honesta sobre a ferramenta e uma
casa real fora dela.

O serial do aparelho é mascarado na gravação: ele é alcançado por uma rede
privada, e esse endereço é infraestrutura, não algo que um README precise
publicar.

**A ressalva é gravada dentro do quadro, não ao lado dele.** Os 56 px de tarja
vermelha no rodapé de *todos* os quadros — "VITRINE LOCAL DE DEMONSTRAÇÃO — NÃO
É IFOOD NEM APP DE ENTREGA" — existem porque GIF é print: ele é recortado,
incorporado e recompartilhado sem uma linha do texto à volta. Como a peça mostra
um aparelho real sendo conduzido por uma compra, é a coisa mais fácil de ler
errado no repositório inteiro, e a tarja é a única parte da ressalva que viaja
junto. Ela é aplicada pelo `make`, não à mão.

Para refazer: sirva `docs/assets/source/` em HTTP, abra a vitrine no aparelho e
rode `make demo-fone`. As pré-condições estão no cabeçalho do `demo-fone.sh`, e
o roteiro **falha em vez de gravar** se a recusa de pagamento não acontecer.

## Rascunho vertical — replay textual, não nova captura

`portrait.mp4` é uma montagem **sem áudio** em cinco cartões de oito segundos,
extraída de `demo-fone.cast`. O script não roda `adb`, `aferidor-fone`, carrinho,
pagamento ou navegador. A captura original foi feita no aparelho com a fixture;
nesta edição só se lê aquele arquivo. Nenhuma conta real foi acessada.

O texto das saídas vem do cast, não de resultados digitados para parecerem uma
execução. A recomposição remove códigos de cor/limpeza de terminal e coordenadas
finais da árvore de acessibilidade, quebra linhas em até 41 caracteres e troca
as colunas da tabela por rótulos em cada linha. Valores, datas históricas, aviso
de múltiplos aparelhos, veredito MANTER e recusa de pagamento são preservados.
Títulos são editoriais. **Tempo editado** aparece no rodapé em todos os quadros;
o cast original tem ~37,89 s, o replay tem 40 s e não simula digitação ao vivo.
Não é prova de integração com aplicativo de entrega nem promessa de economia.

A tarja superior fixa de 280 px traz, em texto de 36 px, **VITRINE LOCAL DE
DEMONSTRAÇÃO / NÃO É IFOOD NEM APP DE ENTREGA / aferidor-fone é experimental**.
O corpo usa DejaVu Sans Mono de 38 px, não a tela de 100 colunas encolhida.
DejaVu Sans/Mono são fontes de sistema sob a
[licença DejaVu/Bitstream Vera](https://dejavu-fonts.github.io/License.html);
nenhum arquivo de fonte é distribuído. Cast, roteiro, composição, vídeo, poster
e evidências visuais são Apache-2.0 do projeto. Sem música, imagens de terceiros
ou serviço de geração de imagem. Implementação desta edição: OpenAI/GPT-6 Astra.

Regenerar: `make portrait` (Python 3, Inkscape, FFmpeg com libx264 e fontes
DejaVu); no desktop a edição foi codificada com VAAPI via
`make portrait MEDIA_ENCODER=h264_vaapi`. Requer `/dev/dri/renderD128` funcional;
não há fallback silencioso nesse modo. O conteúdo e a composição são
reproduzíveis; bytes H.264 podem variar com encoder/driver/versão.

Verificar: `make check && make check-media`. O primeiro mantém todos os testes
anteriores e checa dimensões/peso do poster e cabeçalho/peso MP4 sem dependências
Python extras. O segundo usa FFmpeg para formato/duração/24 fps/ausência de áudio
e compara os glifos da tarja de **todos os 960 quadros** ao poster inspecionado.
O hash RGB da tarja do poster também é fixado: mudança de fonte/renderizador
exige inspeção antes de atualizar o hash, não apagar o teste. Isso prova
integridade visual, não substitui revisão semântica independente. O gate FFmpeg
é local/do coordenador; não foi adicionado ao workflow nesta PR.

Evidência reproduzível em `docs/assets/evidence/portrait/`: `ffprobe.json`,
`contact-sheet.png` (quadros 0, 192, 384, 576 e 959), logs de geração/testes e
checagem negativa. O poster e o cast são alternativas estática e textual ao
vídeo; os pares GIF claro/escuro do README permanecem intactos.

## Modo claro e modo escuro

Metade de quem abre o README lê numa tela quase preta, e um GIF de tema claro é
um bloco branco ali. Cada gravação de terminal é renderizada **duas vezes a
partir do mesmo `.cast`** — `github-light` e `github-dark` — e o README escolhe
com `<picture media="(prefers-color-scheme: dark)">`, que é o mecanismo do
próprio GitHub, não uma segunda cópia do markdown.

O cartão social não tem par escuro de propósito: ele só é usado no *unfurl* de
link, e nenhuma rede social consulta `prefers-color-scheme` — cada uma compõe a
imagem sobre o próprio fundo.

## Acessibilidade

- Todo SVG tem `<title>`, verificado pelo `check-assets.py`.
- Toda imagem no README tem texto alternativo descritivo — também verificado.
- O GIF **não é legível por leitor de tela**. Por isso existem o `demo.png`
  estático e o `demo.cast`, que é texto e pode ser lido linha a linha.
- O diagrama Mermaid vem sempre acompanhado de um parágrafo em prosa dizendo a
  mesma coisa. Leitor de tela não lê caixa e seta.
- A paleta é calculada contra o branco e **falha o CI abaixo de WCAG AA**. Verde
  e vermelho nunca carregam significado sozinhos — sempre há rótulo em texto.
- O GitHub não respeita `prefers-reduced-motion` em imagem de README. O cuidado
  ficou no conteúdo: a demo é lenta, sem piscar, e tem equivalente estático.
