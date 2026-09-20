// Popup logic. Runs the collector in the active tab, shows what it found, and
// hands back CSV. No network calls anywhere in this file, by design — the
// extension's entire trust story is that it never phones home.

const $ = (id) => document.getElementById(id);
const CABECALHO = "data,sku,mercado,marca,embalagem,quantidade,preco_total,fonte,observacao";

const escapar = (v) => (/[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v);

// "12.345,67" -> "12345.67"  (CSV carries a machine-readable decimal)
const numero = (br) => br.replace(/\./g, "").replace(",", ".");

$("data").value = new Date().toLocaleDateString("sv-SE"); // sv-SE is ISO, in local time

let itens = [];

function desenhar() {
  const lista = $("lista");
  lista.textContent = "";

  if (!itens.length) {
    const vazio = document.createElement("div");
    vazio.className = "vazio";
    vazio.textContent =
      "Nenhum preço reconhecido nesta página. Isso é comum em listas que só " +
      "carregam ao rolar — role até ver os produtos e clique de novo. " +
      "Se persistir, registre à mão com `aferidor record`.";
    lista.append(vazio);
    return;
  }

  itens.forEach((item, i) => {
    const linha = document.createElement("div");
    linha.className = "item";

    const marcar = document.createElement("input");
    marcar.type = "checkbox";
    marcar.checked = Boolean(item.embalagem); // sem embalagem, não dá para comparar
    marcar.id = `i${i}`;
    marcar.addEventListener("change", () => { item.marcado = marcar.checked; atualizar(); });
    item.marcado = marcar.checked;

    const corpo = document.createElement("label");
    corpo.setAttribute("for", `i${i}`);

    const nome = document.createElement("div");
    nome.className = "nome";
    nome.textContent = item.nome;

    const meta = document.createElement("div");
    meta.className = "meta";
    if (item.embalagem) {
      meta.textContent = `${item.sku} · ${item.embalagem}`;
    } else {
      meta.className = "meta revisar";
      meta.textContent = `${item.sku} · sem embalagem — preencha antes de usar`;
    }

    corpo.append(nome, meta);

    const preco = document.createElement("div");
    preco.className = "preco";
    preco.textContent = `R$ ${item.preco}`;

    linha.append(marcar, corpo, preco);
    lista.append(linha);
  });
}

function atualizar() {
  const n = itens.filter((i) => i.marcado).length;
  $("copiar").disabled = n === 0;
  $("copiar").textContent = n ? `Copiar ${n} ${n === 1 ? "linha" : "linhas"}` : "Copiar CSV";
}

function montarCsv() {
  const mercado = $("mercado").value.trim() || "desconhecido";
  const data = $("data").value;
  const fonte = "site";
  const linhas = itens
    .filter((i) => i.marcado)
    .map((i) =>
      [data, i.sku, mercado, "", i.embalagem, "1", numero(i.preco), fonte, ""]
        .map(escapar)
        .join(",")
    );
  return [CABECALHO, ...linhas].join("\n");
}

$("todos").addEventListener("click", () => {
  const marcarTudo = itens.some((i) => !i.marcado);
  itens.forEach((i) => { i.marcado = marcarTudo; });
  desenhar();
  atualizar();
});

$("copiar").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(montarCsv());
    $("status").textContent =
      "Copiado. Cole no fim de dados/observacoes.csv (sem o cabeçalho, se já existir).";
  } catch {
    $("status").textContent = "Não consegui copiar. Selecione o texto na página e copie à mão.";
  }
});

(async function iniciar() {
  const [aba] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!aba || !/^https?:/.test(aba.url || "")) {
    $("resumo").textContent = "Abra a página de um mercado e clique de novo.";
    $("lista").textContent = "";
    return;
  }

  let resultado;
  try {
    [{ result: resultado }] = await chrome.scripting.executeScript({
      target: { tabId: aba.id },
      files: ["coletor.js"],
    });
  } catch (erro) {
    $("resumo").textContent =
      "Não consegui ler esta página. Páginas internas do navegador e da loja de " +
      "extensões são bloqueadas pelo próprio navegador.";
    $("lista").textContent = "";
    return;
  }

  itens = resultado?.itens ?? [];
  $("mercado").value = resultado?.mercado ?? "";
  $("resumo").textContent = itens.length
    ? `${itens.length} preços nesta página. Confira antes de copiar — a leitura é automática e erra.`
    : "Nenhum preço reconhecido.";

  desenhar();
  atualizar();
})();
