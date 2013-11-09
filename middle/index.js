/*
var express = require('express');
var app = express();

app.get('/', function(req, res){
  res.header("Access-Control-Allow-Origin", "*");
  res.send('hello world');
  console.log('Server started on localhost:3000....')
  console.log(req);
});

app.listen(3000);
*/

var url = require( "url" );
var queryString = require( "querystring" );
var http = require("http");

http.createServer(
    function (req, res) {

        // parses the request url
        var theUrl = url.parse( req.url );

        // gets the query part of the URL and parses it creating an object
        var queryObj = queryString.parse( theUrl.query );

        // queryObj will contain the data of the query as an object
        // and jsonData will be a property of it
        // so, using JSON.parse will parse the jsonData to create an object
        var obj = JSON.parse( queryObj.jsonData );

        // as the object is created, the live below will print "bar"
        console.log( obj.foo );

    }
).listen(3001);
