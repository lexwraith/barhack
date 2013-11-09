function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(35, -95),
    zoom: 4,
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  // Instantiate the map
  var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

  // Styles, Our map's still pretty ugly
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

  // For the heatmap layer
  var heatmapData = [];
  var heatmap = new google.maps.visualization.HeatmapLayer({});

  // Instantiate counter
  var files = 0;

  // Looping and loading fies with timeout
  (function myLoop (i) {          
    setTimeout(function () {   
      var xhr = new XMLHttpRequest();
      xhr.open('GET', ('js/tweets'+ files + '.json'), true);
      files++;
      if (files >=4){
        files = 0;
      }
      console.log(files);
      xhr.onload = function() {
        loadTweets(this.responseText);
      };
      xhr.send();
      // Clear out map styles          
      if (--i) 
        myLoop(i);
      // Stall for 3 seconds
    }, 3000)
  })(100);  

  // Parse out the JSON and create markers
  function loadTweets(results) {

    // Parse out our JSON file
    var tweetStructure = $.parseJSON(results);
    // heatmap.setMap(null);  

    // Go gets it
    for (a in tweetStructure){
      var co_arr = tweetStructure[a];
      for (coords in co_arr.coordinates){
        var d = co_arr.coordinates;
        
        // Stating our lat/longs 
        var first = d[0];
        var second = d[1];
        var magnitude = d[2];

        // Setting them
        var latLng = new google.maps.LatLng(first, second);

        // Weighted location to express polarity
        var weightedLoc = {
          location: latLng,
          weight: Math.pow(2, magnitude)
        };
        heatmapData.push(weightedLoc);
      }
    }

    heatmap.setMap(null); 
    console.log(heatmap);

    // Instantiate heat map
    heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData,
      dissipating: false,
      map: map
    });
  }
}

function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?libraries=geometry,visualization&key=AIzaSyD8o5eliFAEzQ4uHwjOUQMGe7wNCbZGTeE&sensor=true&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;