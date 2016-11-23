<template>
  <div>
  <div class="container-fluid swinglytics-navbar">
    <div class="container">
      <div class="navbar-custom ">
        <div class="swinglytics-brand">My Dashboard<span class=""><i class="fa fa-sign-out fa-logout-cust" aria-hidden="true"></i></span></div>
      </div>
    </div>
  </div>
<div class="container dashboard-body">
    <div class="row">
      <div class="col-xs-12 col-lg-12 dashboard-wrapper">
        <div class="dash-section-title ">
          <span class="dst-span orange-border">Recent Training</span><span class="dash-section-sub green-text" id="spanRecentSwingCount">X swings</span>
        </div>
        <div class="video-thumbnail-bar">
          <div class="video-thumbnail-bar-info" id="RecentSwingDate">
            No sessions recorded
          </div>
          <div id="divRecentThumbnailsContainer" class="row col-thumbnail">
            <!--  -->

            <div id="divRecentThumbnailsPlay" class="col-xs-3   icon">
              <a href=""><i class="fa fa-play-circle play-green" aria-hidden="true"></i></a>
            </div>
          </div>

        </div>

      </div>
    </div>

      <hr class="dashboard-hr">
    <div class="row">
      <div class="col-xs-12 col-lg-12 dashboard-wrapper">
        <div class="dash-section-title">
          <span class="dst-span">Favorites</span><span class="dash-section-sub orange-text" id="spanFavoriteSwingCount">Y swings</span>
        </div>
        <div class="video-thumbnail-bar">
          <div class="video-thumbnail-bar-info" >
            Review your favorite swings
          </div>
          <div id="divFavouriteThumbnailsContainer" class="row col-thumbnail">
            <!-- -->
            <div id="divFavouriteThumbnailsPlay" class="col-xs-3   icon">
              <i class="fa fa-play-circle play-orange" aria-hidden="true"></i>
            </div>
          </div>

        </div>

      </div>

    </div>

</div>

    <nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
      <div class="container">

<button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-video-camera fa-2x"></i><br/>Sessions</button>
<button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-th-large fa-2x fa-is-active"></i><br/>Dashboard</button>
<button v-on:click="navStationScan" class="col-xs-4"><i class="fa fa-qrcode fa-2x" aria-hidden="true"></i><br/>QR Scan</button>

      </div>
    </nav>

  </div>

</template>

<script>

function getSwingLabel(n) {
  return (n === 1) ?
          "1 swing" :
          n + " swings";
}

