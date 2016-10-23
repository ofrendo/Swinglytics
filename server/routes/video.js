//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();
var firebase = require('../firebaseinit');


//Rasperry posts a Video
router.post('/', function(req, res){
  var body = req.body;
  var body_userid = body.userID;
  var body_stationid = body.stationID;
  var body_timestamp = body.timestamp;
  var body_random = body.random;
  var body_signature = body.signature;

  //Check Parameters
  if(body_userid == undefined || body_stationid == undefined || body_timestamp== undefined || body_random== undefined || body_signature== undefined)
  {
    console.log("Error with Parameters");
    res.status(500).send('Parameters missing or false');
  }
  else{
    console.log("Parameters correct")
  }

  //Upload to Firebase
  var videoid = body_stationid+"_"+body_timestamp+"_"+body_random;
  var ref = firebase.database().ref("user/"+body_userid+"/videos");
  ref.child(videoid).set({
    'rating': -1,
    'tags': ''
  }).then(function()
  {
    // The Promise was accepted.
    res.status(200).send("Nice!");
  }, function(error)
  {
    // The Promise was rejected.
    console.error(error);
    res.status(500).send('Something broke!');
  });
  });

//Return router
module.exports = router;
