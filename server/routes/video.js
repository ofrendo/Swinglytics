//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();
var firebase  = require('../firebaseinit');
var ursa      = require('ursa');
var sha256    = require('js-sha256');
var NodeRSA = require('node-rsa');
var fs        =require('fs');
var crypto = require("crypto");
var publickey;


//Rasperry posts a Video
router.post('/', function(req, res)
{
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
  else
  {
    console.log("Parameters correct")
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
    var SignForProof = body_stationid+"_"+body_timestamp+"_"+body_random;
    var hashesSign   = sha256(SignForProof);
    console.log("HashedSignature: \n"+hashesSign);


    var privkey = ursa.createPrivateKey(fs.readFileSync('./id_rsa_private.pem'));
    var pubkey  = privkey.toPublicPem();

    var msg = privkey.privateEncrypt('test123', 'utf8', 'base64',ursa.RSA_NO_PADDING);
    console.log('Encrypted:\n', msg, '\n');







/*
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
  */
  });



//Return router
module.exports = router;
