# As quatro camadas

O destino do projeto é **um agente que pesquisa preço dentro dos aplicativos de
entrega, no seu celular, monta o carrinho, e para para você finalizar** — a
camada 4b.

Mas ele é quatro coisas empilhadas, e você pode parar em qualquer uma. Isso
importa por dois motivos: as duas primeiras camadas já economizam dinheiro
sozinhas e não exigem nada além de você, e a última exige hardware que nem toda
casa tem. Quem para na camada 2 tem uma ferramenta útil; quem chega na 4b tem o
ciclo fechado.

| Camada | O que é | Exige | Valor |
|---|---|---|---|
| **1. Método** | o jeito de decidir | nada | ★★★★ |
| **2. Ferramenta** | o `aferidor` | um computador | ★★ |
| **3. Agente** | as skills | um assistente de IA | ★★ |
| **4a. Execução web** | fechar pedido no site | navegador | ★ |
| **4b. Execução no app** | fechar pedido no aplicativo | **celular Android dedicado** | ★ |

---

## Camada 1 — o método

[O documento do método](../02-o-metodo.md), inteiro, numa planilha.

Linha de base, preço por unidade-base, a regra de migração, ponto de recompra,
frete e pedido mínimo, e a nota fiscal como fonte de verdade.

**Comece aqui, e comece hoje.** Se a camada 1 não estiver funcionando na sua
casa, automatizá-la só produz erro mais rápido. É também a única camada que
funciona se você não tiver nenhuma vontade de instalar software.

## Camada 2 — a ferramenta

O `aferidor`: um programa em Python, sem dependências, que guarda o histórico em
arquivos de texto e faz a aritmética das seções 4, 5 e 9 do método.

O que ele adiciona sobre a planilha: normalização automática de embalagem, a
regra de migração aplicada consistentemente, e importação de nota fiscal
eletrônica. O que ele **não** adiciona é qualquer julgamento — as decisões
continuam suas.

Vale a partir de umas 30 linhas e 3 mercados, que é quando a planilha começa a
doer.

## Camada 3 — o agente

Duas portas para o mesmo lugar, e elas convivem:

- **O servidor MCP** (`aferidor-mcp`) — expõe os dados e as contas a **qualquer**
  cliente de IA compatível. É o caminho recomendado, porque roda com assinatura
  de consumidor em vez de chave de API. Ver [como conversar](como-conversar.md).
- **As *skills*** — instruções mais ricas, que carregam o procedimento inteiro
  (casar SKU de nota fiscal, montar lista respeitando a doutrina, quando parar e
  perguntar). Funcionam em Claude Code.

As skills descrevem **como raciocinar**; o MCP descreve **o que dá para
chamar**. Nos dois casos a doutrina do `AGENTS.md` da sua casa é a autoridade.

O que ele adiciona: ler a nota fiscal e casar os nomes de produto, montar a
lista a partir da despensa, lembrar das regras da casa (alergia, marca vetada,
quem precisa aprovar), e conversar em português sobre tudo isso.

O que ele **não** adiciona: nenhuma autoridade nova. O agente opera as mesmas
duas camadas de baixo e para nos mesmos portões.

## Camada 4 — a execução

Fechar o pedido. Divide-se em dois caminhos com viabilidades muito diferentes.

### 4a — pelo site, no navegador

Não existe atestação de dispositivo na web. O site do mercado, num navegador
normal, é o único caminho **só-software** capaz de fechar um pedido pago.

Funciona onde o mercado tem loja web de verdade — varejistas de e-commerce
completos costumam ter; serviços que nasceram no celular costumam não ter
paridade. Verifique por mercado antes de contar com isso.

A **extensão de navegador** deste projeto pertence aqui, mas resolve um problema
diferente e mais útil: ela **captura preços** da página que você já está vendo,
logado na sua própria conta. Não precisa de senha, não sincroniza sessão, não
tem robô para detectar — porque não há robô, há você navegando. Ver
[a pesquisa](../pesquisa/harness-de-login.md).

### 4b — pelo aplicativo, num celular conectado

**Exige um aparelho Android físico, homologado pelo Google Play, com bootloader travado,
conectado à máquina.** Não tem contorno por software: emulador, Waydroid,
redroid, BlueStacks e afins falham no Play Integrity, especificamente no passo
do pagamento.

É o caminho de maior fidelidade — o aplicativo é onde estão o cupom, o saldo da
carteira e o fluxo de substituição. Se você tem um celular sobrando, é o melhor
lugar para colocá-lo.

Setup, regras e armadilhas: [camada 4b](../../skills/aferidor-pedido/referencia/tier-3-android.md).

---

## O portão humano

**Vale em todas as camadas, e não muda.**

**Quem finaliza e paga a compra é você, à mão, no aplicativo do mercado**
(decidido em 25/08/2026). O software monta o carrinho; o último passo é seu.

Isso é aplicado de dois jeitos diferentes, de propósito:

- **No servidor MCP: por ausência.** Não existe ferramenta de pedido ou
  pagamento. O servidor não alcança o celular, não conhece `adb`, não abre
  aplicativo. Não há portão para um modelo pular, nem aprovação para forjar,
  nem prompt injection que valha a pena escrever — **a capacidade não existe**.
- **No `aferidor-fone`: por recusa em código.** Tocar num botão cujo texto contenha
  "pagar", "finalizar pedido", "confirmar pagamento", "place order" e afins é
  recusado, e só passa com `--eu-confirmo` naquela invocação específica. Não
  existe modo "confirmar sempre".

Segurança por ausência de capacidade é mais forte que segurança por
confirmação, porque não depende de a confirmação estar certa. Onde dá para
tirar a capacidade, ela foi tirada.

Três razões, em ordem de peso:

1. **Confiança é assimétrica.** Um agente que erra uma compra de R$ 30 apaga a
   economia de um mês em confiança. O portão custa dez segundos.
2. **A responsabilidade é da casa.** Sob a legislação de consumo, quem discute
   com o mercado é você, não o software.
3. **O valor está antes do botão.** Decidir o que comprar, onde, e quando não
   mudar nada é onde a economia acontece. Apertar "finalizar" é trinta segundos.

## Onde parar

| Se você… | Pare na camada |
|---|---|
| quer gastar menos sem instalar nada | 1 |
| tem mais de 30 itens e 3 mercados | 2 |
| quer conversar em português sobre os números | 3 (via [MCP](como-conversar.md)) |
| quer capturar preço sem digitar | 4a (a extensão) |
| tem um celular Android sobrando | 4b |

**Não tem celular sobrando?** Você fica sem o ciclo fechado — que é o ponto de
chegada do projeto —, mas não sem a economia. As camadas 1 a 3 respondem *o que
comprar e onde*, que é onde a decisão acontece; o que falta é quem aperta os
botões no aplicativo. Muita gente vai preferir apertar sozinha, e isso é uma
escolha legítima, não um consolo.
