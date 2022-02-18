# Working folder for the OGC Name Type Specification - definitions - part 1 – basic name

This is a working folder, used for developing draft revisions of the document.

## Compiling a Draft Policy with a docker-containerized Metanorma instance

To convert the draft Policy from asciidoc format to HTML and PDF formats, we use the metanorma software to **compile** the document.

From the folder containing the `document.adoc` file, run the following command.

`docker run -v "$(pwd)":/metanorma -v ${HOME}/.fontist/fonts/:/config/fonts  metanorma/mn  metanorma compile --agree-to-terms -t ogc -x xml,html,doc document.adoc`

NOTE: You need to add this option to retrieve licensed fonts  `--agree-to-terms`
