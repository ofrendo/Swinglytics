var mongoose = require('mongoose');
var schema = mongoose.Schema;

// See http://mongoosejs.com/docs/schematypes.html for more examples
var stationSchema = new schema({
  stationID: Number,
  currentUserID: String,
  publicKey: String
});

var model = mongoose.model('Station', stationSchema);

module.exports = model;