require 'rubygems' # you need this when xbrlware is installed as gem
require 'edgar'
require 'xbrlware'
require 'open-uri'
require 'nokogiri'
require 'sequel'

DB = Sequel.connect('sqlite://capstone.db') 

instances = {
			"iShares MSCI Brazil Capped Index Fund" => "isi15-20130212.xml"
#			"PIMCO Emerging Markets Full Spectrum Bond Fund" => "pimco-20130129.xml",
#			"Schwab Core Equity Fund" => "sct7-20130226.xml",
#			"Schwab Dividend Equity Fund" => "sct7-20130226.xml",
#			"State Street Emerging Markets Fund" => "ssga4-20121214.xml"
			}

urls = {
		"iShares MSCI Brazil Capped Index Fund" => "http://www.sec.gov/Archives/edgar/data/930667/000119312513084675/0001193125-13-084675-index.htm"
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
# 
for fund in instances.keys
	fund=Xbrlware.ins("forms/#{fund}/#{instances.fetch(fund)}")	
 	doc = Nokogiri::HTML(open("http://www.sec.gov/Archives/edgar/data/930667/000119312513084675/0001193125-13-084675-index.htm"))
	rows = doc.css("div#seriesDiv table").css(".contractRow")
# 	for row in rows
# 		td = row.css('td')
# 		cik = td.css('a').text
# 		ticker = td[3].text
# 		puts cik
# 	end
 	items=fund.item("ManagementFeesOverAssets")
 	items.each do |item|
   		ctx=item.context
   		cik = ctx.id[45..54] # cik
   		for row in rows
   			if row.css("td").css('a').text == cik
				data = row.css("td")
		   		ticker = data[3].text
		   		puts ticker
		   	end
		end
   		puts item.value
	end
end

