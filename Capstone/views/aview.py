from Capstone import app
from functools import wraps
from flask import Flask, render_template, request, Response
from Capstone.database import db_session 
from Capstone.models import Issuer, FormD, Form497, Ticker, Region, Tier
import datetime 
from datetime import timedelta
import locale

locale.setlocale( locale.LC_ALL, '' )

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'blk' and password == 'Blk47rock'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated





@app.route('/')
@requires_auth
def home():	
	return render_template('home.html')

@app.route('/about')
@requires_auth
def about():
	return render_template('about.html')

@app.route('/formd', methods=["POST", "GET"])
@requires_auth
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
		region= request.form['region']
		formds = FormD.query.all()
		if request.form['offering_select'] != 'Indefinite':
			if amended == 'new':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
					FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType,Issuer.RegionID==region)
			elif amended == 'amended':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
					FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType,Issuer.RegionID==region)
			else:
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
				FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
					FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType,Issuer.RegionID==region)
		else:
			if amended == 'new':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0,
					FormD.InvestmentFundType == investmentType, Issuer.RegionID==region)
			elif amended == 'amended':
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1,
					FormD.InvestmentFundType == investmentType, Issuer.RegionID==region)
			else:
				formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.InvestmentFundType == investmentType)
				if region!='ALL':
					formds = db_session.query(FormD).join(Issuer).filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1,
					FormD.InvestmentFundType == investmentType,Issuer.RegionID==region)
		for formd in formds:
			if formd.IsTotalOfferingAmountIndefinite == 0:
				formd.TotalOfferingAmount = locale.currency(formd.TotalOfferingAmount, grouping=True)
				formd.TotalRemaining = locale.currency(formd.TotalRemaining, grouping=True)
			formd.TotalAmountSold = locale.currency(formd.TotalAmountSold, grouping=True)
		return render_template('formd.html', dates = dates, formds = formds)
	else:
		return render_template('formd.html', dates = dates)

@app.route('/form497', methods=["POST", "GET"])
@requires_auth
def form497():
	if request.method == 'POST':
		form497s = Form497.query.all()
		company = request.form['company_select'] 
		print company
		if request.form['mutualfund_select'] == 'all' and company == 'all':
			form497s = Form497.query.all()
		else:
			tickers = Ticker.query.filter(Ticker.Company == company)
			ts=[]
			for ticker in tickers:	
				ts.append(ticker.id)
			form497s = Form497.query.filter(Form497.TickerID.in_(ts))
		for form497 in form497s:
			if form497.ManagementFeesOverAssets is not None:
				form497.ManagementFeesOverAssets = form497.ManagementFeesOverAssets * 100
			if form497.DistributionAndService12b1FeesOverAssets is not None:
				form497.DistributionAndService12b1FeesOverAssets = form497.DistributionAndService12b1FeesOverAssets * 100
			if form497.AcquiredFundFeesAndExpensesOverAssets is not None:
				form497.AcquiredFundFeesAndExpensesOverAssets = form497.AcquiredFundFeesAndExpensesOverAssets * 100
			if form497.ExpensesOverAssets is not None:
				form497.ExpensesOverAssets = form497.ExpensesOverAssets * 100
			if form497.FeeWaiverOrReimbursementOverAssets is not None:
				form497.FeeWaiverOrReimbursementOverAssets = form497.FeeWaiverOrReimbursementOverAssets * 100			
			if form497.AnnualReturn2010 is not None:
				form497.AnnualReturn2010 = form497.AnnualReturn2010 * 100
			if form497.AnnualReturn2011 is not None:
				form497.AnnualReturn2011 = form497.AnnualReturn2011 * 100
		return render_template('form497.html', form497s=form497s)
	else:
		return render_template('form497.html')


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')
