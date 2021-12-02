# Creation of http://www.opengis.net/def/crs/OGC/0/BeforePresentTime

Date: 2021-12-01

Fixes issue https://github.com/opengeospatial/NamingAuthority/issues/17#issuecomment-553385027

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<TemporalCRS xmlns="http://www.opengis.net/gml/3.2" xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0" gml:id="before-present-time-crs" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gmlBase.xsd">
    <description>
        Concrete temporal CRS of years elapsed from the present, positive backwards.
    </description>
    <identifier codeSpace="http://www.ietf.org/rfc/rfc3986">
        http://www.opengis.net/def/crs/OGC/0/BeforePresentTime
    </identifier>
    <name>Before Present Time</name>
    <remarks>Version 1.0</remarks>
    <scope>not known</scope>
    <timeCS>
        <TimeCS gml:id="before-present-time-crs_a-cs">
            <description>
                1D coordinate system containing a time axis measuring (Julian) years [a], backwards in time.
            </description>
            <identifier codeSpace="http://www.ietf.org/rfc/rfc3986">%a:cs%</identifier>
            <remarks>Initial version (0.1)</remarks>
            <axis>
                <CoordinateSystemAxis gml:id="before-present-time-crs_a-cs_bp-a" uom="http://www.opengis.net/def/uom/UCUM/0/a">
                    <description>
                        Coordinate system axis for the recording of years before the present [BP], backwards in time. 'Present' is defined as 1950 CE.
                    </description>
                    <identifier codeSpace="http://www.ietf.org/rfc/rfc3986">%bp-a%</identifier>
                    <remarks>Version 1.0</remarks>
                    <axisAbbrev>years BP</axisAbbrev>
                    <axisDirection codeSpace="http://www.ietf.org/rfc/rfc3986">
                        http://www.opengis.net/def/axisDirection/OGC/1.0/past
                    </axisDirection>
                </CoordinateSystemAxis>
            </axis>
        </TimeCS>
    </timeCS>
    <temporalDatum>
        <TemporalDatum gml:id="before-present-time-crs_yz-td">
            <description>
                The year 1950 in the Gregorian calendar.
            </description>
            <identifier codeSpace="http://www.ietf.org/rfc/rfc3986">%yz-td%</identifier>
            <remarks>
                'Present' is defined as 1950 CE, when the first radio carbon dating was done and before the atmosphere was polluted by nuclear fallout.
            </remarks>
            <scope>not known</scope>
            <origin>1950-01-01T00:00:00Z</origin>
        </TemporalDatum>
    </temporalDatum>
</TemporalCRS>

```
