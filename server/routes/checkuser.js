//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();


//Check Current User @ Station
router.get('/:stationid', function(req, res){
  var stationid= req.params.stationid;
  var userid;
  console.log("StationID: "+stationid);


  var ref = firebase.database().ref("station/"+stationid+"/currentuser");
  ref.once('value')
  .then(function(dataSnapshot)
  {
    // The Promise was accepted.
    userid = dataSnapshot.val();
    var body = {"stationID":stationid, "userID":userid};
    res.status(200).send(body);
  }, function(error)
  {
    // The Promise was rejected.
    console.error(error);
    res.status(500).send('Something broke!');
  });
});

//Return router
module.exports = router;
