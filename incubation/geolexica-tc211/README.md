## Geolexica concept list parser

To harvest the concepts, download the concepts list from https://isotc211.geolexica.org/concepts/ to a file named `geolexica.html`

then run the python script `process.py`

Once the asciidoc files have been harvested, you can include them in your metanorma asciidoc documents by using the `include` directive. See below.

```adoc
== Terms and definitions

include::./glossaries/tc211/703_coordinate_reference_system.adoc[]

include::./glossaries/tc211/1018_feature_identifier.adoc[]
```


last modified: 2024-11-22
