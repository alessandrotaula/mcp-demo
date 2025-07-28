import asyncio
from mcp_use import MCPAgent, MCPClient
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = MCPClient.from_config_file("config.json")
    agent = MCPAgent(
        llm=ChatOpenAI(model="gpt-4o"),
        client=client
    )
    response = await agent.run(
        "Aggiungi una task: 'Scrivere report Cookyx entro venerdì'. Poi mostrami tutte le task esistenti."
    )
    print(response)
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
