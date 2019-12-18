import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from clone_back_liter.databases   import Engine, Base, Session
from sqlalchemy                   import Column, Integer, String, CHAR, VARCHAR, Boolean, DATETIME
from sqlalchemy.orm               import relationship
from sqlalchemy.schema            import ForeignKey

engine = Engine("liter")
Base   = Base()

class User(Base):
    __tablename__ = 'users'
    userid                       = Column(Integer, primary_key=True)
    email                        = Column(VARCHAR(50), nullable=False)
    password                     = Column(VARCHAR(300))
    name                         = Column(CHAR(40))
    snsid                        = Column(VARCHAR(40))
    receivingEmail               = Column(VARCHAR(50))
    userTypeCd                   = Column(VARCHAR(10), nullable=False)
    createdAtDate                = Column(DATETIME, nullable=False)
    userLoginTypeCd              = Column(VARCHAR(10), nullable=False)
    isAgreed                     = Column(Boolean, nullable=False)
   
    def __init__(self, email, password, name, snsid, receivingEmail, userTypeCd, createdAtDate ,userLoginTypeCd, isAgreed):

        self.email               = email
        self.password            = password
        self.name                = name
        self.snsid               = snsid
        self.receivingEmail      = receivingEmail
        self.userTypeCd          = userTypeCd
        self.createdAtDate       = createdAtDate
        self.userLoginTypeCd     = userLoginTypeCd
        self.isAgreed            = isAgreed
   
    def __repr__(self):
        return "<User('%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s')>" % (
            self.email, self.password, self.name, self.snsid,
            self.receivingEmail, self.userTypeCd, self.userLoginTypeCd, 
            self.createdAtDate, self.isAgreed)

class TokenManagement(Base):
    __tablename__  = 'tokenmanagements'

    tokenId        = Column(Integer, primary_key=True)
    userToken      = Column(VARCHAR(200))
    dueDate        = Column(DATETIME)
    userid         = Column(Integer, ForeignKey('users.userid'))
    user           = relationship("User", backref="tokenmanagements")

    def __init__(self, userToken, dueDate):
        
        self.userToken    = userToken
        self.dueDate      = dueDate

    def __repr__(self):
        return "<TokenManagements('%s', '%s')>" % (
            self.userToken, self.dueDate )

class ShopInformationTagCdMapping(Base):
    __tablename__              = 'shopInformationTagCdMappings'
    shopId                     = Column(Integer, ForeignKey('shopinformations.shopId'), primary_key=True)
    tagId                      = Column(Integer, ForeignKey('tags.tagId'), primary_key=True)
    tagMapping                 = relationship("Tag", back_populates="shopinfos")
    shopInformationMapping     = relationship("ShopInformation", back_populates="tags")

    def __init__(self, shopId, tagId):

        self.shopId            = shopId
        self.tagId             = tagId

    def __repr__(self):
        return "<shopInformationTagCdMapping('%s', '%s')>" % (
             self.shopId , self.tagId)


class ShopInformation(Base):
    __tablename__               = 'shopinformations'

    shopId                      = Column(Integer, primary_key=True)
    shopTi                      = Column(VARCHAR(20), nullable=False)
    shopSubTi                   = Column(VARCHAR(45), nullable=False)
    shopTiImg                   = Column(VARCHAR(300), nullable=False)
    userid                      = Column(Integer, ForeignKey('users.userid'), unique = True)
    user                        = relationship("User", backref="shopinformations", uselist=False)
    tags                        = relationship("ShopInformationTagCdMapping", back_populates="shopInformationMapping")

    def __init__(self, shopTi, shopSubTi, shopTiImg, user):
        
        self.shopTi             = shopTi
        self.shopSubTi          = shopSubTi
        self.shopTiImg          = shopTiImg
        self.user               = user

    def __repr__(self):
        return "<ShopInformation('%s', '%s', '%s', '%s')>" % (
            self.shopTi, self.shopSubTi , self.shopTiImg, self.user)

class Tag(Base):
    __tablename__               = 'tags'

    tagId                       = Column(Integer, primary_key=True)
    tagName                     = Column(VARCHAR(45), nullable=False)
    shopinfos                   = relationship("ShopInformationTagCdMapping", back_populates="tagMapping")

    def __init__(self, tagName):
        
        self.tagName            = tagName

    def __repr__(self):
        return "<Tag('%s')>" % (
            self.tagName)


if __name__ == '__main__':
    User.__table__.create(bind=engine)
    ShopInformation.__table__.create(bind=engine)
    Tag.__table__.create(bind=engine)
    ShopInformationTagCdMapping.__table__.create(bind=engine)
    TokenManagement.__table__.create(bind=engine)