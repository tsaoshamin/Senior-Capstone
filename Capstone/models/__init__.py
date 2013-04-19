from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Date, Float
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
    RegionID = Column(Integer, ForeignKey("Region.id"))
    TierID = Column(Integer, ForeignKey("Tier.id"))
    #more

class Region(Base):
	__tablename__ = 'Region'
	id = Column(Integer, primary_key=True)
	GeographicName = Column(String(50))

class Tier(Base):
	__tablename__ = 'Tier'
	id = Column(Integer, primary_key=True)
	TierName = Column(String(50))
	
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

class Ticker(Base):
	__tablename__ = 'Ticker'
	id = Column(Integer, primary_key=True)
	Name = Column(String(50))
	Class = Column(String(50))
	FullName = Column(String(50))
	Company = Column(String(50))
	Form497 = relationship("Form497", backref="Ticker")

class Form497(Base):
	__tablename__ = 'Form497'
	id = Column(Integer, primary_key=True)
	TickerID = Column(Integer, ForeignKey('Ticker.id'))
	url = Column(String(100))
	SubmissionDate = Column(Date)
	ManagementFeesOverAssets = Column(Float)
	DistributionAndService12b1FeesOverAssets = Column(Float)
	AcquiredFundFeesAndExpensesOverAssets = Column(Float) 
	ExpensesOverAssets = Column(Float) 
	AnnualReturn2010 = Column(Float)
	AnnualReturn2011 = Column(Float)
	FeeWaiverOrReimbursementOverAssets = Column(Float)

