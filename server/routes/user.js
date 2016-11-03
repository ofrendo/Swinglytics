//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();
var passport = require("passport");

var User = require('../models/userModel.js');
var Station = require("../models/stationModel.js");


/* Handle Login POST */
router.post('/login', passport.authenticate('login', {
  successRedirect: '/authSuccess',
  failureRedirect: '/authFailure',
  failureFlash : true 
}));


/* Handle Registration POST */
router.post('/register',
  passport.authenticate('register', {
    successRedirect: '/authSuccess',
    failureRedirect: '/authFailure',
    failureFlash : true
  }),
  function(err, req, res, next) {
    // failure in login test route
    console.log(err);
    return res.send({'status':'err','message':err.message});
  }
);

/* Handle Logout */
router.get('/logout', function(req, res) {
  req.logout();
  res.redirect('/authSuccess');
});


/* Get all videos for user */
// This needs to be changed, instead deliver all sessions with all videos
router.get("/sessions", function (req, res, next) {
  if (!req.isAuthenticated()) {
    console.log("[GET /user/sessions] User is NOT logged in!")
    res.status(403).send("");
    return;
  }
  User.findOne({"username": req.user.username}, function(err, user) {
    if (err) {
      console.log('[GET /user/sessions] Error in finding userID while getting videos: '+ err);
      res.status(500).send("");
      return;
    }

    console.log("[GET /user/sessions] User with userID=" + req.user.username + " has " + user.sessions.length + " sessions stored.");
    res.status(200).send(user.sessions);
  });

});

router.post("/startSession/:stationID", function(req, res, next) {
  if (!req.isAuthenticated()) {
    console.log("[POST /startSession/:stationID] User is NOT logged in!")
    res.status(403).send("");
    return;
  }

  // Add userID to station node as currently logged in user
  Station.findOne({"stationID": req.params.stationID}, function(err, station) {
    if (err){
      console.log('[POST /startSession/:stationID] Error in finding stationID: '+err);
      res.status(500).send("");
      return;
    }
    if (!station) {
      console.log("[POST /startSession/:stationID] Station with stationID=" + req.params.stationID + " not found");
      res.status(404).send("");
      return;
    }

    station.currentUserID = req.user.username;
    station.save(function(err) {
      if (err){
        console.log('[POST /startSession/:stationID] Error in saving currentUserID to station: '+err);
        res.status(500).send("");
        return;
      }

      // Next, add a new session to user
      User.findOne({"username": req.user.username}, function(err, user) {
        if (err){
          console.log('[POST /startSession/:stationID] Error in finding user: '+err);
          res.status(500).send("");
          return;
        } 

        var newSession = {
          sessionID: req.params.stationID + "_" + (new Date()).getTime(),
          videos: []
        }

        user.sessions.push(newSession);
        user.save(function(err) {
          if (err){
            console.log('[POST /startSession/:stationID] Error in saving user: '+err);
            res.status(500).send("");
            return;
          }

          console.log("[POST /startSession/:stationID] Saved a new session" +
                      " with stationID=" + req.params.stationID + 
                      ", with userID=" + req.user.username +
                      ", with sessionID=" + newSession.sessionID);
          res.status(200).send("");
        })

      });
    });

  });

});

router.post("/endSession/:stationID", function(req, res, next) {
  if (!req.isAuthenticated()) {
    console.log("[POST /endSession/:stationID] User is NOT logged in!")
    res.status(403).send("");
    return;
  }

  Station.findOne({"stationID": req.params.stationID}, function(err, station) {
    if (err){
      console.log('[POST /endSession/:stationID] Error in finding stationID: '+err);
      res.status(500).send("");
      return;
    }
    if (!station) {
      console.log("[POST /endSession/:stationID] Station with stationID=" + req.params.stationID + " not found");
      res.status(404).send("");
      return;
    }

    station.currentUserID = "";
    station.save(function(err) {
      if (err){
        console.log('[POST /startSession/:stationID] Error in saving station: '+err);
        res.status(500).send("");
        return;
      }

      console.log("[POST /startSession/:stationID] Ended a session" +
                      " with stationID=" + req.params.stationID + 
                      ", with userID=" + req.user.username);
      res.status(200).send("");
    });
  });

});




//Return router
module.exports = router;
