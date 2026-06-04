document.addEventListener('DOMContentLoaded', () => {
  const cardsGrid = document.getElementById('cards-grid');
  const detailsSidebar = document.getElementById('details-sidebar');
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  const closeSidebarBtn = document.getElementById('close-sidebar');
  const searchInput = document.getElementById('search-input');
  
  // Elementos da Sidebar
  const detTicker = document.getElementById('det-ticker');
  const detNome = document.getElementById('det-nome');
  const detTipo = document.getElementById('det-tipo');
  const detPreco = document.getElementById('det-preco');
  const detRecom = document.getElementById('det-recom');
  const detAlerta = document.getElementById('det-alerta');
  const detExplicacao = document.getElementById('det-explicacao');
  const detCritico = document.getElementById('det-critico');
  const detBoasNoticias = document.getElementById('det-boasnoticias');
  const detTrendIcon = document.getElementById('det-trend-icon');
  const detTrendText = document.getElementById('det-trend-text');
  const detNoticias = document.getElementById('det-noticias');
  
  let currentChart = null;
  let activeCategoryFilter = 'todos';
  let activeRecomFilter = 'todos';
  let searchQuery = '';
  let activeFii = null; // FII aberto no momento
  let activeDividendoMaisRecente = 0;
  
  // Elementos do Simulador
  const calcCotas = document.getElementById('calc-cotas');
  const calcCusto = document.getElementById('calc-custo');
  const calcResultTotal = document.getElementById('calc-result-total');
  const calcResultMensal = document.getElementById('calc-result-mensal');
  const calcResultYoc = document.getElementById('calc-result-yoc');

  // URL da Planilha do Google Sheets publicada como CSV (Ideia 2)
  // Substitua pela sua URL pública do Sheets (ex: https://docs.google.com/spreadsheets/d/.../pub?output=csv)
  const GOOGLE_SHEETS_CSV_URL = '';

  // Inicializa o Dashboard
  initializeData();

  // Escuta os Filtros de Categoria
  const catButtons = document.querySelectorAll('[data-filter-cat]');
  catButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      catButtons.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      activeCategoryFilter = e.target.getAttribute('data-filter-cat');
      renderCards();
    });
  });

  // Escuta os Filtros de Recomendação
  const recomButtons = document.querySelectorAll('[data-filter-recom]');
  recomButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      recomButtons.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      activeRecomFilter = e.target.getAttribute('data-filter-recom');
      renderCards();
    });
  });

  // Escuta a Barra de Pesquisa
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderCards();
  });

  // Fecha Sidebar
  closeSidebarBtn.addEventListener('click', closeSidebar);
  sidebarOverlay.addEventListener('click', closeSidebar);

  // Escuta os Inputs do Simulador
  calcCotas.addEventListener('input', () => updateSimulation());
  calcCusto.addEventListener('input', () => updateSimulation());

  // Renderiza os Cards com Base nos Filtros Ativos
  function renderCards() {
    cardsGrid.innerHTML = '';
    
    const filteredFiis = Object.keys(fiisData).filter(key => {
      const fii = fiisData[key];
      
      // Filtro de Busca (Ticker ou Nome)
      const matchesSearch = fii.ticker.toLowerCase().includes(searchQuery) || 
                            fii.nome.toLowerCase().includes(searchQuery);
                            
      // Filtro de Categoria
      let matchesCategory = false;
      const tipoLower = fii.tipo.toLowerCase();
      if (activeCategoryFilter === 'todos') {
        matchesCategory = true;
      } else if (activeCategoryFilter === 'tijolo' && tipoLower.includes('tijolo')) {
        matchesCategory = true;
      } else if (activeCategoryFilter === 'papel' && (tipoLower.includes('papel') || tipoLower.includes('recebíveis'))) {
        matchesCategory = true;
      } else if (activeCategoryFilter === 'fiagro' && tipoLower.includes('fiagro')) {
        matchesCategory = true;
      } else if (activeCategoryFilter === 'fi-infra' && tipoLower.includes('fi-infra')) {
        matchesCategory = true;
      }
      
      // Filtro de Recomendação
      let matchesRecom = false;
      const recomLower = fii.recomendacao.toLowerCase();
      if (activeRecomFilter === 'todos') {
        matchesRecom = true;
      } else if (activeRecomFilter === 'comprar' && recomLower === 'comprar') {
        matchesRecom = true;
      } else if (activeRecomFilter === 'manter' && recomLower === 'manter') {
        matchesRecom = true;
      }
      
      return matchesSearch && matchesCategory && matchesRecom;
    });

    if (filteredFiis.length === 0) {
      cardsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-dim);">
          Nenhum fundo imobiliário encontrado com os filtros selecionados.
        </div>
      `;
      return;
    }

    filteredFiis.forEach(key => {
      const fii = fiisData[key];
      const card = createCardElement(fii);
      cardsGrid.appendChild(card);
    });
  }

  // Cria a Estrutura HTML do Card
  function createCardElement(fii) {
    const card = document.createElement('div');
    card.className = `fii-card recom-${fii.recomendacao.toLowerCase()}`;
    
    // Função para pegar ícone e classe da tendência
    function getTrendData(trendValue) {
      let icon = '';
      let trendClass = '';
      if (trendValue === 'aumentar' || trendValue === 'subir') {
        icon = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>';
        trendClass = 'trend-aumentar';
      } else if (trendValue === 'manter') {
        icon = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
        trendClass = 'trend-manter';
      } else {
        icon = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>';
        trendClass = 'trend-cair';
      }
      return { icon, trendClass };
    }

    const trendPreco = getTrendData(fii.tendencia_preco);
    const trendDivs = getTrendData(fii.tendencia_dividendos);

    card.innerHTML = `
      <div class="card-header">
        <div class="card-title-group">
          <h2>${fii.ticker}</h2>
          <span>${fii.nome}</span>
        </div>
        <span class="badge-type">${fii.tipo.split(' ')[0]}</span>
      </div>
      
      <div class="card-body-content" style="display: flex; flex-direction: column; gap: 0.55rem; margin-top: 0.25rem;">
        <!-- Bloco do Preço Principal -->
        <div class="info-item">
          <span class="info-label">Preço Atual</span>
          <span class="info-value" style="font-size: 1.35rem; font-weight: 700; color: var(--text-main);">${fii.preco}</span>
        </div>
        
        <!-- Título da Seção de Tendências -->
        <div style="display: flex; flex-direction: column; gap: 0.35rem; margin-top: 0.15rem;">
          <span class="info-label" style="display: block;">Tendências</span>
          <!-- Badges de Tendências Lado a Lado -->
          <div style="display: flex; gap: 0.5rem; width: 100%;">
            <div class="tendencia-badge ${trendPreco.trendClass}" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.3rem; padding: 0.4rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; background: rgba(255, 255, 255, 0.015); border: 1px solid rgba(255, 255, 255, 0.03);">
              <span style="color: var(--text-dim); font-weight: 500;">Preço:</span>
              <span style="display: inline-flex; align-items: center; gap: 0.15rem;">
                ${trendPreco.icon}
                <span style="text-transform: capitalize;">${fii.tendencia_preco}</span>
              </span>
            </div>
            <div class="tendencia-badge ${trendDivs.trendClass}" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.3rem; padding: 0.4rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; background: rgba(255, 255, 255, 0.015); border: 1px solid rgba(255, 255, 255, 0.03);">
              <span style="color: var(--text-dim); font-weight: 500;">Dividendo:</span>
              <span style="display: inline-flex; align-items: center; gap: 0.15rem;">
                ${trendDivs.icon}
                <span style="text-transform: capitalize;">${fii.tendencia_dividendos === 'aumentar' ? 'Subir' : fii.tendencia_dividendos}</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.02);">
        <span class="badge-status ${fii.recomendacao.toLowerCase()}">
          <span style="width: 6px; height: 6px; background-color: currentColor; border-radius: 50%;"></span>
          ${fii.recomendacao}
        </span>
        <span style="font-size: 0.75rem; color: var(--text-dim);">Risco: ${fii.alerta}/10</span>
      </div>
    `;

    card.addEventListener('click', () => openSidebar(fii));
    return card;
  }

  // Abre a Sidebar de Detalhes
  function openSidebar(fii) {
    activeFii = fii; // Define o FII ativo
    activeDividendoMaisRecente = fii.dividendos_recentes[fii.dividendos_recentes.length - 1];
    
    detTicker.innerText = fii.ticker;
    detNome.innerText = fii.nome;
    detTipo.innerText = fii.tipo;
    detPreco.innerText = fii.preco;
    detAlerta.innerText = `${fii.alerta}/10`;

    // Inicializa os campos do Simulador
    calcCotas.value = 100;
    const precoLimpo = parseFloat(fii.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 100;
    calcCusto.value = precoLimpo;
    updateSimulation();
    
    // Recomendação Badge
    detRecom.className = `badge-status ${fii.recomendacao.toLowerCase()}`;
    detRecom.innerHTML = `
      <span style="width: 8px; height: 8px; background-color: currentColor; border-radius: 50%;"></span>
      ${fii.recomendacao}
    `;

    // Textos Descritivos
    detExplicacao.innerText = fii.explicacoes;
    detCritico.innerText = fii.pontos_criticos;
    detBoasNoticias.innerText = fii.boas_noticias;

    // Tendência de Dividendos na Sidebar
    let trendIconHtml = '';
    let trendClass = '';
    if (fii.tendencia_dividendos === 'aumentar') {
      trendIconHtml = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>';
      trendClass = 'trend-aumentar';
      detTrendText.innerText = 'Tendência de Alta';
    } else if (fii.tendencia_dividendos === 'manter') {
      trendIconHtml = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
      trendClass = 'trend-manter';
      detTrendText.innerText = 'Tendência Estável';
    } else {
      trendIconHtml = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>';
      trendClass = 'trend-cair';
      detTrendText.innerText = 'Tendência de Queda';
    }
    
    detTrendIcon.className = `trend-arrow ${trendClass}`;
    detTrendIcon.innerHTML = trendIconHtml;

    // Abrir Sidebar
    detailsSidebar.classList.add('open');
    sidebarOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Impede o scroll de fundo

    // Renderizar Gráfico de Proventos, Notícias e Preço em tempo real
    loadAndRenderChart(fii);
    loadNews(fii.ticker);
    updateSinglePrice(fii.ticker);
  }

  // Fecha a Sidebar
  function closeSidebar() {
    detailsSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // Lógica de cálculo do Simulador e Yield on Cost (YOC)
  function updateSimulation() {
    if (!activeFii) return;
    
    const cotas = parseInt(calcCotas.value) || 0;
    const custoMedio = parseFloat(calcCusto.value) || 0;
    
    // Custo Total / Total Investido
    const custoTotal = cotas * custoMedio;
    calcResultTotal.innerText = `R$ ${custoTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    
    // Obtém o dividendo mais recente (seja real-time ou fallback)
    const ultimoDividendo = activeDividendoMaisRecente;
    
    // Provento mensal estimado
    const proventoMensal = cotas * ultimoDividendo;
    calcResultMensal.innerText = `R$ ${proventoMensal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    
    // Yield on Cost (YOC) Anualizado
    // Fórmula: (Provento Anual por Cota / Preço de Custo) * 100
    if (custoMedio > 0) {
      const yocAnual = ((ultimoDividendo * 12) / custoMedio) * 100;
      calcResultYoc.innerText = `${yocAnual.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
    } else {
      calcResultYoc.innerText = '0,00%';
    }
  }

  // Função auxiliar de busca resiliente com fallback de proxies CORS
  async function fetchWithCORS(targetUrl) {
    const proxies = [
      url => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
      url => `https://corsproxy.io/?${encodeURIComponent(url)}`,
      url => `https://api.codetabs.com/v1/proxy/?quest=${encodeURIComponent(url)}`
    ];

    let lastError = null;
    for (let i = 0; i < proxies.length; i++) {
      const proxyUrl = proxies[i](targetUrl);
      try {
        const response = await fetch(proxyUrl);
        if (response.ok) {
          return await response.json();
        }
      } catch (e) {
        console.warn(`Proxy CORS #${i + 1} falhou para URL: ${targetUrl}. Tentando o próximo...`);
        lastError = e;
      }
    }
    throw lastError || new Error(`Todos os proxies CORS falharam para URL: ${targetUrl}`);
  }

  // Função auxiliar para obter texto bruto (como CSV) usando proxies CORS
  async function fetchTextWithCORS(targetUrl) {
    const proxies = [
      url => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
      url => `https://corsproxy.io/?${encodeURIComponent(url)}`,
      url => `https://api.codetabs.com/v1/proxy/?quest=${encodeURIComponent(url)}`
    ];

    let lastError = null;
    for (let i = 0; i < proxies.length; i++) {
      const proxyUrl = proxies[i](targetUrl);
      try {
        const response = await fetch(proxyUrl);
        if (response.ok) {
          return await response.text();
        }
      } catch (e) {
        console.warn(`Proxy CORS #${i + 1} (Texto) falhou para URL: ${targetUrl}. Tentando o próximo...`);
        lastError = e;
      }
    }
    throw lastError || new Error(`Todos os proxies CORS falharam para obter texto da URL: ${targetUrl}`);
  }

  // Parseador de CSV compatível com RFC 4180 (trata campos com aspas e quebras de linha de forma correta)
  function parseCSV(csvText) {
    const lines = [];
    let row = [""];
    let insideQuote = false;

    for (let i = 0; i < csvText.length; i++) {
      const char = csvText[i];
      const nextChar = csvText[i + 1];

      if (char === '"') {
        if (insideQuote && nextChar === '"') {
          row[row.length - 1] += '"';
          i++;
        } else {
          insideQuote = !insideQuote;
        }
      } else if (char === ',' && !insideQuote) {
        row.push("");
      } else if ((char === '\r' || char === '\n') && !insideQuote) {
        if (char === '\r' && nextChar === '\n') {
          i++;
        }
        lines.push(row);
        row = [""];
      } else {
        row[row.length - 1] += char;
      }
    }
    
    if (row.length > 1 || row[0] !== "") {
      lines.push(row);
    }
    return lines;
  }

  // Mapeia o CSV parseado para a estrutura de dados global do dashboard
  function loadDataFromSheets(csvText) {
    const rows = parseCSV(csvText);
    if (rows.length < 2) return;

    const headers = rows[0].map(h => h.trim().toLowerCase());
    
    const idxTicker = headers.indexOf('ticker');
    const idxNome = headers.indexOf('nome');
    const idxTipo = headers.indexOf('tipo');
    const idxRecom = headers.indexOf('recomendacao');
    const idxAlerta = headers.indexOf('alerta');
    const idxExplicacoes = headers.indexOf('explicacoes');
    const idxCriticos = headers.indexOf('pontos criticos');
    const idxBoas = headers.indexOf('boas noticias');
    const idxTrendPreco = headers.indexOf('tendencia preco');
    const idxTrendDivs = headers.indexOf('tendencia dividendos');
    const idxDivsRecentes = headers.indexOf('dividendos recentes');

    if (idxTicker === -1) {
      console.error("Erro: Coluna 'Ticker' não encontrada no cabeçalho da planilha Google Sheets!");
      return;
    }

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      const ticker = row[idxTicker]?.trim().toUpperCase();
      if (!ticker) continue;

      // Cria a estrutura caso o ticker seja novo
      if (!fiisData[ticker]) {
        fiisData[ticker] = { ticker };
      }

      if (idxNome !== -1 && row[idxNome]) fiisData[ticker].nome = row[idxNome].trim();
      if (idxTipo !== -1 && row[idxTipo]) fiisData[ticker].tipo = row[idxTipo].trim();
      if (idxRecom !== -1 && row[idxRecom]) fiisData[ticker].recomendacao = row[idxRecom].trim();
      if (idxAlerta !== -1 && row[idxAlerta]) fiisData[ticker].alerta = parseInt(row[idxAlerta].trim()) || 0;
      if (idxExplicacoes !== -1 && row[idxExplicacoes]) fiisData[ticker].explicacoes = row[idxExplicacoes].trim();
      if (idxCriticos !== -1 && row[idxCriticos]) fiisData[ticker].pontos_criticos = row[idxCriticos].trim();
      if (idxBoas !== -1 && row[idxBoas]) fiisData[ticker].boas_noticias = row[idxBoas].trim();
      
      if (idxTrendPreco !== -1 && row[idxTrendPreco]) {
        fiisData[ticker].tendencia_preco = row[idxTrendPreco].trim().toLowerCase();
      }
      if (idxTrendDivs !== -1 && row[idxTrendDivs]) {
        fiisData[ticker].tendencia_dividendos = row[idxTrendDivs].trim().toLowerCase();
      }
      
      if (idxDivsRecentes !== -1 && row[idxDivsRecentes]) {
        const divs = row[idxDivsRecentes].split(',')
          .map(v => parseFloat(v.trim()))
          .filter(v => !isNaN(v));
        if (divs.length > 0) {
          fiisData[ticker].dividendos_recentes = divs;
        }
      }
    }
  }

  // Inicialização assíncrona com suporte e fallback para Google Sheets
  async function initializeData() {
    if (GOOGLE_SHEETS_CSV_URL) {
      try {
        console.log("Carregando dados da planilha do Google Sheets...");
        let csvText = '';
        try {
          const res = await fetch(GOOGLE_SHEETS_CSV_URL);
          if (res.ok) {
            csvText = await res.text();
          } else {
            throw new Error("Erro status " + res.status);
          }
        } catch (errDirect) {
          console.warn("Fetch direto falhou. Tentando obter planilha via proxy CORS...", errDirect);
          csvText = await fetchTextWithCORS(GOOGLE_SHEETS_CSV_URL);
        }

        if (csvText) {
          loadDataFromSheets(csvText);
          console.log("Dados do Google Sheets integrados e sincronizados com sucesso!");
        }
      } catch (e) {
        console.error("Falha ao carregar dados do Google Sheets. Usando base local (data.js) de backup.", e);
      }
    } else {
      console.log("Nenhuma URL do Google Sheets fornecida. Usando base de dados local padrão (data.js).");
    }
    
    // Renderiza a grade de cards com as informações correntes
    renderCards();
  }

  // Gera labels de data retroativa para fallbacks (últimos 6 meses baseados na data atual)
  function getFallbackLabels() {
    const labels = [];
    const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
    const hoje = new Date();
    for (let i = 5; i >= 0; i--) {
      const d = new Date(hoje.getFullYear(), hoje.getMonth() - i, 1);
      labels.push(`${meses[d.getMonth()]}/${String(d.getFullYear()).slice(-2)}`);
    }
    return labels;
  }

  // Formata tempo relativo da publicação da notícia
  function formatRelativeTime(timestampSeconds) {
    const diffMs = Date.now() - (timestampSeconds * 1000);
    const diffMinutes = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMinutes < 60) {
      return `há ${Math.max(1, diffMinutes)} min`;
    } else if (diffHours < 24) {
      return `há ${diffHours} h`;
    } else if (diffDays === 1) {
      return `ontem`;
    } else {
      return `há ${diffDays} dias`;
    }
  }

  // Renderiza o gráfico do Chart.js puro a partir de dados fornecidos
  function renderChartWithData(ticker, recomendacao, values, labels) {
    if (currentChart) {
      currentChart.destroy();
    }

    const ctx = document.getElementById('proventosChart').getContext('2d');
    
    // Cores dinâmicas para o gráfico baseadas na recomendação
    let lineColor = '#3b82f6';
    let gradientStart = 'rgba(59, 130, 246, 0.2)';
    
    if (recomendacao === 'Comprar') {
      lineColor = '#10b981';
      gradientStart = 'rgba(16, 185, 129, 0.2)';
    } else if (recomendacao === 'Vender') {
      lineColor = '#f43f5e';
      gradientStart = 'rgba(244, 63, 94, 0.2)';
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, gradientStart);
    gradient.addColorStop(1, 'rgba(16, 20, 29, 0)');

    currentChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Dividendos por Cota',
          data: values,
          borderColor: lineColor,
          borderWidth: 2,
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointBackgroundColor: lineColor,
          pointBorderColor: '#080b10',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: '#10141d',
            titleFont: { family: 'Outfit', size: 12 },
            bodyFont: { family: 'Outfit', size: 12 },
            borderColor: 'rgba(255, 255, 255, 0.08)',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                return `R$ ${context.parsed.y.toFixed(2)}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: '#64748b',
              font: {
                family: 'Outfit',
                size: 11
              }
            }
          },
          y: {
            grid: {
              color: 'rgba(255, 255, 255, 0.03)'
            },
            ticks: {
              color: '#64748b',
              font: {
                family: 'Outfit',
                size: 11
              },
              callback: function(value) {
                return `R$ ${value.toFixed(2)}`;
              }
            }
          }
        }
      }
    });
  }

  // Carrega e atualiza o gráfico de proventos históricos com dados em tempo real do Yahoo Finance (Ideia 1)
  async function loadAndRenderChart(fii) {
    // Primeiro renderiza imediatamente com dados locais como fallback seguro
    const fallbackLabels = getFallbackLabels();
    renderChartWithData(fii.ticker, fii.recomendacao, fii.dividendos_recentes, fallbackLabels);

    try {
      const targetUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${fii.ticker}.SA?events=div&range=1y`;
      const data = await fetchWithCORS(targetUrl);

      if (data && data.chart && data.chart.result && data.chart.result[0]) {
        const events = data.chart.result[0].events;
        if (events && events.dividends) {
          const dividendsObj = events.dividends;
          const divList = [];
          for (const key in dividendsObj) {
            divList.push({
              date: dividendsObj[key].date,
              amount: dividendsObj[key].amount
            });
          }

          if (divList.length > 0) {
            // Ordena cronologicamente (crescente)
            divList.sort((a, b) => a.date - b.date);

            // Pega os 6 últimos dividendos
            const last6Divs = divList.slice(-6);

            const values = last6Divs.map(d => d.amount);
            const labels = last6Divs.map(d => {
              const dateObj = new Date(d.date * 1000);
              const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
              const mesIndex = dateObj.getUTCMonth();
              const ano = String(dateObj.getUTCFullYear()).slice(-2);
              return `${meses[mesIndex]}/${ano}`;
            });

            // Atualiza a variável reativa de dividendos da simulação
            activeDividendoMaisRecente = values[values.length - 1];
            updateSimulation();

            // Atualiza o gráfico com dados reais do Yahoo Finance!
            renderChartWithData(fii.ticker, fii.recomendacao, values, labels);
            return;
          }
        }
      }
      console.log(`Dados de dividendos em tempo real indisponíveis para ${fii.ticker}. Mantendo locais.`);
    } catch (e) {
      console.warn(`Erro ao obter proventos dinâmicos de ${fii.ticker}:`, e);
    }
  }

  // Carrega o feed de notícias e fatos relevantes em tempo real da sidebar (Ideia 3)
  async function loadNews(ticker) {
    detNoticias.innerHTML = `
      <div style="color: var(--text-dim); font-size: 0.85rem; text-align: center; padding: 1rem;">
        Carregando notícias em tempo real...
      </div>
    `;

    try {
      const targetUrl = `https://query1.finance.yahoo.com/v1/finance/search?q=${ticker}.SA`;
      const data = await fetchWithCORS(targetUrl);

      if (data && data.news && data.news.length > 0) {
        detNoticias.innerHTML = '';
        
        // Filtra para remover notícias sem título ou link e pega no máximo 4
        const validNews = data.news.filter(n => n.title && n.link).slice(0, 4);

        if (validNews.length === 0) {
          showNoNewsMessage();
          return;
        }

        validNews.forEach(item => {
          const timeStr = formatRelativeTime(item.providerPublishTime);
          const itemEl = document.createElement('div');
          itemEl.className = 'news-item';
          
          itemEl.innerHTML = `
            <a href="${item.link}" target="_blank" class="news-title">${item.title}</a>
            <div class="news-meta">
              <span>${item.publisher}</span>
              <span>${timeStr}</span>
            </div>
          `;
          detNoticias.appendChild(itemEl);
        });
      } else {
        showNoNewsMessage();
      }
    } catch (e) {
      console.warn(`Erro ao buscar notícias para ${ticker}:`, e);
      detNoticias.innerHTML = `
        <div style="color: var(--text-dim); font-size: 0.85rem; text-align: center; padding: 1rem;">
          Não foi possível carregar as notícias de mercado.
        </div>
      `;
    }
  }

  function showNoNewsMessage() {
    detNoticias.innerHTML = `
      <div style="color: var(--text-dim); font-size: 0.85rem; text-align: center; padding: 1rem;">
        Nenhuma notícia recente disponível no momento para este ativo.
      </div>
    `;
  }

  // Busca a cotação em tempo real de um único ativo na B3 via API do Yahoo e proxy CORS de forma pontual
  async function updateSinglePrice(ticker) {
    const targetUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}.SA`;
    try {
      const data = await fetchWithCORS(targetUrl);
      if (data && data.chart && data.chart.result && data.chart.result[0]) {
        const price = data.chart.result[0].meta.regularMarketPrice;
        if (price) {
          const formattedPrice = `R$ ${price.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
          // Atualiza na memória global
          fiisData[ticker].preco = formattedPrice;
          
          // Se o ativo selecionado for o mesmo atualizado, reflete na sidebar
          if (activeFii && activeFii.ticker === ticker) {
            detPreco.innerText = formattedPrice;
            const priceLimpo = parseFloat(formattedPrice.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 100;
            calcCusto.value = priceLimpo;
            updateSimulation();
          }

          // Atualiza visualmente o preço no card correspondente na grade
          const cards = document.querySelectorAll('.fii-card');
          cards.forEach(card => {
            const h2 = card.querySelector('.card-title-group h2');
            if (h2 && h2.innerText === ticker) {
              const valueSpan = card.querySelector('.info-value');
              if (valueSpan) {
                valueSpan.innerText = formattedPrice;
              }
            }
          });
        }
      }
    } catch (e) {
      console.warn(`Erro ao buscar cotação de ${ticker}:`, e);
    }
  }
});
