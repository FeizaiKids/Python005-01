# 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

# 一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
# 第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

# 请合理设计三张表的字段类型和表结构；
# 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
 
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime 
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User_table(Base): 
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True) 
    user_name = Column(String(15), nullable=False)   
    
class Asset_table(Base): 
    __tablename__ = 'asset'
    user_id = Column(Integer(), primary_key=True) 
    user_asset = Column(Float(), nullable=False) 

class Account_table(Base): 
    __tablename__ = 'account' 
    account_id = Column(Integer(), primary_key=True)    
    transfer_time = Column(DateTime(), default=datetime.now)
    transfer_id = Column(Integer()) 
    reciever_id = Column(Integer()) 
    transfer_amount = Column(Float(), nullable=False) 

dburl="mysql+pymysql://root:123456@192.168.199.127:3306/db1?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)

SessionClass = sessionmaker(bind=engine)
session = SessionClass()

user_1 = User_table(user_id="1", user_name='ZhangSan')
user_2 = User_table(user_id="2", user_name='LiSi')

session.add(user_1)
session.add(user_2)
session.commit()

asset_1 = Asset_table(user_id="1", user_asset=110)
asset_2 = Asset_table(user_id="2", user_asset=20)

session.add(asset_1)
session.add(asset_2)
session.commit()


def deal(sender_id, reciever_id, amount, session):
    
    sender_id = session.query(User_table.user_id).filter(User_table.user_id == sender_id).one()[0]
    
    reciever_id = session.query(User_table.user_id).filter(User_table.user_id == reciever_id).one()[0]
    
    sender_asset = session.query(Asset_table.user_asset).filter(Asset_table.user_id==sender_id).one()[0]
    
    reciever_asset = session.query(Asset_table.user_asset).filter(Asset_table.user_id==reciever_id).one()[0]

    session.commit()

    if sender_asset > 100: #100极客币
        try:
            #sender asset -100
            query = session.query(Asset_table)
            query = query.filter(Asset_table.user_id == sender_id)
            moeny_update = query[0].user_asset - 100
            query.update({Asset_table.user_asset: moeny_update})    

            #reciever asset +100
            query = session.query(Asset_table)
            query = query.filter(Asset_table.user_id == reciever_id)
            moeny_update = query[0].user_asset + 100
            query.update({Asset_table.user_asset: moeny_update})
            
            #account table add entry
            account = Account_table(transfer_id= sender_id, reciever_id= reciever_id, transfer_amount= 100)
            session.add(account)
            session.commit()
        except:
            session.rollback()
            
    else:
        print("No sufficient money!")

deal(1,2,100,session)