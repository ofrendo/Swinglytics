<template>
<div>
  <div class="container-fluid swinglytics-navbar">
    <div class="container">
      <div class="navbar-custom ">
        <div class="swinglytics-brand">My Sessions</div>
      </div>
    </div>
  </div>

<div class="container">
  <div class="row">
    <div class="col-xs-12 col-lg-12 swing-wrapper">
      <div class="panel-group" id="accordion">

        <!-- each session gets one -->
        <div class="panel panel-default swing-panel" v-for="(session, index) in sessions">
          <div class="panel-heading swing-panel-heading">
            <button v-on:click="navSwing(session.sessionID)" type="button" class="btn session-collection-button"><h4 class="panel-title swing-panel-title">
            <span class="session-number">{{index+1}}.</span> {{session.timeString}}<span class="pull-right swing-subheader">{{session.videos.length}} swings</span>
              </h4></button>
          </div>
        </div>

      </div>
    </div>
  </div>

    <nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
      <div class="container">
        <button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-video-camera fa-2x fa-is-active"></i><br/>Sessions</button>
        <button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-th-large fa-2x"></i><br/>Dashboard</button>
        <button v-on:click="navStationScan" class="col-xs-4"><i class="fa fa-qrcode fa-2x" aria-hidden="true"></i><br/>QR Scan</button>
      </div>
    </nav>
  </div>
</div>

  </template>


  <script>

  export default {
    data () {
      return {
        sessions: []
      }
    },

    created() {
      var that = this;
      doRequest("/api/v1/user/sessions", "GET", {}, function(http) {
        var sessions = JSON.parse(http.responseText);
        for (var i=0;i<sessions.length;i++) {
          var ts = new Date(parseInt(sessions[i].sessionID.split("_")[1]))
          sessions[i].timeString = ts.toLocaleDateString() + " " + ts.toLocaleTimeString();
          that.$data.sessions.push(sessions[i]);
        }
      });

    },

    methods: {

      navSessions: function (event) {
        this.$router.replace(this.$route.query.redirect || '/sessions');
      },

      navDashboard: function (event) {
        this.$router.replace(this.$route.query.redirect || '/dashboard');
      },

      navStationScan: function (event) {
        this.$router.replace(this.$route.query.redirect || '/StationScan');

      },

      navSwing: function (sessionID) {
        this.$router.replace(this.$route.query.redirect || "/swing?sessionID=" + sessionID);

      }

    //end login
    },




    //end method
    }






  </script>
