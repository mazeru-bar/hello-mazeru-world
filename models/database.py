from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DB.db')
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.models

    Base.metadata.create_all(engine)  # 実際にデータベースを構築します
    SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
    session = SessionMaker()  # 経路を実際に作成しました

    user = session.query(User).get(2) # idが2番目の人を取り出したい
    print(user)
