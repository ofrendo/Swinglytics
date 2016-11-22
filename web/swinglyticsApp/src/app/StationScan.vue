<template>
  <div>
    <div class="container-fluid swinglytics-navbar">
      <div class="container">
        <div class="navbar-custom ">
          <div class="swinglytics-brand">QR Scan</div>
        </div>
      </div>
    </div>

    <div class="container container-qr-code">
      <div class="row text-center">
        <select class="camera-select-fallback" id="selectCameraInput"></select>
        <video autoplay="true" id="videoCameraInput"></video>
        <canvas id="canvasHiddenQR"></canvas>
       	<!-- <span>Station ID</span> -->
        <input placeholder="Enter station ID or scan" type="text" id="inputStationID"></input>

        <button class="btn onboard-btn" id="buttonSubmitQR" v-on:click="submitStationID()">Start Session</button>
      </div>
    </div>

    <nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
      <div class="container">
        <button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-video-camera fa-2x"></i><br/>Sessions</button>
        <button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-th-large fa-2x"></i><br/>Dashboard</button>
        <button v-on:click="navStationScan" class="col-xs-4"><i class="fa fa-qrcode fa-2x fa-is-active" aria-hidden="true"></i><br/>QR Scan</button>
      </div>
    </nav>
  </div>
</template>
<script>

export default {
	mounted() {
		document.addEventListener("DOMContentLoaded", function(event) {
			// Init QR code scanner
		  	StationIDReader.init({
				selectCameraInputID: "#selectCameraInput",
				videoCameraInputID: "#videoCameraInput",
				inputStationID: "#inputStationID"
			});
			StationIDReader.startReading();
		});
	},

	methods: {
    	submitStationID () {
    		var stationID = document.querySelector("#inputStationID").value;
    		var that = this;
			doRequest("/api/v1/user/startSession/" + stationID, "POST", {}, function(http) {
				if (http.status === 200) {
					// redirect to dashboard
					//alert("Started a new session!");
					console.log("Started a new session!");
					that.$router.replace(that.$route.query.redirect || '/dashboard');
				}
				else {
					console.log("Did not start a session!");
				}
			});
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

    }
}

</script>
