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
  const detPvp = document.getElementById('det-pvp');
  const detVpa = document.getElementById('det-vpa');
  
  // Elementos Adicionais da Carteira
  const sortSelect = document.getElementById('sort-select');
  const btnMyWallet = document.getElementById('btn-my-wallet');
  const walletModal = document.getElementById('wallet-modal');
  const closeWalletModalBtn = document.getElementById('close-wallet-modal');
  const walletTableBody = document.getElementById('wallet-table-body');
  const btnSaveWallet = document.getElementById('btn-save-wallet');
  const walletTotalInvested = document.getElementById('wallet-total-invested');
  const walletMonthlyIncome = document.getElementById('wallet-monthly-income');
  const walletAverageYoc = document.getElementById('wallet-average-yoc');
  
  // Elementos Adicionais do Comparador
  const compareFloatingBar = document.getElementById('compare-floating-bar');
  const compareBarText = document.getElementById('compare-bar-text');
  const compareBadges = document.getElementById('compare-badges');
  const btnCompareNow = document.getElementById('btn-compare-now');
  const compareModal = document.getElementById('compare-modal');
  const closeCompareModalBtn = document.getElementById('close-compare-modal');
  const compareCol1 = document.getElementById('compare-col-1');
  const compareCol2 = document.getElementById('compare-col-2');
  const compareTableBody = document.getElementById('compare-table-body');
  
  let currentChart = null;
  let activeCategoryFilter = 'todos';
  let activeRecomFilter = 'todos';
  let searchQuery = '';
  let activeFii = null; // FII aberto no momento
  let activeDividendoMaisRecente = 0;
  
  // Variáveis de Estado Novas
  let activeSort = 'alfabetica';
  let myWallet = JSON.parse(localStorage.getItem('my_wallet_data')) || {};
  let selectedForCompare = []; // tickers selecionados para comparador
  
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

  // Escuta a Ordenação
  sortSelect.addEventListener('change', (e) => {
    activeSort = e.target.value;
    renderCards();
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

  // --- Eventos da Carteira ---
  btnMyWallet.addEventListener('click', () => {
    renderWalletTable();
    walletModal.classList.add('open');
  });
  
  closeWalletModalBtn.addEventListener('click', () => {
    walletModal.classList.remove('open');
  });
  
  walletModal.addEventListener('click', (e) => {
    if (e.target === walletModal) {
      walletModal.classList.remove('open');
    }
  });

  btnSaveWallet.addEventListener('click', () => {
    const newWallet = {};
    const tickers = Object.keys(fiisData);
    
    tickers.forEach(ticker => {
      const cotasInput = walletTableBody.querySelector(`.wallet-cotas-input[data-ticker="${ticker}"]`);
      const custoInput = walletTableBody.querySelector(`.wallet-custo-input[data-ticker="${ticker}"]`);
      
      if (cotasInput && custoInput) {
        const cotas = parseInt(cotasInput.value) || 0;
        const custo = parseFloat(custoInput.value) || 0;
        
        if (cotas > 0) {
          newWallet[ticker] = { cotas, custo };
        }
      }
    });
    
    myWallet = newWallet;
    localStorage.setItem('my_wallet_data', JSON.stringify(myWallet));
    alert('Sua carteira de investimentos foi salva com sucesso no navegador!');
    walletModal.classList.remove('open');
    renderCards();
  });

  // --- Eventos do Comparador ---
  btnCompareNow.addEventListener('click', () => {
    if (selectedForCompare.length !== 2) return;
    
    const ticker1 = selectedForCompare[0];
    const ticker2 = selectedForCompare[1];
    const fii1 = fiisData[ticker1];
    const fii2 = fiisData[ticker2];
    
    if (!fii1 || !fii2) return;
    
    compareCol1.innerText = ticker1;
    compareCol2.innerText = ticker2;
    
    const precoLimpo1 = parseFloat(fii1.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
    const precoLimpo2 = parseFloat(fii2.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
    
    const pvp1 = fii1.vpa ? (precoLimpo1 / fii1.vpa) : 0;
    const pvp2 = fii2.vpa ? (precoLimpo2 / fii2.vpa) : 0;
    
    const divRecente1 = fii1.dividendos_recentes ? fii1.dividendos_recentes[fii1.dividendos_recentes.length - 1] : 0;
    const divRecente2 = fii2.dividendos_recentes ? fii2.dividendos_recentes[fii2.dividendos_recentes.length - 1] : 0;
    
    const mediaDiv1 = fii1.dividendos_recentes ? (fii1.dividendos_recentes.reduce((a, b) => a + b, 0) / fii1.dividendos_recentes.length) : 0;
    const mediaDiv2 = fii2.dividendos_recentes ? (fii2.dividendos_recentes.reduce((a, b) => a + b, 0) / fii2.dividendos_recentes.length) : 0;
    
    const metrics = [
      { name: "Nome do Fundo", val1: fii1.nome, val2: fii2.nome },
      { name: "Segmento / Tipo", val1: fii1.tipo, val2: fii2.tipo },
      { name: "Preço de Mercado", val1: fii1.preco, val2: fii2.preco },
      { name: "Valor Patrimonial (VPA)", val1: fii1.vpa ? `R$ ${fii1.vpa.toFixed(2)}` : '-', val2: fii2.vpa ? `R$ ${fii2.vpa.toFixed(2)}` : '-' },
      { name: "Indicador P/VP", val1: pvp1 > 0 ? pvp1.toFixed(2) : '-', val2: pvp2 > 0 ? pvp2.toFixed(2) : '-' },
      { name: "Recomendação Analítica", val1: fii1.recomendacao, val2: fii2.recomendacao, isBadge: true, badgeType1: fii1.recomendacao.toLowerCase(), badgeType2: fii2.recomendacao.toLowerCase() },
      { name: "Nota de Alerta (Risco)", val1: `${fii1.alerta}/10`, val2: `${fii2.alerta}/10` },
      { name: "Tendência de Preço", val1: fii1.tendencia_preco, val2: fii2.tendencia_preco, isTrend: true },
      { name: "Tendência de Dividendos", val1: fii1.tendencia_dividendos, val2: fii2.tendencia_dividendos, isTrend: true },
      { name: "Último Dividendo Pago", val1: divRecente1 ? `R$ ${divRecente1.toFixed(2)}` : '-', val2: divRecente2 ? `R$ ${divRecente2.toFixed(2)}` : '-' },
      { name: "Média de Dividendos (6M)", val1: mediaDiv1 ? `R$ ${mediaDiv1.toFixed(2)}` : '-', val2: mediaDiv2 ? `R$ ${mediaDiv2.toFixed(2)}` : '-' }
    ];
    
    compareTableBody.innerHTML = '';
    
    metrics.forEach(m => {
      const row = document.createElement('tr');
      let colVal1 = m.val1;
      let colVal2 = m.val2;
      
      if (m.isBadge) {
        colVal1 = `<span class="badge-status ${m.badgeType1}" style="display:inline-flex; justify-content:center; width:100px;">${m.val1}</span>`;
        colVal2 = `<span class="badge-status ${m.badgeType2}" style="display:inline-flex; justify-content:center; width:100px;">${m.val2}</span>`;
      } else if (m.isTrend) {
        const tClass1 = m.val1 === 'aumentar' || m.val1 === 'subir' ? 'aumentar' : m.val1 === 'manter' ? 'manter' : 'cair';
        const tClass2 = m.val2 === 'aumentar' || m.val2 === 'subir' ? 'aumentar' : m.val2 === 'manter' ? 'manter' : 'cair';
        colVal1 = `<span style="text-transform: capitalize; font-weight: 600;" class="trend-${tClass1}">${m.val1 === 'aumentar' ? 'Subir' : m.val1}</span>`;
        colVal2 = `<span style="text-transform: capitalize; font-weight: 600;" class="trend-${tClass2}">${m.val2 === 'aumentar' ? 'Subir' : m.val2}</span>`;
      }
      
      row.innerHTML = `
        <td style="font-weight: 500; color: var(--text-muted);">${m.name}</td>
        <td style="text-align: center; font-weight: 600;">${colVal1}</td>
        <td style="text-align: center; font-weight: 600;">${colVal2}</td>
      `;
      compareTableBody.appendChild(row);
    });
    
    compareModal.classList.add('open');
  });

  closeCompareModalBtn.addEventListener('click', () => {
    compareModal.classList.remove('open');
  });
  
  compareModal.addEventListener('click', (e) => {
    if (e.target === compareModal) {
      compareModal.classList.remove('open');
    }
  });

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

    // Ordenação Dinâmica
    filteredFiis.sort((a, b) => {
      const fiiA = fiisData[a];
      const fiiB = fiisData[b];
      
      const precoA = parseFloat(fiiA.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
      const precoB = parseFloat(fiiB.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
      
      const divA = fiiA.dividendos_recentes ? fiiA.dividendos_recentes[fiiA.dividendos_recentes.length - 1] : 0;
      const divB = fiiB.dividendos_recentes ? fiiB.dividendos_recentes[fiiB.dividendos_recentes.length - 1] : 0;
      
      const dyA = precoA > 0 ? (divA / precoA) : 0;
      const dyB = precoB > 0 ? (divB / precoB) : 0;
      
      const pvpA = fiiA.vpa && precoA > 0 ? (precoA / fiiA.vpa) : 999;
      const pvpB = fiiB.vpa && precoB > 0 ? (precoB / fiiB.vpa) : 999;
      
      if (activeSort === 'alfabetica') {
        return fiiA.ticker.localeCompare(fiiB.ticker);
      } else if (activeSort === 'maior-dy') {
        return dyB - dyA;
      } else if (activeSort === 'menor-risco') {
        return fiiA.alerta - fiiB.alerta;
      } else if (activeSort === 'mais-descontado') {
        return pvpA - pvpB;
      }
      return 0;
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

    const precoLimpo = parseFloat(fii.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
    const pvp = fii.vpa ? (precoLimpo / fii.vpa) : 0;
    const isDescontado = pvp > 0 && pvp < 1.0;
    const pvpFormatted = pvp > 0 ? pvp.toFixed(2) : '-';

    const ownsIt = myWallet[fii.ticker] && myWallet[fii.ticker].cotas > 0;
    const isChecked = selectedForCompare.includes(fii.ticker) ? 'checked' : '';

    card.innerHTML = `
      <!-- Checkbox de Comparação -->
      <label class="compare-checkbox-container" onclick="event.stopPropagation();">
        <input type="checkbox" class="compare-checkbox" data-ticker="${fii.ticker}" ${isChecked}>
        <span class="checkmark"></span>
      </label>

      <div class="card-header">
        <div class="card-title-group">
          <h2 style="display: inline-flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
            ${fii.ticker}
            ${ownsIt ? '<span style="font-size: 0.65rem; background: rgba(59, 130, 246, 0.12); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.2); padding: 0.1rem 0.35rem; border-radius: 4px; font-weight: 700; line-height: 1;">CARTEIRA</span>' : ''}
            ${fii.fato_relevante_recente ? '<span class="pulse-dot-inline" title="Fato Relevante Recente"></span>' : ''}
          </h2>
          <span>${fii.nome}</span>
        </div>
        <span class="badge-type">${fii.tipo.split(' ')[0]}</span>
      </div>
      
      <div class="card-body-content" style="display: flex; flex-direction: column; gap: 0.55rem; margin-top: 0.25rem;">
        <!-- Bloco do Preço Principal & P/VP -->
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
          <div class="info-item">
            <span class="info-label">Preço Atual</span>
            <span class="info-value" style="font-size: 1.35rem; font-weight: 700; color: var(--text-main);">${fii.preco}</span>
          </div>
          <div class="info-item" style="align-items: flex-end; text-align: right;">
            <span class="info-label">P/VP</span>
            <div style="display: flex; align-items: center; gap: 0.3rem;">
              ${isDescontado ? '<span style="font-size: 0.65rem; font-weight: 700; padding: 0.1rem 0.35rem; border-radius: 4px; background: rgba(16, 185, 129, 0.12); color: var(--color-buy); border: 1px solid rgba(16, 185, 129, 0.2); letter-spacing: 0.02em; line-height: 1;">DESCONTO</span>' : ''}
              <span class="info-value ${isDescontado ? 'highlight-yoc' : ''}" style="font-size: 1.15rem; font-weight: 700;">${pvpFormatted}</span>
            </div>
          </div>
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

    const checkbox = card.querySelector('.compare-checkbox');
    checkbox.addEventListener('change', (e) => {
      const ticker = e.target.getAttribute('data-ticker');
      if (e.target.checked) {
        if (selectedForCompare.length >= 2) {
          e.target.checked = false;
          alert('Você só pode selecionar até 2 ativos para comparação lado a lado.');
          return;
        }
        if (!selectedForCompare.includes(ticker)) {
          selectedForCompare.push(ticker);
        }
      } else {
        selectedForCompare = selectedForCompare.filter(t => t !== ticker);
      }
      updateCompareBar();
    });

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

    // Atualiza P/VP e VPA na Sidebar
    const precoLimpo = parseFloat(fii.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 100;
    const pvp = fii.vpa ? (precoLimpo / fii.vpa) : 0;
    detPvp.innerText = pvp > 0 ? pvp.toFixed(2) : '-';
    detVpa.innerText = fii.vpa ? `(VPA: R$ ${fii.vpa.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })})` : '(VPA: -)';
    
    if (pvp > 0 && pvp < 1.0) {
      detPvp.className = 'info-value highlight-yoc';
    } else {
      detPvp.className = 'info-value';
    }

    // Inicializa os campos do Simulador
    calcCotas.value = 100;
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
    
    // Busca atualizações de preços em tempo real em lote com delay inteligente
    updatePricesRealTime();
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

  // Auxiliar para atrasar a execução e evitar bloqueios por taxa de requisição (Rate Limit)
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

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

  // Busca as cotações em tempo real de todos os ativos da B3 na inicialização de forma sequencial com delay
  async function updatePricesRealTime() {
    const tickers = Object.keys(fiisData);
    
    for (const ticker of tickers) {
      const targetUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}.SA`;
      
      try {
        const data = await fetchWithCORS(targetUrl);
        if (data && data.chart && data.chart.result && data.chart.result[0]) {
          const price = data.chart.result[0].meta.regularMarketPrice;
          if (price) {
            fiisData[ticker].preco = `R$ ${price.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
          }
        }
      } catch (e) {
        console.warn(`Erro ao buscar cotação em tempo real de ${ticker}:`, e);
      }
      // Pequeno delay de 120ms para espaçar as consultas e evitar o bloqueio de IP 429
      await sleep(120);
    }

    // Renderiza novamente os cards com os preços reais atualizados na grade principal
    renderCards();
    
    // Se a sidebar estiver aberta para um FII, atualiza o preço na tela
    if (activeFii && fiisData[activeFii.ticker]) {
      detPreco.innerText = fiisData[activeFii.ticker].preco;
      const priceStr = fiisData[activeFii.ticker].preco;
      const precoLimpo = parseFloat(priceStr.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 100;
      calcCusto.value = precoLimpo;
      updateSimulation();
    }
  }

  // --- Função Auxiliar do Comparador ---
  function updateCompareBar() {
    if (selectedForCompare.length > 0) {
      compareFloatingBar.classList.add('visible');
      compareBadges.innerHTML = '';
      
      selectedForCompare.forEach(ticker => {
        const badge = document.createElement('div');
        badge.className = 'compare-badge';
        badge.innerHTML = `
          <span>${ticker}</span>
          <button data-remove-ticker="${ticker}">&times;</button>
        `;
        badge.querySelector('button').addEventListener('click', (e) => {
          e.stopPropagation();
          const removeTicker = e.target.getAttribute('data-remove-ticker');
          selectedForCompare = selectedForCompare.filter(t => t !== removeTicker);
          
          // Desmarca checkbox no card
          const cb = document.querySelector(`.compare-checkbox[data-ticker="${removeTicker}"]`);
          if (cb) cb.checked = false;
          
          updateCompareBar();
        });
        compareBadges.appendChild(badge);
      });
      
      if (selectedForCompare.length === 2) {
        compareBarText.innerText = 'Comparar fundos selecionados:';
        btnCompareNow.disabled = false;
      } else {
        compareBarText.innerText = 'Selecione 2 fundos para comparar:';
        btnCompareNow.disabled = true;
      }
    } else {
      compareFloatingBar.classList.remove('visible');
    }
  }

  // --- Função Auxiliar da Carteira ---
  function renderWalletTable() {
    walletTableBody.innerHTML = '';
    const tickers = Object.keys(fiisData).sort();
    
    tickers.forEach(ticker => {
      const fii = fiisData[ticker];
      const data = myWallet[ticker] || { cotas: 0, custo: 0 };
      const precoLimpo = parseFloat(fii.preco.replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
      
      const row = document.createElement('tr');
      row.innerHTML = `
        <td style="font-weight: 600;">
          <div>${ticker}</div>
          <div style="font-size: 0.7rem; color: var(--text-dim); font-weight: normal;">${fii.nome.slice(0, 20)}...</div>
        </td>
        <td>R$ ${precoLimpo.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
        <td>
          <input type="number" class="wallet-input wallet-cotas-input" data-ticker="${ticker}" value="${data.cotas > 0 ? data.cotas : ''}" min="0" placeholder="0">
        </td>
        <td>
          <input type="number" class="wallet-input wallet-custo-input" data-ticker="${ticker}" value="${data.custo > 0 ? data.custo.toFixed(2) : ''}" min="0" step="0.01" placeholder="0,00">
        </td>
        <td class="wallet-row-income" data-ticker="${ticker}">R$ 0,00</td>
        <td class="wallet-row-total" data-ticker="${ticker}">R$ 0,00</td>
      `;
      walletTableBody.appendChild(row);
    });
    
    const cotasInputs = walletTableBody.querySelectorAll('.wallet-cotas-input');
    const custoInputs = walletTableBody.querySelectorAll('.wallet-custo-input');
    
    const updateCalculations = () => {
      let totalPortfolioInvested = 0;
      let totalPortfolioMonthlyIncome = 0;
      
      tickers.forEach(ticker => {
        const fii = fiisData[ticker];
        const cotasInput = walletTableBody.querySelector(`.wallet-cotas-input[data-ticker="${ticker}"]`);
        const custoInput = walletTableBody.querySelector(`.wallet-custo-input[data-ticker="${ticker}"]`);
        
        const cotas = parseInt(cotasInput.value) || 0;
        const custo = parseFloat(custoInput.value) || 0;
        
        const divRecente = fii.dividendos_recentes ? fii.dividendos_recentes[fii.dividendos_recentes.length - 1] : 0;
        
        const rowIncome = cotas * divRecente;
        const rowTotal = cotas * custo;
        
        const incomeCell = walletTableBody.querySelector(`.wallet-row-income[data-ticker="${ticker}"]`);
        const totalCell = walletTableBody.querySelector(`.wallet-row-total[data-ticker="${ticker}"]`);
        
        incomeCell.innerText = `R$ ${rowIncome.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        totalCell.innerText = `R$ ${rowTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        if (cotas > 0) {
          totalPortfolioInvested += rowTotal;
          totalPortfolioMonthlyIncome += rowIncome;
        }
      });
      
      walletTotalInvested.innerText = `R$ ${totalPortfolioInvested.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      walletMonthlyIncome.innerText = `R$ ${totalPortfolioMonthlyIncome.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      
      if (totalPortfolioInvested > 0) {
        const avgYoc = ((totalPortfolioMonthlyIncome * 12) / totalPortfolioInvested) * 100;
        walletAverageYoc.innerText = `${avgYoc.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
      } else {
        walletAverageYoc.innerText = '0,00%';
      }
    };
    
    cotasInputs.forEach(input => input.addEventListener('input', updateCalculations));
    custoInputs.forEach(input => input.addEventListener('input', updateCalculations));
    
    updateCalculations();
  }
});
