blk = open('ListOfBlackRockXBRLTerms.txt', 'w').read()
pimco = open('ListOfPIMCOXBRLTerms.txt', 'w').read()
schwab = open('ListOfSchwabCoreEquityFundTerms.txt', 'w').read()
ststreet = open('ListOfStateStreetEmergingMarketsFundTerms.txt', 'w').read()

blkterms = blk.split("\n")
pimcoterms = pimco.split("\n")
schwabterms = schwab.split("\n")
ststreet = ststreet.split("\n")

requiredterms = [
"Amendment Flag",
"Annual Fund Operating Expenses Table Text Block",
"Bar Chart And Performance Table Heading",
"Distribution And Service 12b1 Fees Over Assets",
"Document Creation Date",
"Document Effective Date",
"Document Period End Date",
"Document Type",
"Expense Example Narrative Text Block",
"Expense Example With Redemption Table Text Block",
"Expense Example Year 01",
"Expense Example Year 03",
"Expense Heading",
"Expense Narrative Text Block",
"Expenses Over Assets",
"Management Fees Over Assets",
"Objective Heading",
"Objective Primary Text Block",
"Operating Expenses Caption",
"Other Expenses Over Assets",
"Performance Availability Website Address",
"Performance Narrative Text Block",
"Portfolio Turnover Heading",
"Portfolio Turnover Text Block",
"Prospectus Date",
"Risk Heading",
"Risk Lose Money",
"Risk Narrative Text Block",
"Strategy Heading"
]


for blkterm in blkterms:
	if blkterm in requiredterms:
		blkterm = blkterm
		
print blkterms
#	for pimcoterm in pimco:
#		for schwabterm in schwab:
#			for ststreetterm in ststreet: