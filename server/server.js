//Dependencies
var express = require('express');
var expressSession = require('express-session');
var bodyParser = require('body-parser');
var flash = require('connect-flash');
var mongoose = require('mongoose');
var passport = require('passport');
var https = require("https");
var fs = require("fs");

var argv = require('minimist')(process.argv.slice(2));
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
app.use(expressSession({
	secret: 'mySecretKey'
	//, cookie: { domain: 'localhost'}
}));
app.use(passport.initialize());
app.use(passport.session())

require("./initPassport.js");

/*if (!argv.originDomain) {
	console.log("ERR: Please supply an origin domain where the frontend is hosted: --originDomain=https://localhost:3001")
	return;
}*/

// Allow requests to come from other domains
app.all('/*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", req.headers.origin); // just allow all origins
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Credentials", "true");
  next();
});

//API Routing
app.use("/api/v1/station", require("./routes/station"));
app.use('/api/v1/video', require('./routes/video')); // includes POST /
app.use('/api/v1/checkuser', require('./routes/checkuser')); // includes GET / (call for rpi to check if anyone is currently logged in)
app.use('/api/v1/user', require('./routes/user')); // includes POST /login, POST /register, GET /videos

app.get("/authSuccess", function(req, res){
	//console.log("/authSuccess");
	res.status(200).send("");
});
app.get("/authFailure", function(req, res) {
	//console.log("/authFailure");
	res.status(403).send("");
});

// For offline use case: allow videos uploaded to the ../storage directory to be accessed
app.use('/ftp', express.static('../storage'))


//Start NodeJS Server
var port = 3000; //Change Port here

// Check if https should be used: command line arg --ssl
if (argv.ssl === true) {
	/*if (!argv.serverLocation) {
		console.log("When using --ssl, please supply --serverLocation=local")
	}*/

	var options = {
	    //key: fs.readFileSync('./id_rsa_private.pem'), // rpi private key
	    key: fs.readFileSync('../web/QRTest/server.key'), //generated key for QR test
	    //cert: fs.readFileSync('./id_rsa.pem')
	    cert: fs.readFileSync('../web/QRTest/server.crt') //generated key for QR test
		
		// DO golf-innovation.com
	    //key: fs.readFileSync("/etc/letsencrypt/live/golf-innovation.com/privkey.pem"), 
	    //key: fs.readFileSync("/etc/letsencrypt/live/golf-innovation.com/fullchain.pem"),
	    //ca: fs.readFileSync('/etc/letsencrypt/live/golf-innovation.com/chain.pem')
	};
	var server = https.createServer(options, app).listen(port, function(){
		console.log('[SERVER] HTTPS API is running on port: ' + port);
	});
}
else {
	app.listen(port);
	console.log('[SERVER] HTTP API is running on port: ' + port);
}





