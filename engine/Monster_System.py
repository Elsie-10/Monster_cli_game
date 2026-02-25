import random
from sqlalchemy.sql import func
from models import Player, MonsterSpecies, PlayerMonster, Achievement, PlayerAchievement

def calculate_catch_rate(species_rarity, player_level):
    """
    rarity: 1 (Common) to 10 (Legendary)
    Calculation: Higher rarity reduces catch chance; Higher player level increases it.
    """
    # Base chance starts at 90% for rarity 1, drops by 8% per rarity level
    base_chance = 90 - (species_rarity * 8)
    # Level bonus: +2% per player level
    level_bonus = player_level * 2
    
    final_chance = base_chance + level_bonus
    return max(5, min(95, final_chance))  # Clamp between 5% and 95%

def encounter_wild_monster(session):
    """Pick a random monster from the species table."""
    return session.query(MonsterSpecies).order_by(func.random()).first()

def catch_monster(session, player_id, species_id):
    """Handles the logic of catching and saving to PlayerMonster table."""
    player = session.query(Player).get(player_id)
    species = session.query(MonsterSpecies).get(species_id)
    
    if not player or not species:
        return False

    chance = calculate_catch_rate(species.rarity, player.level)
    
    if random.randint(1, 100) <= chance:
        new_monster = PlayerMonster(
            player_id=player.id,
            species_id=species.id,
            nickname=species.name,
            level=1,
            current_hp=species.base_hp,
            experience=0
        )
        session.add(new_monster)
        
        # Check for "First Catch" Achievement
        check_and_assign_achievement(session, player_id, "First Discovery")
        
        session.commit()
        return True
    return False

def level_up_monster(session, monster_id):
    """Increases monster level and adjusts stats."""
    monster = session.query(PlayerMonster).get(monster_id)
    if not monster:
        return None

    monster.level += 1
    # Heal monster to full on level up using the base_hp stat from species
    monster.current_hp = monster.species.base_hp + (monster.level * 5)
    
    session.commit()
    return {
        "name": monster.nickname,
        "new_level": monster.level,
        "hp": monster.current_hp
    }

def check_and_assign_achievement(session, player_id, achievement_name):
    """Internal helper to link achievements to players."""
    achievement = session.query(Achievement).filter_by(name=achievement_name).first()
    if not achievement:
        return

    # Check if player already has it
    exists = session.query(PlayerAchievement).filter_by(
        player_id=player_id, 
        achievement_id=achievement.id
    ).first()

    if not exists:
        new_player_ach = PlayerAchievement(
            player_id=player_id,
            achievement_id=achievement.id
        )
        session.add(new_player_ach)