# External sources used

The Naming Authority repository downloads and processes the following external resources (most of them 
defined in `file_downloads.yaml):

* Documents to SWGs
  * Type: Google Docs Spreadsheet (CSV format)
  * URL: https://docs.google.com/spreadsheets/d/1pqFUR6F7FM5ASgKRKev8mLvR5NoXilq5BX0rZQG6fQM/export?format=csv
  * Output:
    * `definitions/docs/docs-working-groups.ttl`
  * Notes: Downloaded and processed in memory by `scripts/swgdocmatch.py`.

* OGC Working Groups
  * Type: JSON API
  * URL: https://portal.ogc.org/public_ogc/api/working_groups.php
  * Output:
    * `entities/bodies.json`

* OGC Standards Roadmap
  * Type: JSON API
  * URL: https://portal.ogc.org/services/srv_standards_roadmap_json.php
  * Output:
    * `incubation/standards-roadmap/standards-roadmap.json`

* Namespaces defined in Specifications
  * Type: Google Docs Spreadsheet (CSV format)
  * URL: https://docs.google.com/spreadsheets/d/1NX8mLwnqUSBDaIq7go9IwEeCJsbcDV2vdhrscRqG5jc/export?format=csv
  * Output:
    * `definitions/docs/is-namespaces.csv`

* Specifications to Engineering Reports mapping
  * Type: Google Docs Spreadsheet (CSV format)
  * URL: https://docs.google.com/spreadsheets/d/1e22BAKzxrI67kBp5qA2WJrbKulJ0-ALHfI8w6aKvv3Q/export?format=csv
  * Output:
    * `definitions/docs/specs-to-engineering-reports.csv`