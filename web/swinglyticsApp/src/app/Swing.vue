<template>
  <div>
      <div class="container-fluid swinglytics-navbar">
      <div class="container">
        <div class="navbar-custom ">
          <div class="swinglytics-brand"><span>Swing Analyzer</span> <span id="swingAnalyzerCount" class="swing-count">{{parseInt(videoIndex)+parseInt(1)}} of {{session.videos.length}}</span></div>
        </div>
      </div>
    </div>


    <div class="container col-nopad video-container">
  <div clas="row">
    <div class="col-xs-12 col-nopad">

      <div class="video-wrapper text-center embed-responsive embed-responsive-4by3">
          <video id="swingVideo" style="visibility:hidden;" v-bind:src="videoSrc" class="embed-responsive-item" webkit-playsinline="true" playsinline="true">

          <!-- <source id="swingVideoSrc" src="" type="video/mp4"> -->
            Your browser does not support the video tag.
        </video>
        <canvas id="swingVideoCanvasOverlay"></canvas>
        <button id="canvasNewLine" class="canvas-btn-newLine btn"><i class="fa fa-paint-brush" aria-hidden="true"></i></button>
        <button id="canvasErase" class="canvas-btn-erase btn"><i class="fa fa-eraser" aria-hidden="true"></i></button>
        <!--<div id="favStar" class="favorite-hover" onClick="addRemoveFavorite()"><i class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i></div>-->
      </div>
    </div>


    <div class="move-up">
    <div class="col-xs-12 text-center col-nopad">
      <div class="video-controls">
        <!-- keep comments for correct spacing: otherwise browsers add tiny amount of pixels between buttons -->
        <button id="playButton" type="button" class="btn btn-default btn-play" v-on:click="startPauseVideo()">
          <i v-if="videoPlaying" class="fa fa-pause fa-pause-cust" aria-hidden="true"></i>
          <i v-if="!videoPlaying" class="fa fa-play fa-play-cust" aria-hidden="true"></i>
        </button><!--
        
        --><button id="speedHalfButton" type="button" class="btn btn-default btn-speed" 
                   v-on:click="decreaseSpeed()"
                   v-bind:class="{'btn-speed-active': playbackSpeed === 0.5}">
           0.5x
        </button><!--

        --><button id="speedNormalButton" type="button" class="btn btn-default btn-speed" 
                   v-on:click="resetSpeed()"
                   v-bind:class="{'btn-speed-active': playbackSpeed === 1}">
          1x
        </button><!--

        --><button type="button" class="btn btn-default btn-repeat" v-on:click="repeat()">
          <i class="fa fa-repeat fa-repeat-cust" aria-hidden="true"></i>
        </button><!--

        --><button id="favStar" type="button" class="btn btn-default btn-favorite" v-on:click="addRemoveFavorite()">
          <i v-if="!isFavorite" class="fa fa-star-o fa-star-o-cust" aria-hidden="true"></i>
          <i v-if="isFavorite" class="fa fa-star fa-star-cust" aria-hidden="true"></i>
        </button>
      </div>
    </div>

      <div class="col-xs-12 text-center col-nopad">
        <div class="video-menu-options">
          <!--<button type="button" class="btn btn-default btn-tag" onclick="showHideTagMenu()"><i class="fa fa-tags" aria-hidden="true"></i></button>--><!--
          --><button type="button" class="btn  btn-divider" v-on:click="previous(videoIndex)">Previous</button><!--
          --><button type="button" class="btn " v-on:click="next(videoIndex)">Next</button>
        </div>
      </div>


    </div>
  </div>
</div>


<nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
  <div class="container">

<button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-video-camera fa-2x "></i><br/>Sessions</button>
<button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-th-large fa-2x"></i><br/>Dashboard</button>
<button v-on:click="navStationScan" class="col-xs-4"><i class="fa fa-qrcode fa-2x" aria-hidden="true"></i><br/>QR Scan</button>

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
      videoPlaying: false,
      playbackSpeed: 1,
      isFavorite: false,
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
          console.log("Loaded session: ");
          console.log(sessions[i]);
          that.session = sessions[i];
        }
      }
      var videoID = that.session.videos[that.videoIndex].videoID;
      that.videoSrc = buildVideoURL(videoID);
      //videoElem.src = buildVideoURL(videoID);  // buildVideoURL(getParameterByName("videoID"))
      videoElem.addEventListener("ended", function(e) {
        that.videoPlaying = false;
      })

      //check initial favorite status
      //if favorite
      if (that.session.videos[that.videoIndex].rating === 1){
        that.isFavorite = true;
      }

      VideoOverlay.initCanvasVideoOverlay();
    });

  },

  methods: {

    next: function(videoIndex) {
      if (videoIndex < this.session.videos.length-1) {
        this.videoIndex++;
        VideoOverlay.resetLines();
        this.videoPlaying = false;
      }
      
      this.resetUIValues();
    },

    previous: function(videoIndex) {
      if (videoIndex > 0) {
        this.videoIndex--;
        VideoOverlay.resetLines();
        this.videoPlaying = false;
      }
      
      this.resetUIValues();
    },

    resetUIValues() {
      console.log("Now at: " + this.videoIndex);
      this.videoSrc = buildVideoURL(this.session.videos[this.videoIndex].videoID);

      var video = this.session.videos[this.videoIndex];
      this.isFavorite = (video.rating === 1) ? true : false;
      this.playbackSpeed = 1;
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

      var newRating = (this.isFavorite === false) ?
                   1 :
                   0;

      // do API Call to set favorite
      var that = this;
      var vidID = that.session.videos[that.videoIndex].videoID;
      console.log("Changing favorite status to " + newRating + " for " + vidID);
      var url = "/api/v1/user/videos/" + vidID;
      var jsonParams = {
        videoID: vidID,
        rating: newRating
      };

      doRequest(url, "POST", jsonParams, function(http) {
        if (http.status === 200){
          that.isFavorite = !that.isFavorite;
        }
      });

    },

    startPauseVideo: function () {
      var videoElem = document.getElementById("swingVideo");
      if (this.videoPlaying === false) {
        videoElem.play();
        this.videoPlaying = true;
      }
      else {
        videoElem.pause();
        this.videoPlaying = false;
      }

    },

    decreaseSpeed: function () {
      this.playbackSpeed = 0.5;
      document.getElementById("swingVideo").playbackRate = 0.5;
    },

    resetSpeed: function (){
      this.playbackSpeed = 1;
      document.getElementById("swingVideo").playbackRate = 1;
    },

    repeat: function () {
      document.getElementById("swingVideo").currentTime = 0;
      document.getElementById("swingVideo").play();
      this.videoPlaying = true;
    }



  }

}

</script>
