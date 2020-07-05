Markdown documentation created by [pyLODE](http://github.com/rdflib/pyLODE) 

# Register Item status values
### A taxonomy

## Metadata
* **URI**
  * `http://www.opengis.net/def/status`
* **Publisher(s)**
  * [Open Geospatial Consortium](https://www.ogc.org)
* **Creators(s)**
  * [Open Geospatial Consortium](https://www.ogc.org)
* **Contributor(s)**
  * None
* **Created**
  * 2020-07-05
* **Modified**
  * 2020-07-05
* **Source**
  * [https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml](https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml)

* **Taxonomy RDF**
  * RDF ([turtle](status.ttl))
### Description
<p>Statuses of items within a controlled register.</p>
<p>This vocabulary is a SKOS Concept Hierarchy of the RE_ItemStatus enumeration of ISO 19135: Geographic Information -- Procedures for item registration's Register with additional Concepts from the Core Ontology for Linked Data Registry Services.</p>


## Table of Contents
1. [Collections](#collections)
1. [Object Concepts](#concepts)
1. [Namespaces](#namespaces)
1. [Legend](#legend)


## Overview

**Figure 1:** Ontology overview
## Collections
* [Register Item status values](#RegisterItemstatusvalues)
* [ISO 19135 Register Item status values](#ISO19135RegisterItemstatusvalues)
### Register Item status values
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/`
Preferred Labels |Register Item status values (en)<br />
Definition | Register Item status values according to ISO19135.
Source | <http://purl.org/linked-data/registry>
Members |[retired](retired) (cp)<br />[valid](valid) (cp)<br />[accepted](accepted) (cp)<br />[superseded](superseded) (cp)<br />[submitted](submitted) (cp)<br />[not accepted](notaccepted) (cp)<br />[invalid](invalid) (cp)<br />[deprecated](deprecated) (cp)<br />[stable](stable) (cp)<br />[experimental](experimental) (cp)<br />[reserved](reserved) (cp)<br />

### ISO 19135 Register Item status values
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/iso19135`
Preferred Labels |ISO 19135 Register Item status values (en)<br />
Definition | Register Item statuses from ISO19135 and subsequent Linked Data Registry extensions.
Source | https://def.isotc211.org/iso19135/-1/2015/CoreModel.rdf
Members |[retired](retired) (cp)<br />[valid](valid) (cp)<br />[superseded](superseded) (cp)<br />[invalid](invalid) (cp)<br />[submitted](submitted) (cp)<br />

## Concepts
* [accepted](http://www.opengis.net/def/status/accepted)
	* [deprecated](http://www.opengis.net/def/status/deprecated)
		* [retired](http://www.opengis.net/def/status/retired)
		* [superseded](http://www.opengis.net/def/status/superseded)
	* [valid](http://www.opengis.net/def/status/valid)
		* [experimental](http://www.opengis.net/def/status/experimental)
		* [stable](http://www.opengis.net/def/status/stable)
* [not accepted](http://www.opengis.net/def/status/notAccepted)
	* [invalid](http://www.opengis.net/def/status/invalid)
	* [reserved](http://www.opengis.net/def/status/reserved)
	* [submitted](http://www.opengis.net/def/status/submitted)

### accepted
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/accepted`
Preferred Labels |accepted (en)<br />
Definition | An entry that has been accepted for use and is visible in the default register listing. Includes entries that have seen been retired or superseded.
Source | http://purl.org/linked-data/registry
Narrower Concepts |[deprecated](deprecated) (cp)<br />[valid](valid) (cp)<br />
### deprecated
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/deprecated`
Preferred Labels |deprecated (en)<br />
Definition | An entry that has been retired or replaced and is no longer to be used.
Source | http://purl.org/linked-data/registry
Broader Concepts |[accepted](accepted) (cp)<br />
Narrower Concepts |[superseded](superseded) (cp)<br />[retired](retired) (cp)<br />
### experimental
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/experimental`
Preferred Labels |experimental (en)<br />
Definition | An entry that has been accepted into the register temporarily and may be subject to change or withdrawal.
Source | http://purl.org/linked-data/registry
Broader Concepts |[valid](valid) (cp)<br />
### invalid
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/invalid`
Preferred Labels |invalid (en)<br />
Definition | An entry which has been invalidated due to serious flaws, distinct from retrirement. Corresponds to ISO 19135(redraft) 'invalid'.
Source | https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml
Broader Concepts |[not accepted](notaccepted) (cp)<br />
### not accepted
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/notAccepted`
Preferred Labels |not accepted (en)<br />
Definition | An entry that should not be visible in the default register listing. Corresponds to ISO 19135:2005 'notValid'.
Source | http://purl.org/linked-data/registry
Narrower Concepts |[invalid](invalid) (cp)<br />[submitted](submitted) (cp)<br />[reserved](reserved) (cp)<br />
### reserved
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/reserved`
Preferred Labels |reserved (en)<br />
Definition | A reserved entry allocated for some as yet undetermined future use.
Source | http://purl.org/linked-data/registry
Broader Concepts |[not accepted](notaccepted) (cp)<br />
### retired
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/retired`
Preferred Labels |retired (en)<br />
Definition | An entry that has been withdrawn from use.  Corresponds to ISO 19135:2005 'retired'.
Source | https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml
Broader Concepts |[deprecated](deprecated) (cp)<br />
### stable
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/stable`
Preferred Labels |stable (en)<br />
Definition | An entry that is seen as having a reasonable measure of stability, may be used to mark the full adoption of a previously 'experimental' entry.
Source | http://purl.org/linked-data/registry
Broader Concepts |[valid](valid) (cp)<br />
### submitted
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/submitted`
Preferred Labels |submitted (en)<br />
Definition | A proposed entry which is not yet approved for use for use. Corresponds to ISO 19135:(redraft) 'submitted'.
Source | https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml
Broader Concepts |[not accepted](notaccepted) (cp)<br />
### superseded
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/superseded`
Preferred Labels |superseded (en)<br />
Definition | An entry that has been replaced by a new alternative which should be used instead.  Corresponds to ISO 19135:2005 'superseded'.
Source | https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml
Broader Concepts |[deprecated](deprecated) (cp)<br />
### valid
Property | Value
--- | ---
URI | `http://www.opengis.net/def/status/valid`
Preferred Labels |valid (en)<br />
Definition | An entry that has been accepted into the register and is deemed fit for use. Corresponds to ISO 19135:2005 'valid'.
Source | https://def.isotc211.org/iso19135/-1/2015/catalog-v001.xml
Broader Concepts |[accepted](accepted) (cp)<br />
Narrower Concepts |[stable](stable) (cp)<br />[experimental](experimental) (cp)<br />

## Namespaces
* **cs**
  * `http://www.opengis.net/def/status`
* **dcterms**
  * `http://purl.org/dc/terms/`
* **owl**
  * `http://www.w3.org/2002/07/owl#`
* **policy**
  * `http://www.opengis.net/def/metamodel/ogc-na/`
* **rdf**
  * `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
* **rdfs**
  * `http://www.w3.org/2000/01/rdf-schema#`
* **reg**
  * `http://purl.org/linked-data/registry#`
* **sdo**
  * `https://schema.org/`
* **skos**
  * `http://www.w3.org/2004/02/skos/core#`
* **status**
  * `http://www.opengis.net/def/status/`
* **xsd**
  * `http://www.w3.org/2001/XMLSchema#`

## Legend
* Collections: cl
* Concepts: cp
