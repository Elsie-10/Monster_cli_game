# engine/trade_system.py
from models import Trade, PlayerMonster, Player

def propose_trade(session, sender_id, receiver_username, monster_id):
    """Creates a pending trade record."""
    receiver = session.query(Player).filter_by(username=receiver_username).first()
    if not receiver:
        return "Receiver not found."

    # Check if sender actually owns the monster
    monster = session.query(PlayerMonster).filter_by(id=monster_id, player_id=sender_id).first()
    if not monster:
        return "You do not own this monster."

    new_trade = Trade(
        sender_id=sender_id,
        receiver_id=receiver.id,
        monster_id=monster_id,
        status="Pending"
    )
    session.add(new_trade)
    session.commit()
    return f"Trade proposal sent to {receiver_username}!"

def complete_trade(session, trade_id, accept=True):
    """Executes the transfer of ownership."""
    trade = session.query(Trade).get(trade_id)
    if not trade or trade.status != "Pending":
        return "Invalid or expired trade."

    if accept:
        # Transfer ownership
        monster = session.query(PlayerMonster).get(trade.monster_id)
        monster.player_id = trade.receiver_id
        trade.status = "Completed"
        session.commit()
        return f"Trade complete! {monster.nickname} has a new owner."
    else:
        trade.status = "Rejected"
        session.commit()
        return "Trade rejected."