from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import json
with open("geolexica.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')


for term in soup.find_all('tr'):
    filename = ''
    label = ''
    termid_number = ''
    for termid in term.find_all('td', {'class' : 'field-termid'}):
        for a_termid in termid.find_all('a'):
            filename = a_termid.get_text()
            termid_number = a_termid.get_text()

    for term_label in term.find_all('td', {'class' : 'field-term'}):
        for a_term_label in term_label.find_all('a'):
            label = a_term_label.get_text().strip()
            filename = filename +'_'+ a_term_label.get_text().strip().replace(' ','_')
    if len(filename) > 0:

        path, headers = urlretrieve('https://isotc211.geolexica.org/api/concepts/'+termid_number+'.json', './data/json/'+filename+".json")
        for name, value in headers.items():
            print(name, value)

        with open('./data/json/'+filename+".json") as f:
            d = json.load(f)
            fout = open('./data/tc211/'+filename+".adoc",'w')
            print(filename)
            fout.write("=== "+d['term']+"\n\n")
            fout.write(d['eng']['definition'][0]['content']+"\n\n")
            fout.write("(Source: ISO)\n\n")
            fout.close()