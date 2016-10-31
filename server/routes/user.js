//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var bCrypt = require("bcrypt-nodejs")

var User = require('../models/userModel.js');



passport.serializeUser(function(user, done) {
  //console.log("SerializeUser called: " + user)
  done(null, user._id);
});
 
passport.deserializeUser(function(id, done) {
  //console.log("deserializeUser called: " + id);
  User.findById(id, function(err, user) {
    done(err, user);
  });
});

passport.use('login', new LocalStrategy({
    passReqToCallback : true
  },
  function(req, username, password, done) { 
    // check in mongo if a user with username exists or not
    User.findOne({ 'username' :  username }, 
      function(err, user) {
        // In case of any error, return using the done method
        if (err)
          return done(err);
        // Username does not exist, log error & redirect back
        if (!user){
          console.log('User Not Found with username '+username);
          return done(null, false, 
                req.flash('message', 'User Not found.'));                 
        }
        // User exists but wrong password, log the error 
        if (!isValidPassword(user, password)){
          console.log('Invalid Password');
          return done(null, false, 
              req.flash('message', 'Invalid Password'));
        }
        // User and password both match, return user from 
        // done method which will be treated like success
        console.log("[POST /user/login] User with username=" + username + " logged in.");
        return done(null, user);
      }
    );
}));

passport.use('register', new LocalStrategy({
    passReqToCallback : true
  },
  function(req, username, password, done) {
    findOrCreateUser = function(){
      // find a user in Mongo with provided username
      User.findOne({'username':username},function(err, user) {
        // In case of any error return
        if (err){
          console.log('[POST /user/register] Error in Register: '+err);
          return done(err);
        }
        // already exists
        if (user) {
          console.log('[POST /user/register] User already exists');
          return done(null, false, 
             req.flash('message','User Already Exists'));
        } else {
          // if there is no user with that email
          // create the user
          var newUser = new User();
          // set the user's local credentials
          newUser.username = username;
          newUser.password = createHash(password);
          newUser.email = req.param('email');
          newUser.firstname = req.param('firstname');
          newUser.lastname = req.param('lastname');
 
          // save the user
          newUser.save(function(err) {
            if (err){
              console.log('Error in Saving user: '+err);  
              throw err;  
            }
            console.log('[POST /user/register] User Registration succesful');    
            return done(null, newUser);
          });
        }
      });
    };

    // Delay the execution of findOrCreateUser and execute 
    // the method in the next tick of the event loop
    process.nextTick(findOrCreateUser);
  })
);


var isValidPassword = function(user, password){
  return bCrypt.compareSync(password, user.password);
}



// Generates hash using bCrypt
var createHash = function(password){
 return bCrypt.hashSync(password, bCrypt.genSaltSync(10), null);
}



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
router.get("/videos", function (req, res, next) {
  if (!req.isAuthenticated()) {
    console.log("[GET /user/videos] User is NOT logged in!")
    res.status(403).send("");
    return;
  }
  User.findOne({'username': req.user.username}, function(err, user) {
    if (err) {
      console.log('[GET /user/video] Error in finding userID while getting videos: '+ err);
      res.status(500).send("");
      return;
    }

    console.log("[GET /user/video] User with userID=" + req.user.username + " has " + user.videos.length + " videos stored.");
    res.status(200).send(user.videos);
  });

});


//Return router
module.exports = router;
