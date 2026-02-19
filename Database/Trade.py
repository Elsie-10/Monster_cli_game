class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('players.id'))
    receiver_id = Column(Integer, ForeignKey('players.id'))
    monster_id = Column(Integer, ForeignKey('player_monsters.id'))
    status = Column(String) # e.g., 'Pending', 'Completed'