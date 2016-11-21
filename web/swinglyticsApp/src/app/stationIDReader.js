// sources:
// https://developers.google.com/web/updates/2015/10/media-devices
console.log("Loaded stationIDReader.js");


// Make sure we have a getUserMedia function to call in different browsers
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;
var StationIDReader_CONST = {
	PICTURE_INTERVAL: 1000, // How many ms between each picture taken (will freeze browser each time a few ms)
	BACK_CAMERA_IDS: [
		"camera2 0, facing back" // tested on OnePlus2, Samsung S7
		// Apple does not have enumerateDevices()
	]
}

var StationIDReader = (function() {
	var selectCameraInput = null;
	var videoElem = null;
	var inputStationID = null;

	var canvas = document.createElement("canvas");
	canvas.style.display = "none";

	var qr = new QrCode();
	// options:
	// options.qrCallback: What happens when qr.decode() is called [optional]
	// options.selectCameraInputID: ID for <select> elem
	// options.videoCameraInputID: ID for <video> elem

	function init(options) {
		console.log("[StationIDReader] Init");
		// Add callback to qr what happens when qr.decode() is called
		if (typeof options.qrCallback === "function") {
			qr.callback = options.qrCallback;
		}
		else {
			qr.callback = defaultQRCallback;
		}

		selectCameraInput = document.querySelector(options.selectCameraInputID);
		videoElem = document.querySelector(options.videoCameraInputID);
		inputStationID = document.querySelector(options.inputStationID);

		// Find all mediaDevices available
		navigator.mediaDevices.enumerateDevices().then(function(devices) {
			var videoDevice = null;
			fillDeviceOptions(devices);

			// Loop over available mediaDevices
			devices.forEach(function(device) {
				// device.kind: "audioinput" | "videoinput"
				// device.label: "camera2 0, facing back" (OnePlus2)
				// device.deviceId: Long string
				if (device.kind === "videoinput" &&
					StationIDReader_CONST.BACK_CAMERA_IDS.indexOf(device.label) !== null) {
					// Check if Camera is part of preferred labels
					videoDevice = device;
				}
				else if (device.kind === "videoinput") { // in case camera is named differently, use different
					videoDevice = device;
				}
			});
			setVideoDevice(videoDevice);

			// Set initial ID for the select
			selectCameraInput.value = videoDevice.deviceId;
			//alert(selectCameraInput.length);
			//selectCameraInput.selectedIndex = 2;

			// Add on change event after setting the first videoDevice
			selectCameraInput.onchange = function() {
				var newDeviceId = selectCameraInput.value;
				setVideoDevice({deviceId: newDeviceId});
			};
		})
		/*.catch(function(err) {
			console.log(err);
			alert(err.name + ": " + err.message);
		});*/
	}

	// Fill camera option in case default chosen device is not correct
	function fillDeviceOptions(devices) {
		for (var i = 0; i !== devices.length; ++i) {
			var deviceInfo = devices[i];
			var option = document.createElement('option');
			option.value = deviceInfo.deviceId;
			//if (deviceInfo.kind === 'audioinput') {
			//	option.text = deviceInfo.label ||
			//	'Microphone ' + (audioInputSelect.length + 1);
			//	audioInputSelect.appendChild(option);
			//} else if (deviceInfo.kind === 'audiooutput') {
			//option.text = deviceInfo.label || 'Speaker ' +
			//(audioOutputSelect.length + 1);
			//audioOutputSelect.appendChild(option);
			//}
			if (deviceInfo.kind === 'videoinput') {
				option.text = deviceInfo.label || 'Camera ' + (selectCameraInput.length + 1);
				selectCameraInput.appendChild(option);
			}
		}
	}

	// Called upon deciding which device should be used
	function setVideoDevice(device) {
		console.log("[StationIDReader] Using device for video stream: ");
		console.log(device);
		if (navigator.getUserMedia) {
		    //navigator.getUserMedia({video: true}, handleVideo, videoError);
		    //navigator.getUserMedia({video: { facingMode: { exact: "environment" } } }, handleVideo, videoError);
		    var constraints = {
		    	video: {deviceId: {exact: device.deviceId}}
		    };
		    navigator.getUserMedia(constraints, handleVideo, videoError);
		}
		else {
			alert("unable to create video")
		}
	}

	// Callback for finding a video stream
	function handleVideo(stream) {
		var url = window.URL.createObjectURL(stream);
	    videoElem.src = url;
	}

	// Callback for not finding a video stream
	function videoError(e) {
	    alert("videoError: " + e.message)
	}

	// Called every x ms to reread video input
	function takePicture() {
	    var context = canvas.getContext('2d');
		canvas.width = videoElem.offsetWidth;
		canvas.height = videoElem.offsetHeight;
		context.drawImage(videoElem, 0, 0, videoElem.offsetWidth, videoElem.offsetHeight);
		var data = context.getImageData(0, 0, videoElem.offsetWidth, videoElem.offsetHeight);

		return data;
		//var data = canvas.toDataURL('image/png');
		//photo.setAttribute('src', data);
		//return data;
	}

	function defaultQRCallback(result, error) {
		if (result) {
			inputStationID.value = result.split("/")[4];
		}
		if (error) {
			//console.log(error);
		}
	}

	function startReading() {
		console.log("[StationIDReader] Starting to read every " + StationIDReader_CONST.PICTURE_INTERVAL + "ms...");
		timerID = setInterval(function() {
			var data = takePicture();
			qr.decode(data);
		}, StationIDReader_CONST.PICTURE_INTERVAL);
	}

	function stopReading() {
		console.log("[StationIDReader] Stopping read.");
		if (timerID !== null) {
			clearInterval(timerID);
		}
	}

	var module = {};
	module.init = init;
	module.startReading = startReading;
	module.stopReading = stopReading;
	return module;
})();
