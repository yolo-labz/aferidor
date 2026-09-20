# Camada 4b — celular Android conectado à máquina

O único caminho que realmente fecha um pedido pago num aplicativo de entrega
brasileiro. Exige hardware, e o motivo é técnico e definitivo.

## Por que não dá para usar emulador

Os aplicativos consultam o **Play Integrity API**, que devolve um veredito sobre
o dispositivo. O nível que os apps exigem, `MEETS_DEVICE_INTEGRITY`, significa
"build certificado pelo Google, em hardware que o Google reconhece". A
verificação é **do lado do servidor**: confere se a assinatura do build e a
impressão do hardware batem com um aparelho certificado.

Uma máquina virtual não tem TEE para assinar essa cadeia. Não é um bloqueio a
contornar, é o desenho. Emulador (AVD), Waydroid, redroid, Genymotion, Anbox,
BlueStacks, Android-x86, WSA — todos morrem no mesmo muro, e morrem
especificamente **no passo do pagamento**: instalam, abrem, às vezes logam, e
recusam a transação.

O modo de falha é pior que uma recusa limpa: a conta é marcada de risco. Você
perde a conta que já tinha.

> **Nada de root, Magisk ou módulo de correção de integridade.** Não está na
> documentação, não está no código, não está numa sugestão. É corrida
> armamentista contra o Google, viola os termos, leva a banimento, e — o que
> decide — instrui alguém a enfraquecer a segurança do próprio telefone, num
> aparelho que provavelmente tem o banco dele instalado.

## O aparelho

- **Certificado pelo Google, bootloader travado.** Qualquer aparelho de linha de
  entrada serve. Destravar o bootloader anula toda a estratégia acima.
- **Dedicado.** Compartilhar com o telefone pessoal é a origem da maior parte dos
  problemas: notificação rouba o primeiro plano, outro app abre por deep link, e
  a automação toca no lugar errado.
- **Isolado:** conta Google separada, sem aplicativo de banco, sem WhatsApp
  pessoal, sem SIM (ou um pré-pago dedicado). O aparelho guarda credencial de
  entrega e um cartão — trate como dispositivo de credencial, não como brinquedo.
- **Atualizado.** Um aparelho barato com cartão salvo e porta adb aberta vira
  passivo no dia em que parar de receber correção.
- **Na rede:** de preferência numa VLAN/SSID próprio, sem porta exposta para
  fora. Quem alcança a porta adb controla o telefone.

## Conectar

**USB:** ativar Opções do desenvolvedor (tocar 7× em *Número da versão*), ligar
*Depuração USB*, plugar, desbloquear a tela e aceitar o aviso.

**Sem fio** (Android 11+), que é o modo de uso normal aqui:

```bash
# no telefone: Opções do desenvolvedor → Depuração por Wi-Fi → Parear com código
adb pair <ip>:<porta-de-pareamento>       # código de 6 dígitos, uma vez só
adb connect <ip>:5555
```

Confirmar:

```bash
aferidor-fone dispositivos
```

## A regra do serial

**Se houver mais de um aparelho, fixe qual.** O `aferidor-fone` se recusa a agir
sem isso, de propósito:

```bash
export ANDROID_SERIAL=192.168.1.50:5555
```

Sem fixar, os comandos caem no aparelho errado e o dump volta vazio — que é
indistinguível de um script quebrado. Já custou uma sessão inteira de depuração
neste projeto.

## Operar

```bash
aferidor-fone tela                      # o que está na tela agora
aferidor-fone achar "Adicionar"         # onde está o elemento
aferidor-fone tocar "Adicionar ao carrinho"
```

O `tocar` resolve o elemento num dump **novo**, no momento do toque. Nunca passe
coordenada: coordenada de uma tela anterior é toque no lugar errado, e no meio
de um checkout isso compra a coisa errada.

Quando vários elementos casam, ele recusa e lista — porque o texto do botão
também aparece no cartão inteiro que o contém. Seja mais específico, ou
`--primeiro` para pegar o menor (o botão, não o cartão).

## O portão de pagamento é código

```
$ aferidor-fone tocar "Finalizar pedido"

aferidor-fone: REFUSED — 'Finalizar pedido' matches the payment word 'finalizar pedido'.

  This taps a button that spends money or contacts someone. The human
  approves it, in the moment, or it does not happen.
```

Passa só com `--eu-confirmo` **naquela invocação específica**. Não existe modo
"confirmar sempre", e não deve existir: aprovação de ontem não vale para hoje.

Antes de pedir a confirmação, mostre o total, o mercado, o cartão e o endereço.

## Substituição de item em falta

É a parte difícil, não o caminho feliz.

A escolha entre substituir e reembolsar é **decisão de política da casa**
(`AGENTS.md`, seções 2 e 3), não um quebra-cabeça de interface para resolver
rápido. Item marcado como "nunca substituir" é reembolsado sempre, mesmo quando
o substituto parece obviamente equivalente. Alérgeno é reembolso absoluto.

Detalhe observado em campo que trava o fluxo: em alguns aplicativos o modal de
falta é **horizontal** — as sugestões do separador ficam visíveis e a opção de
reembolso só aparece depois de **arrastar o carrossel**. Sem isso o fluxo trava
e parece que o script quebrou.

## Quando não bater com o descrito

**Pare e devolva para o humano.** Layout de app muda sem aviso, e improvisar
toques dentro de um fluxo de pagamento é como se compra a coisa errada.

Tire um print, descreva o que está na tela, entregue. Cinco minutos de dedo
humano custam menos que um pedido errado.

## Higiene

- Não deixe override de geometria de tela (`wm size`, `wm density`) — persiste
  entre reinícios e reescala a interface para quem pegar o telefone depois.
- Não deixe pacote desabilitado. Desabilitar um app para ele parar de roubar o
  primeiro plano funciona, mas `pm disable-user` no app errado deixa o próprio
  aplicativo de compra sem atividade de lançamento.
- Toques com menos de ~700 ms de intervalo têm assinatura de robô. Os
  aplicativos pontuam ritmo de interação. O `aferidor-fone` já espaça e adiciona
  jitter; não contorne isso com laço.

## Custo corrente

Estimado, não medido: **20 a 60 horas por mercado por ano** de manutenção, por
mudança de layout. Esse número é a razão de a camada 4 ser opcional, e a razão
principal para não vender isto como serviço hoje.
