//Dependencies
var express = require('express');
var expressSession = require('express-session');
var bodyParser = require('body-parser');
var flash = require('connect-flash');
var mongoose = require('mongoose');
var passport = require('passport');


var dbConfig = require('./db.js');


//Express Setup
var app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json()); // RY IF WE CAN STILL USE THIS
app.use(flash());


//Start database connection
var db = mongoose.connection;

db.on('error', console.error);
db.once('open', function() {
  console.log('[DB] MongoDB connection is opened.');
});

console.log("[DB] Opening connection to MongoDB...");
mongoose.connect(dbConfig.url);


// Configuring Passport
app.use(expressSession({secret: 'mySecretKey'}));
app.use(passport.initialize());
app.use(passport.session())

require("./initPassport.js");




//API Routing
app.use("/api/v1/station", require("./routes/station"));
app.use('/api/v1/video', require('./routes/video')); // includes POST /
app.use('/api/v1/checkuser', require('./routes/checkuser')); // includes GET / (call for rpi to check if anyone is currently logged in)
app.use('/api/v1/user', require('./routes/user')); // includes POST /login, POST /register, GET /videos

app.get("/authSuccess", function(req, res){
	res.status(200).send("");
});
app.get("/authFailure", function(req, res) {
	res.status(403).send("");
});



//Start NodeJS Server
var port = 3000; //Change Port here
app.listen(port);
console.log('[SERVER] API is running on port: ' + port);


