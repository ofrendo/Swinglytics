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
  var body_userid = body.userID;
  var body_stationid = body.stationID;
  var body_timestamp = body.timestamp;
  var body_random = body.random;
  var body_signature = body.signature;

  //Check Parameters
  if (body_userid == undefined || body_stationid == undefined || body_timestamp== undefined || body_random== undefined || body_signature== undefined) {
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
  User.findOne({'username': body_userid}, function(err, user) {
    // In case of any error return
    if (err){
      console.log('[POST /video] Error in finding userID while pushing video: '+err);
      res.status(500).send("");
      return;
    }
    if (!user) {
      console.log("[POST /video] User with userID=" + body_userid + " not found");
      res.status(404).send("");
    }
    else {
      console.log("[POST /video] User with userID=" + body_userid + " has " + user.videos.length + " videos stored.");
      user.videos.push({
        videoID: body_stationid + "_" + body_timestamp + "_" + body_random,
        rating: 5,
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
