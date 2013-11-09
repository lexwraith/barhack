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

  // tweets();

  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?libraries=geometry,visualization&key=AIzaSyD8o5eliFAEzQ4uHwjOUQMGe7wNCbZGTeE&sensor=true&callback=initialize";
  document.body.appendChild(script);

  // Create a <script> tag and set the USGS URL as the source.
        var script = document.createElement('script');
        script.src = 'http://earthquake.usgs.gov/earthquakes/feed/geojsonp/2.5/week';
        document.getElementsByTagName('head')[0].appendChild(script);

      // Loop through the results array and place a marker for each
      // set of coordinates.
      function eqfeed_callback(results){
        for (var i = 0; i < results.features.length; i++) {
          var earthquake = results.features[i];
          var coords = earthquake.geometry.coordinates;
          var latLng = new google.maps.LatLng(coords[1],coords[0]);
          var marker = new google.maps.Marker({
            position: latLng,
            map: map
          });
        }
      }
}

// var script = 'js/tweets.json';

// var tweets = $.getJSON(script, function(data) {
//     var tweetly = script.tweets[i];
//     var coords = tweets.coordinates;
//     console.log(coords);
//     var latLng = new google.maps.LatLng(coords[1],coords[0]);
//     var marker = new google.maps.Marker({
//       position: latLng,
//       map: map
//     });
//   });

window.onload = initialize;