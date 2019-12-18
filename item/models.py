import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from clone_back_liter.databases   import Engine, Base, Session
from sqlalchemy                   import Column, Integer, String, CHAR, VARCHAR, Boolean, DATETIME, DATE, BIGINT
from sqlalchemy.orm               import relationship, backref
from sqlalchemy.schema            import ForeignKey
from user.models                  import ShopInformation

engine = Engine("liter")
Base   = Base()

class ItemMaster(Base):
    __tablename__            = 'itemmaster'
    __table_args__           = { 'extend_existing' : True }

    itemId                   = Column(Integer, primary_key=True)
    itemTi                   = Column(VARCHAR(50), nullable=False)
    price                    = Column(BIGINT, nullable=False)
    discount                 = Column(BIGINT, nullable=False)
    createdAtDate            = Column(DATETIME, nullable=False)
    endDate                  = Column(DATETIME, nullable=False)
    vatTypeCd                = Column(VARCHAR(10), nullable=False)
    itemStateCd              = Column(VARCHAR(10), nullable=False)
    itemReceiptCd            = Column(VARCHAR(10), nullable=False)
    itemBizClassCd           = Column(VARCHAR(10), nullable=False)
    ori                      = Column(VARCHAR(45), nullable=False)
    madeInYear               = Column(VARCHAR(45), nullable=False)
    maIm                     = Column(VARCHAR(45), nullable=False)
    managerTel               = Column(VARCHAR(45), nullable=False)
    cauOfUse                 = Column(VARCHAR(100), nullable=False)
    qa                       = Column(VARCHAR(100), nullable=False)
    special                  = Column(VARCHAR(200), nullable=False)
    mat                      = Column(VARCHAR(100), nullable=False)
    sizeVolume               = Column(VARCHAR(100), nullable=False)
    madeIn                   = Column(VARCHAR(100), nullable=False)
    expiryDate               = Column(VARCHAR(100), nullable=False)
    optionDescription        = Column(VARCHAR(150), nullable=False)
    itemImg                  = relationship("ItemImg", backref="itemmaster")
    itemInformationImg       = relationship("ItemInformationImg", backref="itemmaster")
    shopinformation          = relationship("ShopInformationItemMapping")
    itemOption               = relationship("ItemOption", backref="itemmaster")

    def __init__(
        self,             itemTi,        price,          discount, createdAtDate,  endDate,   vatTypeCd, 
        itemStateCd,      itemReceiptCd, itemBizClassCd, ori,      madeInYear,     maIm,      managerTel, 
        cauOfUse,         qa,            special,        mat,      sizeVolume,     madeIn,    optionDescription
        ):
        self.itemTi            = itemTi
        self.price             = price
        self.discount          = discount
        self.createdAtDate     = createdAtDate
        self.endDate           = endDate
        self.vatTypeCd         = vatTypeCd
        self.itemStateCd       = itemStateCd
        self.itemReceiptCd     = itemReceiptCd
        self.ori               = ori
        self.madeInYear        = madeInYear
        self.maIm              = maIm
        self.managerTel        = managerTel
        self.cauOfUse          = cauOfUse
        self.qa                = qa
        self.special           = special
        self.mat               = mat
        self.sizeVolume        = sizeVolume
        self.madeIn            = madeIn
        self.optionDescription = optionDescription

    def __repr__(self):
        return "<ItemMaster('%s', '%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s','%s', '%s','%s', '%s', '%s','%s', '%s' )>" % (
            self.itemTi,     self.price,       self.discount,          self.createdAtDate,     self.endDate, 
            self.vatTypeCd,  self.itemStateCd, self.itemReceiptCd,     self.ori,               self.madeInYear,
            self.maIm,       self.managerTel,  self.cauOfUse,          self.special,           self.mat, 
            self.sizeVolume,  self.madeIn,     self.optionDescription, self.qa
            )

class ItemImg(Base):
    __tablename__ = 'itemimgs'

    itemImgId     = Column(Integer, primary_key=True)
    itemImg       = Column(VARCHAR(300), nullable=False)
    itemMasterId  = Column(Integer, ForeignKey('itemmaster.itemId'))

    def __init__(self, itemImg):
        self.itemImg  = itemImg

    def __repr__(self):
        return "<ItemImg('%s')>" % (self.itemImgId)

class ItemInformationImg(Base):
    __tablename__             = 'iteminformationimgs'

    itemInformationImgId      = Column(Integer, primary_key=True)
    itemInformationImg        = Column(VARCHAR(300), nullable=False)
    itemMasterId              = Column(Integer, ForeignKey('itemmaster.itemId'))

    def __init__(self,  itemInformationImg):
        self.itemInformationImg  =  itemInformationImg

    def __repr__(self):
        return "< ItemInformationImg('%s')>" % (self.itemInformationImg)

class ItemOption(Base):
    __tablename__    = 'itemoptions'

    itemOptionId     = Column(Integer, primary_key=True)
    optionName       = Column(VARCHAR(50), nullable=False)
    targetQuantity   = Column(Integer, nullable=False)
    salesOfItem      = Column(Integer, nullable=False)
    stock            = Column(Integer, nullable=False)
    optionPrice      = Column(BIGINT, nullable=False)
    itemMasterId     = Column(Integer, ForeignKey('itemmaster.itemId'))
    itemMaster       = relationship("ItemMaster", backref="itemoptions")

    def __init__(self,  optionName, targetQuantity, salesOfItem, stock, optionPrice):
        self.optionName      = optionName
        self.targetQuantity  = targetQuantity
        self.salesOfItem     = salesOfItem
        self.stock           = stock
        self.optionPrice     = optionPrice

    def __repr__(self):
        return "< ItemOption('%s','%s','%s','%s','%s')>" % (
            self.optionName,
            self.targetQuantity,
            self.salesOfItem,
            self.stock,
            self.optionPrice,
        )

# join table(N:M)
class ShopInformationItemMapping(Base):
    __tablename__     = 'shopinformationitemmapping'
    __table_args__    = { 'extend_existing' : True }

    shopId            = Column(Integer, ForeignKey(ShopInformation.shopId), primary_key=True)
    itemId            = Column(Integer, ForeignKey('itemmaster.itemId'), primary_key=True)
    shopInformation   = relationship(ShopInformation)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
