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
  
  let currentChart = null;
  let activeCategoryFilter = 'todos';
  let activeRecomFilter = 'todos';
  let searchQuery = '';
  let activeFii = null; // FII aberto no momento
  
  // Elementos do Simulador
  const calcCotas = document.getElementById('calc-cotas');
  const calcCusto = document.getElementById('calc-custo');
  const calcResultTotal = document.getElementById('calc-result-total');
  const calcResultMensal = document.getElementById('calc-result-mensal');
  const calcResultYoc = document.getElementById('calc-result-yoc');

  // Inicializa o Renderizador
  renderCards();

  // Busca e atualiza preços em tempo real em segundo plano
  updatePricesRealTime();

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
    
    // Configura o Ícone de Tendência e Classe
    let trendIcon = '';
    let trendClass = '';
    if (fii.tendencia_dividendos === 'aumentar') {
      trendIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>';
      trendClass = 'trend-aumentar';
    } else if (fii.tendencia_dividendos === 'manter') {
      trendIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
      trendClass = 'trend-manter';
    } else {
      trendIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>';
      trendClass = 'trend-cair';
    }

    card.innerHTML = `
      <div class="card-header">
        <div class="card-title-group">
          <h2>${fii.ticker}</h2>
          <span>${fii.nome}</span>
        </div>
        <span class="badge-type">${fii.tipo.split(' ')[0]}</span>
      </div>
      <div class="card-info-row">
        <div class="info-item">
          <span class="info-label">Preço</span>
          <span class="info-value">${fii.preco}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Tendência Divs</span>
          <div class="tendencia-wrapper ${trendClass}">
            <span class="trend-arrow">${trendIcon}</span>
            <span class="info-value" style="font-size: 0.85rem; text-transform: capitalize;">${fii.tendencia_dividendos}</span>
          </div>
        </div>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
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
    
    detTicker.innerText = fii.ticker;
    detNome.innerText = fii.nome;
    detTipo.innerText = fii.tipo;
    detPreco.innerText = fii.preco;
    detAlerta.innerText = `${fii.alerta}/10`;

    // Inicializa os campos do Simulador
    calcCotas.value = 100;
    const precoLimpo = parseFloat(fii.preco.replace('R$', '').replace('.', '').replace(',', '.').trim()) || 100;
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

    // Renderizar Gráfico de Proventos
    renderChart(fii);
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
    
    // Obtém o dividendo mais recente (último item do array dividendos_recentes)
    const ultimoDividendo = activeFii.dividendos_recentes[activeFii.dividendos_recentes.length - 1];
    
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

  // Renderiza o Gráfico de Dividendos com base nas cores do Fundo
  function renderChart(fii) {
    if (currentChart) {
      currentChart.destroy();
    }

    const ctx = document.getElementById('proventosChart').getContext('2d');
    
    // Cores dinâmicas para o gráfico baseadas na recomendação
    let lineColor = '#3b82f6';
    let gradientStart = 'rgba(59, 130, 246, 0.2)';
    
    if (fii.recomendacao === 'Comprar') {
      lineColor = '#10b981';
      gradientStart = 'rgba(16, 185, 129, 0.2)';
    } else if (fii.recomendacao === 'Vender') {
      lineColor = '#f43f5e';
      gradientStart = 'rgba(244, 63, 94, 0.2)';
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, gradientStart);
    gradient.addColorStop(1, 'rgba(16, 20, 29, 0)');

    // Gera os labels para os últimos 6 meses (ex: Mês 1 a Mês 6)
    const labels = ['Dez/24', 'Jan/25', 'Fev/25', 'Mar/25', 'Abr/25', 'Mai/25'];

    currentChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Dividendos por Cota',
          data: fii.dividendos_recentes,
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

  // Busca as cotações em tempo real da B3 via API do Yahoo e proxy CORS
  async function updatePricesRealTime() {
    const tickers = Object.keys(fiisData);
    
    // Dispara as consultas em paralelo para todos os tickers
    const promises = tickers.map(async (ticker) => {
      const url = `https://api.allorigins.win/raw?url=${encodeURIComponent(`https://query1.finance.yahoo.com/v8/finance/chart/${ticker}.SA`)}`;
      
      try {
        const response = await fetch(url);
        if (!response.ok) return;
        const data = await response.json();
        
        if (data && data.chart && data.chart.result && data.chart.result[0]) {
          const price = data.chart.result[0].meta.regularMarketPrice;
          if (price) {
            fiisData[ticker].preco = `R$ ${price.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
          }
        }
      } catch (e) {
        console.warn(`Erro ao buscar cotação de ${ticker}:`, e);
      }
    });

    try {
      await Promise.all(promises);
      
      // Renderiza novamente os cards com os preços reais atualizados
      renderCards();
      
      // Se o modal lateral estiver aberto, atualiza o preço e o simulador na tela
      if (activeFii && fiisData[activeFii.ticker]) {
        detPreco.innerText = fiisData[activeFii.ticker].preco;
        const precoLimpo = parseFloat(fiisData[activeFii.ticker].preco.replace('R$', '').replace('.', '').replace(',', '.').trim()) || 100;
        calcCusto.value = precoLimpo;
        updateSimulation();
      }
    } catch (err) {
      console.error('Erro na atualização em lote de cotações:', err);
    }
  }
});
