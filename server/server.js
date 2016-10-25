//Dependencies
var express = require('express');
var bodyParser = require('body-parser');

//Express Setup
var app = express();


app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());


//API Routing
app.use('/api/v1/video', require('./routes/video'));
app.use('/api/v1/checkuser', require('./routes/checkuser'));

//Start NodeJS Server
var port = 3000; //Change Port here
app.listen(port);
console.log('API IS RUNNING on Port: ' + port);
