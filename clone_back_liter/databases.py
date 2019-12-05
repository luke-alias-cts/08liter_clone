from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence

'''
    Author    : DevfbRyu
    Date      : 2019-12-03
    Name      : Django-Sqlalchemy create model
    Useage    : This replace DjangoORM to Sqlalchemy

    Procedure : 1. Use Engine() first for connections
                2. Then Use Base() for Define Mapping
                3. Define your own model using Sqlalchemy
                4. To keep each variables scopes, Use if __name__ == '__main__':

                5. Define Your Class model as variable 
                6. Use Session(Base, engine) in your code, (parameters are return values from Engine(), Base())
                7. Then use sqlalchemy.orm function
                8. For example,  session.add(5) will make you to insert your mysqlDB
'''


def Engine(name):

    '''
    Author : DevfbRyu
    Date   : 2019-12-03
    Usage  : 1. Open this file and rename to this func  ex) mysql+mysqldb://<user>:<password>@<localhost>:<port>:<databaseName>
             2. You must create database in mysql before excuting this func
    '''

    engine = create_engine('mysql+mysqldb://root:1397@127.0.0.1:3306/{}'.format(name), echo = True)
    connection = engine.connect()
    
    return engine

def Base():

    '''
    Author : DevfbRyu
    Date   : 2019-12-03
    Usage  : 1. Base is for declare ORM mapping
             2. Get Base from Base = declarative_base() in sqlalchemy 
             3. Insert Base in Model class parameter
    '''

    Base = declarative_base()
  
    return Base

def Session(Base, engine):

    '''
    Author : DevfbRyu
    Date   : 2019-12-03
    Usage  : 1. Session is logically login to DB after Connection
             2. Before using this func you have to excute Engine,Base func because of dependencies
             3. Input Base(in func Base()) engine (in func Engine(name))
             4. Return values session. For example,  session.add(), session.commit()
    '''

    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

