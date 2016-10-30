//Dependencies
var express   = require('express');
var router    = express.Router();
var mongoose = require('mongoose');
var usermodel = require('../models/user.js');


//Add User
router.get('/', function(req, res){

var User = mongoose.model('User',usermodel);

var person_data = {
  username: 'Dome1',
  password: 'pass123',
  email: 'dome@fox.de'
};

var person = new User(person_data);

person.save( function(error, data){
    if(error){
        res.json(error);
    }
    else{
        res.json(data);
    }
});

  User.find({}, function(error, data){
      console.log(data);
      res.json(data);
  });



});

//Return router
module.exports = router;
