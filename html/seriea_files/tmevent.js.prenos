// TMEvent.js
(function() {
    // Constants
    var PROP = 'UA-3816204-21';

    function TMEvent(sampling) {
        if (arguments.length == 1) {
            this.sampling = sampling;
        } else {
            this.sampling = 10;
        }
    
        this.gaproperty = PROP;
        
        return this;
    }
    var setCookie = function(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
    var getCookie = function(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    var generateUUID = function() { // Public Domain/MIT
        var d = new Date().getTime();
        if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
            d += performance.now(); //use high-precision timer if available
        }
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }
    var generateEventPayload = function(a, b, c, d, v) {
        data = "v=1&t=event&tid="+PROP+"&cid=" + d + "&ec=" + a + "&ea=" + b + "&el=" + c + "&ev=" + v;
        return data;
    }
    var getTMGuid = function() {
        g = getCookie("tm_GUID")
        if (g.length == 0) {
            g = generateUUID();
            setCookie("tm_GUID", g, 999);
        }
        return g;
    }
    var sendTMEvent = function(payload) {
        var http = new XMLHttpRequest();
        var url = window.location.protocol + "//" + window.location.host + "/senddata";
        var params = payload;
        http.open("POST", url, true);
        http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        http.send(params);
    }
    TMEvent.prototype.VERSION = "0.0.1";
    TMEvent.prototype.SendAB = function() {
    	//if (typeof(window.GoogleAnalyticsObject) == "string") {
    	//	g=window[window.GoogleAnalyticsObject];
    	//	g('send','event','pageview','adblockViaGA','adblock',1);
    	//} else {
	        if (this.sampling > 0) {
	            var xabc = Math.floor(Math.random() * 100) + 1;
	            if (xabc > this.sampling) {
	                return false;
	            }
	        }
	        x = generateEventPayload("pageview", "adblockViaTM", "adblock", getTMGuid(), 1)
	        sendTMEvent(x);
	        return true;
	    //}
    }
    // CommonJS module
    //if (typeof exports !== 'undefined') {
    //	if (typeof module !== 'undefined' && module.exports) {
    //		exports = module.exports = Chance;
    //	}
    //	exports.TMEvent = TMEvent;
    //}
    // Register as an anonymous AMD module
    //if (typeof define === 'function' && define.amd) {
    //	define([], function () {
    //		return TMEvent;
    //	});
    //}
    // if there is a importsScrips object define chance for worker
    //if (typeof importScripts !== 'undefined') {
    //	tmevent = new TMEvent();
    //}
    // If there is a window object, that at least has a document property,
    // instantiate and define chance on the window
    if (typeof window === "object" && typeof window.document === "object") {
        window.TMEvent = TMEvent;
        //window.tmevent = new TMEvent();
    }
})();