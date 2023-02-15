# Upgrading to CaLAThe v5

## Building

One time only
```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install rdflib
```

Then each you build

```
python3 process.py
```


## The worflow implemented by the script can be summarised as follows.

```mermaid

flowchart TD
    A(start) --> B[Create an empty RDF model]
    B --> C[Read in v4 and v5 concepts into the model]
    C --> E[Examine v4 concept]
    E --> F{v4 concept has matching v5 concept?}            
    F -->|Yes| G[Supersede]
    G --> I[go back]
    I -->|Yes| E
    F -->|No| H[Deprecate]
    H ----> I{More concepts?}
    I -->|No| J[Export updated model]
    J --> K(End)

```
