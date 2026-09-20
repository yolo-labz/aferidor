# Contribuir

O jeito mais útil de contribuir hoje **não é código**. É instalar isto e contar
o que quebrou — ninguém além do autor instalou este projeto ainda, então todo
relato de primeira instalação vale mais que qualquer PR.

## Antes de mexer em código

```sh
sh tests/run.sh
```

Cinco suítes, sem rede, sem celular, sem navegador. Se passar, a aritmética de
que toda decisão depende está intacta.

## As duas regras que não se negociam

### 1. Nada paga nada

Quem finaliza e paga a compra é **a pessoa**, à mão, no aplicativo do mercado.

- O servidor MCP **não tem** ferramenta de pedido ou pagamento, não alcança o
  `aferidor-fone` e não conhece `adb`. Um PR que adicione qualquer uma dessas
  coisas será recusado, e `tests/test_mcp.py` já falha antes disso.
- O `aferidor-fone` **recusa em código** tocar em botão de pagamento sem
  `--eu-confirmo` naquela invocação. Não existe modo "confirmar sempre", e não
  vai existir.

Segurança por ausência de capacidade é mais forte que segurança por
confirmação: não depende de a confirmação estar certa. Adicionou um mercado
cujo botão de pagamento usa outra palavra? Acrescente a palavra à lista `PERIGO`
em `bin/aferidor-fone` **e** o caso em `tests/test_fone.py`. Um falso negativo ali
é uma compra que ninguém autorizou.

### 2. Zero dependência

`bin/aferidor`, `bin/aferidor-fone` e `bin/aferidor-mcp` usam **só a biblioteca padrão do
Python**. Sem `pip install`, sem ambiente virtual, sem cadeia de suprimento para
auditar. A extensão não tem build.

Isso é uma restrição de produto, não preguiça: o projeto é instalado por
`curl | sh` e precisa ser auditável numa sentada. Um PR que traga dependência
precisa argumentar por que o problema não cabe na stdlib — e a resposta quase
sempre é que cabe.

## Como o código se parece

- Português nos textos que o usuário lê; inglês no código e nos comentários.
- Comentário explica **por quê**, não o quê. `# incrementa i` não ajuda ninguém.
- Lógica não-trivial deixa **uma verificação executável** — a menor coisa que
  falha se a lógica quebrar. Sem framework, sem fixture.
- Datas: `DD/MM/AAAA` na prosa, `AAAA-MM-DD` em frontmatter, commit e nome de
  arquivo.

## Commits e PRs

Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`), assunto em até 72
caracteres. Assine com `git commit -s` (DCO) — é higiene, não contrato: não há
CLA aqui.

No PR, diga o que quebrou antes e o que passou depois. Cole a saída do
`tests/run.sh`.

## Relatar problema

Abra uma issue. Se for de segurança — algo que exponha dados ou permita gasto
não autorizado —, leia o [SECURITY.md](SECURITY.md) primeiro: há um canal
privado.

Ao relatar, **não cole nota fiscal**. Ela tem CPF e a lista completa do que a
sua casa consome. Descreva o problema, não o documento.

## O que provavelmente não será aceito

- Ferramenta de pedido ou pagamento no MCP (ver regra 1).
- Dependência de runtime (ver regra 2).
- Instruções de root, Magisk ou burla de atestação de integridade — o projeto
  não pede a ninguém que enfraqueça a segurança do próprio telefone.
- Daemon não-oficial de WhatsApp.
- Adaptador por mercado que vire manutenção permanente sem alguém que a mantenha.
- Número de economia sem contrafactual. Se você medir de verdade, com linha de
  base, isso é a contribuição mais valiosa que o projeto pode receber.
