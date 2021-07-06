These files contain further details for specifications for specific documents - they must be named using the <document_no> .ttl.

GIT workflows will combine these with the necessary baseline documents and perform entailment and validation (and eventually automated loading to staging repository)

TODO:
- a manual workflow to push to the production repository can be designed - but may need to include status checking and metadata.
- add provenance trace information automatically during entailment
- consider validation checking post-publication that all referenced objects (e.g. previous versions and dependencies) are present and valid - this is hard to do peicemeal as finding all the possible files to build the appropriate graph dynamically is not easy.