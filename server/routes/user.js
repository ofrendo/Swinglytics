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

// Delete session with specific ID
router.delete("/sessions/:sessionID", function(req, res, next) {
   
   if (!req.isAuthenticated()) {
    console.log("[DELETE /user/sessions] User is NOT logged in!")
    res.status(403).send("");
    return;
  }
  User.findOne({"username": req.user.username}, function(err, user) {
    if (err) {
      console.log('[DELETE /user/sessions] Error in finding userID while getting videos: '+ err);
      res.status(500).send("");
      return;
    }
    var index = -1;
    for (var i=0;i<user.sessions.length;i++) {
      if (user.sessions[i].sessionID === req.params.sessionID) {
        index = i;
      }
    }
    if (index === -1) {
      console.log('[DELETE /user/sessions] Error in finding userID while getting videos: '+ err);
      res.status(404).send("");
      return;
    }
    console.log("[DELETE /user/sessions] User with userID=" + req.user.username + " had " + user.sessions.length + " sessions.");
    user.sessions.splice(index, 1);
    user.save(function(err) {
      console.log("[DELETE /user/sessions] User with userID=" + req.user.username + " has " + user.sessions.length + " sessions stored.");
      res.status(200).send("");
    });
    
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

// Update a video's tags and rating
router.post("/videos/:videoID", function(req, res, next) {
  if (!req.isAuthenticated()) {
    console.log("[POST /user/videos/:videoID] User is NOT logged in!")
    res.status(403).send("");
    return;
  }

  User.findOne({"username": req.user.username}, function(err, user) {
    if (err) {
      console.log('[POST /user/videos/:videoID] Error in finding userID while getting videos: '+ err);
      res.status(500).send("");
      return;
    }

    var done = false;
    for (var i=0;i<user.sessions.length;i++) {
      for (var j=0;j<user.sessions[i].videos.length;j++) {
        if (user.sessions[i].videos[j].videoID === req.params.videoID) {
          user.sessions[i].videos[j].rating = req.body.rating;
          user.sessions[i].videos[j].tags = req.body.tags;
          done = true;
          break;
        }
      }
    }
    if (done === false) {
      console.log("[POST /user/videos/:videoID] video with videoID=" + req.params.videoID + " not found.");
      res.status(404).send("");
      return;
    }
    user.save(function() {
      console.log("[POST /user/videos/:videoID] video with videoID=" + req.params.videoID + " updated with rating=" + req.body.rating + ", tags=" + req.body.tags);
      res.status(200).send("");
    });
  });

});




//Return router
module.exports = router;
