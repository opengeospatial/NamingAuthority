from html.parser import HTMLParser


reading_tt = 0
current_id = ""
current_start = ""
current_end = ""

fout = open('/Users/ogckm/Downloads/staplusstuff/staplus2.csv','w')

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        current_start = tag
        if(tag == "table"):
            print(tag)
            current_id = ""
            for attr in attrs:
                #print("$"+attr[0]+"|"+str(attr[1])+"|")
                if str(attr[0]) == 'id':
                    current_id = str(attr[1]).replace("3D\"","").replace("\"","")
                if str(attr[0]) == 'class':
                    print(current_id+" "+attr[1].replace("3D\"","").replace("\"",""))
                    #fout.write(current_id+",")
                #print("     attr:", attr)

    def handle_endtag(self, tag):
        current_end = tag
        if(tag == "tt"):
            print("END TT ")        
            reading_tt = 0


    def handle_data(self, data):

        if("opengis.net" in data):
            fout.write(str(data).replace('=\n','')+"\n")
            print("AHK "+current_start+"|"+str(data).replace('=\n','')+"|"+current_end+" BHK")

parser = MyHTMLParser()
fin = open('/Users/ogckm/Downloads/staplusstuff/staplus.mhtml','r')
parser.feed(fin.read())
fout.close()