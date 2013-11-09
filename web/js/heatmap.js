function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(38, -95),
    zoom: 4,
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

  // Styles
  var styles = [
    {
      stylers: [
        { hue: "#00ffe6" },
        { saturation: -20 }
      ]
    },{
      featureType: "road",
      elementType: "geometry",
      stylers: [
        { lightness: 100 },
        { visibility: "simplified" }
      ]
    },{
      featureType: "road",
      elementType: "labels",
      stylers: [
        { visibility: "off" }
      ]
    }
  ];
  // Set to map
  map.setOptions({styles: styles});

  tweets();
}

var script = 'js/tweets.json';

var tweets = $.getJSON(script, function(data) {
    var tweetly = script.tweets[i];
    var coords = tweets.coordinates;
    console.log(coords);
    var latLng = new google.maps.LatLng(coords[1],coords[0]);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
  });

function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?libraries=geometry,visualization&key=AIzaSyD8o5eliFAEzQ4uHwjOUQMGe7wNCbZGTeE&sensor=true&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;