# OGC and specifications modules and relationships

Directory contain:

one ttl file per specification document
additional files embracing several specifications or commonly referenced definitions not defined elsewhere

## Namespaces used in this documents


* @prefix adms: <http://www.w3.org/ns/adms#> 
* @prefix dcat: <http://www.w3.org/ns/dcat#> 
* @prefix dct: <http://purl.org/dc/terms/> 
* @prefix na: <http://www.opengis.net/def/metamodel/ogc-na/> 
* @prefix ogcdt: <http://www.opengis.net/def/doc-type/> 
* @prefix owl: <http://www.w3.org/2002/07/owl#> 
* @prefix reg: <http://purl.org/linked-data/registry#> 
* @prefix skos: <http://www.w3.org/2004/02/skos/core#> 
* @prefix spec: <http://www.opengis.net/def/ont/modspec/> 
* @prefix specrel: <http://www.opengis.net/def/ont/specrel/> 
* @prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
* @prefix status: <http://www.opengis.net/def/status/> 
* @prefix bodies: <http://www.opengis.net/def/entities/bodies/> 



## Specification modules

Paragraph define convention of the Specification that shall be followed for each document in the directory as the minimum T-Box.
All the titles shall contain modular specification name followed by colon and space, e.g. "ConformanceClass: [name_of_the_conformance_class]".


Schema

* concept scheme have to be defined e.g.: <http://www.opengis.net/spec/OMS/3.0> a skos:ConceptScheme


spec:Specification document - obligatory
* dct:creator - author - rdfs:literal
* dct:dateAccepted - xsd:date ;
* dct:dateSubmitted - xsd:date ;
* dct:identifier "http://www.opengis.net/doc/is/OMS/3.0"
* na:doctype - from http://www.opengis.net/def/doc-type
* spec:status - from http://www.opengis.net/def/status/
* dct:source - one of ../../entities/bodies.ttl, replaces deprecated prov:wasAttributedTo
* spec:authority - "Open Geospatial Consortium"
* spec:class - spec:ConformanceClass(es) * top levelclasses
* spec:date - xsd:date
* specrel:modspec <http://www.opengis.net/spec/OMS/3.0>
* skos:notation - internal ID compliant with na:doc_no type
* skos:prefLabel - title, rdfs:literal
* adms:version - version e.g. "X.Y", rdfsliteral

spec:Specification document - conditional
* adms:prev/adms:next - URI of the previous/next version of the specification, can be multiple, but only direct ancestors/descendants shall be referred,
* dcat:landingPage - URL of specification document on the web
* specrel:implementation/implements - relation between abstract specification and its implementation
* specrel:normativeReference - Superset of different types of relations that are included in Normative Reference sections
* specrel:uses - The subject specification uses the referenced specification as a normative component
* specrel:relatesTo - unspecified relation to the referenced document
* skos:exactMatch - equivalent specification that can be used in exchange
* specrel:wasInfluencedBy - artifact that influenced subject document editors but is not referenced


spec:ConformanceClass - obligatory
* spec:conformanceTest - spec:ConformanceTest(s), it is skos:narrower relation
* spec:requirementsTested - spec:RequirementsClass covered by the ConformanceClass, it is skos:narrower relation
* skos:definition - description, rdfs:Literal
* skos:prefLabel - title, rdfs:Literal

spec:ConformanceClass - conditional
* spec:dependency - the class witch which one must be conformant if conformant with this class
* dct:hasPart - composite of the this conformance class

* _NOTE:ConformanceClass without spec:dependency is the top concepts of the Scheme_*


spec:ConformanceTest - obligatory
* skos:prefLabel  - title, rdfs:Literal
* skos:definition - general description, rdfs:Literal
* spec:method - test method description, rdfs:Literal
* spec:purpose - test purpose description, rdfs:Literal
* spec:requirement - requiremnt(s) covered by test, spec:Requirement; it is skos:narrower relation
* spec:testType - spec:Capabilities or spec:Basic

spec:Requirement - obligatory
* skos:prefLabel - title, rdfs:Literal
* skos:definition - description, rdfs:Literal
spec:Requirement - optional
* spec:dependency - parent Requirement, it is skos:broader relation


spec:RequirementsClass - obligatory

* skos:prefLabel - title, rdfs:Literal
* skos:definition - description, rdfs:Literal
* spec:normativeStatement - spec:Requirement(s); it is skos:narrower relation


_NOTE: there are no RequirementsModule in the base ../../definitions/models/modspec.ttl_
_NOTE: any skos:broader/narrower relation assume system generate reverse direction relation in the entailment_

_For the moment, recomendations that have no related conformnceTest will not be navigable from schema_


## Entailment, validtion and upload

Specification documents defined in this directory are uploaded into Definition Server test environment http://defs-dev.opengis.net/vocprez.
Procedure and tools are described https://github.com/opengeospatial/NamingAuthority/tree/master/scripts.
