# Casar SKUs vindos da nota fiscal

Depois de `aferidor nfce notas/ --importar`, a sua planilha ganha linhas com nomes
assim:

```
oleo-soja-liza-900ml
ol-soja-liza-900
oleo-de-soja-liza-pet-900ml
```

São o mesmo óleo. O mercado digita a descrição do jeito que quer, muda de um mês
para o outro, e a nota fiscal registra fielmente essa bagunça. Enquanto os três
nomes existirem separados, o `aferidor` acha que você comprou três produtos
diferentes uma vez cada — e três amostras de um item viram uma amostra de três.

**Isso não é cosmético.** A regra de migração exige 3 amostras para opinar. SKU
espalhado é a forma mais comum de o `aferidor advise` responder `COLETAR` numa casa
que já tem dados de sobra.

## O que fazer

Escolha um nome e junte tudo nele. O nome bom é o que **você** reconhece daqui a
seis meses, não o que o mercado imprimiu:

```sh
cd ~/minha-casa
sed -i 's/^\(.*,\)ol-soja-liza-900,/\1oleo-de-soja,/' dados/observacoes.csv
```

Ou, sem `sed`, abra `dados/observacoes.csv` em qualquer editor de planilha,
ordene pela coluna `sku` e corrija na mão. São dez minutos uma vez, não um
trabalho recorrente.

Depois:

```sh
aferidor check      # aponta sku sem arquivo em itens/
aferidor compare oleo-de-soja
```

## Quanto vale juntar

| | antes | depois |
|---|---|---|
| linhas | 3 SKUs × 1 compra | 1 SKU × 3 compras |
| o que o `aferidor` diz | `COLETAR` (faltam amostras) | um veredito de verdade |

## O que **não** juntar

Junte descrições do **mesmo produto**. Não junte produtos que a sua casa trata
como diferentes:

- **Tamanhos diferentes do mesmo produto** — junte. É para isso que existe a
  coluna `embalagem`: o `aferidor` normaliza 900 ml e 1 L para preço por litro.
- **Marcas diferentes** — junte só se a casa aceita substituir uma pela outra, e
  registre isso em `marcas_substitutas` no arquivo do item. Se `pode_substituir`
  é `não`, são itens diferentes e devem continuar separados.
- **Produtos parecidos com uso diferente** — arroz branco e arroz integral não
  são o mesmo item, por mais parecido que o nome fique depois do `slugify`.

Na dúvida, o critério é o do método: **se a casa aceitaria receber um no lugar
do outro, é o mesmo item.** Se não aceitaria, juntar os dois faz o programa
recomendar uma troca que ninguém queria.

## Importar duas vezes é seguro

O `--importar` guarda a chave de acesso de cada nota e pula as que já entraram:

```
imported 0 observations into dados/observacoes.csv
skipped 3 receipt(s) already imported — matched by access key
```

Pode rodar a pasta inteira de novo depois de baixar mais notas, sem medo de
duplicar o histórico. Duplicata aqui não dá erro — ela só torce silenciosamente
toda mediana daí para a frente, que é bem pior.

**Uma exceção, se você usou uma versão anterior.** Até esta mudança, a chave era
gravada cortada em 12 caracteres, e chave cortada não dá para casar: os 12
primeiros dígitos são UF, ano-mês e parte do CNPJ, então **todas** as notas do
mesmo mercado no mesmo mês começam igual. Casar por prefixo pularia nota nova de
verdade, o que é pior que duplicar. Por isso o `aferidor` avisa em vez de adivinhar:

```
warning: 34 row(s) were imported by an older version that stored a
         truncated key, so they cannot be matched and may now be duplicated.
```

Se isso aparecer e o histórico parecer dobrado, a saída é apagar as linhas com
`fonte=nfce` e importar a pasta de novo, uma vez só:

```sh
grep -v ',nfce,' dados/observacoes.csv > /tmp/limpo.csv && mv /tmp/limpo.csv dados/observacoes.csv
aferidor nfce ~/notas --importar
```

A coluna `observacao` guarda a chave, e é ela que faz a checagem funcionar — se
você reescrever essa célula à mão, aquela nota perde a proteção e pode entrar
duas vezes.

---

Volta para [o apêndice técnico](../03-apendice-tecnico.md) ·
[o método](../02-o-metodo.md)
