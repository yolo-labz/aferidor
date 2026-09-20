# Extensão — capturar preços da página

Lê os preços da página que você está vendo e devolve as linhas prontas para o
seu `dados/observacoes.csv`.

## Por que uma extensão

Porque ela resolve o problema de login **por não ter um**.

Todo o resto — navegador headless, sessão sincronizada, cookie exportado,
credencial guardada — precisa reproduzir o seu login em outro lugar, e cada uma
dessas coisas é uma senha para guardar, uma sessão para renovar e uma detecção
de robô para contornar.

A extensão roda dentro do navegador onde **você já está logado**. Passkey e
2FA continuam funcionando porque nada foi contornado. O mercado vê o seu
navegador de sempre, no seu IP de sempre, porque é o seu navegador de sempre.

Ver [a pesquisa que levou a esta decisão](../docs/pesquisa/harness-de-login.md).

## Instalar

Não está em loja de extensões. Carregue descompactada:

**Chrome, Edge, Brave**
1. `chrome://extensions`
2. Ligue *Modo do desenvolvedor* (canto superior direito)
3. *Carregar sem compactação* → escolha esta pasta

**Firefox** (temporária, some ao fechar o navegador)
1. `about:debugging#/runtime/this-firefox`
2. *Carregar extensão temporária* → escolha o `manifest.json` desta pasta

## Usar

1. Abra a página de produtos do mercado, logado normalmente.
2. **Role até ver os produtos.** Listas que carregam ao rolar só existem no DOM
   depois de aparecerem — o que não foi renderizado não é lido.
3. Clique no ícone da extensão.
4. Confira a lista. Ajuste o mercado e a data.
5. *Copiar* → cole no fim de `dados/observacoes.csv`, sem repetir o cabeçalho.

Depois:

```bash
aferidor check     # confere se as linhas novas fazem sentido
aferidor advise    # o que mudou na recomendação
```

## Confira antes de colar

A leitura é automática e **erra**. Os dois erros a procurar:

- **Embalagem vazia.** O item aparece marcado em laranja e desmarcado. Sem
  embalagem não dá para normalizar, e um preço sem unidade-base é um preço que
  vai enganar você depois. Preencha à mão ou descarte a linha.
- **Nome errado.** Layouts de cartão variam; às vezes o nome capturado é o da
  promoção ou o da categoria. O `sku` sai do nome, então um nome errado cria um
  item novo em vez de somar ao existente.

Nenhum desses erros é ruidoso. É por isso que o passo 4 existe.

## Permissões

`activeTab` e `scripting`. **Nenhuma permissão de host.**

Consequência prática: a extensão não consegue rodar em página nenhuma até você
clicar no botão, e só naquela aba. Ela não lê cookie, não lê armazenamento, não
lê tráfego de rede, e não faz nenhuma requisição — o texto vai para a sua área
de transferência e para mais lugar nenhum.

São três arquivos pequenos, sem minificação e sem dependência:

| Arquivo | O quê |
|---|---|
| `manifest.json` | as permissões, que você pode conferir em dez segundos |
| `coletor.js` | injetado na aba ao clicar; lê a página renderizada |
| `popup.js` + `popup.html` | a lista, a conferência e o CSV |

## Quando não funciona

- **"Nenhum preço reconhecido"** — role até os produtos aparecerem e clique de
  novo. Se persistir, o mercado provavelmente monta o preço de um jeito que o
  coletor não reconhece; registre à mão com `aferidor record`.
- **Página interna do navegador** (`chrome://`, loja de extensões) — bloqueada
  pelo próprio navegador, não pela extensão.
- **Preço em imagem** — não tem o que ler. Acontece em encarte.

## Limite honesto

Cada mercado tem um DOM diferente e muda sem aviso. Este coletor é genérico:
procura padrões de preço em reais e o texto mais próximo que parece nome de
produto. Funciona razoavelmente em muitos lugares e mal em alguns.

Um adaptador por mercado leria melhor — e viraria manutenção permanente,
estimada em dezenas de horas por mercado por ano. Por ora, genérico e conferido
por você é a troca certa.
