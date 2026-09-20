# Aviso — leia antes de automatizar qualquer coisa que gaste dinheiro

*English below.*

## Em português

**Este software não é conselho financeiro, nutricional, médico ou jurídico.**
Ele organiza dados que você mesmo coletou e faz aritmética sobre eles. Todas as
decisões — o que comprar, onde, quanto, e se paga — são suas.

**Você opera com as suas próprias contas.** O projeto nunca pede, guarda ou
transmite senha, código de dois fatores, número de cartão ou token de sessão.
Onde há login, é o seu, no seu navegador ou no seu aparelho, feito por você.

**Automatizar sites e aplicativos de terceiros pode contrariar os termos de uso
deles.** A consequência realista é contratual, não criminal — bloqueio ou
encerramento da sua conta —, mas a conta é sua e o risco também. Avalie antes de
ligar qualquer automação. Usar a própria conta autenticada no próprio
dispositivo é materialmente diferente de acesso não autorizado, e ainda assim
não é o mesmo que ter permissão.

**Nenhum pagamento acontece sem você.** O portão humano descrito na
[camada 4](docs/explicacao/camadas.md#o-portão-humano) é a regra central do
projeto, e no `aferidor-fone` ele é aplicado em código. Não o contorne. Se
contornar, a responsabilidade pelo pedido é inteiramente sua — inclusive
perante o mercado e a operadora do cartão.

**Notas fiscais contêm dados pessoais.** Uma NFC-e traz o seu CPF e a lista
completa do que a sua casa consome — inclusive remédio, bebida e itens que
revelam condição de saúde. Não versione essas notas em repositório público nem
compartilhado. O `.gitignore` do modelo já exclui `notas/`; não remova essa
linha "para organizar melhor".

**Sobre dispositivos Android:** o projeto não recomenda, não documenta e não
apoia root, Magisk ou qualquer burla de atestação de integridade. Isso viola os
termos da plataforma, leva a banimento, e enfraquece a segurança de um aparelho
que provavelmente tem o seu banco instalado.

**Sem garantia.** Nos termos da [licença Apache-2.0](LICENSE), o software é
fornecido "no estado em que se encontra", sem garantia de qualquer espécie. Ele
pode ler um preço errado, casar o produto errado, ou parar de funcionar quando
um site mudar de layout.

**A economia não está medida.** Nenhuma porcentagem de economia foi
estabelecida contra uma linha de base controlada. Ver
[o caso](docs/01-o-caso.md#o-que-ainda-não-está-provado). Desconfie de qualquer
número que alguém — inclusive este projeto — cite sem contrafactual.

Em caso de dúvida jurídica, tributária ou de proteção de dados, consulte um
profissional. Nada aqui substitui isso.

---

## In English

**Not financial, nutritional, medical or legal advice.** This software organises
data you collected yourself and does arithmetic on it. Every decision is yours.

**You use your own accounts.** The project never asks for, stores or transmits a
password, second factor, card number or session token.

**Automating third-party sites and apps may breach their terms of service.** The
realistic consequence is contractual — your account being blocked or terminated
— and the account is yours, as is the risk.

**No payment happens without you.** The human gate is enforced in code in
`aferidor-fone`. Do not route around it.

**Brazilian electronic receipts contain personal data**, including a national
tax ID and a complete record of household consumption. Never commit them to a
shared or public repository.

**No root, no Magisk, no integrity bypass** — not recommended, not documented,
not supported.

**No warranty**, per the [Apache-2.0 licence](LICENSE). It can misread a price,
match the wrong product, or break when a website changes.

**Savings are unmeasured.** No percentage has been established against a
controlled baseline.
