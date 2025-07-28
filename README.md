# MCP Task Demo

## Avvio
1. Avvia il server MCP:
   ```bash
   cd server
   pip install -r requirements.txt
   uvicorn mcp_server:app --reload --port 8000
   ```

2. Avvia l'agente:
   ```bash
   cd ../agent
   pip install -r requirements.txt
   python agent.py
   ```