export default {
  data () {
    return {
      email: 'kingkuta@example.com',
      pass: '',
      error: false
    }
  },

  created: function () {
    // `this` points to the vm instance
    var that = this;
    //sendGetRequest
    var url = "/api/v1/user/sessions";
    doRequest(url, "GET", {}, function(http) {

      var sessions = JSON.parse(http.responseText);
      console.log(sessions);
      //console.log(sessions[0].timeString);

      // Add last session thumbnails
      var lastSessionVideos = (sessions.length > 0) ?
                               sessions[sessions.length-1].videos :
                               [];
      var divContainer = document.querySelector("#divRecentThumbnailsContainer");
      var playContainer = document.querySelector("#divRecentThumbnailsPlay");
      document.getElementById("spanRecentSwingCount").innerHTML = getSwingLabel(lastSessionVideos.length);
      var RecentSwingDate = document.getElementById("RecentSwingDate");

      for (var i=0; i<Math.min(lastSessionVideos.length, 3);i++) {
        var div = document.createElement("div");
        div.classList.add("col-xs-3");
        var img = document.createElement("img");
        img.dataset.videoIndex = i + "";
        img.dataset.sessionID = sessions[sessions.length-1].sessionID;
        img.classList.add("img-responsive");
        img.classList.add("video-thumbnail");
        img.classList.add("video-thumbnail-clickable");
        img.classList.add("img-circle");
        img.src = buildThumbnailURL(lastSessionVideos[i].videoID);


        div.appendChild(img);
        divContainer.insertBefore(div, playContainer);
      }
      // Add placeholder if any missing
      for (var i=lastSessionVideos.length-3; i<0; i++) {
        var div = document.createElement("div");
        div.classList.add("col-xs-3");
        var img = document.createElement("img");
        img.classList.add("img-responsive");
        img.classList.add("video-thumbnail");
        img.classList.add("img-circle");
        img.src = "app/images/thumbnailPlaceholder.jpg";

        div.appendChild(img);
        divContainer.insertBefore(div, playContainer);
      }

      if (sessions.length > 0) {
        var lastSession = sessions[sessions.length-1];
        var ts = new Date(parseInt(lastSession.sessionID.split("_")[1]))

        var myDate = ts.toString();
        console.log(myDate);
        var dayLong = myDate.split(" ")[0];
        var monthShort = myDate.split(" ")[1];
        var dayCount = myDate.split(" ")[2];
        var year = myDate.split(" ")[3];

        var dateFormatted = dayLong + ". " + monthShort + " " + dayCount + ", " + year;
        console.log("Finished date: " + dateFormatted);

        lastSession.timeString = dateFormatted + " at " + ts.toLocaleTimeString();
        RecentSwingDate.innerHTML = lastSession.timeString;

        // Link player
        playContainer.addEventListener("click", function(e) {
          var sessionID = sessions[sessions.length-1].sessionID;
          that.$router.replace(that.$route.query.redirect || "/Swing?sessionID=" + sessionID);
        });
      }

      // ====================
      // Add favourite videos
      var divContainer = document.querySelector("#divFavouriteThumbnailsContainer");
      var playContainer = document.querySelector("#divFavouriteThumbnailsPlay");
      var favouriteVideos = [];
      var videosAppended = 0;
      for (var i=0;i<sessions.length;i++) {
        for (var j=0;j<sessions[i].videos.length;j++) {
          if (sessions[i].videos[j].rating === 1) {
            favouriteVideos.push(sessions[i].videos[j]);
          }

          if (sessions[i].videos[j].rating === 1 && videosAppended < 3) {
            var div = document.createElement("div");
            div.classList.add("col-xs-3");
            var img = document.createElement("img");
            img.dataset.videoIndex = j + "";
            img.dataset.sessionID = sessions[i].sessionID;
            img.classList.add("img-responsive");
            img.classList.add("video-thumbnail");
            img.classList.add("video-thumbnail-clickable");
            img.classList.add("img-circle");
            img.src = buildThumbnailURL(sessions[i].videos[j].videoID);

            div.appendChild(img);
            divContainer.insertBefore(div, playContainer);
            videosAppended++;
          }
        }
      }
      document.getElementById("spanFavoriteSwingCount").innerHTML = getSwingLabel(favouriteVideos.length);

      // Add placeholder if any missing
      for (var i=videosAppended-3; i<0; i++) {
        var div = document.createElement("div");
        div.classList.add("col-xs-3");
        var img = document.createElement("img");
        img.classList.add("img-responsive");
        img.classList.add("video-thumbnail");
        img.classList.add("img-circle");
        img.src = "app/images/thumbnailPlaceholder.jpg";

        div.appendChild(img);
        divContainer.insertBefore(div, playContainer);
      }

      // Link player
      playContainer.addEventListener("click", function(e) {
        //var sessionID = sessions[sessions.length-1].sessionID;
        //that.$router.replace(that.$route.query.redirect || "/SingleSession?sessionID=" + sessionID);
      });


      var allImages = document.querySelectorAll(".video-thumbnail-clickable");
      for (var i=0;i<allImages.length;i++) {
        allImages[i].addEventListener("click", function(e) {
          var img = e.target;

          that.$router.replace(that.$route.query.redirect || "/Swing?sessionID=" + img.dataset.sessionID + "&videoIndex=" + img.dataset.videoIndex);
        });
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

  //end login
  },




  //end method
  }






</script>
