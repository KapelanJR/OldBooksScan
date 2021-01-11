import enchant

#Download polish dict 
#Windows  https://cgit.freedesktop.org/libreoffice/dictionaries/tree/pl_PL :
#         paste pl_PL.dic and pl_PL.aff to .Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
#Linux sudo apt-get install myspell-pl-pl
d = enchant.Dict("pl_PL")
x = d.suggest("101010")
print(x)