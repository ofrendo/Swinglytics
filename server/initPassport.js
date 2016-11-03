var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var bCrypt = require("bcrypt-nodejs");

var User = require("./models/userModel.js");

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
