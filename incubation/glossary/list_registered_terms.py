live_register_path = '/Users/gobehobona/Documents/GitHub/NamingAuthority/definitions/conceptschemes/ogc_glossary.ttl'

fin = open(live_register_path,'r')
fout = open('terms.txt','w')

lines = fin.readlines()

for line in lines:
    if line.startswith("<http://www.opengis.net/def/glossary/term"):
        print(line)
        fout.write(line.replace("<http://www.opengis.net/def/glossary/term/","").replace(">",""))

fin.close()
fout.close()