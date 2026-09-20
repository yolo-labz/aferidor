# Privacidade — o que fica onde

A decisão de arquitetura mais importante do projeto é chata de explicar e fácil
de verificar: **não existe servidor.**

Não há conta para criar, não há sincronização, não há telemetria, não há "aceite
os termos". O CLI não faz nenhuma requisição de rede. A extensão não faz nenhuma
requisição de rede. O `aferidor-fone` fala só com o aparelho que está na sua mesa.

Isso não é minimalismo estético. É o que faz a pergunta "que dados vocês
coletam?" ter resposta de uma palavra, e o que mantém o projeto longe de um
monte de obrigação que só faz sentido para quem opera serviço.

## O que é seguro versionar

| Dado | Onde | Versionar? | Por quê |
|---|---|---|---|
| Observações de preço | `dados/observacoes.csv` | ✅ | data, produto, mercado, valor — não identifica ninguém |
| Itens e mercados | `itens/`, `mercados/` | ✅ | catálogo, não pessoa |
| Despensa | `despensa/` | ✅ | revela hábito de consumo, mas não identidade |
| Diário | `DIARIO.md` | ⚠️ | você escreve nele — não coloque o que não quer publicar |
| **Doutrina** | `AGENTS.md` | ⚠️ **revise** | costuma ter alergia e restrição médica |
| **Notas fiscais** | `notas/` | ❌ **nunca** | CPF + consumo completo |
| Credenciais | em lugar nenhum | ❌ | não existem no projeto |

## As notas fiscais são o ponto sensível

Uma NFC-e traz o seu CPF, o CNPJ e o endereço do mercado, e a lista **item a
item** do que a sua casa comprou.

Essa última parte é mais reveladora do que as pessoas esperam. Uma lista de
compras mostra remédio de uso contínuo, quantidade de álcool, fralda, fórmula
infantil, teste de gravidez. Dá para inferir condição de saúde, composição da
família e situação financeira de um jeito que nenhuma dessas informações
isoladas permitiria.

O `.gitignore` do modelo já exclui `notas/`, `*.xml`, `*.pdf` e `*.zip`. **Não
apague essas linhas para "organizar melhor".**

Os *preços* extraídos delas vão para `observacoes.csv`, que é seguro: data,
produto, mercado, valor. O CPF fica no XML, e o XML fica na sua máquina.

## A doutrina merece uma revisão antes de publicar

O `AGENTS.md` é o arquivo mais útil para compartilhar — é onde o método vira
concreto — e é o que mais frequentemente contém dado sensível.

A seção "restrições que não se negociam" existe para registrar alergia e
prescrição. Isso é **dado de saúde**, e sobre pessoas que talvez não tenham
opinado sobre publicar. Se for tornar o repositório público, releia essa seção e
generalize ("alérgeno A", "restrição médica em vigor") ou remova.

## Sobre outras pessoas da casa

O sistema registra preferência, veto e negociação de gente que não instalou
nada e não leu nenhum documento.

Duas regras que valem mais que qualquer configuração:

1. **Preferência de outra pessoa se pergunta, não se deduz.** Um sistema que
   infere gosto a partir de comportamento observado constrói uma teoria
   confiante e errada, e a sustenta por meses porque nunca é checada. Aconteceu
   neste projeto: metade das restrições de cardápio vinham de uma inferência
   sobre alguém que nunca foi consultada. Ver
   [o caso](../01-o-caso.md#a-cozinheira).
2. **Conversa não entra no repositório.** Resuma a decisão ("prefere a marca X"),
   não o diálogo.

## Se você for publicar o seu repositório

Antes:

- [ ] `notas/` está vazio e ignorado
- [ ] `AGENTS.md` revisado — sem alergia nomeada, sem prescrição, sem nome de terceiro
- [ ] `DIARIO.md` relido — é append-only, então o que está lá está lá
- [ ] Sem endereço completo, telefone, CPF ou final de cartão em nenhum arquivo
- [ ] `git log -p | grep -iE 'cpf|cartão|senha'` não devolve nada
- [ ] Nomes de outras pessoas: só se elas concordarem

O último item não é formalidade. Publicar é irreversível na prática: cópia
indexada continua existindo depois de você apagar.

## O que o `aferidor check` faz por você

Ele valida estrutura — datas, preços, embalagens que não normalizam, itens sem
arquivo. **Não é um detector de dado pessoal**, e a lista `proibido_no_repo` no
`aferidor.toml` é um lembrete, não uma garantia.

A revisão antes de publicar é sua.
