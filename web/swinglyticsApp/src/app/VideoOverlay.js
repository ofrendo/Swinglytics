var VideoOverlay = (function() {

  var OVERLAY = {
    BUTTON_W: 40,
    MARGIN_LEFT: 10,
    MARGIN_TOP_NEW_LINE: 10,
    MARGIN_TOP_REMOVE: 60
  };
  // http://stackoverflow.com/questions/24384368/simple-button-in-html5-canvas

  var newLineActive = false;
  var mouseDown = false;
  var currentLines = [];

  function getMousePos(canvas, event) {
    var rect = canvas.getBoundingClientRect();
    var e = event;
    if (event.touches) {
      e = event.touches[0];
    }
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  }
  function isInside(pos, rect){
    return pos.x > rect.x && pos.x < rect.x+rect.width && pos.y < rect.y+rect.height && pos.y > rect.y
  }
  function onClick(pos) {
    // New line button
    if (isInside(pos, {x: OVERLAY.MARGIN_LEFT, y: OVERLAY.MARGIN_TOP_NEW_LINE, width: OVERLAY.BUTTON_W, height: OVERLAY.BUTTON_W})) {
      onNewLineClick();
    }
    else if (isInside(pos, {x: OVERLAY.MARGIN_LEFT, y: OVERLAY.MARGIN_TOP_REMOVE, width: OVERLAY.BUTTON_W, height: OVERLAY.BUTTON_W})) {
      onRemoveClick();
    }
  }

  // test for new buttons
  function canvasBtnClickNew(){
    onNewLineClick();
    //console.log("new line button click");
  }
  function canvasBtnClickErase(){
    onRemoveClick();
    //console.log("erase button click");
  }

  function onNewLineClick() {
    if (newLineActive === false) {
      newLineActive = true;
    }
    /*else {
      newLineActive = false;
    }*/
  }
  function getNewLineActiveButtonColor() {
    return (newLineActive === true) ?
            "gray" :
            "white";
  }
  function getNewLineActiveLineColor() {
    return (newLineActive === true) ?
            "gray" :
            "black";
  }

  function onRemoveClick() {
    newLineActive = false;
    currentLines = [];
  }

  function onDragStart(pos) {
    mouseDown = true;
    if (newLineActive === true) {
      currentLines.push({
        x1: pos.x,
        y1: pos.y,
        x2: pos.x,
        y2: pos.y
      });
    }
  }
  function onDragMove(pos) {
    if (newLineActive === true && mouseDown === true) {
      // Modify newest line
      currentLines[currentLines.length-1].x2 = pos.x;
      currentLines[currentLines.length-1].y2 = pos.y;
    }
  }
  function onDragStop(pos) {
    if (newLineActive === true && mouseDown === false) {
      // Modify newest line
      currentLines[currentLines.length-1].x2 = pos.x;
      currentLines[currentLines.length-1].y2 = pos.y;
      newLineActive = false;
    }
    mouseDown = false;
  }

  function initCanvasVideoOverlay() {
    // remove lines from previous videos
    currentLines = [];

    var video = document.getElementById("swingVideo");
    var canvas = document.getElementById("swingVideoCanvasOverlay");

    var NewLineButton = document.getElementById("canvasNewLine");
    var EraseButton = document.getElementById("canvasErase");

    var w = video.offsetWidth;
    var h = video.offsetHeight;
    //console.log("w=" + w + ", h=" + h);
    canvas.width = w;
    canvas.height = h;
    var context = canvas.getContext("2d");

    function frameLoop() {
      window.setTimeout(frameLoop, 33);
      drawScreen(video, context, w, h);
    }

    frameLoop();

    if (("ontouchstart" in window) === false) {
      // Desktop
      NewLineButton.addEventListener('click', function(e) {
        //var pos = getMousePos(canvas, e);
        //onClick(pos);
        canvasBtnClickNew();
      });
      EraseButton.addEventListener('click', function(e) {
        //var pos = getMousePos(canvas, e);
        //onClick(pos);
        canvasBtnClickErase();
      });
      addMultipleEvents(canvas, "mousedown", function(e) {
        var pos = getMousePos(canvas, e);
        onDragStart(pos);
      });
      addMultipleEvents(canvas, "mousemove", function(e) {
        var pos = getMousePos(canvas, e);
        onDragMove(pos);
      });
      addMultipleEvents(canvas, "mouseup", function(e) {
        var pos = getMousePos(canvas, e);
        onDragStop(pos);
      });
    }
    else {
      // Mobile
      NewLineButton.addEventListener('click', function(e) {
        //var pos = getMousePos(canvas, e);
        //onClick(pos);
        canvasBtnClickNew();
      });
      EraseButton.addEventListener('click', function(e) {
        //var pos = getMousePos(canvas, e);
        //onClick(pos);
        canvasBtnClickErase();
      });
      addMultipleEvents(canvas, "touchstart", function(e) {
        var pos = getMousePos(canvas, e);
        onDragStart(pos);
        //alert("HERE");
      });
      addMultipleEvents(canvas, "touchmove", function(e) {
        e.preventDefault();
        var pos = getMousePos(canvas, e);
        onDragMove(pos);
      });
      addMultipleEvents(canvas, "touchend", function(e) {
        var pos = getMousePos(canvas, e);
        onDragStop(pos);
      });
    }


  }
  function addMultipleEvents(element, events, callback) {
    events.split(" ").forEach(function(eName) {
      element.addEventListener(eName, callback);
    });
  }

  function drawScreen(video, context, w, h) {
    // Draw current video frame
    context.drawImage(video, 0, 0, w, h);

    // Draw UI
    // Draw new line button

    // context.fillStyle= getNewLineActiveButtonColor();
    // context.fillRect( OVERLAY.MARGIN_LEFT, OVERLAY.MARGIN_TOP_NEW_LINE,
    //                   OVERLAY.BUTTON_W, OVERLAY.BUTTON_W );
    // context.font = "bold 30px Arial";
    // context.fillStyle = "black";
    // context.fillText( "L", OVERLAY.BUTTON_W/2, OVERLAY.BUTTON_W );

    // Draw remove line button

    // context.fillStyle="white";
    // context.fillRect( OVERLAY.MARGIN_LEFT, OVERLAY.MARGIN_TOP_REMOVE,
    //                   OVERLAY.BUTTON_W, OVERLAY.BUTTON_W );
    // context.font = "bold 30px Arial";
    // context.fillStyle = "black";
    // context.fillText( "X", OVERLAY.BUTTON_W/2, OVERLAY.MARGIN_TOP_REMOVE+OVERLAY.BUTTON_W - 10 );

    // Draw lines
    for (var i=0;i<currentLines.length;i++) {
      context.beginPath();
      context.moveTo(currentLines[i].x1, currentLines[i].y1);
      context.lineTo(currentLines[i].x2, currentLines[i].y2);
      context.strokeStyle = "#f44336";
      /*(i === currentLines.length-1) ?
                                getNewLineActiveLineColor(): // only draw last line gray while dragging
                                "black"*/
      context.lineWidth = 3;
      context.stroke();
    }
  }

  function resetLines() {
    currentLines = [];
  }

  var module = {};
  module.initCanvasVideoOverlay = initCanvasVideoOverlay;
  module.resetLines = resetLines;
  return module;
})();
