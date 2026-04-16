from pathlib import Path
from strands import Agent
from strands.session import FileSessionManager
from core.model import get_model
from core.mcp import get_mcp_client
from core.router import route
from tools import ALL_TOOLS

SYSTEM_PROMPT = Path("prompts/system.md").read_text(encoding="utf-8")
SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)

LOGO = r"""
 _     _   _ ____   _      __  __ _   _ _   _ ___ ____ ___ ____   _    _     
| |   | | | |  _ \ / \    |  \/  | | | | \ | |_ _/ ___|_ _|  _ \ / \  | |    
| |   | | | | |_) / _ \   | |\/| | | | |  \| || | |    | || |_) / _ \ | |    
| |___| |_| |  __/ ___ \  | |  | | |_| | |\  || | |___ | ||  __/ ___ \| |___ 
|_____|\___/|_| /_/   \_\ |_|  |_|\___/|_| \_|___\____|___|_| /_/   \_\_____|
"""

def main():
    print(LOGO)
    print("Auditoría de ciberseguridad — 345 municipios chilenos\n")

    session_manager = FileSessionManager(
        session_id="lupa-municipal-session",
        storage_dir=str(SESSION_DIR),
    )
    with get_mcp_client() as mcp:
        mcp_tools = mcp.list_tools_sync()
        agent = Agent(
            model=get_model(),
            tools=ALL_TOOLS + mcp_tools,
            system_prompt=SYSTEM_PROMPT,
            session_manager=session_manager,
            name="lupa-agent",
            )

        print("¿Qué quieres saber sobre ciberseguridad municipal en Chile?")
        print("(escribe 'salir' para terminar)\n")

        while True:
            try:
                user_input = input(">> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nHasta luego.")
                break

            if not user_input:
                continue
            if user_input.lower() in ("salir", "exit", "quit"):
                print("Hasta luego.")
                break

            agent(route(user_input))
            print()

if __name__ == "__main__":
    main()