//Dependencies
var express   = require('express');
var app       = express();
var router    = express.Router();


//Get all Videos
router.get('/', function(req, res){
console.log("Request for ALL Video IDs");
});

//Rasperry posts a Video
router.post('/', function(req, res){
  var body = req.body;
  var body_userid = body.userid;
  var body_videourl = body.videourl;
  var body_thumbnailurl = body.thumbnailurl;
  var body_timestamp = body.timestamp;

  //Check Parameters
  if(body_userid == undefined || body_videourl == undefined || body_thumbnailurl == undefined || body_timestamp == undefined)
  {
    console.log("Error with Parameters");
    res.status(500).send('Parameters missing or false');
  }
  else{
    console.log("Parameters correct")
  }

  //Build video
  var video = {
	"userid": body_userid,
	"videoUrl": body_videourl,
	"thumbnailUrl": body_thumbnailurl,
	"timestamp": body_timestamp
  }
  //Connect to Firebase
  const FirebaseREST = require('firebase-rest').default;
  var jsonClient  = new FirebaseREST.JSONClient('https://hopinone.firebaseio.com');
  jsonClient.post('/user/'+body_userid+'/session',video)
    .then(console.log)
    .catch(
      console.log);
  });

//Get a Video with ID
router.get('/:id', function(req, res){
  var videoid= req.params.method;
  console.log("Request for Video ID: "+videoid);
  jsonClient.get('/user/'+body_userid+'/session',video);
});


//Delete a Video with ID
router.delete('/:id', function(req, res){
  var videoid= req.params.method;
  console.log("Delete Request for Video ID: "+videoid);
});

//Return router
module.exports = router;
