blk = open('ListOfBlackRockXBRLTerms.txt', 'r').read()
pimco = open('ListOfPIMCOXBRLTerms.txt', 'r').read()
schwab = open('ListOfSchwabCoreEquityFundTerms.txt', 'r').read()
ststreet = open('ListOfStateStreetEmergingMarketsFundTerms.txt', 'r').read()

blkterms = blk.split("\n")
pimcoterms = pimco.split("\n")
schwabterms = schwab.split("\n")
ststreet = ststreet.split("\n")


for blkterm in blkterms:
	print blkterm
#	for pimcoterm in pimco:
#		for schwabterm in schwab:
#			for ststreetterm in ststreet: