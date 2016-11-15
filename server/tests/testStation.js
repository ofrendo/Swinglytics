var expect = require("chai").expect;
var mongoose = require("mongoose");

var stationRouter = require("../routes/station.js");
var dbConfig = require("../db.js");

var db = mongoose.connection;

db.on('error', console.error);
db.once('open', function() {
  console.log('[DB] MongoDB connection is opened.');
});

console.log("[DB] Opening connection to MongoDB...");
mongoose.connect(dbConfig.url);


var testStationID = -1;

// Unit test to add a station, then get to see if it's there, then remove it, check if it's removed
describe("Station unit tests", function() {

	it("Should create, get, remove, check a new station", function(done) {

		// Create
		stationRouter.dbMethods.createStation(testStationID, "", function(err) {
			expect(err).to.equal(null);

			// Get
			stationRouter.dbMethods.getStation(testStationID, function(err, station) {
				expect(err).to.equal(null);
				expect(station).to.not.equal(null);

				// Remove
				stationRouter.dbMethods.deleteStation(testStationID, function(err) {
					expect(err).to.equal(null);

					// Check
					stationRouter.dbMethods.getStation(testStationID, function(err, station) {
						expect(err).to.equal(null);
						expect(station).to.equal(null);
						done();
					});
				});

			});

		});

	});

});
