# Skill: Mapear RI e Baixar Relatórios
Description: Busca sites de Relações com Investidores, identifica o relatório mais recente de FIIs/Fiagros e realiza o download.

## Diretrizes de Execução
1. Leia a lista de fundos fornecida pelo usuário no arquivo local.
2. Para cada fundo, use o MCP de busca para encontrar o site oficial de RI. Priorize termos como "Relatório Mensal", "Relatório Trimestral" ou "Lâmina".
3. Use o Fetch MCP para acessar a página de RI e extrair os links diretos dos PDFs mais recentes.
4. Baixe os PDFs utilizando o ecossistema local e armazene-os temporariamente em uma pasta `/.temp/`.

## Critérios de Sucesso
- Identificar e baixar exatamente 2 relatórios mais recente por fundo da lista.
- Reportar ao usuário caso o link de algum fundo esteja quebrado ou indisponível.
