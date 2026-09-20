# Exposição jurídica — memorando de pesquisa

**Data:** 25/08/2026.

> ⚠️ **Isto não é parecer jurídico.** É pesquisa feita por modelo de linguagem,
> sem acesso a fontes primárias, para orientar decisões de arquitetura. Todo
> ponto marcado **[confirmar]** — e qualquer ponto antes de haver receita —
> precisa de advogado e contador. Ver [DISCLAIMER](../../DISCLAIMER.md).

---

## A conclusão que orienta a arquitetura

**Quase toda a exposição jurídica deste projeto desaparece se ele for
local-first e não custodiar credencial.** Não é uma escolha estética — é a
medida de redução de risco com melhor retorno por unidade de esforço, e o
projeto já a tomou.

| Escolha | Esforço | Risco que elimina |
|---|---|---|
| **1. Processar só na máquina do usuário** | já feito | tira o caso do escopo de obrigação de controlador |
| **2. Nunca custodiar credencial** | já feito | acesso indevido, vazamento de autenticação |
| **3. Portão humano antes de pagar** | já feito, em código | consumidor, estorno, compra não autorizada |
| **4. Consentimento explícito por ação** | parcial | base legal para dado sensível |
| **5. Nunca armazenar cartão** | já feito | LGPD + PCI |
| 6. Agregação em servidor | alto | *cria* obrigação, não elimina |

## LGPD — o divisor de águas

**Caso auto-hospedado.** O usuário trata os próprios dados na própria máquina.
A hipótese de **uso exclusivamente pessoal** (art. 4º, I) tende a se aplicar.

**A isenção deixa de valer no momento em que** [confirmar]:

1. O repositório é compartilhado ou publicado.
2. Um terceiro — inclusive o desenvolvedor, via telemetria ou sincronização —
   ganha **qualquer** acesso técnico ao dado.
3. Existe serviço central que armazena ou analisa em nome do usuário.

**Caso hospedado.** No instante em que o operador grava um CPF, endereço,
histórico de compra ou informação alimentar em infraestrutura dele, ele vira
**controlador** e nada da isenção sobra. Passam a valer base legal (art. 7º),
consentimento **explícito e destacado** para dado de saúde (art. 5º, II),
segurança (arts. 46-48), notificação de incidente (arts. 33-34), direitos do
titular (arts. 18-22) e, na prática, relatório de impacto e encarregado.

