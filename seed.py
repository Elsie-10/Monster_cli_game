from database import Session, init_db
from models import MonsterSpecies, Achievement

def seed_data():
    init_db()
    session = Session()
    
    # 1. Add some species
    species_list = [
        MonsterSpecies(name="Cinderkit", element_type="Fire", base_hp=50, base_attack=15, base_defense=10, rarity=2),
        MonsterSpecies(name="Aquapup", element_type="Water", base_hp=60, base_attack=12, base_defense=15, rarity=2),
        MonsterSpecies(name="Terratort", element_type="Earth", base_hp=80, base_attack=10, base_defense=25, rarity=4),
        MonsterSpecies(name="Zaptalon", element_type="Air", base_hp=45, base_attack=20, base_defense=8, rarity=7),
        MonsterSpecies(name="Voidghoul", element_type="Ghost", base_hp=100, base_attack=30, base_defense=30, rarity=10)
    ]
    
    # 2. Add some achievements
    achievements = [
        Achievement(name="First Discovery", description="Catch your first monster", requirement_val=1),
        Achievement(name="Veteran Trainer", description="Reach Player Level 10", requirement_val=10)
    ]

    session.add_all(species_list)
    session.add_all(achievements)
    session.commit()
    print("Database seeded!")

if __name__ == "__main__":
    seed_data()