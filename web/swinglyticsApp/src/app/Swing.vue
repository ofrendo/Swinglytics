<template>
  <div>
      <div class="container-fluid swinglytics-navbar-alt">
      <div class="container">
        <div class="navbar-custom ">
          <div class="swinglytics-brand">Swing Analyzer <span id="swingAnalyzerCount">({{parseInt(videoIndex)+parseInt(1)}}/{{session.videos.length}})</span></div>
        </div>
      </div>
    </div>


    <div class="container col-nopad video-container" >
  <div clas="row">
    <div class="col-xs-12 col-nopad">

      <div class="video-wrapper text-center embed-responsive embed-responsive-4by3">
          <video id="swingVideo" style="visibility:hidden;" v-bind:src="videoSrc" class="embed-responsive-item" muted autoplay webkit-playsinline="true" playsinline="true">

          <!-- <source id="swingVideoSrc" src="" type="video/mp4"> -->
            Your browser does not support the video tag.
        </video>
        <canvas id="swingVideoCanvasOverlay"></canvas>
        <!--<div id="favStar" class="favorite-hover" onClick="addRemoveFavorite()"><i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i></div>-->
      </div>
    </div>


    <div class="move-up">
    <div class="col-xs-12 text-center col-nopad">
      <div class="video-controls">
        <!-- keep comments for correct spacing -->
        <button id="playButton" type="button" class="btn btn-default btn-play" v-on:click="startPauseVideo()"><i class="fa fa-play fa-play-cust" aria-hidden="true"></i></button><!--
        --><button id="speedHalfButton" type="button" class="btn btn-default btn-speed" v-on:click="decreaseSpeed()">0.5x</button><!--
        --><button id="speedNormalButton" type="button" class="btn btn-default btn-speed btn-speed-active" v-on:click="resetSpeed()">1x</button><!--
        --><button type="button" class="btn btn-default btn-repeat" v-on:click="repeat()"><i class="fa fa-repeat fa-repeat-cust" aria-hidden="true"></i></button><!--
        --><button id="favStar" type="button" class="btn btn-default btn-favorite" v-on:click="addRemoveFavorite()"><i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i></button>
      </div>
    </div>

      <div class="col-xs-12 text-center col-nopad">
        <div class="video-menu-options">
          <!--<button type="button" class="btn btn-default btn-tag" onclick="showHideTagMenu()"><i class="fa fa-tags" aria-hidden="true"></i></button>--><!--
          --><button type="button" class="btn  btn-divider" v-on:click="previous(videoIndex)">Previous</button><!--
          --><button type="button" class="btn " v-on:click="next(videoIndex)">Next</button>
        </div>
      </div>

      <div class="col-xs-12 text-center col-nopad">
        <div id="tagBox" class="video-tag-options" style="visibility: hidden">
          <button type="button" class="btn btn-default">Good</button><!--
          --><button type="button" class="btn btn-default">Bad</button><!--
          --><button type="button" class="btn btn-default">Great</button><br/>
          <button type="button" class="btn btn-default">Posture</button><!--
          --><button type="button" class="btn btn-default">Angle</button><!--
          --><button type="button" class="btn btn-default">Feet</button><br/>

        </div>
      </div>
    </div>
  </div>
</div>


<nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
  <div class="container">

<button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-check fa-2x"></i><br/>Sessions</button>
<button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-dashcube fa-2x"></i><br/>Dashboard</button>
<button v-on:click="navStationScan" class="col-xs-4"><i class="fa fa-qrcode fa-2x" aria-hidden="true"></i><br/>QR Code</button>

  </div>
</nav>

</div>
</template>


<script>

