## Setting up the project
 1 . Install python and pipenv
 2 . Create a virtual environment.
 """
 python -m venv venv
 source venv/bin/activate
 """"
 3 . Install SQLAlchemy
 """
 pip install sqlalchemy alembic python-dotenv rich

 pip install --dev ipython
 """
 """Run python seed.py to start fresh.

Test Catching: python main.py explore Trainer1.

Test Trading:

python main.py start Trainer1

python main.py start Trainer2

Trainer 1 catches a monster.

python main.py send_trade Trainer1 Trainer2 [ID]

python main.py view_trades Trainer2 """