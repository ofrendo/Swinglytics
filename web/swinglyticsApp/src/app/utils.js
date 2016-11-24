//const VIDEO_STORAGE_DOMAIN = "https://s3.eu-central-1.amazonaws.com/hopinone/";
const VIDEO_STORAGE_DOMAIN = "https://192.168.178.76:3000/ftp/";

function doRequest(url, method, jsonParams, callback) {
  //var domain = "https://localhost:3000";
  var domain = "https://192.168.178.76:3000";
  //var domain = "https://golf-innovation.com:3000";
  url = domain + url;
  var params = "";
  for (var key in jsonParams) {
    params += key + "=" + jsonParams[key] + '&';
  }
  // remove last "&"
  params = params.substring(0, params.length-1);
  var http = new XMLHttpRequest();
  http.open(method, url, true);
  http.withCredentials = true;
  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.onreadystatechange = function() {//Call a function when the state changes.

    if (http.readyState == 4) {
      if (typeof callback === "function") {
        callback(http);
      }
    }
  }
  console.log(http);
  http.send(params);
}

function buildThumbnailURL(videoID) {
  return VIDEO_STORAGE_DOMAIN + "swingClip_" + videoID + ".png";
}
function buildVideoURL(videoID) {
  return VIDEO_STORAGE_DOMAIN + "swingClip_" + videoID + ".mp4";
}


function getParameterByName(name, url) {
  // see http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
  if (!url) url = window.location.href;
  //url = url.toLowerCase(); // This is just to avoid case sensitiveness  
  name = name.replace(/[\[\]]/g, "\\$&");//.toLowerCase();// This is just to avoid case sensitiveness for query parameter name
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}