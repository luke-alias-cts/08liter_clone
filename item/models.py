import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from clone_back_liter.databases   import Engine, Base, Session
from sqlalchemy                   import Column, Integer, String, CHAR, VARCHAR, Boolean, DATETIME, DATE, BIGINT
from sqlalchemy.orm               import relationship
from sqlalchemy.schema            import ForeignKey

engine = Engine("tests")
Base   = Base()

class ItemMaster(Base):
    __tablename__ = 'itemmaster'
    itemId                   = Column(Integer, primary_key=True)
    itemTi                   = Column(VARCHAR(50), nullable=False)
    price                    = Column(BIGINT, nullable=False)
    discount                 = Column(BIGINT, nullable=False)
    createdAtDate            = Column(DATETIME, nullable=False)
    endDate                  = Column(DATETIME, nullable=False)
    vatTypeCd                = Column(VARCHAR(10), nullable=False)
    itemStateCD              = Column(VARCHAR(10), nullable=False)
    itemReceiptCd            = Column(VARCHAR(10), nullable=False)
    itemBizClassCd           = Column(VARCHAR(10), nullable=False)
    ori                      = Column(VARCHAR(45), nullable=False)
    madeInYear               = Column(DATE, nullable=False)
    maIm                     = Column(VARCHAR(45), nullable=False)
    managerTel               = Column(VARCHAR(45), nullable=False)
    cauOfUse                 = Column(VARCHAR(100), nullable=False)
    special                  = Column(VARCHAR(200), nullable=False)
    mat                      = Column(VARCHAR(100), nullable=False)
    col                      = Column(VARCHAR(100), nullable=False)
    sizeVolume               = Column(VARCHAR(100), nullable=False)
    madeIn                   = Column(VARCHAR(100), nullable=False)
    optionDescription        = Column(VARCHAR(150), nullable=False)
    itemImg                  = relationship("ItemImg", uselist=False, backref="itemmaster")
    itemInformationImg       = relationship("ItemInformationImg", uselist=False, backref="itemmaster")

    def __init__(
        self, itemTi, price, discount, createdAtDate, endDate, vatTypeCd, 
        itemTypeCd, itemReceiptCd, itemBizClassCd, ori, madeInYear, maIm,
        managerTel, cauOfUse, special, mat, col, sizeVolume, madeIn, optionDescription):
        self.itemTi  = itemTi
        self.price   = price
        self.discount = discount
        self.createdAtDate = createdAtDate
        self.endDate   = endDate
        self.vatTypeCd = vatTypeCd
        self.itemStateCD = itemStateCD
        self.itemReceiptCd = itemReceiptCd
        self.ori           = ori
        self.madeInYear  = madeInYear
        self.maIm        = maIm
        self.managerTel  = managerTel
        self.cauOfUse    = cauOfUse
        self.special     = special
        self.mat         = mat
        self.col         = col
        self.sizeVolume  = sizeVolume
        self.madeIn      = madeIn
        self.optionDescription = optionDescription

    def __repr__(self):
        return "<ItemMaster('%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s', '%s', '%s','%s', '%s','%s', '%s', '%s','%s', '%s', '%s')>" % (
            self.itemTi, self.price, self.discount, self.createdAtDate, self.endDate, 
            self.vatTypeCd, self.itemStateCD, self.itemReceiptCd, self.ori, self.madeInYear,
            self.maIm, self.managerTel, self.cauOfUse, self.special, self.mat, self.col, 
            self.sizeVolume, self.madeIn, self.optionDescription
            )

class ItemImg(Base):
    __tablename__ = 'itemimgs'
    itemImgId     = Column(Integer, primary_key=True)
    itemImg       = Column(VARCHAR(300), nullable=False)
    itemmaster    = Column(Integer, ForeignKey('itemmaster.itemId'))

    def __init__(self, itemImg):
        self.itemImg  = itemImg

    def __repr__(self):
        return "<ItemImg('%s')>" % (self.itemImgId)

class ItemInformationImg(Base):
    __tablename__ = 'iteminformationimgs'
    itemInformationImgId      = Column(Integer, primary_key=True)
    itemInformationImg        = Column(VARCHAR(300), nullable=False)
    itemmaster                = Column(Integer, ForeignKey('itemmaster.itemId'))

    def __init__(self,  itemInformationImg):
        self. itemInformationImg  =  itemInformationImg

    def __repr__(self):
        return "< ItemInformationImg('%s')>" % (self. itemInformationImg)



if __name__ == '__main__':
    ItemMaster.__table__.create(bind=engine)
    ItemImg.__table__.create(bind=engine)
    ItemInformationImg.__table__.create(bind=engine)
