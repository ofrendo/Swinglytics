var express   = require('express');
var app       = express();
var router    = express.Router();

var mongoose = require("mongoose");
var Station = require("../models/stationModel.js");

// Calls for adding and checking stations (called manually)
router.get("/", function(req, res, next) {
	Station.find({}, function(err, stations) {
		if (err) {
			res.status(500).send(err);
			return;
		}
		res.status(200).send(stations);
	});
});

// Create a new station
router.post("/", function(req, res, next) {

	var station = new Station();
	station.stationID = req.body.stationID;
	station.currentUserID = "";
	station.publicKey = req.body.publicKey;
	station.save(function(err) {
		if (err) {
			res.status(500).send(err);
			console.log("Error creating a new station: " + err);
			return;
		}
		res.status(200).send("");
	});

});


function getStation(stationID, callback) {
	Station.findOne({"stationID": stationID}, callback);
}

function createStation(stationID, publicKey, callback) {
	var station = new Station();
	station.stationID = stationID;
	station.currentUserID = "";
	station.publicKey = publicKey;
	station.save(callback);
}

function deleteStation(stationID, callback) {
	Station.find({"stationID": stationID}).remove(callback);
}

router.dbMethods = {
	getStation: getStation,
	createStation: createStation,
	deleteStation: deleteStation
};




module.exports = router;