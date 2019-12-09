import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from clone_back_liter.databases   import Engine, Base, Session
from sqlalchemy                   import Column, Integer, String, CHAR, VARCHAR, Boolean, DATETIME
from sqlalchemy.orm               import relationship
from sqlalchemy.schema            import ForeignKey

engine = Engine("tests")
Base   = Base()

class User(Base):
    __tablename__ = 'users'
    userid                   = Column(Integer, primary_key=True)
    email                    = Column(VARCHAR(50), nullable=False)
    password                 = Column(VARCHAR(300))
    name                     = Column(CHAR(40))
    snsid                    = Column(Integer)
    receivingEmail           = Column(VARCHAR(50))
    userTypeCd               = Column(VARCHAR(10), nullable=False)
    createdAtDate            = Column(DATETIME, nullable=False)
    userLoginTypeCd          = Column(VARCHAR(10), nullable=False)
    isAgreed                 = Column(Boolean, nullable=False)
    shopinformation          = relationship("ShopInformation", uselist=False, backref="users")
   
    def __init__(self, email, password, name, snsid, receivingEmail, userTypeCd, createdAtDate ,userLoginTypeCd, isAgreed):
        self.email              = email
        self.password           = password
        self.name               = name
        self.snsid              = snsid
        self.receivingEmail     = receivingEmail
        self.userTypeCd         = userTypeCd
        self.createdAtDate      = createdAtDate
        self.userLoginTypeCd    = userLoginTypeCd
        self.isAgreed           = isAgreed
   
    def __repr__(self):
        return "<User('%s', '%s', '%s','%s', '%s','%s', '%s', '%s')>" % (
            self.email, self.password, self.name, self.snsid,
            self.receivingEmail, self.userTypeCd, self.createdAtDate,
            self.userLoginTypeCd, self.isAgreed)



class ShopInformation(Base):
    __tablename__ = 'shopinformation'

    shopInformationId  = Column(Integer, primary_key=True)
    shopTi             = Column(VARCHAR(20), nullable=False)
    shopSubTi          = Column(VARCHAR(45), nullable=False)
    shopTiImg          = Column(VARCHAR(300), nullable=False)
    user               = Column(Integer, ForeignKey('users.userid'))

    def __init__(self, shopTi, shopSubTi, shopTiImg):
        
        self.shopTi    = shopTi
        self.shopSubTi = shopSubTi
        self.shopTiImg = shopTiImg

    def __repr__(self):
        return "<ShopInformation('%s', '%s', '%s')>" % (
            self.shopTi, self.shopSubTi , self.shopTiImg )



if __name__ == '__main__':
    User.__table__.create(bind=engine)
    ShopInformation.__table__.create(bind=engine)