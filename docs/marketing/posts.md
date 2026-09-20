# Textos de lançamento

Rascunhos. **Nenhum foi publicado.** Cada um passou pela
[tabela de alegações](README.md#tabela-de-alegações--evidência).

O tom é o mesmo do README, de propósito: uma alegação, um comando, uma demo
honesta, zero ponto de exclamação. Num projeto cuja credibilidade inteira é não
exagerar, o texto de lançamento é onde isso costuma vazar.

---

## 1. Post em português — público geral

> Escrevi um agente que faz a minha compra de mercado. Ele pesquisa preço nos
> aplicativos, pelo celular, monta o carrinho — e para no botão de pagar.
>
> Parar ali não é limitação técnica. É onde eu pus a fronteira: quem discute com
> o mercado e com a operadora do cartão sou eu, não o programa. No servidor de
> IA que acompanha o projeto a ferramenta de pagar **não existe** — não é um
> "confirma?" que dá pra convencer o modelo a pular.
>
> Mas a parte que economiza dinheiro não precisa de celular nenhum, e é chata:
>
> **1. Comparar etiqueta com etiqueta escolhe errado.** Óleo de 900 ml a
> R$ 7,49 parece mais barato que o de 1 litro a R$ 7,90. Por litro, é 5% mais
> caro. Enquanto você compara etiquetas, o tamanho da embalagem decide por você.
>
> **2. Trocar de mercado quase nunca compensa.** Frete, pedido mínimo e a sua
> tarde custam mais que 5% de diferença. A regra que uso: só mudar acima de 8%,
> e com pelo menos 3 observações, senão você está reagindo a uma promoção de um
> dia. O veredito mais comum é *não mude nada*.
>
> Os preços saem da nota fiscal eletrônica que o mercado já emite pra você — o
> que você **pagou**, não o que estava anunciado.
>
> **O método roda numa planilha, sem instalar nada.** O programa só automatiza a
> conta.
>
> Duas ressalvas, porque prometer demais aqui seria fácil: a parte do celular é
> experimental — uma casa, um aparelho — e eu **não** medi economia contra uma
> linha de base controlada. Quem promete porcentagem sem isso está chutando.
>
> github.com/yolo-labz/aferidor

**Peça:** `demo-fone.gif` (use o `-dark` em fundo escuro).
**Canal:** LinkedIn, Instagram, grupo de família.
**Legenda obrigatória do GIF:** ver [a regra](README.md#inventário-de-peças) —
a vitrine é de demonstração, não é um aplicativo de entrega.

---

## 2. Post técnico — OSS

> **aferidor** — um agente que lê preço de mercado na tela de um Android físico,
> decide comparando por quilo/litro, monta o carrinho e **para no pagamento**.
> Os preços históricos saem da nota fiscal eletrônica brasileira (NFC-e): o que
> a casa pagou, não o que estava anunciado.
>
> - Python de biblioteca padrão. Zero dependência de runtime, zero chamada de
>   rede. Os dados são CSV e Markdown que abrem em qualquer editor.
> - Normaliza tudo para R$/kg, R$/L ou R$/un antes de comparar — a garrafa de
>   900 ml não ganha da de 1 litro por ter etiqueta menor.
> - Regra de migração explícita: só troca de mercado com ≥8% de diferença e ≥3
>   observações. O veredito mais comum é `MANTER`, e quando faltam dados ele
>   responde `COLETAR` em vez de chutar.
> - Servidor **MCP** incluso, para perguntar em português pelo cliente de IA que
>   você já usa — sem chave de API do lado do `aferidor`.
>
> A parte que talvez interesse a quem trabalha com agentes: **o servidor MCP não
> tem nenhuma ferramenta de pedido ou pagamento.** Não é um portão de
> confirmação que dá pra convencer o modelo a pular — a capacidade não existe. O
> teste verifica a ausência, inclusive se o código do servidor apenas mencionar
> o driver do celular, e foi validado ao contrário: plantando uma ferramenta
> `pagar_pedido`, ele quebra.
>
> Segurança por ausência de capacidade é mais forte que segurança por
> confirmação, porque não depende de a confirmação estar certa.
>
> 0.1.0, sem release publicada, sem instalação externa conhecida. Se você for a
> primeira pessoa a instalar, o relato do que quebrou vale mais que um PR.
>
> github.com/yolo-labz/aferidor

**Peça:** `demo-fone.gif`. **Canal:** Hacker News (Show HN), Lobsters, Mastodon.

> **Nota para Show HN:** o título deve ser factual — *"Show HN: aferidor – an agent
> that prices groceries on your own Android and stops at payment"*. Sem
> "revolutionary", sem "AI-powered". Três respostas que já têm que estar prontas
> antes de postar, porque virão nos primeiros dez comentários:
>
> - *"does it save money?"* → não medido contra linha de base controlada;
> - *"does it work with iFood/Rappi?"* → não. Nenhum app de entrega real foi
>   automatizado, a demo roda contra uma vitrine local, e não há lista de apps
>   suportados;
> - *"is this against their ToS?"* → automatizar app de terceiro pode contrariar
>   os termos dele; a conta é sua e o risco realista é bloqueio. Está no
>   DISCLAIMER.

---

## 3. Enquadramento acadêmico — professora, pesquisa

> O material tem dois documentos, nessa ordem:
>
> 1. **O caso** — o que é, com os números de uma compra real e o que ainda não
>    está provado.
> 2. **O método** — o procedimento em si. Roda numa planilha, sem software
>    nenhum: linha de base, normalização por unidade, regra de decisão, ponto de
>    recompra, e a nota fiscal como fonte de verdade.
>
> O segundo é o que interessa fora da computação. Ele descreve um problema de
> operações doméstico — decisão sob incerteza com custo de troca, informação
> assimétrica na embalagem, e coordenação entre duas pessoas — que dá para
> ensinar e para testar sem nenhuma tecnologia.
>
> O que o material **não** tem: economia medida contra linha de base controlada.
> Um piloto de quatro semanas com quatro casas resolveria isso, e o desenho está
> no repositório.

**Peça:** nenhuma, ou `demo-fone.png` estático. **Canal:** e-mail (o rascunho
vive fora deste repositório, no vault pessoal).

> **Não peça encaixe.** A versão anterior deste texto terminava oferecendo
> "caso de ensino, extensão, PIBIC". Saiu por correção do Pedro em 26/08: quem
> pediu o material pediu uma dica, e a resposta entrega a dica e para. Se der em
> alguma coisa, a proposta parte de quem está do outro lado — e proposta que
> parte de lá vale mais que uma que a gente foi buscar. Um apêndice técnico
> também não vai: para quem não é da computação, ele só transforma um documento
> útil numa escada de três degraus.

---

## Roteiro do trailer — ~20 s

**Não gravado.** Só produzir depois que as peças do README estiverem estáveis, e
só se o resultado couber no orçamento de peso sem virar binário gigante no git.

| t | Tela | Legenda (queimada, sem áudio) |
|---|---|---|
| 0–4 s | o celular na mão, `aferidor-fone tela` lendo a vitrine | *Ele lê o preço na tela.* |
| 4–9 s | `aferidor compare`: R$ 8,32/L contra R$ 7,90/L | *900 ml parece mais barato. Não é.* |
| 9–13 s | o veredito `MANTER` em destaque | *E mesmo assim: não troque por 5%.* |
| 13–17 s | `aferidor-fone tocar 'Pagar'` → **RECUSADO** | *Pagar é com você.* |
| 17–20 s | `github.com/yolo-labz/aferidor` | *O método funciona numa planilha.* |

A tarja da vitrine tem que estar em todos os quadros, como já está no GIF.

Regras: sem música com pancada, sem corte rápido, sem contador de estrelas. A
fonte do vídeo tem que ser regenerável — se virar um MP4 que ninguém sabe
refazer, não entra no repositório; vai como anexo de release ou link.

### Checklist de gravação (Cap ou equivalente)

- [ ] Terminal limpo: sem hostname, sem usuário, sem caminho da máquina
- [ ] Só dados de fixture — nunca uma casa real
- [ ] 100 colunas (abaixo disso a tabela do `aferidor` quebra a linha)
- [ ] Tema claro; conferir também no modo escuro do GitHub
- [ ] Sem notificação na tela, sem aba de navegador com dado pessoal
- [ ] Legenda queimada, porque a maioria assiste sem som
- [ ] Exportar equivalente estático + transcrição em texto
