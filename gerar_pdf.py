import json
import os
import subprocess

# Config
WORKSPACE = "/home/toten/projeto-antigravity"
TEMP_DIR = os.path.join(WORKSPACE, ".temp")
HTML_FILE = os.path.join(TEMP_DIR, "consolidado.html")
PDF_FILE = os.path.join(WORKSPACE, "Relatorios_Consolidados.pdf")


# Data collected from subagents
ANALYSES = {
  "KNCA11": {
    "explicacoes": "Fundo focado em ativos de crédito do agronegócio (FIAGRO), investindo majoritariamente em CRAs e FIAGRO FIDCs. Em jun/24, apresentava 103,4% de alocação em ativos alvo (64,8% em CDI com taxa média de CDI + 4,53% e 38,6% em IPCA com taxa média de IPCA + 7,98%) e 0,9% em caixa. A carteira é concentrada setorialmente em bioenergia, produção de insumos e proteína animal.",
    "pontos_criticos": "Presença de alavancagem através de operações compromissadas reversas atreladas a CRAs, equivalendo a 4,3% do PL (R$ 95 milhões). Rendimentos e resultados gerados sofrem oscilações decorrentes da inflação e patamar da Selic (distribuição caiu de R$ 1,15/cota em jan/24 para R$ 1,00/cota em jun/24). Sem inadimplência registrada.",
    "recomendacoes": "Hold / Buy. Cenário de manutenção dos juros locais elevados continua favorecendo a carteira pós-fixada em CDI. Recomendado comprar se negociado próximo ou abaixo do valor patrimonial.",
    "alerta": 2,
    "tipo": "Fiagro"
  },
  "KNIP11": {
    "explicacoes": "Fundo de CRI de baixo risco de crédito indexado à inflação (IPCA). Ao fim de nov/24, a carteira continha 104,9% do PL em ativos-alvo (97,1% em IPCA com taxa média de IPCA + 9,46% e duration de 4,1 anos) e 2,8% em caixa, com foco setorial em Shoppings (30,0%), Escritórios (29,2%) e Logística (24,9%).",
    "pontos_criticos": "Alavancagem relevante via compromissadas reversas atreladas a CRIs, totalizando 7,7% do PL. Apresenta volatilidade de curto prazo na distribuição de rendimentos ligada à variação do IPCA (queda para R$ 0,70 e R$ 0,75 no 3T24 decorrente da deflação de agosto, recuperando-se para R$ 0,90 em nov/24). Cotas negociadas no secundário com deságio relevante.",
    "recomendacoes": "Buy. O deságio de mercado (mercado a R$ 90,73 vs patrimonial a R$ 92,91) propicia um yield de entrada altamente atrativo em relação às NTN-Bs e a carteira de crédito permanece 100% adimplente e saudável.",
    "alerta": 2,
    "tipo": "Papel (CRI)"
  },
  "KNRI11": {
    "explicacoes": "Fundo híbrido de tijolo detentor de portfólio de lajes corporativas e condomínios logísticos de alto padrão em SP, RJ e Jundiaí. Reajustes dos contratos de locação são indexados majoritariamente ao IPCA (55,51% das receitas) e IGP-M (27,70%). Possui liquidez complementar investida em CRIs da VERT Securitizadora.",
    "pontos_criticos": "Apesar da vacância muito baixa e sob controle nos principais ativos (ex. Lagoa Corporate com 1,86% e Botafogo TC com 1,33%), há inadimplência pontual expressiva de 10,36% no Edifício Joaquim Floriano em SP (que responde por 1,24% da receita total do FII). As taxas de administração e despesas de manutenção representam impacto expressivo na receita.",
    "recomendacoes": "Hold. Portfólio de tijolo resiliente e tradicional de excelente qualidade imobiliária. Ideal para manutenção em carteira com foco em fluxo constante de renda no longo prazo.",
    "alerta": 1,
    "tipo": "Híbrido (Tijolo)"
  },
  "SNAG11": {
    "explicacoes": "Fiagro de papel gerido pela Suno Asset, focado em ativos de crédito privado do agronegócio (CRAs e CRIs) e imóveis rurais. A principal alocação é o CRA Boa Safra (89% do PL), distribuído em 55 contratos pulverizados por 32 municípios. O portfólio tem 95% de exposição à soja e 3% a alimentos (CRI Bem Brasil), gerando Dividend Yield anualizado de 15,28% (junho/2023).",
    "pontos_criticos": "Elevada concentração do portfólio em um único grupo devedor (Boa Safra Sementes S/A com 89% do PL). Exposição a riscos inerentes do setor agrícola, como intempéries climáticas, variação de preços de commodities e variação cambial/insumos. Adicionalmente, há registro de deterioração de crédito geral no mercado de Fiagros (ex: Languiru e AgroGalaxy).",
    "recomendacoes": "Recomendação de MANUTENÇÃO/COMPRA (Hold) justificada pela resiliência histórica do setor de soja, taxa de rendimento elevada (~15%) e governança ativa auxiliada pela Serasa Experian na avaliação contínua de crédito dos produtores.",
    "alerta": 4,
    "tipo": "Fiagro"
  },
  "TRXF11": {
    "explicacoes": "Fundo de tijolo de renda urbana e logística com 74 imóveis em 12 estados e WALE (prazo médio) de 14,28 anos. Foca em locações de longo prazo para grandes empresas (81,04% de contratos atípicos) com vacância física mínima de 0,22%. Destaca-se a aquisição de 70% do Hospital Albert Einstein - Parque Global (SP) com início em julho de 2026 e a 12ª emissão de cotas para captar R$ 2 bilhões voltados para um pipeline de R$ 2,38 bilhões.",
    "pontos_criticos": "Risco de execução e atraso nas obras de ativos em desenvolvimento (como o Hospital Albert Einstein, 77% concluído). Alavancagem implícita ou risco financeiro associado a obrigações de pagamentos a prazo das aquisições do novo pipeline, além de concentração em inquilinos de varejo de grande porte.",
    "recomendacoes": "Recomendação de COMPRA baseada no perfil altamente defensivo dos contratos atípicos longos, vacância quase nula e ativos imobiliários premium adicionados ao portfólio. O atual ciclo macroeconômico favorece fundos de tijolo com alta previsibilidade de renda.",
    "alerta": 3,
    "tipo": "Tijolo (Renda Urbana)"
  },
  "TVRI11": {
    "explicacoes": "Fundo de tijolo focado em renda urbana e lajes corporativas com 61 imóveis em 14 estados, negociando com desconto relevante (P/VP de 0,86) e Dividend Yield anualizado de 14,11%. Realizou reciclagem ativa de ativos gerando R$ 2,07 por cota de ganhos extraordinários desde nov/2023.",
    "pontos_criticos": "Altíssima concentração de vencimentos de locações em Novembro de 2027 (incluindo Ed. Sede III - DF com 20,5% da receita e CSL São Paulo com 7,8%), impondo elevado risco de renovação ou revisional. Além disso, 10 imóveis (16% do total) ainda encontram-se pendentes de regularização de matrícula cartorária. A distribuição mensal recente (R$ 1,03) superou a geração de caixa recorrente (R$ 0,99).",
    "recomendacoes": "Recomendação de MANUTENÇÃO (Hold) pelo atraente retorno imediato (DY de 14%) e desconto patrimonial, porém com sinal de cautela que impede recomendação forte de compra devido ao risco concentrado de vencimento do portfólio em 2027 e pendências operacionais cartoriais.",
    "alerta": 5,
    "tipo": "Tijolo (Renda Urbana)"
  },
  "KNSC11": {
    "explicacoes": "Fundo de papel gerido pela Kinea Investimentos focado em ativos de renda fixa imobiliária, principalmente CRIs. Possui alta taxa de alocação de seu patrimônio (97,1% em ativos-alvo), com 60,2% alocados em CRIs indexados ao IPCA (remuneração média de IPCA + 9,60% a.a. e duration de 7 anos) e 36,7% em CRIs indexados ao CDI (remuneração média de CDI + 3,33% a.a. e duration de 3,5 anos). Os recursos captados na 5ª emissão foram rapidamente alocados.",
    "pontos_criticos": "Cenário de inflação incerto com pressões fiscais domésticas e depreciação cambial. A taxa Selic elevada impacta a parcela de ativos em CDI e aumenta o custo de crédito do mercado, embora o fundo não apresente inadimplências ou eventos negativos de crédito em sua carteira.",
    "recomendacoes": "Recomendação de compra/manutenção devido à alta qualidade de crédito das operações, taxas médias de originação atrativas e proteção de capital robusta em cenários de juros altos e inflação.",
    "alerta": 2,
    "tipo": "Papel (CRI)"
  },
  "LVBI11": {
    "explicacoes": "Fundo de tijolo focado em galpões logísticos de alto padrão (95% da receita vem de ativos classe A/A+), gerido pelo Pátria-VBI Asset. Possui imóveis premium com foco em contratos de longo prazo, inquilinos de primeira linha e gestão ativa voltada a reformas, melhorias e expansão da ABL (com retornos elevados, como 17% a.a. na expansão de Betim). A carteira apresenta exposição predominante a contratos típicos de locação.",
    "pontos_criticos": "Elevação temporária da vacância para 10,7% em fevereiro de 2025 após desocupações da Sequoia (Extrema) e Dia% (Mauá), ambas em recuperação judicial e que geraram inadimplências acumuladas de R$ 0,17/cota (incluindo débitos da Americanas). O fundo precisou utilizar suas reservas financeiras para manter a distribuição em R$ 0,75/cota no 1S25. Juros altos impactaram a precificação dos ativos, resultando em queda no valor patrimonial (VPA) de R$ 124,77 para R$ 117,64.",
    "recomendacoes": "Recomendação de MANTER (Hold) conforme relatório da Capitalizo de 04/06/2025 (preço de mercado R$ 101,24, preço-teto R$ 135,00 e valor justo R$ 150,00). A vacância projetada deve recuar para 3,9% em julho de 2025 e fechar o ano em 6,4% com a rápida reocupação por Nestlé, Solistica, ArcelorMittal, Interbrands Foods e Atakarejo, tornando os dividendos sustentáveis recorrentemente.",
    "alerta": 4,
    "tipo": "Tijolo (Logística)"
  },
  "MXRF11": {
    "explicacoes": "Fundo híbrido multiestratégia gerido pela XP Asset, sendo o maior da B3 em número de cotistas (1,28 milhão). Foca na geração de renda estável por meio de investimentos em CRIs (80,7% da carteira ou R$ 3,23 bilhões), cotas de FIIs (12%), permutas financeiras (7%) e caixa (4%). A carteira de CRIs é majoritariamente indexada ao IPCA (85%) e CDI (15%).",
    "pontos_criticos": "Exposição significativa a índices de inflação (85% do portfólio de CRIs atrelado ao IPCA), o que traz volatilidade nos rendimentos em períodos de deflação ou oscilações no indexador. Riscos específicos de incorporação imobiliária nas permutas financeiras e volatilidade de mercado na carteira de FIIs.",
    "recomendacoes": "Recomendação de COMPRA (Buy) conforme cobertura do BTG Pactual (Rating Compra), com preço-teto de R$ 9,72 (preço de mercado de R$ 9,41 no período). O fundo oferece excelente liquidez diária, boa diversificação de devedores e setores, e consistência nos dividendos com rendimento mensal estável (dividend yield médio entre 0,90% e 1,08% ao mês).",
    "alerta": 2,
    "tipo": "Híbrido (Recebíveis)"
  },
  "VISC11": {
    "explicacoes": "O Vinci Shopping Centers FII (VISC11) foca na exploração de shopping centers com gestão ativa para geração de renda e valorização dos imóveis a longo prazo. O portfólio é composto por ativos como West Shopping, Shopping Paralela, Center Shopping Rio, Shopping Crystal e Ilha Plaza. Recentemente, concluiu a aquisição de 5,0% do Shopping Plaza Sul por R$ 30 milhões (cap rate de 8,5%) e realizou a venda de um terreno adjacente ao RibeirãoShopping por R$ 9 milhões. Os contratos de locação são reajustados majoritariamente pelo IGP-M (60,76%) e IGP-DI (35,51%).",
    "pontos_criticos": "O fundo apresenta taxa de vacância física elevada em ativos específicos: Shopping Crystal (26,51%) e Center Shopping Rio (18,20%). No trimestre analisado, o resultado contábil foi fortemente impactado negativamente por um ajuste ao valor justo de -R$ 40,95 milhões, reduzindo o resultado contábil trimestral para R$ 20,55 milhões, muito inferior ao resultado financeiro de R$ 65,03 milhões. Além disso, a venda do terreno adjacente ao RibeirãoShopping possui cláusulas que permitem ao comprador exigir a recompra do terreno em até 3 anos se condições específicas não forem superadas.",
    "recomendacoes": "Hold (Manter). Embora o fundo possua excelente liquidez na B3 (negociando entre R$ 3 milhões e R$ 13 milhões por dia), tenha distribuído dividendos consistentes (R$ 0,80 em fev/2025 e R$ 1,00 em mar/2024) e conte com reserva de lucros acumulados não distribuídos (R$ 1,21 por cota), a vacância expressiva em ativos como o Shopping Crystal e Center Shopping Rio, somada ao cenário macroeconômico de juros altos (Selic mantida em 15%), sugere uma postura de cautela.",
    "alerta": 3,
    "tipo": "Tijolo (Shoppings)"
  },
  "XPLG11": {
    "explicacoes": "O XP Log FII (XPLG11) tem por objetivo a aquisição, desenvolvimento e gestão ativa de galpões logísticos de alto padrão (Class A/A+) localizados em regiões premium de distribuição no Brasil, visando capturar o crescimento do e-commerce. A carteira é composta por imóveis como Cajamar, Cachoeirinha, CD Renner, CD Leroy M, Duquecx RJ e Imo Itapeva. O fundo também possui R$ 697 milhões alocados em FIIs logísticos, concentrados massivamente no FII NE LOGI (R$ 658 milhões). Os contratos são majoritariamente indexados ao IPCA.",
    "pontos_criticos": "O fundo reportou um resultado contábil trimestral negativo de -R$ 37,2 milhões devido a despesas extraordinárias e ajustes de valor justo negativos, embora a geração de caixa financeiro permaneça saudável (R$ 65,6 milhões). Existem focos pontuais de vacância física, como no CD Leroy M (10,09%) e no Duquecx_RJ (9,63%). Há também uma forte dependência/concentração de recursos na carteira de FIIs no ativo FII NE LOGI.",
    "recomendacoes": "Hold (Manter). O preço de mercado da cota (R$ 99,51 em jun/2025) está abaixo do preço teto (R$ 126,00) e do valor justo estimado (R$ 140,00) por modelos de crescimento constante (Modelo de Gordon), indicando desconto. No entanto, analistas recomendam manter o ativo em carteira (Hold) por considerarem que existem outras oportunidades de mercado com melhor relação de risco-retorno no momento.",
    "alerta": 2,
    "tipo": "Tijolo (Logística)"
  },
  "XPML11": {
    "explicacoes": "O XP Malls FII (XPML11) foca na aquisição e gestão ativa de shopping centers com alto fluxo de consumidores. Seus principais ativos de renda são o Catarina Fashion Outlet (8,87% da receita do FII), Shopping Cidade Jardim (4,41%), Shopping Cidade de São Paulo (4,40%), Shopping Plaza Sul (2,13%) e Caxias Shopping (1,44%). O fundo mantém alta liquidez de caixa (R$ 367,7 milhões em fundos de renda fixa e R$ 49,6 milhões em disponibilidades). Adicionalmente, os relatórios vinculados sob este código trazem o ARRI11 (Átrio Recebíveis Imobiliários), fundo de papel focado em CRIs High Yield (indexados a IPCA+ e CDI+).",
    "pontos_criticos": "O XPML11 registrou uma desvalorização contábil de ativos de R$ 106,4 milhões que impactou temporariamente seu resultado contábil trimestral (R$ 64,67 milhões vs. R$ 172,56 milhões no critério financeiro). No portfólio de shoppings, o Caxias Shopping apresenta a maior vacância física (5,08%). No tocante aos relatórios do ARRI11 anexados, o ponto crítico reside no risco de crédito elevado da carteira de CRIs High Yield, focada em loteamentos e incorporações, em um ambiente macroeconômico de juros elevados (Selic a 15%).",
    "recomendacoes": "Hold (Manter). Para o portfólio de shopping centers (XPML11), o fluxo de caixa permanece robusto e a vacância é baixa na maioria dos ativos. Porém, considerando a desvalorização contábil dos imóveis e o risco de crédito do portfólio de recebíveis High Yield (ARRI11) misturado na análise do ativo sob este código, o investidor deve adotar uma postura neutra (Hold) para monitorar as taxas de juros e a saúde financeira das devedoras de crédito imobiliário.",
    "alerta": 4,
    "tipo": "Tijolo (Shoppings)"
  },
  "HGRU11": {
    "explicacoes": "Fundo de renda urbana gerido pela Pátria Investimentos (antiga CSHG, mantendo a equipe sob gestão de Bruno Margato). Foco em varejo comercial e educacional com tese de gestão ativa e rotatividade ('wholesale to retail' - compra em atacado e venda fracionada com lucro). Portfólio bem diversificado com prazo médio de contratos de 9,5 anos, sendo mais de 70% contratos atípicos indexados ao IPCA. A distribuição básica de dividendos está estabilizada em R$ 0,90/cota em 2025, com distribuições extraordinárias expressivas ao final de semestres (ex: R$ 1,55 em junho/2025) decorrentes do ganho de capital das vendas de imóveis.",
    "pontos_criticos": "Exposição relevante ao setor educacional (cerca de 32% da receita), que sofre pressão estrutural devido ao avanço do ensino à distância (EAD). Alta concentração de inquilinos em Lojas Pernambucanas (17% da receita, com componente de aluguel variável) e no grupo Yduqs (IBMEC/Estácio). A estratégia de giro constante traz risco de reinvestimento de capital. Houve captação de recursos pela 5ª emissão (R$ 596,7M) que necessitou de alavancagem complementar de R$ 238M para fazer frente a 39 aquisições em 2024, embora a alavancagem geral permaneça sob controle.",
    "recomendacoes": "Recomendação de Compra/Manutenção (Hold/Buy) no cenário macroeconômico atual. O fundo apresenta elevada resiliência em virtude da qualidade de crédito dos ativos, contratos longos e portfólio de imóveis líquidos e bem localizados, além de boa reserva acumulada de lucros para proteger a distribuição recorrente de dividendos de R$ 0,90/cota.",
    "alerta": 2,
    "tipo": "Tijolo (Renda Urbana)"
  },
  "IFRA11": {
    "explicacoes": "Fundo de infraestrutura (FI-Infra) voltado ao investimento em ativos de crédito privado de infraestrutura (debêntures incentivadas), com isenção fiscal para pessoas físicas. O portfólio original do IFRA11 (Itaú Asset) conta com duration de 6,71 anos e yield de IPCA + 5,12% (base jan/2024). Os relatórios contam também com dados do RIFF11 (Paramis Capital, inserido no arquivo de IFRA11_2), fundo de infraestrutura diversificado com 67 emissores (alocação média de 1,2% por ativo) e rendimento médio de IPCA+7,84% no book IPCA e CDI+1,62% no book CDI, apresentando cerca de 72% da carteira com rating AAA nacional.",
    "pontos_criticos": "Forte compressão dos spreads de crédito no mercado geral de debêntures incentivadas ao longo do ano, reduzindo os prêmios sobre as NTN-Bs e limitando a taxa de carregamento de novas aquisições. Há risco de resgate antecipado (prepayment) de dívidas por parte dos emissores que buscam refinanciamento a taxas mais baixas. Há também o risco de oscilação do valor da cota patrimonial frente à marcação a mercado da curva de juros futuros e flutuações da inflação (IPCA).",
    "recomendacoes": "Recomendação de Manutenção (Hold) em virtude da isenção tributária que beneficia o investidor individual e a qualidade de crédito AAA dominante dos emissores. O investidor deve atentar-se a compras com ágios elevados no mercado secundário diante de yields reais que podem estar estreitos comparados às taxas históricas das NTN-Bs.",
    "alerta": 3,
    "tipo": "FI-Infra (Crédito)"
  },
  "KDIF11": {
    "explicacoes": "Kinea Infra (KDIF11) é um fundo de investimento em debêntures incentivadas de infraestrutura gerido pela Kinea Investimentos. Conta com portfólio muito bem diversificado em setores essenciais como saneamento, rodovias, transmissão e geração de energia. Em abril de 2025, contava com R$ 2,5 bilhões de patrimônio líquido, 97% alocado em debêntures, com 67 emissões e 41% da carteira avaliada em rating AAA. O rendimento mensal recorrente em abril de 2025 foi de R$ 1,30/cota (yield médio de IPCA + 9,2% das debêntures e yield de IPCA + 7,86% a mercado).",
    "pontos_criticos": "Alta volatilidade nos dividendos mensais decorrente das flutuações do IPCA corrente, uma vez que o fundo repassa diretamente a inflação dos ativos (como a queda temporária da inflação em abr/2025 que reduziu o dividendo de R$ 1,50 para R$ 1,30). Prêmios de crédito em patamares baixos (compressão de spreads), o que afeta o retorno das novas alocações de capital. Sensibilidade à marcação a mercado devido à duration longa dos ativos (5,6 a 7,1 anos) diante das oscilações da taxa de juro real (NTN-B).",
    "recomendacoes": "Recomendação de Compra/Manutenção (Hold/Buy) para investidores que buscam proteção contra a inflação e rendimento isento de IR. O fundo é muito bem gerido, possui carteira defensiva e baixo risco de crédito. Contudo, recomenda-se cautela com a compra de cotas com ágio expressivo no mercado secundário em relação ao valor patrimonial.",
    "alerta": 2,
    "tipo": "FI-Infra (Crédito)"
  },
  "BRCO11": {
    "explicacoes": "Fundo logístico com portfólio estratégico composto por 12 propriedades (472 mil m² de ABL), com 64% da receita proveniente de ativos last mile e 34% em um raio de 25 km de São Paulo. A gestão é ativa, detém 100% de participação nos ativos e não utiliza Renda Mínima Garantida (RMG). A carteira possui 38% de contratos atípicos e prazo médio remanescente (WAULT) de 4,9 anos, com mais de 82% dos inquilinos com rating investment grade (AAA ou AA). O Dividend Yield anualizado anunciado em jun/25 foi de 11,4% (R$ 1,05/cota, acima do guidance de R$ 0,87/cota). O fundo também conta com receitas não recorrentes da venda do imóvel Bresco São Paulo (48 parcelas de R$ 2,5 milhões corrigidas pelo CDI desde jul/23).",
    "pontos_criticos": "Aumento da vacância física de 0,0% (em jan/25) para 4,5% (em jun/25). Há desocupações programadas relevantes: no ativo Bresco Canoas, a FM Logistic deve desocupar 12.488 m² (2,7% da ABL) em ago/25, somando-se a uma área já vaga de 20.789 m² (4,4% da ABL), o que deixa o ativo com 62% de vacância; no Bresco Embu, a MRO desocupa em jul/25 (3,8% da ABL); e no Bresco Itupeva, a WestRock sairá em abr/26 (3,0% da ABL). A receita imobiliária de jun/25 sofreu impacto negativo por ajuste de pagamento em duplicidade pela WestRock. O caixa diminuiu após quitação de R$ 138,5 milhões pela aquisição de Bresco Osasco e Natura Murici. A alavancagem é muito baixa (LTV de 1,2%), com obrigações de R$ 23,1 milhões securitizadas.",
    "recomendacoes": "Hold/Buy. O portfólio é de altíssima qualidade (padrão A+ em 11 das 12 propriedades) e muito bem localizado. O aumento recente da vacância é um ponto de atenção, mas o fundo possui negociações comerciais ativas e avançadas (como cerca de 50 mil m² em Canoas, equivalente a 1,5x a área vaga e em aviso). A baixíssima alavancagem e inquilinos resilientes recomendam a manutenção do ativo no portfólio no cenário macroeconômico atual.",
    "alerta": 3,
    "tipo": "Tijolo (Logística)"
  },
  "GGRC11": {
    "explicacoes": "Fundo focado em ativos industriais e logísticos sob contratos atípicos (Built to Suit, Sale and Leaseback e Retrofit). Passou por uma reestruturação estratégica que resultou na duplicação da base de cotistas e aumento expressivo de liquidez (volume médio diário de R$ 4,06 milhões em ago/25). Possui 33 ativos (incluindo 2 indiretos via Triple A FII) e ABL de +613 mil m², com WAULT de 5,92 anos. Distribuiu dividendo de R$ 0,10/cota em ago/25 (DY de 1,01% mensal e 12,21% anualizado). Está realizando a 10ª emissão de cotas para financiar a aquisição do ativo VTLT11 em Quatro Barras/PR (Renault, R$ 214 milhões) e ativos da BLMG11 (R$ 125 milhões), consolidando-se entre os maiores do segmento.",
    "pontos_criticos": "Presença de alavancagem com despesas financeiras mensais significativas (R$ 1,54 milhão em ago/25, representando 9,1% da receita total). O resultado de caixa gerado no mês de ago/25 (R$ 12,56 milhões) foi inferior ao total distribuído aos cotistas (R$ 15,25 milhões), demandando a utilização de R$ 2,68 milhões de reservas de caixa acumuladas. O fundo tem contratos com vencimento próximo (como Suzano e Ambev/Pelotas), cuja renovação ou reposicionamento está em negociação.",
    "recomendacoes": "Buy/Hold. A estratégia de expansão por meio da 10ª emissão e aquisições robustas (VTLT11 e BLMG11) deve gerar ganho de escala e diluição de custos. O yield atual é atrativo e os contratos atípicos conferem estabilidade. A alavancagem e a distribuição acima do resultado caixa gerado exigem monitoramento, mas o fundo demonstra forte dinâmica comercial.",
    "alerta": 4,
    "tipo": "Tijolo (Logística/Industrial)"
  },
  "HGLG11": {
    "explicacoes": "Um dos maiores e mais consolidados fundos de logística do mercado, gerido pela Pátria Investimentos (após transição da CSHG). Possui portfólio robusto de 27 imóveis logísticos (ABL superior a 1 milhão de m²), concentrados estrategicamente na região Sudeste (SP, MG, RJ). Para reduzir a volatilidade e estabilizar receitas, o fundo mantém alocação diversificada em CRIs (True, Opea, Virgo, Vert) e FIIs logísticos/industriais (INLG11, FIIB11, XPIN11, BTLG11, etc.). Apresenta forte geração de caixa, com receita financeira/cash trimestral robusta (R$ 116,9 milhões de resultado líquido financeiro contra R$ 106,9 milhões em aluguéis).",
    "pontos_criticos": "O portfólio físico enfrenta taxas de vacância elevadas em ativos específicos, destacando-se o Condomínio SJC (30,02% de vacância) e o HGLG Itupeva G200 (16,16% de vacância). Outros ativos menores também registram vacâncias marginais (Tech Town com 7,90%, DCR Rodoanel com 6,73%, CLE Embu com 6,67% e Torino com 4,95%). A transição de gestão da antiga CSHG para a Pátria Investimentos gera um período de adaptação de equipe e cultura que exige atenção dos cotistas.",
    "recomendacoes": "Buy/Hold. Trata-se de um ativo core e defensivo para qualquer carteira de FIIs logísticos devido à sua liquidez massiva, diversificação de ativos e solidez de caixa. A vacância em SJC e Itupeva representa uma oportunidade de aumento futuro na distribuição de dividendos quando locados. A estrutura de alocação de caixa reduz riscos e mitiga flutuações de mercado.",
    "alerta": 3,
    "tipo": "Tijolo (Logística)"
  }
}

