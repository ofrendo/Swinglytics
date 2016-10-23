//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();


//Register User @ Raspberry
router.get('/', function(req, res){
  var body = req.body;
  var body_userid = body.userid;
  var body_stationid = body.stationid;
});


//Return router
module.exports = router;
