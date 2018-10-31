from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:Nomelose123@87.4.5.139:3306/faveolivetest')
Session = sessionmaker(bind=engine)

Base = declarative_base()