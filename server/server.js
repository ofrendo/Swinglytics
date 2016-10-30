//Dependencies
var express = require('express');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var dbConfig = require('./db.js');
var passport = require('passport');
var expressSession = require('express-session');


// Configuring Passport
//app.use(expressSession({secret: 'mySecretKey'}));
//app.use(passport.initialize());
//app.use(passport.session())

//Express Setup
var app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

//API Routing
app.use('/api/v1/video', require('./routes/video'));
app.use('/api/v1/checkuser', require('./routes/checkuser'));
app.use('/users', require('./routes/users'));


//Start NodeJS Server
var port = 3000; //Change Port here
app.listen(port);
console.log('API IS RUNNING on Port: ' + port);

//Start database
var db = mongoose.connection;

db.on('error', console.error);
db.once('open', function() {
  console.log('open');
});

mongoose.connect('mongodb://localhost/test');
