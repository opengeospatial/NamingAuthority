import requests
import csv

csvfile = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/concepts_in_funcs.csv', newline='')
fout = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/outputfuncs.txt','w')


conceptreader = csv.reader(csvfile, delimiter=',', quotechar='|')

for row in conceptreader:
        #print(row[0])
        r = requests.head(row[0])
        #print("CODE1 "+str(r.status_code)+","+row[0])
        if r.status_code == 303:            
            r2 = requests.head(r.headers['Location'])
            #print("CODE2 "+str(r2.status_code)+","+r.headers['Location'])
            if r2.status_code == 200:
                #print("200,"+r.headers['Location'])
                fout.write(str(r2.status_code)+","+(str(r.headers['Location']).replace('&_mediatype=text/turtle','').replace('http://defs.opengis.net/vocprez/object?uri=','')+"\n"))
            else:
                print(str(r2.status_code)+","+r.headers['Location'])
                fout.write(str(r2.status_code)+","+(str(r.headers['Location']).replace('&_mediatype=text/turtle','').replace('http://defs.opengis.net/vocprez/object?uri=','')+"\n"))



csvfile.close()
fout.close()