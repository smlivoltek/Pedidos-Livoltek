# SM Livoltek — Design System de Dashboards

Referência de padronização visual para todos os dashboards da área (Pedidos, Estoque, Comercial, Executivo, Entregas). Use este documento ao criar ou revisar qualquer novo relatório para garantir que ele seja reconhecido como parte da mesma plataforma.

Implementado pela primeira vez no **Painel de Status de Pedidos** (`Pedidos-Livoltek`). Use esse arquivo como referência de código ao aplicar o padrão nos demais.

---

## 1. Identidade Visual

### Marca fixa
Todo dashboard exibe, no topo, a marca **"SM Livoltek"** — pequena, em azul, acima do título do relatório específico.

```html
<div class="brand-mark">SM Livoltek</div>
<h1 data-i18n="title">📊 Nome do Relatório</h1>
<p class="subtitle" data-i18n="subtitle">Livoltek - Sales Management | [frequência de atualização]</p>
```

```css
.brand-mark {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--cor-azul);
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 3px 10px;
    margin-bottom: 10px;
}
```

### Nomes de relatório (exemplos já em uso ou previstos)
- Painel de Status de Pedidos
- Dashboard de Estoque
- Dashboard Comercial
- Dashboard Executivo
- Indicadores
- Relatório de Entregas

---

## 2. Estrutura Padrão (ordem obrigatória)

1. **Cabeçalho** — marca + título + subtítulo + seletor de idioma
2. **Filtros** — busca por texto + selects, sempre no topo da área de dados
3. **Indicadores (Cards)** — números-chave, mesmo padrão visual
4. **Gráficos** — usando a paleta de 4 cores e opções padronizadas
5. **Tabela detalhada** — cabeçalho fixo, ordenada por data mais recente

Não inverter essa ordem entre dashboards — o usuário deve encontrar a mesma lógica de leitura em qualquer relatório da área.

---

## 3. Paleta de Cores (usar SEMPRE estas 4, com este significado)

```css
:root{
    --cor-azul: #2563eb;     /* Informações gerais, produtos, origem, tendências */
    --cor-verde: #16a34a;    /* Indicadores positivos, processos concluídos */
    --cor-laranja: #f59e0b;  /* Em andamento, atenção */
    --cor-vermelho: #dc2626; /* Pendências, alertas, ações necessárias */
}
```

**Nunca** misturar roxo, verde, azul e vermelho aleatoriamente em gráficos diferentes do mesmo dashboard — cada cor tem um significado fixo, não decorativo.

---

## 4. Cards (Indicadores)

Todos os cards seguem o mesmo HTML/CSS — só o conteúdo muda:

```html
<div class="cards">
    <div class="card">
        <h3 data-i18n="cardX">Nome do Indicador</h3>
        <div class="number" id="cardXValue">0</div>
    </div>
    <div class="card vendedor"><!-- variante vermelha: pendência --></div>
    <div class="card analise"><!-- variante laranja: em andamento --></div>
    <div class="card faturamento"><!-- variante verde: concluído --></div>
</div>
```

```css
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
}
.card {
    background: white;
    padding: 24px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    text-align: center;
    border-left: 4px solid var(--cor-azul); /* padrão = azul */
}
.card.vendedor { border-left-color: var(--cor-vermelho); }
.card.analise { border-left-color: var(--cor-laranja); }
.card.faturamento { border-left-color: var(--cor-verde); }
.card h3 { font-size: 12px; text-transform: uppercase; color: #888; margin-bottom: 8px; }
.card .number { font-size: 36px; font-weight: 700; color: #222; }
```

Regra: mesmo tamanho, mesmo padding, mesmo alinhamento central, mesma fonte — independente do dashboard.

---

## 5. Gráficos (Chart.js)

### Função de opções compartilhada — copiar literalmente em todo dashboard

```javascript
function PADRAO_CHART_OPTIONS(tituloEixoX){
    return {
        indexAxis: 'y', // barra horizontal — padrão preferencial
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: '#1f2937',
                titleFont: { size: 12, weight: '600' },
                bodyFont: { size: 12 },
                padding: 10
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: tituloEixoX ? { display: true, text: tituloEixoX, font: { size: 11 } } : undefined,
                grid: { color: '#f1f3f5' },
                ticks: { font: { size: 11 } }
            },
            y: {
                grid: { display: false },
                ticks: { font: { size: 11 } }
            }
        }
    };
}
```

### Estilo dos containers de gráfico

```css
.chart-container {
    background: white;
    padding: 20px 24px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    border: 1px solid #eef0f2;
}
.chart-container h3 {
    margin-bottom: 4px;
    font-size: 15px;
    font-weight: 600;
    color: #1f2937;
}
.chart-subtitle {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 16px;
}
.row-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}
@media (max-width: 900px) { .row-2col { grid-template-columns: 1fr; } }
```

### Regras de cor por gráfico
- Gráfico de produto/origem/tendência → `backgroundColor: '#2563eb'` (azul)
- Gráfico de pendências/alertas → `backgroundColor: '#dc2626'` (vermelho)
- Nunca usar roxo, verde-claro, ou cores fora da paleta nas barras

