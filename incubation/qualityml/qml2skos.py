from rdflib import Graph, Namespace,  URIRef, Literal, RDF, RDFS


import json

import sys
import re
import csv
import getopt

JSON="qualityml.json"
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
QML= Namespace('http://defs-dev.opengis.net/def/qualityml/')
SCHEME = URIRef('http://defs-dev.opengis.net/def/qualityml')
lan2std = { 'spa':'sp' , 'eng': 'en' , 'cat': 'ca' }

def label(gr,id,node):
    """ adds names and descriptions to a object in a graph for a json node """
    names = node.get('name')
    if names:
        for lan in names :
            gr.add( (id, SKOS.prefLabel, Literal( names[lan], lang=lan2std[lan]) ))
    alts = node.get('alternativeName')
    if alts:
        for name in alts :
            for lan in name:
                gr.add( (id, SKOS.altLabel, Literal( name[lan], lang=lan2std[lan]) ))
    descs = node.get('desc')
    if descs:
        for lan in descs :
            gr.add( (id, SKOS.definition, Literal(descs[lan], lang=lan2std[lan]) ))
        
def main():
    with open(JSON) as infile:
        data = json.load(infile)
    gr = Graph()
    gr.namespace_manager.bind('skos', SKOS)
    gr.namespace_manager.bind('qml', QML)
    import pdb; pdb.set_trace()                        
    gr.add ( (SCHEME , RDF.type , SKOS.ConceptScheme))
    gr.add ( (SCHEME , RDFS.label , Literal('Quality Indicators Dictionary and Markup Language - QualityML')))
    for c in data['class']:
        name = c['id']
        id = URIRef(QML[name])
        gr.add( (id, RDF.type, SKOS.Concept ))
        gr.add( (id, RDF.type, QML.Class ))
        gr.add( (id, SKOS.topConceptOf, SCHEME ))
        gr.add( (id, SKOS.inScheme, SCHEME ))
        gr.add ( (SCHEME , SKOS.hasTopConcept , id ))
        label(gr, id, c )

    for i in data['indicator'] :
        name = i['id']
        qc = URIRef(QML[i['class']]) 
        id = URIRef(QML[name])
        gr.add( (id, RDF.type, SKOS.Concept ))
        gr.add( (id, RDF.type, QML.Indicator ))
        gr.add( (id, SKOS.broader, qc ))
        gr.add( (id, SKOS.inScheme, SCHEME ))
        label(gr, id, i )

    for m in data['measure'] :
        name = m['id']
        qc = URIRef(QML[i['class']]) 
        id = URIRef(QML["/".join( ('measure',name))])
        gr.add( (id, RDF.type, SKOS.Concept ))
        gr.add( (id, RDF.type, QML.Measure ))
        gr.add( (id, SKOS.broader, qc ))
        gr.add( (id, SKOS.inScheme, SCHEME ))
        label(gr, id, m )
        
    with open ('qml.ttl' , "w") as outfile:
        outfile.write(gr.serialize(format='turtle'))
    
if __name__ == '__main__':
    main()
