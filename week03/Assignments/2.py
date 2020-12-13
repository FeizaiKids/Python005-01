# 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

# 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
# 将 ORM、插入、查询语句作为作业内容提交
 
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime 
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User_table(Base): 
    __tablename__ = 'userTable'
    user_id = Column(Integer(), primary_key=True) 
    user_name = Column(String(15), nullable=False)
    user_age = Column(Integer(), nullable=False)
    user_birthday = Column(DateTime(), nullable=False)
    user_sex = Column(Enum("Male","Female"), nullable=False)
    user_education = Column(String(15), nullable=False)
    created_on = Column(DateTime(), default=datetime.now) 
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "User_table(user_id='{self.user_id}', " \
            "user_name={self.user_name})".format(self=self)

dburl="mysql+pymysql://root:123456@192.168.199.127:3306/db1?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)

SessionClass = sessionmaker(bind=engine)
session = SessionClass()

user_1 = User_table(user_name='Sam', user_age=18, user_birthday='1988-04-02', user_sex="Male", user_education="Master")
user_2 = User_table(user_name='David', user_age=22, user_birthday='1992-10-04', user_sex="Male", user_education="Master")
user_3 = User_table(user_name='Allen', user_age=34, user_birthday='1980-07-12', user_sex="Female", user_education="None")

session.add(user_1)
session.add(user_2)
session.add(user_3)

session.commit()

for result in session.query(User_table.user_name, User_table.user_birthday, User_table.user_sex):
    print(result)