---

## 6. Tabelas

```css
.table-wrapper {
    overflow-x: auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    max-height: 70vh; /* permite cabeçalho fixo com rolagem interna */
}
th {
    background: #f8f8f8;
    padding: 12px 8px;
    font-weight: 600;
    border-bottom: 2px solid #eee;
    font-size: 12px;
    color: #555;
    white-space: nowrap;
    position: sticky; /* cabeçalho fixo */
    top: 0;
    z-index: 10;
}
td { padding: 10px 8px; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
```

Checklist obrigatório por tabela:
- [ ] Cabeçalho fixo (`position: sticky`)
- [ ] Mesmo tamanho de fonte em th/td entre dashboards
- [ ] **Ordenação padrão por data mais recente primeiro** (campo de data principal do registro)
- [ ] Campo de busca rápida por texto (ex: nº de pedido, SKU, nome)
- [ ] Filtros de select acima da tabela (ex: KAM, Status, Categoria)

### Ordenação padrão (JavaScript)

```javascript
filtered.sort((a, b) => {
    const parseData = (s) => {
        if (!s) return 0;
        const partes = s.split('/');
        if (partes.length !== 3) return 0;
        return new Date(partes[2], partes[1]-1, partes[0]).getTime();
    };
    return parseData(b['Campo de Data']) - parseData(a['Campo de Data']);
});
```

---

## 7. Internacionalização (i18n)

Todo dashboard deve suportar **Português e Inglês**, traduzindo apenas a interface — nunca os dados.

### Seletor no cabeçalho

```html
<div class="lang-selector">
    <button class="lang-btn" onclick="toggleLangMenu()">
        🌐 <span id="langCurrentLabel">Português</span> <span style="font-size:10px">▾</span>
    </button>
    <div id="langMenu" class="lang-menu">
        <button onclick="setLang('pt')">🇧🇷 Português</button>
        <button onclick="setLang('en')">🇺🇸 English</button>
    </div>
</div>
```

### Estrutura do dicionário

```javascript
const I18N = {
    pt: { title: '...', cardTotal: '...', /* todas as chaves de interface */ },
    en: { title: '...', cardTotal: '...', /* mesmas chaves, traduzidas */ }
};
let currentLang = localStorage.getItem('[nome]_lang') || 'pt';
function t(key){ return (I18N[currentLang] && I18N[currentLang][key]) ?? (I18N.pt[key] ?? key); }
function applyTranslations(){
    document.querySelectorAll('[data-i18n]').forEach(el => el.textContent = t(el.getAttribute('data-i18n')));
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => el.placeholder = t(el.getAttribute('data-i18n-placeholder')));
}
```

### O que traduzir
Menus, cards, títulos, colunas, botões, status (visualmente, sem alterar o valor interno usado em filtros), mensagens de erro/vazio.

### O que NUNCA traduzir
Nome de cliente, nome de vendedor/KAM, código de produto, texto livre digitado por humanos (ex: descrição de pendência), qualquer valor numérico ou data.

---

## 8. Responsividade

Breakpoint principal: **600px**.

```css
@media (max-width: 600px) {
    body { padding: 10px; }
    h1 { font-size: 22px; }
    .cards { grid-template-columns: 1fr; gap: 12px; }
    .card { padding: 16px; }
    .card .number { font-size: 32px; }
    .filters { flex-direction: column; align-items: stretch; gap: 12px; }
    .filter-group { flex-direction: column; align-items: stretch; gap: 4px; }
    .filter-group select, .filter-group input { width: 100%; min-width: 0 !important; }
    th, td { padding: 8px 6px; font-size: 12px; }
    .chart-container { padding: 14px 16px; }
    .chart-container h3 { font-size: 14px; }
}
```

Testar sempre em: desktop/notebook (>1200px), tablet (~768px), celular (~375px).

---

## 9. Checklist de Conformidade — usar antes de publicar um novo dashboard

- [ ] Marca "SM Livoltek" visível no cabeçalho
- [ ] Nome do relatório como `<h1>`
- [ ] Estrutura na ordem: Cabeçalho → Filtros → Cards → Gráficos → Tabela
- [ ] Cards com mesmo tamanho/espaçamento/cor do padrão
- [ ] Gráficos usando `PADRAO_CHART_OPTIONS()` e só as 4 cores da paleta
- [ ] Tabela com cabeçalho fixo, ordenada por data mais recente, busca + filtros
- [ ] Seletor de idioma PT/EN funcional, sem afetar os dados
- [ ] Testado em mobile (≤600px)
- [ ] Nenhuma cor fora da paleta (roxo, verde-claro, etc.) em uso

---

## Referência de implementação completa

O código de referência completo (HTML + CSS + JS) está implementado em produção no **Painel de Status de Pedidos**, repositório `Pedidos-Livoltek`. Use esse arquivo `index.html` como ponto de partida ao construir os próximos dashboards (copiar estrutura, cabeçalho, paleta, i18n e funções de gráfico, depois adaptar cards/gráficos/tabela ao conteúdo específico de cada relatório).
