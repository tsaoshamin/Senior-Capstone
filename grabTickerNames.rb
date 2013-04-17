require 'rubygems' # you need this when xbrlware is installed as gem
require 'open-uri'
require 'nokogiri'
require 'sequel'

DB = Sequel.connect('sqlite://capstone.db') 

dataset = DB[:Ticker]

dataset.each do |row|
	if row[:Name] != ''
		url = "http://www.bloomberg.com/quote/" + row[:Name] + ":US"
		puts url 
		doc = Nokogiri::HTML(open(url))
		fullName = doc.css("div.ticker_header_top").css("h2")
		puts fullName.text
		dataset2=dataset.where(:Name=>row[:Name])
		dataset2.update(:FullName=>fullName.text)
	end
end
	
#doc = Nokogiri::HTML(open(filing))
