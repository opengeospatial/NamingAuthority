import requests


f = open('/Users/gobehobona/Downloads/queryResults_v3.csv')
fout = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/alllines.txt','w')


lines = f.readlines()

for line in lines:
    r = requests.head(line.replace("\n",""))
    #print(str(r.status_code)+" "+line.replace("\n",""))
    if r.status_code == 303:
        r2 = requests.head(r.headers['Location'])
        if r2.status_code == 400:
            print("400,"+r.headers['Location'])
            fout.write(str(r.headers['Location']).replace('&_mediatype=text/turtle','').replace('http://defs.opengis.net/vocprez/object?uri=','')+"\n")

f.close()
fout.close()