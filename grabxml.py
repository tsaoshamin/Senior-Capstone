from Capstone.database import db_session 
from Capstone.models import Issuer, FormD
import re
import requests
import xmltodict
import dateutil.parser
from datetime import date
from sqlalchemy import desc
from bs4 import BeautifulSoup


def addRSSentry(entry):
	formTitle = entry["title"][0:3]
	if formTitle == 'D -' or formTitle == 'D/A':	
		filingURL = entry["link"]["@href"]
		r2 = requests.get(filingURL)
		soup = BeautifulSoup(filingURL)
		allFilings = soup.find(_class='companyName')
#		if doc["edgarSubmission"]["offeringData"]["typeOfFiling"]["newOrAmendment"]["isAmendment"] == 'true':
#				addAmendedDocuments(allFilings.a['href'])
		form = "http://www.sec.gov" + re.search('<a href="(.*?primary_doc.xml)">primary_doc.xml', r2.text).group(1)
		print form
		r3 = requests.get(form)
		doc = xmltodict.parse(r3.text)				
		i = Issuer()
		i.Name = doc["edgarSubmission"]["primaryIssuer"]["entityName"]
		i.City = doc["edgarSubmission"]["primaryIssuer"]["issuerAddress"]["city"]
		i.Country = doc["edgarSubmission"]["primaryIssuer"]["issuerAddress"]["stateOrCountryDescription"]			
		db_session.add(i)
		db_session.commit()

		j = FormD()
		j.url = form
		j.SubmissionDate = entryUpdatedTime
		j.IndustryGroupType = doc["edgarSubmission"]["offeringData"]["industryGroup"]["industryGroupType"]
		if j.IndustryGroupType == 'Pooled Investment Fund':
			j.InvestmentFundType = doc["edgarSubmission"]["offeringData"]["industryGroup"]["investmentFundInfo"]["investmentFundType"]
		else:
			j.InvestmentFundType = None
		if doc["edgarSubmission"]["offeringData"]["typeOfFiling"]["newOrAmendment"]["isAmendment"] == 'true':
			j.Amended = 1 #1 is true; 0 is false
		else:
			j.Amended = 0
		firstSaleDict = doc["edgarSubmission"]["offeringData"]["typeOfFiling"]["dateOfFirstSale"]
		if firstSaleDict.keys() == ['yetToOccur']:
			j.IsDateOfFirstSaleYetToOccur = 1
		else:
			unformattedDate = firstSaleDict['value']
			year = int(unformattedDate[0:4])
			month = int(unformattedDate[5:7])
			day = int(unformattedDate[8:10])
			j.DateOfFirstSale = date(year, month, day)
		j.MinimumInvestmentAccepted = doc["edgarSubmission"]["offeringData"]["minimumInvestmentAccepted"]
		j.TotalAmountSold = doc["edgarSubmission"]["offeringData"]["offeringSalesAmounts"]["totalAmountSold"] 
		if doc["edgarSubmission"]["offeringData"]["offeringSalesAmounts"]["totalOfferingAmount"] == 'Indefinite':
			j.TotalOfferingAmount = None
			j.IsTotalOfferingAmountIndefinite = 1 
		else:
			j.TotalOfferingAmount = doc["edgarSubmission"]["offeringData"]["offeringSalesAmounts"]["totalOfferingAmount"]
			j.IsTotalOfferingAmountIndefinite = 0
		if doc["edgarSubmission"]["offeringData"]["offeringSalesAmounts"]["totalRemaining"] == 'Indefinite':
			j.TotalRemaining = None
			j.IsTotalRemainingIndefinite = 1
		else:
			j.TotalRemaining = doc["edgarSubmission"]["offeringData"]["offeringSalesAmounts"]["totalRemaining"]
			j.IsTotalRemainingIndefinite = 0
		j.Issuer = i
		db_session.add(j)
		db_session.commit()
		print 'parsing complete, added it to the DB'

# def addAmendedDocuments(CIK):           
# 	d = {'action': 'getcompany', 'CIK': CIK, 'type': 'D', 'dateb': '', 'owner': 'include'}
# 	r4 = requests.get('http://www.sec.gov/cgi-bin/browse-edgar', params=d)
# 	soup = BeautifulSoup(r4.text)
# 	results = soup.body
# 	r = results.contents
# 	print r[0]


#addAmendedDocuments('0001512333')

r = requests.get('http://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=D&company=&dateb=&owner=include&start=0&count=100&output=atom')

rssfeed = xmltodict.parse(r.text)
lastUpdated = db_session.query(FormD).order_by(desc('SubmissionDate')).first()

for entry in rssfeed["feed"]["entry"]:
	entryUpdatedTime = dateutil.parser.parse(entry["updated"], ignoretz=True)
 	if entryUpdatedTime > lastUpdated.SubmissionDate:
		addRSSentry(entry)
	else: 
		break
