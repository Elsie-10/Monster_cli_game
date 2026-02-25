import click
import random
from rich.console import Console
from rich.prompt import Prompt

# Import Database & Models (Crucial: Must import models before create_all)
from Database.database import engine, Session
from models import Base, Player, MonsterSpecies, PlayerMonster
from utils.helpers import print_banner, create_collection_table, MONSTER_ART
from engine.trade_system import propose_trade, complete_trade
from models import Trade

# Import Engine Logic
from engine.monster_system import catch_monster, encounter_wild_monster
from engine.battle_system import execute_battle

console = Console()
session = Session()

def init_db():
    """Ensure tables exist before game starts."""
    Base.metadata.create_all(bind=engine)

@click.group()
def cli():
    """Welcome to the Monster Collector CLI!"""
    pass

@cli.command()
@click.argument('username')
def start(username):
    """Create a new player or login."""
    player = session.query(Player).filter_by(username=username).first()
    if not player:
        player = Player(username=username, currency=100, level=1)
        session.add(player)
        session.commit()
        print_banner(f"Welcome New Trainer: {username}")
    else:
        print_banner(f"Welcome Back: {username}")
    
    console.print(f"Current Level: [bold green]{player.level}[/bold green] | Wallet: [bold yellow]{player.currency}G[/bold yellow]")

@cli.command()
@click.argument('username')
def explore(username):
    """Encounter and attempt to catch wild monsters."""
    player = session.query(Player).filter_by(username=username).first()
    if not player:
        console.print("[red]Please 'start' your profile first![/red]")
        return

    wild_species = encounter_wild_monster(session)
    if not wild_species:
        console.print("[yellow]No monsters found in the tall grass. (Did you run seed.py?)[/yellow]")
        return

    console.print(f"\n[bold]A wild {wild_species.name} appears![/bold]")
    console.print(MONSTER_ART.get(wild_species.element_type, MONSTER_ART["Default"]))
    
    if click.confirm(f"Do you want to try catching this {wild_species.element_type} type?"):
        success = catch_monster(session, player.id, wild_species.id)
        if success:
            console.print(f"[green]Gotcha! {wild_species.name} was caught![/green]")
        else:
            console.print("[red]Oh no! The monster broke free and fled![/red]")

@cli.command()
@click.argument('username')
def collection(username):
    """View your caught monsters in a beautiful table."""
    player = session.query(Player).filter_by(username=username).first()
    if player and player.monsters:
        table = create_collection_table(player.username, player.monsters)
        console.print(table)
    else:
        console.print("[yellow]Your collection is empty. Go explore![/yellow]")

@cli.command()
@click.argument('username')
@click.option('--opponent', default="Wild AI")
def battle(username, opponent):
    """Fight a battle!"""
    player = session.query(Player).filter_by(username=username).first()
    
    if not player or not player.monsters:
        console.print("[red]You need at least one monster to battle![/red]")
        return

    # Let player choose their monster
    monster_names = [m.nickname for m in player.monsters]
    choice = Prompt.ask("Choose your monster", choices=monster_names)
    selected_monster = next(m for m in player.monsters if m.nickname == choice)

    # Simplified Battle Logic: Encounter a random wild monster as an opponent
    wild_opp = encounter_wild_monster(session)
    console.print(f"Battle Commencing: [cyan]{selected_monster.nickname}[/cyan] vs [red]{wild_opp.name}[/red]")
    
    # We pass 'None' or a dummy ID for the AI opponent in this example
    result = execute_battle(session, player.id, 0, selected_monster.id, wild_opp.id)
    
    for line in result['log']:
        console.print(line)
        import time; time.sleep(0.5)

    if result['winner_id'] == player.id:
        console.print(f"[bold green]Victory! Gained {result['xp_reward']} XP.[/bold green]")
    else:
        console.print("[bold red]Defeat... your monster needs rest.[/bold red]")
@cli.command()
@click.argument('your_name')
@click.argument('target_player')
@click.argument('monster_id', type=int)
def send_trade(your_name, target_player, monster_id):
    """Propose a trade to another player."""
    player = session.query(Player).filter_by(username=your_name).first()
    message = propose_trade(session, player.id, target_player, monster_id)
    console.print(f"[bold green]{message}[/bold green]")

@cli.command()
@click.argument('username')
def view_trades(username):
    """See pending trades sent to you."""
    user = session.query(Player).filter_by(username=username).first()
    pending = session.query(Trade).filter_by(receiver_id=user.id, status="Pending").all()
    
    if not pending:
        console.print("No pending trade requests.")
        return

    for t in pending:
        monster = session.query(PlayerMonster).get(t.monster_id)
        console.print(f"ID: {t.id} | From: Player {t.sender_id} | Monster: {monster.nickname} (LVL {monster.level})")
        if click.confirm(f"Accept trade ID {t.id}?"):
            res = complete_trade(session, t.id, accept=True)
            console.print(f"[green]{res}[/green]")
            
if __name__ == "__main__":
    init_db()  # Run this every time to ensure DB is ready
    cli()