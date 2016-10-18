var seabus = {

    map: null,

    markers: {},

    initMap: function() {
        // called back by google maps api after map is initialized
        this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 49.2985, lng: -123.0957},
            zoom: 14
        });
        this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.createAboutBox());
        this.getBoatsSocketIO();
    },

    point_has_moved: function(old_lat, old_lon, new_lat, new_lon) {
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
    },

    updateMap: function(data) {
        // draw boats on the map
        for (var boat in data.boats) {
            lat = data.boats[boat].lat;
            lon = data.boats[boat].lon;
            name = data.boats[boat].name;
            id = data.boats[boat].id;
            if (id in this.markers) {
                // update an existing marker if its already on the map
                current_pos = this.markers[id].getPosition();
                if (this.point_has_moved(current_pos.lat(), current_pos.lng(), lat, lon)) {
                    console.log(name);
                    this.markers[id].setPosition(new google.maps.LatLng(lat, lon));
                } else {
                    if (name.includes('BURRARD')) {
                        console.log(name + ' has not moved.');
                    }
                }
            } else {
                // create a new marker
                var boatLatLon = new google.maps.LatLng(lat, lon);
                icon = this.setIcon(name);
                var marker = new SlidingMarker({
                    position: boatLatLon,
                    icon: icon
                });
                marker.setMap(this.map);
                this.markers[id] = marker;
            }
        }
    },

    setIcon: function(name) {
        // return wifi enabled icon for boats which have wifi installed
        if (name.includes('OTTER II') || name.includes('PACIFIC BRZE')) {
            return '/img/seabus-wifi.png';
        } else {
            return '/img/seabus.png';
        }
    },

    getBoatsSocketIO: function() {
        // establish websocket connection
        var socket = io.connect('/seabus_data')
        document.beforeUnload = function() { socket.disconnect() }
        var that = this;
        socket.on('seabus_moved', function(data) {
            that.updateMap(data);
            console.log('seabus_moved event received');
        });
    },

    createAboutBox: function() {
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
    },
}

