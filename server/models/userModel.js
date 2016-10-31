var mongoose = require('mongoose');
var schema = mongoose.Schema;

// See http://mongoosejs.com/docs/schematypes.html for more examples
var userSchema = new schema({
  username: String,
  password: String,
  email: String,
  firstname: String,
  lastname: String,
  videos: [
  	{
  		videoID: String,
  		rating: Number,
  		tags: String
  	}
  ]
});

var model = mongoose.model('User', userSchema);

module.exports = model;