**Consequência de produto:** hospedar não é "a mesma coisa na nuvem". É outro
negócio, com outro custo fixo. Ver
[a armadilha do SaaS](mercado-e-produto.md#a-escada-de-produto).

⚠️ **O dado alimentar e de saúde é o ponto mais sensível.** Alergia e prescrição
no `AGENTS.md` são **dado pessoal sensível** e frequentemente sobre pessoas que
não instalaram nada. Ver [privacidade](../explicacao/privacidade.md).

## Termos de uso e automação

A distinção que importa:

| | Natureza | Consequência realista |
|---|---|---|
| **Contratual** | raspagem e automação costumam ser vedadas em termos de uso | bloqueio ou encerramento da conta; em tese, indenização se houver dano comprovado |
| **Criminal** | Lei 12.737/2012, art. 154-A CP | **não se configura** quando se usa a **própria conta autenticada** no **próprio dispositivo** — não há violação de mecanismo de segurança nem acesso não autorizado [confirmar] |

**Usar a própria conta não é o mesmo que ter permissão**, mas é materialmente
diferente de invasão. O risco realista é perder a conta, e a conta é do usuário.

Sobre dado de preço: **o Brasil não tem direito *sui generis* de banco de dados**
como o europeu [confirmar]. Preço público não goza dessa proteção específica.

## WhatsApp

| | API oficial (Business Cloud) | Cliente não-oficial |
|---|---|---|
| Termos | permitido, com contrato | **veda** cliente não-oficial |
| Banimento | baixo | **alto** |
| Ao **distribuir** a terceiros | requer ser provedor de solução | **agrava** — deixa de ser uso pessoal e vira facilitação |

**Recomendação:** **não** distribuir daemon não-oficial de WhatsApp junto do
projeto. Se houver integração, que seja pela API oficial. Se um usuário quiser
usar por conta, o projeto deve avisar do risco de banimento, não facilitar.

Este é o motivo de **não existir camada de WhatsApp neste repositório**, embora
exista na instalação original da casa.

## Pagamento automatizado

| Questão | Regra | Desenho que defende |
|---|---|---|
| Pedido automático com cartão salvo | CDC (Lei 8.078/1990); direito de arrependimento em 7 dias na compra a distância (art. 49) | **confirmação humana antes de cada pagamento**, com total, mercado e cartão visíveis |
| Armazenar cartão | dado sensível; PCI-DSS | **nunca armazenar**; nem número, nem CVV, nem token |
| Estorno / fraude | responsabilidade recai sobre quem autorizou | log datado de cada pedido; nunca repetir tentativa após recusa |

**O que o software nunca deve fazer sem supervisão:** iniciar pagamento sem
interação humana na hora; guardar credencial de pagamento; aceitar
automaticamente substituição em item restrito; repetir tentativa após recusa —
recusa costuma ser regra antifraude que a repetição escala.

No `aferidor-fone` isso é **recusa em código**, não parágrafo em documentação.

## Se houver receita [confirmar tudo com contador]

| Forma | Teto | Serve? |
|---|---:|---|
| MEI | ~R$ 81 mil/ano | atividade de software/consultoria **pode não ser elegível** — confirmar |
| ME / Simples | ~R$ 4,8 mi/ano | caminho normal para consultoria e SaaS pequeno |
| LTDA / Lucro Presumido | sem teto | só com investimento ou porte |

CNAE candidatos: desenvolvimento de software sob encomenda; consultoria em TI;
portais e provedores de conteúdo. **Confirmar quais cobrem SaaS.**

Serviço gera ISS municipal e NFS-e — **alíquota e obrigação variam por
município**, e Recife precisa de confirmação local. Vender produto versus
serviço tem tratamento diferente.

## Licença

**Apache-2.0**, adotada. O raciocínio:

- O código é o ativo **menos** defensável. O fosso de um serviço seria operação,
  histórico acumulado e integrações — nada disso é protegido por licença.
- Permissiva maximiza adoção e expõe a bifurcação comercial. Copyleft de rede
  (AGPL) protege mais e afasta adoção; BSL protege mais ainda e **não é código
  aberto**, o que é difícil de defender num projeto voltado a universidade.
- Marca registrada, e não licença, é o que impede reuso do **nome**.
- Se um dia fizer falta ter dentes jurídicos: AGPL **com CLA** de todo
  contribuidor permite licenciamento duplo. Sem CLA, não permite.

**Observação que importa mais do que parece:** o valor proprietário está na
**doutrina e nas skills** — conteúdo em Markdown —, não nos scripts. Uma licença
permissiva deixa qualquer um reempacotar as regras da casa. Como as regras desta
casa não são segredo comercial e o objetivo agora é adoção, isso está aceito
conscientemente.

## Checklist do repositório

- [x] `LICENSE` — Apache-2.0
- [x] `DISCLAIMER.md` — pt-BR e inglês
- [x] `SECURITY.md` — modelo de ameaça e como reportar
- [x] `docs/explicacao/privacidade.md` — o que fica onde
- [x] `.gitignore` excluindo notas fiscais, no repositório **e** no modelo
- [x] Portão de pagamento aplicado em código, com teste
- [x] Nenhum daemon não-oficial de WhatsApp distribuído
- [x] Nenhuma instrução de root ou burla de atestação
- [ ] Revisão por advogado — **pendente, antes de qualquer receita**
