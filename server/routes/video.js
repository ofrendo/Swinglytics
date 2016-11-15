//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();
var fs        = require('fs');
var mongoose = require("mongoose");
var User = require("../models/userModel.js");

//var ursa      = require('ursa');
var sha256    = require('js-sha256');
var NodeRSA = require('node-rsa');
var crypto = require("crypto");

var publickey;




//Rasperry posts a Video
router.post('/', function(req, res) {
  var body = req.body;

  //Check Parameters
  if (body.userID == undefined || body.stationID == undefined || body.timestamp== undefined || body.random== undefined || body.signature== undefined) {
    console.log("[POST /video] One or more parameters is missing.");
    res.status(400).send("");
    return;
  }

  /*
  //Get Public Key from Station
  var ref = firebase.database().ref("station/"+body_stationid+"/publicKey");
  ref.once('value')
    .then(function(dataSnapshot)
    {
      // The Promise was accepted.
      publickey = dataSnapshot.val();
    //  console.log(publickey);
    }, function(error)
    {
      // The Promise was rejected.
      console.error(error);
      res.status(500).send('Something broke!');
    });
    */

  //Build signature
  /* var SignForProof = body_stationid+"_"+body_timestamp+"_"+body_random;
  var hashesSign   = sha256(SignForProof);
  console.log("HashedSignature: \n"+hashesSign);


  var privkey = ursa.createPrivateKey(fs.readFileSync('./id_rsa_private.pem'));
  var pubkey  = privkey.toPublicPem();

  var msg = privkey.privateEncrypt('test123', 'utf8', 'base64',ursa.RSA_NO_PADDING);
  console.log('Encrypted:\n', msg, '\n'); */

  // If signature correct, push to mongoDB
  User.findOne({'username': body.userID}, function(err, user) {
    // In case of any error return
    if (err){
      console.log('[POST /video] Error in finding userID while pushing video: '+err);
      res.status(500).send("");
      return;
    }
    if (!user) {
      console.log("[POST /video] User with userID=" + body.userID + " not found");
      res.status(404).send("");
    }
    else {
      console.log("[POST /video] User with userID=" + body.userID + " has " + user.sessions.length + " sessions stored.");

      if (user.sessions.length === 0) {
        console.log("[POST /video] User must have at least one session.");
        res.status(500).send("");
        return;
      }

      // find the correct session to push the video to: the one with max timestamp
      var maxTS = -1;
      var latestSession = null;
      for (var i=0;i<user.sessions.length;i++) {
        var session = user.sessions[i];
        // sessionID is {stationID}_{timestamp}
        var ts = Number(session.sessionID.split("_")[1]);
        if (ts > maxTS) {
          maxTS = ts;
          latestSession = session;
        }
      }

      // Once it is found, push a new video to it
      session.videos.push({
        videoID: body.stationID + "_" + body.timestamp + "_" + body.random,
        rating: 0,
        tags: ""
      });
      user.save(function(err) {
        if (err) {
          console.log("[POST /video] Video NOT added: " + err);
          res.status(500).send("");
        }
        else {
          console.log("[POST /video] Video added and saved.");
          res.status(200).send("");
        }
      });
    }
  });

});



//Return router
module.exports = router;
