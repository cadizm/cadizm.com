
var Bookmarks = {

    map: null,
    markers: {},
    latLng: {},
    infoWindow: null,
    wpId: 0,
    directionsService: null,
    directionsDisplay: null,
    overview_polyline: null,
    ajaxReqFlag: false,
    distance_meters: 0,

    initialize: function() {
        var mapOptions = {
            center: new google.maps.LatLng(34.0486859, -118.2422464),
            zoom: 14,
        };

        Bookmarks.map = new google.maps.Map(document.getElementById("map-canvas"),
                mapOptions);

        Bookmarks.infoWindow = new google.maps.InfoWindow();
        Bookmarks.directionsService = new google.maps.DirectionsService();

        var rendererOptions = {
            draggable: true
        };
        Bookmarks.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
        Bookmarks.directionsDisplay.setMap(Bookmarks.map);

        Bookmarks.origin = new google.maps.places.Autocomplete(
            document.getElementById('origin'),
            { bounds: Bookmarks.map.getBounds() }
        );

        // Store autocomplete as attribute
        _.each($('#map-waypoints').children(), function(e, i, L) {
            // Origin special case
            if (i == 0) {
                e['waypoint'] = Bookmarks.origin;
                return;
            }
            var autocomplete = new google.maps.places.Autocomplete(
                $(e).children(":input")[0],
                { bounds: Bookmarks.map.getBounds() }
            );
            e['waypoint'] = autocomplete;
        });

        google.maps.event.addListener(Bookmarks.map, 'idle', function() {
            Bookmarks.handleBoundsChanged();
            Bookmarks.handleShowAlongPath();
        });

        google.maps.event.addListener(Bookmarks.directionsDisplay,
                'directions_changed', function() {
            var directions = Bookmarks.directionsDisplay.directions;
            Bookmarks.overview_polyline = directions.routes[0].overview_polyline;
            Bookmarks.handleShowAlongPath();
        });

        $('#map-mode').change(function() {
            Bookmarks.handleBoundsChanged();
            Bookmarks.handleShowAlongPath();
            if ($('#map-mode option:selected').val() == 'show_along_path') {
                $('#radius').show();
            }
            else {
                $('#radius').hide();
            }
        });

        $('#add-destination').click(function() {
            if ($('#map-waypoints .waypoint').length > 7) {
                return;
            }
            Bookmarks.addDestination();
        });

        $('#map-waypoints').on('click', '.remove-waypoint', function() {
            if ($('#map-waypoints .waypoint').length > 2) {
                $(this).closest('div').remove();
            }
        });

        $('#get-directions').click(function() {
            var div = $('#map-waypoints div');
            var len = div.length;
            _.each(div, function(e, i, L) {
                var place = e.waypoint.getPlace();
                if (len > 2 && place === undefined) {
                    e.remove();
                    len -= 1;
                }
            });
            var waypoints = [];
            _.each($('#map-waypoints div'), function(e, i, L) {
                waypoints.push({
                    location: e.waypoint.getPlace().geometry.location,
                    stopover: false
                });
            });
            if (waypoints.length < 2) {
                return;
            }
            var request = {
                origin: waypoints.shift().location,
                destination: waypoints.pop().location,
                travelMode: google.maps.TravelMode.DRIVING,
                unitSystem: google.maps.UnitSystem.IMPERIAL,
                waypoints: waypoints,
                optimizeWaypoints: false,
                provideRouteAlternatives: false,
                avoidHighways: false
            };
            Bookmarks.directionsService.route(request, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    Bookmarks.directionsDisplay.setDirections(response);
                    Bookmarks.overview_polyline = response.routes[0].overview_polyline;
                }
            });
        });

        $("#d_slider").slider();
        $("#d_slider").on("slide", function(slideEvt) {
            Bookmarks.distance_meters = slideEvt.value;
            if ($('#map-mode option:selected').val() == 'show_along_path'
                    && !Bookmarks.ajaxReqFlag) {
                Bookmarks.handleShowAlongPath();
            }
        });
        $('#radius').hide();

    }, // initialize()

    addDestination: function() {
        var div = $('#map-waypoints').children().last()[0];
        var waypoint = $(div).clone().appendTo($('#map-waypoints'));
        var autocomplete = new google.maps.places.Autocomplete(
            waypoint.children(":input")[0],
            { bounds: Bookmarks.map.getBounds() }
        );
        waypoint.children(":input").val('');
        waypoint[0]['waypoint'] = autocomplete;  // waypoint in list context
    },

    handleBoundsChanged: function() {
        if ($('#map-mode option:selected').val() !== 'show_all') {
            return;
        }
        var bounds = Bookmarks.map.getBounds().toUrlValue();
        bounds = bounds.split(',');
        var boundingBox = {
            lat_lo: bounds[0],
            lng_lo: bounds[1],
            lat_hi: bounds[2],
            lng_hi: bounds[3],
        };

        $.ajax({
            type: 'GET',
            url: '/bookmarks/ws/items_within_bounds',
            data: { boundingBox: JSON.stringify(boundingBox) },
        })
        .done(function(data) {
            if (!data || !data.status) {
                return;
            }
            items = JSON.parse(data.items);
            Bookmarks.addItemMarkers(items);
        })
        .fail(function() {
            console.log('FAIL items_within_bounds');
        })
        .always(function() {
        });
    },

    handleShowAlongPath: function() {
        if ($('#map-mode option:selected').val() !== 'show_along_path') {
            return;
        }
        var encodedPolyline = Bookmarks.overview_polyline;
        if (encodedPolyline == undefined || encodedPolyline == null) {
            return;
        }
        Bookmarks.ajaxReqFlag = true;
        $.ajax({
            type: 'GET',
            url: '/bookmarks/ws/items_along_polyline',
            data: {
                polyline: encodedPolyline,
                distance_meters: Bookmarks.distance_meters
            }
        })
        .done(function(data) {
            if (!data || !data.status) {
                return;
            }
            items = JSON.parse(data.items);
            Bookmarks.addItemMarkers(items);
        })
        .fail(function() {
            console.log('FAIL items_along_polyline');
        })
        .always(function() {
            Bookmarks.ajaxReqFlag = false;
        });
    },

    addItemMarkers: function(items) {
        Bookmarks.removeNonVisibleMarkers(items);
        _.each(items, function(e, i, L) {
            if (!(e.pk in Bookmarks.markers)) {
                // TODO: in database, store lat/lng in addition to geom
                var lngLat = Bookmarks.parseLatLngPointWkt(e.fields.geom);
                var latLng = new google.maps.LatLng(lngLat.lat, lngLat.lng);

                // offset marker if there's already another marker at this postition
                if (latLng.toUrlValue() in Bookmarks.latLng) {
                    var i = 0;
                    while (latLng.toUrlValue() in Bookmarks.latLng && i < 100) {
                        latLng = Bookmarks.jitterLatLng(latLng);
                        i += 1;
                    }
                }
                else {
                    Bookmarks.latLng[latLng.toUrlValue()] = e;
                }

                var marker = new google.maps.Marker({
                    position: latLng,
                    map: Bookmarks.map,
                    title: e.fields.name,
                });

                marker['geom'] = e;

                google.maps.event.addListener(marker, 'click', function() {
                    var latLng = marker.getPosition();
                    var item = marker['geom'];
                    Bookmarks.infoWindow.setContent(item.fields.name);
                    Bookmarks.infoWindow.open(Bookmarks.map, marker);
                });

                Bookmarks.markers[e.pk] = marker;
            }
            else {
                Bookmarks.markers[e.pk].setMap(Bookmarks.map);
            }
        });
    },

    removeNonVisibleMarkers: function(items) {
        // remove markers not visible within viewport bounds or not in items
        _.each(Bookmarks.markers, function(v, k, L) {
            if (!Bookmarks.map.getBounds().contains(v.getPosition()) ||
                    _.find(items, function(e) { return e.pk == k }) == undefined) {
                v.setMap(null);
            }
        });
    },

    csrfSafeMethod: function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },

    // http://gis.stackexchange.com/questions/15436/google-markers-at-same-address-not-showing-all-markers
    jitterLatLng: function(latLng) {
        var min = .999999;
        var max = 1.000001;

        var lat = latLng.lat() * (Math.random() * (max - min) + min);
        var lng = latLng.lng() * (Math.random() * (max - min) + min);

        return new google.maps.LatLng(lat, lng);
    },

    parseLatLngPointWkt: function(pointWkt, precision) {
        if (!precision) {
            precision = 6;
        }
        var lngLat = pointWkt.replace(/[^0-9^\.\-^\s]/g, '').trim().split(/\s+/);
        return { lng: Number(lngLat[0]), lat: Number(lngLat[1]) };
    }

};

// ----------------------------------------------------------------------------

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!Bookmarks.csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = $.cookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

google.maps.event.addDomListener(window, 'load', Bookmarks.initialize);
