# Projeto para o Futuro: Melhorias e Otimizações

Este documento serve como guia arquitetural para futuras IAs que assumirem o desenvolvimento do painel (FII Explorer / Terminal de Investimentos). 

## 1. Expansão Multi-Ativos (Ações, ETFs, BDRs)
Atualmente o painel é focado exclusivamente na análise de Fundos Imobiliários e Fiagros. O usuário possui uma lista extensa de Ações Brasileiras e BDRs que deverão ser inseridos no futuro.
Como a lógica de avaliação de Ações difere drasticamente da de FIIs, a arquitetura deverá ser adaptada:

* **Separação de Banco de Dados:** Substituir o monolítico `data.js` por arquivos separados (ex: `data_fiis.js`, `data_acoes.js`, `data_internacional.js`).
* **Métricas Específicas:** Enquanto FIIs exibem P/VP, Vacância e Dividend Yield, os *Cards* de Ações deverão exibir múltiplos apropriados, como P/L (Preço/Lucro), ROE, Margem Líquida e Dívida.
* **Interface com Abas (Tabs):** O frontend deverá acomodar um menu de navegação separando as categorias (ex: [ FIIs ] | [ Ações ] | [ BDRs / ETFs ]).

## 2. Novo Motor de Cotações (Backend Serverless)
A API gratuita atual (*MFinance*) possui limitações críticas: bloqueios por requisições (rate limits) e ausência de dados para ETFs (ex: COIN11, AURO11) e BDRs.

* **Solução Proposta:** Criar um backend próprio utilizando as *Serverless Functions* do Vercel (diretório `/api/`).
* **Tecnologia:** Scripts em Python utilizando a biblioteca `yfinance` para buscar cotações e histórico de qualquer ativo global (ex: `PETR4.SA`, `AAPL34.SA`, `COIN11.SA`) sem problemas de CORS ou ausência de dados de ETFs.

## 3. Protocolos de Deploy Automático
* Qualquer futura atualização de funcionalidades visuais ou alteração em bases de dados locais deve, OBRIGATORIAMENTE, ser "commitada" e despachada para o repositório (`git push`) imediatamente após a modificação, garantindo que as mudanças reflitam em tempo real na URL de produção do Vercel para a aprovação visual do usuário.
