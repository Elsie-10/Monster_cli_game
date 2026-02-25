import random
from datetime import datetime
from models import Battle, PlayerMonster, Player

# Type Advantage System (Fire > Air > Water > Earth > Fire)
# Based on your prompt's specific logic: Fire > Air > Water > Earth
TYPE_CHART = {
    "Fire": {"Air": 2.0, "Water": 0.5},
    "Air": {"Water": 2.0, "Earth": 0.5},
    "Water": {"Earth": 2.0, "Fire": 0.5},
    "Earth": {"Fire": 2.0, "Air": 0.5}
}

def calculate_damage(attacker_pm, defender_pm):
    """
    Uses the base stats from the Species relationship.
    Formula: ((Atk * Level) - (Def * Level/2)) * TypeModifier
    """
    atk_stat = attacker_pm.species.base_attack + (attacker_pm.level * 2)
    def_stat = defender_pm.species.base_defense + (defender_pm.level * 1.5)
    
    # Calculate Type Modifier
    atk_type = attacker_pm.species.element_type
    def_type = defender_pm.species.element_type
    modifier = TYPE_CHART.get(atk_type, {}).get(def_type, 1.0)
    
    damage = max(5, (atk_stat - (def_stat / 2))) * modifier
    return int(damage)

def execute_battle(session, player_id, opponent_id, player_monster_id, opponent_monster_id):
    """
    Runs a full turn-based loop and saves the result to the Battles table.
    """
    p_monster = session.query(PlayerMonster).get(player_monster_id)
    o_monster = session.query(PlayerMonster).get(opponent_monster_id)
    
    # Track initial HP for the battle log
    p_hp = p_monster.current_hp
    o_hp = o_monster.current_hp
    
    battle_log = []
    
    while p_hp > 0 and o_hp > 0:
        # Player Turn
        dmg = calculate_damage(p_monster, o_monster)
        o_hp -= dmg
        battle_log.append(f"{p_monster.nickname} dealt {dmg} damage!")
        
        if o_hp <= 0: break
            
        # Opponent Turn
        dmg = calculate_damage(o_monster, p_monster)
        p_hp -= dmg
        battle_log.append(f"Opponent dealt {dmg} damage!")

    # Determine Winner
    winner_id = player_id if o_hp <= 0 else opponent_id
    xp_reward = 20 if winner_id == player_id else 5
    
    # Update Player and Monster Progress
    if winner_id == player_id:
        p_monster.experience += xp_reward
        # Potential level up logic call here
        
    # Record in the Battles Table (Matches your model.py)
    new_battle = Battle(
        player_id=player_id,
        opponent_id=opponent_id,
        winner_id=winner_id,
        battle_date=datetime.utcnow(),
        xp_gained=xp_reward
    )
    
    session.add(new_battle)
    session.commit()
    
    return {
        "winner_id": winner_id,
        "log": battle_log,
        "xp_reward": xp_reward
    }

def create_ai_opponent(session, difficulty_level):
    """
    Generates a temporary 'Wild' or 'NPC' opponent.
    Returns a dictionary of stats since AI doesn't always need a Player record.
    """
    # Logic to fetch a random monster and scale it to difficulty_level
    pass