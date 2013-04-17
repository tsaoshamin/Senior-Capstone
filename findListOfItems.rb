require 'rubygems' # you need this when xbrlware is installed as gem
require 'edgar'
require 'xbrlware'

instance=Xbrlware.ins('forms/State Street Emerging Markets Fund/ssga4-20121214.xml')

item_all=instance.item_all_map # Fetch all facts as map, key is fact name and value is array of facts
item_all.each do |name, items| # iterate
 puts "#{name}".downcase # Print item name
# items.each do |item|
 #  puts item.value # Print value of each item
 #end
end