//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();

var Station = require("../models/stationModel.js");

// Check Current User @ Station
router.get('/:stationID', function(req, res){

  Station.findOne({"stationID": req.params.stationID}, function(err, station) {
    if (err){
      console.log('[GET /checkuser/:stationID] Error in finding stationID: '+err);
      res.status(500).send("");
      return;
    }
    if (!station) {
      console.log("[GET /checkuser/:stationID] StationID=" + req.params.stationID + " not found");
      res.status(404).send("");
      return;
    }

    res.status(200).send(station.currentUserID);
  })
  
});

//Return router
module.exports = router;
