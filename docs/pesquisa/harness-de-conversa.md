# Como o aferidor fala com uma IA — pesquisa e decisão

**Data:** 25/08/2026
**Pergunta:** existe um harness pequeno que dê para incorporar, para que a
ferramenta converse com uma IA sozinha?

**Resposta curta:** existe, e a decisão foi **não incorporar nenhum**. O que
faltava não era um harness — era um *limite*. Ficou um servidor MCP.

---

## O problema

O `aferidor` não fala com modelo nenhum: sem chamada de rede, sem chave de API. As
quatro skills só funcionam para quem **já tem** Claude Code — o instalador
copia para `~/.claude/skills` e imprime "skipping" quando a pasta não existe.

Para a usuária que motivou o projeto — professora de administração, não
programadora — a metade conversacional simplesmente não existia.

## As duas frentes discordaram

Foi o desacordo mais útil de toda a pesquisa deste projeto.

| | Recomendou | Argumento central |
|---|---|---|
| **Frente A** | escrever um laço próprio (~300 linhas) + detectar `llm`/`aichat` se estiverem no PATH | é o único caminho que preserva "só stdlib, auditável numa sentada" e em que a professora roda **um** comando; o protocolo de tool-calling é o mais estável do mercado |
| **Frente B** | servidor MCP; **não** escrever laço próprio, **não** empacotar harness de terceiro | o laço próprio faz o projeto herdar autenticação, retry, limite de contexto, mudança de formato, cobrança e suporte — "um diff pequeno que vira obrigação permanente" |

## O que decidiu

**A parede da chave de API**, que as duas frentes levantaram e nenhuma
resolveu direito.

- Um **laço próprio** obriga toda usuária a tirar **chave de API**: conta de
  desenvolvedor, cartão internacional, cobrança por token em dólar. É uma
  interface comercial para desenvolvedor.
- Um **cliente MCP** roda com **assinatura de consumidor** — a mesma natureza
  de assinar streaming.

Para uma professora no Brasil, essa é a diferença entre dá e não dá. Não é
detalhe de configuração: é a barreira.

E há a assimetria de manutenção. O laço próprio é pequeno **no primeiro dia**;
depois vem 429, formato de resposta que muda, modo de raciocínio estendido,
contexto estourado, streaming, nome de modelo descontinuado. Para um mantenedor
solo, isso concorre com o trabalho que só este projeto faz.

## O que ficou de cada frente

Nem tudo da Frente A foi descartado:

- ✅ **`llm`, `aichat` e Claude Code como caminhos opcionais**, documentados,
  nunca empacotados. Custo: prosa.
- ✅ **Modelo local é armadilha para não-programador.** Instalação de gigabytes,
  escolha de modelo, e falha em formatação de chamada de ferramenta — pior em
  português. Documentado como opção avançada, nunca padrão.
- ❌ **O laço próprio**, adiado. Se um dia houver evidência de gente com chave de
  API e sem cliente MCP, ele volta à mesa. Hoje é especulação.

E o alerta da Frente B sobre portabilidade ficou: Agent Skills é formato de um
fornecedor. As skills continuam, mas a doutrina (`AGENTS.md`) é a fonte
canônica, e ela é markdown comum que qualquer agente lê.

## Onde o desenho ficou mais simples que as duas propostas

A Frente B desenhou um "token de aprovação" para pagamento: o modelo propõe, o
código exige confirmação fresca, a aprovação expira se o carrinho mudar.
Cuidadoso — e desnecessário aqui.

**Pedro decidiu (25/08/2026): quem paga é a pessoa, à mão, no aplicativo do
mercado.** Isso apaga o problema inteiro em vez de administrá-lo:

| Risco que a Frente B mapeou | Com token de aprovação | Aqui |
|---|---|---|
| Prompt injection de nota/página | mitigar com delimitação e proveniência | **não há o que atacar** |
| Modelo convencido a pular o portão | token fresco, expira ao mudar | **não há portão para pular** |
| Aprovação reusada | invalidar ao mudar carrinho | **não há aprovação** |
| Modelo inventando preço | rastrear fato vs estimativa | continua valendo — instrução + dado estruturado |

O servidor MCP não alcança o `aferidor-fone`, não conhece `adb`, não abre app.
**A capacidade não existe**, e `tests/test_mcp.py` falha se alguém a
introduzir — inclusive se o código apenas mencionar o driver do celular. O teste
foi validado ao contrário: com uma ferramenta `pagar_pedido` plantada de
propósito, ele quebra.

Segurança por ausência de capacidade é mais forte que segurança por
confirmação, porque não depende de a confirmação estar certa.

Só a quarta linha continua sendo trabalho de verdade: um modelo pode inventar
preço. Contra isso valem as instruções de abertura, dados estruturados vindo das
ferramentas, e o veredito `COLETAR`, que é o programa se recusando a opinar.

## O que não foi incorporado, e por quê

| Candidato | Por que não |
|---|---|
| `llm` (Simon Willison) | ótimo, Apache-2.0, estável — mas é **segunda instalação + chave de API**. Fica como opção documentada |
| `aichat` | binário único, MIT — mesma barreira, e config em TOML não é para não-programador |
| `mods` | **sem tool-calling.** Conversaria sem conseguir rodar `aferidor compare` |
| Claude Code / Agent SDK | proprietário, não empacotável. Já suportado pelas skills |
| smolagents / pydantic-ai | são a resposta certa *se* o projeto aceitasse dependência. Aceitar é que é a decisão |
| LangChain / LlamaIndex | pesados demais para cinco ferramentas sobre arquivos de texto |
| Goose | financiamento aberto do Block cortado em 2025 [não verificado] — risco de dependência alto |
| Ollama / modelo local | gigabytes, escolha de modelo, e falha de formatação em português. Armadilha para o público-alvo |

## O que ficou por verificar

- **Quão amigável é a configuração de MCP** nos clientes de consumidor, para
  quem não programa. Não verificado — é o próximo teste real, e o documento
  [como conversar](../explicacao/como-conversar.md) diz isso em vez de fingir.
- Se algum cliente de assinatura comum **restringe** servidor MCP local.
- Se a professora consegue seguir o passo a passo sem ajuda. **Esse é o teste
  que decide** se este caminho valeu.

Se a resposta for não, a conclusão honesta não é "escreva o laço próprio" — é
que a metade conversacional não está pronta para esse público, e o caminho 1
(sem IA nenhuma) é o produto dela.
