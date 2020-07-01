# OGC Catalogue Services 3.0 Specification - HTTP Protocol Binding
identifier = "12-176r7"
specURL = "http://docs.opengeospatial.org/is/12-176r7/12-176r7.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
elementList = []
confClasses = ['Basic-Catalogue','OpenSearch','GetCapabilities-XML','GetRecordById-XML','GetRecords-Basic-XML','GetRecords-Distributed-XML','GetRecords-Distributed-KVP','GetRecords-Async-XML','GetRecords-Async-KVP','GetDomain-XML','GetDomain-KVP','Transaction','Harvest-Basic-XML','Harvest-Basic-KVP','Harvest-Async-XML','Harvest-Async-KVP','Harvest-Periodic-XML','Harvest-Periodic-KVP','Filter-CQL','Filter-FES-XML','Filter-FES-KVP','Filter-FES-KVP-Advanced','CSW-Response','ATOM-response']
reqClasses = ['Basic-Catalogue','OpenSearch','GetCapabilities-XML','GetRecordById-XML','GetRecords-Basic-XML','GetRecords-Distributed-XML','GetRecords-Distributed-KVP','GetRecords-Async-XML','GetRecords-Async-KVP','GetDomain-XML','GetDomain-KVP','Transaction','Harvest-Basic-XML','Harvest-Basic-KVP','Harvest-Async-XML','Harvest-Async-KVP','Harvest-Periodic-XML','Harvest-Periodic-KVP','Filter-CQL','Filter-FES-XML','Filter-FES-KVP','Filter-FES-KVP-Advanced','CSW-response','ATOM-response']

# processing the input file

for confToken in confClasses:
    elementList.append("http://www.opengis.net/spec/csw/3.0/conf/"+confToken)

for reqclassToken in reqClasses:
    elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+reqclassToken)

i = 0
while i < 176:
    if i >0 and i<10:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-00"+str(i))
    if i >10 and i<=14:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=35 and i<=48:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=63 and i<=68:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=73 and i<=78:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=81 and i<=93:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=95 and i<100:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-0"+str(i))
    if i >=100 and i<=102:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-"+str(i))
    if i >=123 and i<=133:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-"+str(i))
    if i >=136 and i<=139:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-"+str(i))
    if i == 133:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-"+str(i)+"a") #133a
    if i ==141:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Basic-Catalogue"+"/Requirement-"+str(i))
    if i ==8:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"OpenSearch"+"/Requirement-00"+str(i))
    if i >=21 and i<=23:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"OpenSearch"+"/Requirement-0"+str(i))
    if i >=44 and i<=48:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetCapabilities-XML"+"/Requirement-0"+str(i))
    if i ==174:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetCapabilities-XML"+"/Requirement-"+str(i))
    if i >=123 and i<=133:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecordById-XML"+"/Requirement-"+str(i))
    if i == 133:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecordById-XML"+"/Requirement-"+str(i)+"a") #133a
    if i >=73 and i<=78:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Basic-XML"+"/Requirement-0"+str(i))
    if i >=81 and i<=93:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Basic-XML"+"/Requirement-0"+str(i))
    if i >=95 and i<100:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Basic-XML"+"/Requirement-0"+str(i))
    if i >=100 and i<=102:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Basic-XML"+"/Requirement-"+str(i))
    if i >=69 and i<=71:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Distributed-XML"+"/Requirement-0"+str(i))
    if i >=69 and i<=71:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Distributed-KVP"+"/Requirement-0"+str(i))
    if i == 72:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Async-XML"+"/Requirement-0"+str(i))
    if i >=111 and i<=117:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Async-XML"+"/Requirement-"+str(i))
    if i == 72:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Async-KVP"+"/Requirement-0"+str(i))
    if i >=111 and i<=117:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetRecords-Async-KVP"+"/Requirement-"+str(i))
    if i >=49 and i<=62:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetDomain-XML"+"/Requirement-0"+str(i))
    if i ==49:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetDomain-KVP"+"/Requirement-0"+str(i))
    if i ==50:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetDomain-KVP"+"/Requirement-0"+str(i))
    if i >=52 and i<=62:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"GetDomain-KVP"+"/Requirement-0"+str(i))
    if i >=142 and i<=151:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Transaction"+"/Requirement-"+str(i))
    if i >=152 and i<=154:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Basic-XML"+"/Requirement-"+str(i))
    if i >=159 and i<=164:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Basic-XML"+"/Requirement-"+str(i))
    if i ==167:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Basic-XML"+"/Requirement-"+str(i))
    if i >=152 and i<=154:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Basic-KVP"+"/Requirement-"+str(i))
    if i ==167:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Basic-KVP"+"/Requirement-"+str(i))
    if i >=155 and i<=158:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-XML"+"/Requirement-"+str(i))
    if i ==165:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-XML"+"/Requirement-"+str(i))
    if i ==166:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-XML"+"/Requirement-"+str(i))
    if i >=168 and i<=172:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-XML"+"/Requirement-"+str(i))
    if i >=155 and i<=158:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-KVP"+"/Requirement-"+str(i))
    if i ==165:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-KVP"+"/Requirement-"+str(i))
    if i ==166:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-KVP"+"/Requirement-"+str(i))
    if i >=168 and i<=173:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Async-KVP"+"/Requirement-"+str(i))
    if i ==175:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Periodic-XML"+"/Requirement-"+str(i))
    if i ==176:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Periodic-XML"+"/Requirement-"+str(i))
    if i ==175:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Periodic-KVP"+"/Requirement-"+str(i))
    if i ==176:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Harvest-Periodic-KVP"+"/Requirement-"+str(i))
    if i ==104:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-CQL"+"/Requirement-"+str(i))
    if i ==15:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-XML"+"/Requirement-0"+str(i))
    if i ==16:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-XML"+"/Requirement-0"+str(i))
    if i ==103:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-XML"+"/Requirement-"+str(i))
    if i ==105:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-XML"+"/Requirement-"+str(i))
    if i >=108 and i<=110:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-XML"+"/Requirement-"+str(i))
    if i ==17:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-KVP"+"/Requirement-0"+str(i))
    if i ==18:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-KVP-Advanced"+"/Requirement-0"+str(i))
    if i >=106 and i<=109:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"Filter-FES-KVP-Advanced"+"/Requirement-"+str(i))
    if i >=24 and i<=34:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-0"+str(i))
    if i ==79:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-0"+str(i))
    if i ==118:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-"+str(i))
    if i ==120:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-"+str(i))
    if i ==121:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-"+str(i))
    if i ==134:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"CSW-response"+"/Requirement-"+str(i))
    if i >=19 and i<=23:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-0"+str(i))
    if i ==80:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-0"+str(i))
    if i ==119:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-"+str(i))
    if i ==112:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-"+str(i))
    if i ==135:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-"+str(i))
    if i ==140:
        elementList.append("http://www.opengis.net/spec/csw/3.0/req/"+"ATOM-response"+"/Requirement-"+str(i))
    i += 1


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    fout.write(specURL+","+e+"\n")
