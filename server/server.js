//Dependencies
var express = require('express');
var bodyParser = require('body-parser');

//Express Setup
var app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

//API Routing
app.use('/api/v1/video', require('./routes/video'));
app.use('/api/v1/login', require('./routes/login'));
app.use('/api/v1/logout', require('./routes/logout'));

//Start NodeJS Server
app.listen(3000);
console.log('API IS RUNNING on Port 3000');
