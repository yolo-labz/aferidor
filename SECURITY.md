# Segurança

## Como reportar

Encontrou algo que expõe dados ou permite gasto não autorizado? Abra uma issue
com o rótulo `security` em <https://github.com/yolo-labz/aferidor/issues>, ou, se o
problema for explorável por terceiros, mande em privado antes de publicar.

Não há programa de recompensa. Há gratidão e crédito no changelog.

## O modelo de ameaça

O projeto é **local-first** e essa é a decisão de segurança mais importante que
ele toma. Não existe servidor, não existe conta, não existe sincronização.
Nenhum dado sai da sua máquina, exceto quando você mesmo o publica.

### O que o software nunca faz

- Não pede, guarda ou transmite senha, TOTP, número de cartão, CVV ou token.
- Não faz requisição de rede em nenhum ponto do CLI (`aferidor`), nem da extensão.
  O `aferidor-fone` fala apenas com o seu próprio aparelho, via `adb`.
- Não completa pagamento sozinho. Ver abaixo.
- Não instala nada com `sudo`. O instalador se recusa a rodar como root.

### O portão de pagamento é código

O `aferidor-fone tocar` recusa qualquer elemento cujo texto contenha um termo de
pagamento (`pagar`, `finalizar pedido`, `confirmar pagamento`, `place order`,
`enviar`, entre outros). Passa somente com `--eu-confirmo` naquela invocação
específica. Não existe modo persistente, e não deve existir.

A lista está em `bin/aferidor-fone` (`PERIGO`) e é verificada por
`tests/test_fone.py`. **Se você adicionar um mercado cujo botão de pagamento
usa outra palavra, adicione a palavra à lista e ao teste.** Um falso negativo
aqui é uma compra não autorizada.

### Onde ficam os seus dados

| Dado | Onde | Versionar? |
|---|---|---|
| Observações de preço | `dados/observacoes.csv` | sim — não tem dado pessoal |
| Itens, mercados, despensa | `itens/`, `mercados/`, `despensa/` | sim |
| Doutrina da casa | `AGENTS.md` | **cuidado** — costuma conter alergia e restrição médica |
| Notas fiscais (XML/PDF) | `notas/` | **não** — CPF + consumo completo. Já está no `.gitignore` |
| Credenciais | em lugar nenhum | — |

O `AGENTS.md` merece atenção: ele frequentemente registra alergia, prescrição e
restrição alimentar, que são **dados sensíveis**. Se for publicar o seu
repositório, revise-o antes.

### A extensão de navegador

Pede `activeTab` e `scripting`, e **nenhuma permissão de host**. Consequência
prática: ela não consegue rodar em página nenhuma até você clicar no botão, e só
naquela aba. Não lê cookie, não lê armazenamento, não lê tráfego, não faz
requisição. O que ela extrai vai para a sua área de transferência e para mais
lugar nenhum.

Você pode verificar isso: são três arquivos pequenos em `extensao/`, sem
minificação e sem dependência.

### Se você deixar o aparelho Android acessível na rede

A porta do `adb` não tem autenticação além do pareamento inicial. **Quem alcança
a porta controla o telefone.** Coloque o aparelho numa rede isolada, não exponha
a porta para fora, e trate o aparelho como dispositivo de credencial — ele
guarda login de entrega e um cartão. Ver
[camada 4b](skills/aferidor-pedido/referencia/tier-3-android.md).

### O instalador

É `curl | sh`, o que é uma transferência de confiança e não um mecanismo de
segurança. O que foi feito para que ela seja responsável:

- Corpo inteiro em grupo de chaves `{ ... }` — download truncado falha como erro
  de sintaxe em vez de executar metade.
- Recusa rodar como root.
- Instala só sob `$HOME`, sem `sudo`.
- `--dry-run` mostra tudo antes.
- Imprime o SHA-256 do que baixou; `AFERIDOR_SHA256` verifica contra um valor seu.
- `--version` fixa uma tag exata.
- Não edita nenhum arquivo de shell seu — imprime a linha de PATH para você
  colar.
- Roda o autoteste no fim e falha se ele falhar.

Se preferir não confiar no pipe, o caminho está documentado no
[README](README.md#instalação): baixe, leia, execute.
