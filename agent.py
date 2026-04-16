import sys
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

_DIM   = "\033[2;90m"
_RESET = "\033[0m"

LOGO = r"""
    .----.
   /  __  \      LUPA MUNICIPAL AI
  | / \/ \ |     ══════════════════════════════════════════
  |  \  /  |     Auditoría de ciberseguridad
   \ \ /  /      345 municipios chilenos · Felipe Carvajal Brown Software
    '----'
       \
        \___
             \  ~crack~
              X
"""

HINTS = (
    _DIM
    + "  sugerencias: \"sitios más seguros\"  ·  \"top 10 más vulnerables\"\n"
    + "               \"municipios con MySQL expuesto\"  ·  \"mediana de riesgo\"\n"
    + "               \"cuántos tienen php expuesto\"  ·  \"busca munistgo.cl\""
    + _RESET
)

_in_thinking = False  # track if we opened the thinking block

def callback_handler(**kwargs):
    global _in_thinking

    # tool call starting
    tool = kwargs.get("current_tool_use", {})
    if tool.get("name") and not kwargs.get("data"):
        if not _in_thinking:
            print(f"\n{_DIM}  ┌─ procesando ─────────────────────────{_RESET}")
            _in_thinking = True
        print(f"{_DIM}  │ → {tool['name']}(){_RESET}")

    # streaming tokens from the model
    if "data" in kwargs:
        chunk = kwargs["data"]
        if _in_thinking:
            print(f"{_DIM}  └───────────────────────────────────────{_RESET}\n")
            _in_thinking = False
        print(chunk, end="", flush=True)

    # end of full response
    if kwargs.get("complete"):
        if _in_thinking:
            print(f"{_DIM}  └───────────────────────────────────────{_RESET}\n")
            _in_thinking = False

def main():
    global _in_thinking
    print(LOGO)
    print(HINTS)
    print()

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
            callback_handler=callback_handler,
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

            _in_thinking = False
            agent(route(user_input))
            print("\n")

if __name__ == "__main__":
    main()