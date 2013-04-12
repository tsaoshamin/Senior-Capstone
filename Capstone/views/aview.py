from Capstone import app
from flask import Flask, render_template, request
from Capstone.database import db_session 
from Capstone.models import Issuer, FormD
import datetime 
from datetime import timedelta
import locale

locale.setlocale( locale.LC_ALL, '' )

@app.route('/')
def home():	
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/formd', methods=["POST", "GET"])
def formd():
	dates = {}
	dates["today"] = datetime.datetime.now()
	dates["lastweek"] = datetime.datetime.now() - timedelta(days = 7)
	dates["lastmonth"] = datetime.datetime.now() - timedelta(days = 31)
	if request.method == 'POST':
		date = request.form['date_select'][0:10]
		if request.form['offering_select'] != 'Indefinite':
			(offeringLowerBound, offeringHigherBound) = request.form['offering_select'].split('-')
		amended = request.form['new_amended_select']
		investmentType = request.form['investment_type_select']
		formds = FormD.query.all()
		if request.form['offering_select'] != 'Indefinite':
			if amended == 'new':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
			elif amended == 'amended':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
			else:
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType)
		else:
			if amended == 'new':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
			elif amended == 'amended':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
			else:
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.InvestmentFundType == investmentType)
		for formd in formds:
			if formd.IsTotalOfferingAmountIndefinite == 0:
				formd.TotalOfferingAmount = locale.currency(formd.TotalOfferingAmount, grouping=True)
				formd.TotalRemaining = locale.currency(formd.TotalRemaining, grouping=True)
			formd.TotalAmountSold = locale.currency(formd.TotalAmountSold, grouping=True)
		return render_template('formd.html', dates = dates, formds = formds)
	else:
		return render_template('formd.html', dates = dates)
