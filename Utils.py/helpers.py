from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

# --- ASCII ART & VISUALS ---

MONSTER_ART = {
    "Fire": "🔥 (╯°□°)╯︵ 🔥",
    "Water": "💧 🌊(•_•)🌊 💧",
    "Air": "🌪️ ヽ(°〇°)ﾉ 🌪️",
    "Earth": "🌿 ᕙ(⇀‸↼‶)ᕗ 🌿",
    "Default": "👾 [  ?  ] 👾"
}

def print_banner(title: str):
    """Prints a styled game banner."""
    console.print(Panel(Text(title, justify="center", style="bold magenta"), border_style="bright_blue"))

def display_battle_scene(p1_monster, p2_monster, p1_hp, p2_hp):
    """Creates a split-screen view for the battle."""
    p1_info = f"[bold cyan]{p1_monster.nickname}[/bold cyan]\nHP: {p1_hp}/{p1_monster.species.base_hp}\nType: {p1_monster.species.element_type}"
    p2_info = f"[bold red]Opponent {p2_monster.species.name}[/bold red]\nHP: {p2_hp}/{p2_monster.species.base_hp}\nType: {p2_monster.species.element_type}"
    
    table = Table.grid(expand=True)
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_row(
        Panel(p1_info, title="PLAYER", border_style="cyan"),
        Panel(p2_info, title="OPPONENT", border_style="red")
    )
    console.print(table)

# --- GAME LOGIC HELPERS ---

def get_type_modifier(attacker_type: str, defender_type: str) -> float:
    """
    Returns damage multiplier based on your prompt: 
    Fire > Air > Water > Earth > Fire
    """
    effectiveness = {
        "Fire": {"Air": 2.0, "Water": 0.5},
        "Air": {"Water": 2.0, "Earth": 0.5},
        "Water": {"Earth": 2.0, "Fire": 0.5},
        "Earth": {"Fire": 2.0, "Air": 0.5}
    }
    return effectiveness.get(attacker_type, {}).get(defender_type, 1.0)

def format_currency(amount: int) -> str:
    """Formats the player's currency with a gold color."""
    return f"[bold yellow]{amount}G[/bold yellow]"

# --- DATA FORMATTING ---

def create_collection_table(player_name, monsters):
    """Generates a Rich Table for the player's collection."""
    table = Table(title=f"[bold gold1]{player_name}'s Monster Collection[/bold gold1]", show_header=True, header_style="bold white")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Nickname", style="cyan")
    table.add_column("Species", style="magenta")
    table.add_column("Type", justify="center")
    table.add_column("LVL", justify="right", style="green")
    table.add_column("HP", justify="right", style="red")

    for m in monsters:
        type_icon = MONSTER_ART.get(m.species.element_type, MONSTER_ART["Default"])
        table.add_row(
            str(m.id),
            m.nickname,
            m.species.name,
            type_icon,
            str(m.level),
            f"{m.current_hp}/{m.species.base_hp + (m.level * 5)}"
        )
    return table