# Create HTML content
html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório Consolidado de Análise de FIIs e Fiagros</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        @page {
            size: A4;
            margin: 15mm;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #1E293B;
            background-color: #FFFFFF;
            line-height: 1.5;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
        }

        .cover-page {
            page-break-after: always;
            padding-bottom: 20px;
        }

        header {
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        .header-title h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: #0F172A;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .header-title p {
            font-size: 13px;
            color: #64748B;
            margin: 3px 0 0 0;
        }

        .header-meta {
            text-align: right;
            font-size: 11px;
            color: #94A3B8;
        }

        /* Executive Summary Styles */
        .exec-summary-title {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            margin-top: 0;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }

        .exec-summary-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 18px;
            background-color: #3B82F6;
            margin-right: 8px;
            border-radius: 2px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 25px;
        }

        .summary-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 15px;
            position: relative;
        }

        .summary-card.alert-high {
            background: #FFF5F5;
            border-color: #FEE2E2;
        }

        .card-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 9999px;
            font-size: 11px;
            text-transform: uppercase;
        }

        .badge-red {
            background-color: #FEE2E2;
            color: #EF4444;
        }

        .badge-orange {
            background-color: #FFEDD5;
            color: #F97316;
        }

        .badge-yellow {
            background-color: #FEF9C3;
            color: #CA8A04;
        }

        .badge-green {
            background-color: #DCFCE7;
            color: #22C55E;
        }

        .summary-card h3 {
            margin: 0 0 5px 0;
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: #0F172A;
        }

        .summary-card .meta {
            font-size: 11px;
            color: #64748B;
            margin-bottom: 10px;
        }

        .summary-card p {
            font-size: 12px;
            margin: 0;
            color: #334155;
            line-height: 1.4;
        }

        /* Table styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 20px;
            font-size: 12px;
        }

        th {
            background-color: #F1F5F9;
            color: #475569;
            font-weight: 600;
            text-align: left;
            padding: 8px 12px;
            border-bottom: 2px solid #E2E8F0;
        }

        td {
            padding: 8px 12px;
            border-bottom: 1px solid #E2E8F0;
        }

        tr:nth-child(even) td {
            background-color: #F8FAFC;
        }

        .alert-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }

        .dot-red { background-color: #EF4444; }
        .dot-orange { background-color: #F97316; }
        .dot-yellow { background-color: #EAB308; }
        .dot-green { background-color: #22C55E; }

        /* Report Pages */
        .report-section {
            page-break-inside: avoid;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            background: #FFFFFF;
        }

        .report-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 12px;
            margin-bottom: 15px;
        }

        .report-title-area {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .report-fii-name {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: #0F172A;
            margin: 0;
        }

        .report-fii-type {
            font-size: 11px;
            background-color: #F1F5F9;
            color: #475569;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 500;
        }

        .report-badges {
            display: flex;
            gap: 8px;
        }

        .section-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .info-block {
            font-size: 12px;
        }

        .info-block-title {
            font-weight: 700;
            font-size: 12px;
            color: #475569;
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .info-block-content {
            color: #334155;
            text-align: justify;
        }

        .critical-block {
            background-color: #FFF5F5;
            border-left: 3px solid #EF4444;
            padding: 10px 12px;
            border-radius: 0 8px 8px 0;
        }

        .critical-block .info-block-title {
            color: #991B1B;
        }

        .critical-block .info-block-content {
            color: #7F1D1D;
        }

        .footer {
            text-align: center;
            font-size: 10px;
            color: #94A3B8;
            margin-top: 30px;
            border-top: 1px solid #E2E8F0;
            padding-top: 10px;
        }
    </style>
</head>
<body>

    <!-- PRIMEIRA PÁGINA (SUMÁRIO EXECUTIVO) -->
    <div class="cover-page">
        <header>
            <div class="header-title">
                <h1>Relatório de Consolidação de FIIs & Fiagros</h1>
                <p>Análise de Risco, Portfólio e Recomendações de Investimento</p>
            </div>
            <div class="header-meta">
                <div>Data: 01 de Junho de 2026</div>
                <div>Elaborado por: Antigravity AI</div>
            </div>
        </header>

        <div class="exec-summary-title">Sumário Executivo e Destaques de Alerta</div>
        
        <div class="summary-grid">
            <div class="summary-card alert-high">
                <span class="card-badge badge-red">Alerta 5/10</span>
                <h3>TVRI11</h3>
                <div class="meta">Tijolo (Renda Urbana)</div>
                <p><strong>Pontos Críticos:</strong> Altíssima concentração de vencimentos de locações em Novembro de 2027 (28,3% da receita). Possui 16% dos imóveis pendentes de regularização de matrículas. Distribuição recente superou a geração recorrente.</p>
            </div>
            
            <div class="summary-card alert-high">
                <span class="card-badge badge-orange">Alerta 4/10</span>
                <h3>LVBI11</h3>
                <div class="meta">Tijolo (Logística)</div>
                <p><strong>Pontos Críticos:</strong> Vacância saltou para 10,7% devido a desocupações e calotes da Sequoia e Supermercados Dia% (em recuperação judicial), impactando R$ 0,17/cota. Utilizou reservas para manter rendimento.</p>
            </div>
            
            <div class="summary-card alert-high">
                <span class="card-badge badge-orange">Alerta 4/10</span>
                <h3>SNAG11</h3>
                <div class="meta">Fiagro (Papel)</div>
                <p><strong>Pontos Críticos:</strong> Concentração de risco extremamente elevada em um único devedor (Boa Safra Sementes com 89% do PL), além de fraqueza generalizada no mercado de crédito agrícola nacional.</p>
            </div>
        </div>

        <div class="exec-summary-title">Tabela Geral de Ativos Monitorados</div>
        <table>
            <thead>
                <tr>
                    <th>Fundo</th>
                    <th>Segmento</th>
                    <th>Nível de Alerta</th>
                    <th>Recomendação</th>
                    <th>Principal Destaque / Direção</th>
                </tr>
            </thead>
            <tbody>
"""

# Sort funds by alert level descending, then alphabetically by ticker
sorted_fiis = sorted(ANALYSES.items(), key=lambda item: (-item[1]['alerta'], item[0]))

for ticker, details in sorted_fiis:
    alert = details['alerta']
    recom = details['recomendacoes'].split('.')[0] # Get first sentence or phrase
    tipo = details['tipo']
    
    if alert >= 5:
        dot_class = "dot-red"
        badge_class = "badge-red"
    elif alert == 4:
        dot_class = "dot-orange"
        badge_class = "badge-orange"
    elif alert == 3:
        dot_class = "dot-yellow"
        badge_class = "badge-yellow"
    else:
        dot_class = "dot-green"
        badge_class = "badge-green"
        
    html_template += f"""
                <tr>
                    <td><strong>{ticker}</strong></td>
                    <td>{tipo}</td>
                    <td><span class="alert-dot {dot_class}"></span> {alert}/10</td>
                    <td><span class="card-badge {badge_class}" style="position:relative; top:0; right:0; display:inline-block; font-size:10px; padding: 1px 6px;">{recom}</span></td>
                    <td>{details['pontos_criticos'][:80]}...</td>
                </tr>
    """

html_template += """
            </tbody>
        </table>
        
        <div style="font-size: 11px; color: #64748B; margin-top: 15px; border-left: 3px solid #3B82F6; padding-left: 10px;">
            <strong>Nota metodológica:</strong> Os dados contidos neste consolidado são oriundos de relatórios gerenciais e fatos relevantes oficiais capturados das páginas de relações com investidores de cada fundo. As avaliações de risco e as recomendações consideram a saúde do portfólio físico, a estrutura de garantias de crédito e o atual cenário macroeconômico brasileiro (Selic a 15%).
        </div>
        
        <div class="footer">Página 1 de 7 | Relatório de Consolidação de FIIs</div>
    </div>
"""

# Now write individual sections, grouping 3 per page to avoid cutting boxes
items_per_page = 3
for index, (ticker, details) in enumerate(sorted_fiis):
    if index % items_per_page == 0:
        html_template += f"""
    <!-- PÁGINA DE ANÁLISE DETALHADA {index // items_per_page + 2} -->
    <div style="page-break-after: always; padding-top: 10px;">
        <header>
            <div class="header-title">
                <h1>Relatório de Consolidação de FIIs & Fiagros</h1>
                <p>Seção de Detalhamento de Ativos ({index + 1} a {min(index + items_per_page, len(sorted_fiis))} de {len(sorted_fiis)})</p>
            </div>
            <div class="header-meta">
                <div>Grau de Alerta Descendente</div>
            </div>
        </header>
        """
        
    alert = details['alerta']
    tipo = details['tipo']
    recom = details['recomendacoes']
    
    if alert >= 5:
        badge_class = "badge-red"
    elif alert == 4:
        badge_class = "badge-orange"
    elif alert == 3:
        badge_class = "badge-yellow"
    else:
        badge_class = "badge-green"
        
    html_template += f"""
        <div class="report-section">
            <div class="report-header">
                <div class="report-title-area">
                    <span class="report-fii-name">{ticker}</span>
                    <span class="report-fii-type">{tipo}</span>
                </div>
                <div class="report-badges">
                    <span class="card-badge {badge_class}" style="position:relative; top:0; right:0; display:inline-block;">Alerta {alert}/10</span>
                </div>
            </div>
            <div class="section-grid">
                <div class="info-block">
                    <div class="info-block-title">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline; margin-right:3px; vertical-align:middle;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                        Tese e Alocação de Ativos
                    </div>
                    <div class="info-block-content">{details['explicacoes']}</div>
                </div>
                
                <div class="info-block critical-block">
                    <div class="info-block-title">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline; margin-right:3px; vertical-align:middle;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                        Pontos Críticos e Fatores de Risco
                    </div>
                    <div class="info-block-content">{details['pontos_criticos']}</div>
                </div>
                
                <div class="info-block">
                    <div class="info-block-title">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline; margin-right:3px; vertical-align:middle;"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
                        Recomendação e Perspectivas de Longo Prazo
                    </div>
                    <div class="info-block-content">{recom}</div>
                </div>
            </div>
        </div>
    """
    
    if (index + 1) % items_per_page == 0 or (index + 1) == len(sorted_fiis):
        page_num = index // items_per_page + 2
        html_template += f"""
        <div class="footer">Página {page_num} de {len(sorted_fiis) // items_per_page + 1} | Relatório de Consolidação de FIIs</div>
    </div>
    """

# Close document html tags
# Note: strip the last page break to prevent an empty extra page
html_template = html_template.replace('style="page-break-after: always; padding-top: 10px;"', 'style="padding-top: 10px;"', 1) # Wait, it is better to just keep them and close body

html_template += """
</body>
</html>
"""

# Write HTML file
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Generated HTML template at {HTML_FILE}")

# Convert to PDF using headless google-chrome
try:
    print(f"Printing HTML to PDF at {PDF_FILE}...")
    chrome_cmd = [
        "/usr/bin/google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={PDF_FILE}",
        f"file://{HTML_FILE}"
    ]
    subprocess.run(chrome_cmd, check=True)
    print(f"Successfully generated consolidated PDF at: {PDF_FILE}")
    # Open PDF automatically on user request
    try:
        subprocess.run(["xdg-open", PDF_FILE], check=True)
        print("Opened PDF automatically on user desktop.")
    except Exception as e:
        print(f"Could not open PDF: {e}")
except Exception as e:
    print(f"Failed to generate PDF via google-chrome: {e}")

