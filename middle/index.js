var express = require('express');
var app = express();

app.get('/', function(req, res){
  res.send('hello world');
  console.log('Server started on localhost:3000....')
});

app.listen(3000);