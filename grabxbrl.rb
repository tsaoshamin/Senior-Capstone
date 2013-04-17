require 'rubygems' # you need this when xbrlware is installed as gem
require 'edgar'
require 'xbrlware'
require 'open-uri'
require 'nokogiri'
require 'sequel'

DB = Sequel.connect('sqlite://capstone.db') 

instances = {
			"iShares MSCI Brazil Capped Index Fund" => "isi15-20130212.xml",
			"PIMCO Emerging Markets Full Spectrum Bond Fund" => "pimco-20130129.xml",
			"Schwab Core Equity Fund" => "sct7-20130226.xml",
#			"Schwab Dividend Equity Fund" => "sct7-20130226.xml",
			"State Street Emerging Markets Fund" => "ssga4-20121214.xml"
			}

urls = {
		"iShares MSCI Brazil Capped Index Fund" => "http://www.sec.gov/Archives/edgar/data/930667/000119312513084675/0001193125-13-084675-index.htm",
	  	"PIMCO Emerging Markets Full Spectrum Bond Fund" => "http://www.sec.gov/Archives/edgar/data/810893/000113322813000474/0001133228-13-000474-index.htm",
	  	"Schwab Core Equity Fund" => "http://www.sec.gov/Archives/edgar/data/904333/000119312513107097/0001193125-13-107097-index.htm",
#	  	"Schwab Dividend Equity Fund" =>"http://www.sec.gov/Archives/edgar/data/904333/000119312513107097/0001193125-13-107097-index.htm",
	  	"State Street Emerging Markets Fund" => "http://www.sec.gov/Archives/edgar/data/826686/000119312513005324/0001193125-13-005324-index.htm"
	   }

def downloadMutualFund(url, name)
	dl=Edgar::HTMLFeedDownloader.new()
	download_dir='forms/' + name
	dl.download(url, download_dir)

end

# downloadMutualFund("http://www.sec.gov/Archives/edgar/data/810893/000113322813000474/0001133228-13-000474-index.htm", "PIMCO Emerging Markets Full Spectrum Bond Fund")

# def showInfo(download_dir)
# 	instance_file=Xbrlware.file_grep(download_dir)["ins"] # use file_grep to filter xbrl files and get instance file


# iSharesBrazil=Xbrlware.ins("000119312513084675/isi15-20130212.xml")
# FidelitySmallCapDiscoveryFund=Xbrlware.ins("000031570012000017/fct-20120628.xml")
# SchwabCoreEquityFund = Xbrlware.ins("000119312513107097/sct7-20130226.xml")

for fund in instances.keys
	ins=Xbrlware.ins("forms/#{fund}/#{instances.fetch(fund)}")
 	filing=urls.fetch(fund)
 	doc = Nokogiri::HTML(open(filing))
	rows = doc.css("div#seriesDiv table").css(".contractRow")
	subDate = doc.css("div.formContent").css(".formGrouping")[0].css(".info")[0]	
	data=[ManagementFeesOverAssets, DistributionAndService12b1FeesOverAssets, AcquiredFundFeesAndExpensesOverAssets, ExpensesOverAssets, AnnualReturn2010, AnnualReturn2011, FeeWaiverOrReimbursementOverAssets]
#   data=[ManagementFeesOverAssets]
 	data.each do |val|
 		val.each do |item| 
			ctx=item.context
			cik = 0
			ticker = 'ZZZ'
			classType = 'Class X'
			if fund == 'State Street Emerging Markets Fund' or fund == 'iShares MSCI Brazil Capped Index Fund' or fund == 'Schwab Core Equity Fund' or fund == 'Schwab Dividend Equity Fund' 
				cik = ctx.id[45..54]
			elsif fund == 'PIMCO Emerging Markets Full Spectrum Bond Fund'
				cik = ctx.id[13..22]
			else
				puts "no cik found!"
			end
			i = 0
			while rows[i].css("td").css("a").text != cik and i < rows.size
				i+=1
			end
			row = rows[i].css("td")
			ticker = row[3].text
			classType = row[2].text
   			dataset = DB[:Form497]
   			tickerID = DB.fetch("SELECT id FROM Ticker WHERE Name = ? AND Class = ?", ticker, classType)
#	   		dataset.insert(:SubmissionDate=>subDate.text, :url=>filing, :TickerID=>tickerID)
			DB.transaction do
# 				DB[:Ticker].insert(:Name=>ticker, :Class=>classType)
				dataset=dataset.where(:TickerID=>tickerID)
				dataset.update(item.name=>item.value)
			end
	   		#puts "#{ticker}, #{classType} ; #{item.name}: #{item.value}"
		end
	end
end

