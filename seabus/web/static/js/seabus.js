var map;
var markers = {};

function initMap() {
    // called by google maps api callback after map is initialized
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 49.2985, lng: -123.0957},
        zoom: 14
    });
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(createAboutBox());
    getBoatsSocketIO();
}

function point_has_moved(old_lat, old_lon, new_lat, new_lon) {
    /* determine if a boat position has actually changed, eliminates "wobble" from 
    minute changes in GPS coordinates */
    ACCURACY = 3;
    r_new_lat = new_lat.toFixed(ACCURACY);
    r_new_lon = new_lon.toFixed(ACCURACY);
    r_old_lat = old_lat.toFixed(ACCURACY);
    r_old_lon = old_lon.toFixed(ACCURACY);
    if (r_old_lat != r_new_lat || r_old_lon != r_new_lon) {
        console.log(r_old_lat, r_old_lon);
        console.log(r_new_lat, r_new_lon);
        return true
    } else {
        return false;
    }
}

function updateMap(map, data, markers) {
    // draw boats on the map
    for (var boat in data.boats) {
        lat = data.boats[boat].lat;
        lon = data.boats[boat].lon;
        name = data.boats[boat].name;
        id = data.boats[boat].id;
        if (id in markers) {
            // update an existing marker if its already on the map
            current_pos = markers[id].getPosition();
            if (point_has_moved(current_pos.lat(), current_pos.lng(), lat, lon)) {
                console.log(name);
                markers[id].setPosition(new google.maps.LatLng(lat, lon));
                setTimeout(function(marker) {
                    marker.setAnimation(null);
                }, 500, markers[id]);
            } else {
                if (name.includes('BURRARD')) {
                    console.log(name + ' has not moved.');
                }
            }
        } else {
            // create a new marker
            var boatLatLon = new google.maps.LatLng(lat, lon);
            icon = setIcon(name);
            //var marker = new google.maps.Marker({
            var marker = new SlidingMarker({
                position: boatLatLon,
                icon: icon
            });
            marker.setMap(map);
            markers[id] = marker;
        }
    }
}

function setIcon(name) {
    // return wifi enabled icon for boats which have wifi installed
    if (name.includes('OTTER II') || name.includes('PACIFIC BRZE')) {
        return '/img/seabus-wifi.png';
    } else {
        return '/img/seabus.png';
    }
}

function getBoatsSocketIO() {
    // establish websocket connection
    var socket = io.connect('/seabus_data')
    document.beforeUnload = function() { socket.disconnect() }
    socket.on('seabus_moved', function(data) {
        updateMap(map, data, markers);
        console.log('seabus_moved event received');
    });
}


function createAboutBox() {

    var about = document.createElement('div');
    var aboutUI = document.createElement('div');
    aboutLink = document.createElement('a');

    aboutUI.style.backgroundColor = '#fff';
    aboutUI.style.textAlign = 'center';
    aboutUI.style.border = '2px solid #fff';
    aboutUI.style.borderRadius = '3px';
    aboutUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    aboutUI.style.marginBottom = '22px';

    aboutLink.style.fontSize = '11px';
    aboutLink.style.fontFamily = 'Robot, Arial, sans-serif';
    aboutLink.style.color = '#000';
    aboutLink.style.textDecoration = 'none';
    aboutLink.style.lineHeight = '38px';
    aboutLink.style.paddingLeft = '5px';
    aboutLink.style.paddingRight = '5px';
    aboutLink.href = '/about.html';
    aboutLink.innerHTML = 'About This App';
    
    about.appendChild(aboutUI);
    aboutUI.appendChild(aboutLink);

    return about;
}
