# Falar com o vendedor pelo WhatsApp

No Brasil, boa parte do mercado de bairro não tem site nem aplicativo. Tem um
número de WhatsApp, e o pedido é uma mensagem de texto. Ignorar isso é ignorar
onde a compra realmente acontece.

O `aferidor` escreve a mensagem. **Ele não envia.**

```sh
aferidor zap                  # o pedido do que está faltando
aferidor zap oleo-de-soja     # uma pergunta de preço sobre um item
```

```
Oi! Queria fazer um pedido:
• Óleo de soja
• Papel higiênico

──────────────────────────────────────────────────────────────────
O aferidor não envia mensagem — ele não tem essa capacidade.
Para mandar esta, com allowlist e limite de taxa por baixo de tudo,
use o wa (github.com/yolo-labz/wa):

  wa allow add <numero>@s.whatsapp.net --actions send
  wa send --to <numero>@s.whatsapp.net --body $'Oi! Queria fazer um pedido:\n• Óleo de soja\n• Papel higiênico'
```

## Por que o envio mora em outro programa

A mesma razão de o pagamento morar no seu dedo: **a fronteira é mais forte
quando a capacidade não existe.** O `aferidor` não tem código de rede, não tem
sessão de WhatsApp, não guarda o seu número. Não há gate a burlar aqui porque
não há porta.

Mandar mensagem em nome de alguém é diferente de ler um preço. Se der errado, dá
errado no telefone de uma pessoa real, com um vendedor real que atende aquela
casa. Isso merece um programa feito para essa responsabilidade — com lista de
permissão, limite de taxa e registro do que foi enviado — e não um `print()`
dentro de um comparador de preço.

## O `wa`

[`yolo-labz/wa`](https://github.com/yolo-labz/wa) é um daemon em Go que segura a
sessão do WhatsApp Multi-Device e atende por um socket Unix. O que importa aqui:

- **Default-deny.** Um número só recebe mensagem depois de entrar na allowlist,
  por ação. Sem `wa allow add`, o envio sai com código 11 e nada acontece.
- **Limite de taxa não-sobrescrevível.** Não existe `--force`.
- **Registro append-only.** Dá para auditar o que foi enviado, quando e para
  quem.

Instalação, pareamento e o resto estão [no manual do próprio
`wa`](https://github.com/yolo-labz/wa/blob/main/docs/manual.md).

### O `$'...'` não é enfeite

`wa send --body` recebe uma string e não lê nada da entrada padrão. Entre aspas
simples comuns, `\n` chega ao vendedor como as letras `\` e `n`, e o pedido vira
uma linha só ilegível. As aspas `$'...'` são o que faz o bash e o zsh
transformarem `\n` em quebra de linha de verdade — por isso o `aferidor zap` já
imprime o comando nesse formato.

## Antes de mandar

O texto é um rascunho, não um pedido pronto:

1. **Confira a lista.** Ela sai do `aferidor falta`, que lê compras e não o
   armário. Ele sugere onde olhar; quem sabe o que tem em casa é você.
2. **Confira o número.** Uma lista de compras para o contato errado é constrangimento,
   não prejuízo — mas é constrangimento evitável.
3. **Escreva como você escreve.** O texto padrão é neutro de propósito. Se o
   vendedor te conhece, um "bom dia, seu Antônio" vale mais que a eficiência.

## O que isto não faz

- Não fecha pedido, não combina entrega, não paga. O vendedor responde, e a
  conversa é sua.
- Não lê as respostas nem extrai preço delas. Se o vendedor mandar um preço que
  vale a pena, registre com `aferidor record`.
- Não manda em massa. Um pedido para o seu mercado é uma mensagem; o `wa` tem
  limite de taxa exatamente para que nunca vire outra coisa.

---

Volta para [as quatro camadas](../explicacao/camadas.md) ·
[como conversar](../explicacao/como-conversar.md)
