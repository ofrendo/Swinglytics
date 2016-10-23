var express = require('express');
var bodyParser = require('body-parser');
var app = express();

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

app.post("/video", function(req, res){
	// Post to firebase
	console.log(req.body)
	res.send(req.body) // echo what was sent
});

console.log("Starting server...")

app.listen(3000);