export default {
  data () {
    return {
      videoSrc: "",
      videoIndex: getParameterByName("videoIndex") || 0,
      session: {
        videos: []
      }
    }
  },


  mounted () {
    var that = this;
    var videoElem = document.querySelector("#swingVideo");
    doRequest("/api/v1/user/sessions", "GET", {}, function(http) {

      var sessions = JSON.parse(http.responseText);
      var sessionID = getParameterByName("sessionID");
      var session = null;
      for (var i=0;i<sessions.length;i++) {
        if (sessions[i].sessionID === sessionID) {
          that.session = sessions[i];
        }
      }

      var videoID = that.session.videos[that.videoIndex].videoID;
      that.videoSrc = buildVideoURL(videoID);
      //videoElem.src = buildVideoURL(videoID);  // buildVideoURL(getParameterByName("videoID"))

      //check initial favorite status
      //if favorite
      if (that.session.videos[that.videoIndex].rating === 1){
        document.getElementById("favStar").innerHTML = '<i class="fa fa-star fa-star-cust" aria-hidden="true"></i>';
      }

      //if not favorite
      else{
        document.getElementById("favStar").innerHTML = '<i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i>'
      }

      VideoOverlay.initCanvasVideoOverlay();
    });

  },

  methods: {

    next: function(videoIndex) {
      if (videoIndex < this.session.videos.length-1) {
        this.videoIndex++;
        VideoOverlay.resetLines();
      }
      console.log("Now at: " + this.videoIndex);
      this.videoSrc = buildVideoURL(this.session.videos[this.videoIndex].videoID);
    },

    previous: function(videoIndex) {
      if (videoIndex > 0) {
        this.videoIndex--;
        VideoOverlay.resetLines();
      }
      console.log("Now at: " + this.videoIndex);
      this.videoSrc = buildVideoURL(this.session.videos[this.videoIndex].videoID);
    },

    navSessions: function (event) {
      this.$router.replace(this.$route.query.redirect || '/sessions');
    },

    navDashboard: function (event) {
      this.$router.replace(this.$route.query.redirect || '/dashboard');
    },

    navStationScan: function (event) {
      this.$router.replace(this.$route.query.redirect || '/StationScan');

    },

    addRemoveFavorite: function (event) {

      //if not yet a favorite check via classes
      if(document.getElementById("favStar").innerHTML == '<i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i>'){

        //do API Call to set favorite
        var that = this;
        var url = "/api/v1/videos/";
        var jsonParams = {
          videoID: videoID,
          rating: 1
        };

        doRequest(url, "POST", jsonParams, function(http) {
          console.log(http);
          console.log(http.status); //returns 200, 403, etc IF STATUS CHECKEN
          console.log(http.responseText); //returns text if any is returned (see documentation)
          console.log(this);
          console.log(that);
            if(http.status === 200){
              console.log(that);
              // add to favorite and replace star
              that.document.getElementById("favStar").innerHTML = '<i class="fa fa-star fa-star-cust" aria-hidden="true"></i>';
            }
        });
      }

      //if not a favorite check via classes
      else{

        //do API Call
        var that = this;
        var url = "/api/v1/videos/";
        var jsonParams = {
          videoID: videoID,
          rating: 0
        };

        doRequest(url, "POST", jsonParams, function(http) {
          console.log(http);
          console.log(http.status); //returns 200, 403, etc IF STATUS CHECKEN
          console.log(http.responseText); //returns text if any is returned (see documentation)
          console.log(this);
          console.log(that);
            if(http.status === 200){
              console.log(that);
              /// delete from favorites
              that.document.getElementById("favStar").innerHTML = '<i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i>'
            }
        });
      }
    },

    startPauseVideo: function () {
      //document.getElementById("swingVideo").play();
      if (document.getElementById("playButton").innerHTML == '<i class="fa fa-play fa-play-cust" aria-hidden="true"></i>'){
        console.log("Play button was pressed");
        document.getElementById("playButton").innerHTML = '<i class="fa fa-pause fa-pause-cust" aria-hidden="true"></i>';
        document.getElementById("swingVideo").play();
      }
      else{
        document.getElementById("playButton").innerHTML = '<i class="fa fa-play fa-play-cust" aria-hidden="true"></i>';
        document.getElementById("swingVideo").pause();
      }
    },

    decreaseSpeed: function () {
      if(document.getElementById("speedHalfButton").className.match(/(?:^|\s)btn-speed-active(?!\S)/)){
      // button is already active
      }
      else{
        // add active class
        document.getElementById("speedHalfButton").className += " btn-speed-active";
        // check if "normal" speed is active remove active class
        if(document.getElementById("speedNormalButton").className.match(/(?:^|\s)btn-speed-active(?!\S)/)){
          document.getElementById("speedNormalButton").className = document.getElementById("speedNormalButton").className.replace( /(?:^|\s)btn-speed-active(?!\S)/g , '' )
        }
      }
      document.getElementById("swingVideo").playbackRate = 0.5;
      //document.getElementById("swingVideo").play();
    },

    repeat: function () {
      document.getElementById("swingVideo").currentTime = 0;
      document.getElementById("swingVideo").play();
      document.getElementById("playButton").innerHTML = '<i class="fa fa-pause fa-pause-cust" aria-hidden="true"></i>';
    },

    resetSpeed: function (){
      document.getElementById("swingVideo").playbackRate = 1;
      //document.getElementById("swingVideo").play();

      if(document.getElementById("speedNormalButton").className.match(/(?:^|\s)btn-speed-active(?!\S)/)){
        // if it already has the class do nothing
      }
      else{
        // add active class
        document.getElementById("speedNormalButton").className += " btn-speed-active";
        // check if "halfSpeed" is active
        if(document.getElementById("speedHalfButton").className.match(/(?:^|\s)btn-speed-active(?!\S)/)){
          document.getElementById("speedHalfButton").className = document.getElementById("speedHalfButton").className.replace( /(?:^|\s)btn-speed-active(?!\S)/g , '' )
        }
      }
    }



  }

}

</script>
