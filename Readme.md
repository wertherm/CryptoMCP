# MCP que compra criptomoedas conforme análise das bandas de bollinger

### Funções
- `get_crypto`: Obtém os preços de fechamento da criptomoeda.
- `analyze_bollinger`: Calcula as Bandas de Bollinger e determina se o preço está no topo, fundo ou neutro.
- `buy`: Realiza a compra da criptomoeda se houver um sinal de fundo.
- `mcp_decision`: Aplica a lógica do Model Context Protocol (MCP) para tomar a decisão de compra.