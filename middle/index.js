var express = require('express');
var app = express();

app.get('/', function(req, res){
  res.header("Access-Control-Allow-Origin", "*");
  res.send('hello world');
  console.log('Server started on localhost:3000....')
  console.log(req);
}).listen(3000);