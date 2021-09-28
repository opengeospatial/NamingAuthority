# OGC and specifications modules and relationships

Directory contain:

* one ttl file per specification document
* additional files embracing several specifications or commonly referenced definitions not defined elsewhere

## Namespaces used in this documents

@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix na: <http://www.opengis.net/def/metamodel/ogc-na/> .
@prefix ogcdt: <http://www.opengis.net/def/doc-type/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix spec: <http://www.opengis.net/def/ont/modspec/> .
@prefix specrel: <http://www.opengis.net/def/ont/specrel/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix status: <http://www.opengis.net/def/status/> .
@prefix bodies: <http://www.opengis.net/def/entities/bodies/> .


## Specification modules

* Specification document - obligatory
  * dct:creator - author - rdfs:literal
  * dct:dateAccepted - xsd:date ;
  * dct:dateSubmitted - xsd:date ;
  * dct:identifier "http://www.opengis.net/doc/is/OMS/3.0"
  * na:doctype - from http://www.opengis.net/def/doc-type
  * spec:status - from http://www.opengis.net/def/status/
  * dct:source - one of ../../entities/bodies.ttl
  * spec:authority - "Open Geospatial Consortium"
  * spec:class - spec:ConformanceClass(es)
  * spec:date - xsd:date
  * specrel:modspec <http://www.opengis.net/spec/OMS/3.0>
  * skos:notation - internal ID compliant with na:doc_no type
  * skos:prefLabel - title, rdfs:literal
  * adms:version - version e.g. "X.Y", rdfsliteral
* Specification document - optional
  * adms:prev - URI of the previous version of the specification, can be multiple, but direct ancestors shall be referred only
  * dcat:landingPage - URL of specification document on the web

## Entailment, validtion and upload

Specification documents defined in this directory are uploaded into Definition Server test environment http://defs-dev.opengis.net/vocprez.
Procedure and tools are described https://github.com/opengeospatial/NamingAuthority/tree/master/scripts.
