import argparse
from parser.error_parser import ErrorParser
from search.pageindex_search import PageIndexSearch
from index.build_index import build_index
import os
from llm.explain import LLMExplainer
from search.context_retrieval import ContextRetriever
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.status import Status
from rich.table import Table

console = Console(width=120)

def show_banner():

    title = Text("""
██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗
██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗
██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║
██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝
╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝
""", style="bold cyan")

    info = Text(
        "\nAI Debug Code Search\n"
        "Developer: Rishabh Pandey\n"
        "Version: v1.0\n",
        style="white"
    )

    console.print(
        Panel.fit(
            title + info,
            border_style="cyan",
            title="🚀 AIRROR CLI"
        )
    )

def show_result(result):

    table = Table(show_header=False, box=None)

    table.add_row("📄 File", result.get("file", "Unknown"))
    table.add_row("🔧 Function", result.get("function", "Unknown"))

    console.print(Panel(table, title="Location", border_style="cyan", width=120))

    console.print(
        Panel(
            result.get("explanation", ""),
            title="🧠 Explanation",
            border_style="green",
            width=120
        )
    )

    console.print(
        Panel(
            result.get("suggested_fix", ""),
            title="🛠 Suggested Fix",
            border_style="yellow",
            width=120
        )
    )

def ensure_index(project_path):

    index_dir = os.path.join(project_path, ".debug_index")

    if not os.path.exists(index_dir):

        console.print("\n[bold yellow]⚡ First time setup detected[/bold yellow]")

        with console.status("[bold green]Building project index..."):
            build_index(project_path)

        console.print("[bold green]✅ Index created successfully![/bold green]\n")


def main():
    show_banner()
    parser = argparse.ArgumentParser(description="Debug Code Search")
    context = ContextRetriever()
    llm = LLMExplainer(provider="gemini")

    parser.add_argument(
        "--project",
        default=".",
        help="Path to project"
    )

    parser.add_argument(
        "error",
        nargs="?",
        help="Error message"
    )

    args = parser.parse_args()

    ensure_index(args.project)

    if args.error:
        error_message = args.error
    else:
        error_message = input("Paste error message:\n")

    ep = ErrorParser()

    parsed = ep.parse(error_message)

    query = parsed["query"]

    print("\nGenerated Query:", query)

    snippets = []

    search = PageIndexSearch(args.project)

    if parsed["files"] and parsed["lines"]:

        context_snippet = context.get_context(
            parsed["files"][0],
            parsed["lines"][0]
        )

        if context_snippet:
            snippets.append(context_snippet)

    if not snippets:
        snippets = search.search(query)

    # for r in snippets:

    #     print("\n--- RESULT ---")

    #     print("Function:", r.get("function_name"))
    #     print("File:", r.get("file_path"))
    #     print("Line:", r.get("line_number"))

    #     print("\nCode:\n")
    #     print(r.get("code_snippet"))

    llm_result = llm.explain(error_message, snippets)

    show_result(llm_result)

if __name__ == "__main__":
    main()