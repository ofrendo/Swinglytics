var mongoose = require('mongoose');
var schema = mongoose.Schema;

var userSchema = new schema({
  username: String,
  password: String,
  email: String
});

var model = mongoose.model('User', userSchema);

module.exports = model;
