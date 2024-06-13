from sqlalchemy.orm import sessionmaker
from pkgs.sqlalchemy_db import TEST_Expense, engine

Session = sessionmaker(bind=engine)
session = Session()

expense = TEST_Expense(expense_category="cat", expense_type="type", expense_price=3.01)
session.add(expense)
session.commit()
