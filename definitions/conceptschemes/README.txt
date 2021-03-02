
OGC definition space refactoring decisions and process:
(Rob Atkinson 3 Feb 2018)

ConceptSchemes will reflect delegatable policy domains.

There may (or may not) be a need to define a top level ConceptScheme that binds to each and every definitions in every scheme.

SKOS model complicates things - ConceptScheme and Collection are disjoint - so we can't simply treat a ConceptScheme as a Collection member
of an aggregate ConceptScheme.

Assuming we can search across multiple ConceptSchemes, then a ConceptScheme for the top level delegation can be created, simply to provide
an object to annotate. We can however treat nested ConceptSchemes as Collections, by defining a non-SKOS memebership predicate.

We do this in the policy metamodel. 

this has been factored out of ogc-na into the managed definition space, by treating it as an Ontology, and using an Ontology->SKOS mapping

all such metamodels moved to /dev/metamodel, renamed meaningfully (policy, register, specification, profile etc) and using a / namespace so individual
terms can be linked. (note that if a system asks for an ontology it can be redirected to a composite OWL file that contains the / based definition)

e.g.

http://www.opengis.net/ogc-na#  => http://www.opengis.net/def/metamodel/policy/


Files are refactored into discrete ConceptSchemes that can be loaded and managed via the CMS with appropriate delegations.
skos:changeNotes record metadata about original sources.

Tricksy thing:

instead of declaring x and x/ to be owl:sameAs...

x/ is a skos:Collection containing all members (or transitively subcollections containing all members)

x/ skos:inScheme x .

x/ as a collection is a member of a collection in the top level concept scheme:
<http://www.opengis.net/def/> rdf:type skos:Collection ;
	skos:member x;
	skos:inScheme <http://www.opengis.net/def>
	
	

this avoids violating SKOS requirement that conceptschemes and collections are disjoint, all concepts declare the scheme they are in, but there is a trace from the "master" to all contained defintions

where a top level authority/space is defined, for example /functions for /functions/geosparql  then the containing file is renamed - eg functions_geosparql.ttl
 it will declare whatever necessary for the top level - eg.  
     <http://www.opengis.net/def/functions/>
		a skos:Collection ;
		skos:member <http://www.opengis.net/def/functions/geosparql/>
		
    and the root register will be a concept scheme:
	<http://www.opengis.net/def/functions/geosparql> a skos:ConceptScheme
	