function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(-15, -55),
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

  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'js/tweets.json', true);
  xhr.onload = function() {
    loadTweets(this.responseText);
  };
  xhr.send();

  function loadTweets(results) {
    var obj = $.parseJSON( results );
    console.log(obj);
    for(var key in obj){
      console.log('key name: ' + key + ' value: ' + obj[key]);
    }
  }
  // var heatmap = new google.maps.visualization.HeatmapLayer({
  //   data: heatMapData
  // });

  // heatmap.setMap(map);
}


function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?libraries=geometry,visualization&key=AIzaSyD8o5eliFAEzQ4uHwjOUQMGe7wNCbZGTeE&sensor=true&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;