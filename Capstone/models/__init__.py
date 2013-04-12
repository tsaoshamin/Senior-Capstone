from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from Capstone.database import Base


class Issuer(Base):
    __tablename__ = 'Issuers'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))
    City = Column(String(50))
    Country = Column(String(50))
    FormD = relationship("FormD", backref="Issuer")
    #more

class FormD(Base):
    __tablename__ = 'FormD'
    id = Column(Integer, primary_key=True)
    IssuerID = Column(Integer, ForeignKey('Issuers.id'))
    url = Column(String(100))
    SubmissionDate = Column(DateTime)
    IndustryGroupType = Column(String(50))
    InvestmentFundType = Column(String(50))
    Amended = Column(Boolean)
    DateOfFirstSale = Column(Date)
    IsDateOfFirstSaleYetToOccur = Column(Boolean)
    MinimumInvestmentAccepted = Column(Integer)
    TotalOfferingAmount = Column(Integer)
    IsTotalOfferingAmountIndefinite = Column(Boolean)
    TotalAmountSold = Column(Integer)
    TotalRemaining = Column(Integer)
    IsTotalRemainingIndefinite = Column(Boolean)


