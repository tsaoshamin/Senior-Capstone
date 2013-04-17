require 'rubygems'
require 'sequel'

DB = Sequel.connect('sqlite://capstone.db') 

dataset = DB[:Ticker]

dataset.each do |row|
	id = row[:id]
	name = row[:FullName][0..4]
	if name == 'PIMCO'
		dataset2=dataset.where(:id=>id)
		dataset2.update(:Company=>'PIMCO') 
	elsif name == 'iShar'
		dataset2=dataset.where(:id=>id)
		dataset2.update(:Company=>'BlackRock')
	elsif name == 'Schwa'
		dataset2=dataset.where(:id=>id)
		dataset2.update(:Company=>'Schwab')  
	elsif name == 'Laudu'
		dataset2=dataset.where(:id=>id)
		dataset2.update(:Company=>'Laudus Funds')
	elsif name == 'SSgA '
		dataset2=dataset.where(:id=>id)
		dataset2.update(:Company=>'State Street')	  
	end
end