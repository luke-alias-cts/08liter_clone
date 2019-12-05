import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from clone_back_liter.databases   import Engine, Base, Session
from sqlalchemy                   import Column, Integer, String, VARCHAR, Boolean, DATETIME

engine = Engine("tests")
Base   = Base()

class User(Base):


    __tablename__ = 'users'

    id                       = Column(Integer, primary_key=True)
    email                    = Column(VARCHAR(50))
    password                 = Column(VARCHAR(300))
    name                     = Column(String(50))
    snsid                    = Column(Integer)
    forReceivingEmail        = Column(VARCHAR(50))
    companyTf                = Column(Boolean)
    influencerTf             = Column(Boolean)
    createdAtYearDate        = Column(DATETIME)


    def __init__(self, email, password, name, snsid, forReceivingEmail, companyTf, influencerTf ,createdAtYearDate):

        self.email              = email
        self.password           = password
        self.name               = name
        self.snsid              = snsid
        self.forReceivingEmail  = forReceivingEmail
        self.companyTf          = companyTf
        self.influencerTf       = influencerTf
        self.createdAtYearDate  = createdAtYearDate

    def __repr__(self):

        return "<User('%s', '%s', '%s','%s', '%s','%s', '%s', '%s')>" % (
            self.email, self.password , self.name , self.snsid ,
            self.forReceivingEmail , self.companyTf , self.influencerTf,
            self.createdAtYearDate )


