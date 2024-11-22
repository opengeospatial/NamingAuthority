from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import json
with open("geolexica.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

cfout = open('./data/adoc/0.csv','w')

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
        filename = filename.replace(',','_')
        print('reading '+'https://isotc211.geolexica.org/api/concepts/'+termid_number+'.json')
        urlretrieve('https://isotc211.geolexica.org/api/concepts/'+termid_number+'.json','./data/json/'+filename+".json")
        cfout.write(filename+".json"+','+label+'\n')
        with open('./data/json/'+filename+".json") as f:
            d = json.load(f)
            fout = open('./data/adoc/'+filename+".adoc",'w')
            print(filename)
            fout.write("=== "+d['term']+"\n\n")
            for definition in d['eng']['definition']:
                fout.write(definition['content']+"\n\n")
            for note in d['eng']['notes']:
                fout.write('NOTE: '+note['content']+"\n\n")
            for source in d['eng']['sources']:
                fout.write('(Source: '+source['origin']['ref']+")\n\n")                
         
            fout.close()
cfout.close()