#!/usr/bin/env python


def m2dd(m):
    """Approximate distance in meters to decimal degrees.

    http://en.wikipedia.org/wiki/Decimal_degrees
    """

    return 8.983e-06 * m


def decode_gpolyline(encoded):
    """Decodes a polyline that was encoded using the Google Maps method.

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a straightforward Python port of Mark McClure's JavaScript polyline decoder
    (http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/decode.js)
    and Peter Chng's PHP polyline decode
    (http://unitstep.net/blog/2008/08/02/decoding-google-maps-encoded-polylines-using-php/)
    """
    encoded_len = len(encoded)
    index = 0
    array = []
    lat = 0
    lng = 0
    while index < encoded_len:
        b = 0
        shift = 0
        result = 0
        while True:
            b = ord(encoded[index]) - 63
            index = index + 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat
        shift = 0
        result = 0
        while True:
            b = ord(encoded[index]) - 63
            index = index + 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng
        array.append((lng * 1e-5, lat * 1e-5))  # (x-axis, y-axis)
    return array


if __name__ == "__main__":
    latlngs = decode_line("{bynEpcupUiCy@gClFw@xAkA{@kDkCqBwAgGuE}BkBO]eDyC][u@m@]MKGSQAUUUEMAQDUFQJKJIVEN?TFJHNXF^A`@Mr@Mp@i@rBCR@XqAbCwEtIkAvBuC|EmAlBaCbD{AjBwAzAg@f@s@j@cBtAoH`Gc@^mC|BmAtAqBzCwIxMeC|DkAxB}@pB_AhCwA`FoBpHqDxNsAjFaAvDmBfGKVM\cA~C_CtG?@{BhHw@lC_@nA{@dCqBfFg@nA_@bAi@fBeBfGe@|BuEnVs@pDaAtF}@hGa@hDi@hDo@nEiArJm@jFYtBq@|C_AnDiAxC{G|OkDfJ[|@oC~Hq@`Bi@nAaArBe@z@qFbJgHnL}BjDqA~AuArAqAdAaC`BuJdFqCxAyAz@oAx@wBvBi@p@i@x@sAbCmEbIcAlB_A|AmAlBcBpB_A`A_Az@qCnBkAt@gU~Ku@^}BnBuA~AqApBeAbCw@tC_@~BI|@KhBIpFCdCIzBIbAYnB]fBK\_AjCwEfJgNpXyC~FKAMH}A|BcA`AiBpAUNKAECKICOA_@D_@JQDEPAf@NZR`@j@Zv@Nb@Ld@XfBJr@Lv@oC]_BUOCWp@_@\M`@QZq@f@WP]H_@BS@SLc@~@[d@]lAYdBGb@t@R@B@BEJ")
    for latlng in latlngs:
        print str(latlng[0]) + "," + str(latlng[1])

