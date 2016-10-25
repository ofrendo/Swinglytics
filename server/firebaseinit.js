//Firebase Setup
var firebase = require('firebase');
firebase.initializeApp({
serviceAccount: "./service_account.json",
databaseURL: "https://hopinone.firebaseio.com"
});

module.exports = firebase;
