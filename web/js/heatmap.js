function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(38, -95),
    zoom: 4,
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

  // STYLES
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

  // Create a script tag and set the USGS URL as the source.
  var script = document.createElement('script');
  script.src = 'http://earthquake.usgs.gov/earthquakes/feed/geojsonp/2.5/week';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(script, s);

  window.eqfeed_callback = function(results) {
    var heatmapData = [];
    for (var i = 0; i < results.features.length; i++) {
      var coords = results.features[i].geometry.coordinates;
      var latLng = new google.maps.LatLng(coords[1], coords[0]);
      var magnitude = results.features[i].properties.mag;
      var weightedLoc = {
        location: latLng,
        weight: Math.pow(2, magnitude)
      };
      heatmapData.push(weightedLoc);
    }
    var heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData,
      dissipating: false,
      map: map
    });
  }

}

function getCircle(magnitude) {
  return {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: 'red',
    fillOpacity: .2,
    scale: Math.pow(2, magnitude) / Math.PI,
    strokeColor: 'white',
    strokeWeight: .5
  };
}

google.maps.event.addDomListener(window, 'load', initialize);