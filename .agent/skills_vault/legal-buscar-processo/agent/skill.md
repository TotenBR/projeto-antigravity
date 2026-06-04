# Skill: Buscar Processo Judicial
Description: Valida número CNJ, pesquisa movimentações no TJMG de 2ª Instância, lida com captchas e busca publicações no DJEN.

## Diretrizes de Busca
1. Valide o dígito verificador CNJ do processo usando a fórmula correspondente (módulo 97).
2. Utilize o Playwright/Puppeteer MCP para acessar o site do tribunal da segunda instância.
3. Se um CAPTCHA for exibido na tela, tire um screenshot e peça para o usuário resolver ou utilize um resolvedor automático.
4. Extraia a folha de rosto do processo, a lista completa de movimentações recentes e as decisões interlocutórias.
5. Busque por referências e publicações associadas a este processo em Diários Oficiais utilizando busca na web ou pdfplumber.
