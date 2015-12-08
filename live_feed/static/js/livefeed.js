var REFRESH_INTERVAL = 5000;
var response = {};
var lastdate = "";

/**
 * Creates pins like pinterest
 * 
 * @param object input
 * @returns {Element|pinFactory.pin}
 */
var pinFactory = function (input) {
    var img = document.createElement('img');
    img.src = input.url;

    var social = document.createElement('i');
    var cssSocial = 'fa fa-' + input.source.toLowerCase() + ' fa-2x';
    social.className = cssSocial;
    social.innerHTML = '&nbsp;';

    var thumbs = document.createElement('i');
    var cssThumbs = 'fa fa-' + input.thumbs + ' fa-2x';
    thumbs.className = cssThumbs;
    thumbs.innerHTML = '&nbsp;';

    var user = document.createElement('b');
    user.appendChild(document.createTextNode(input.username + ": "));
    var caption = document.createTextNode(input.caption);
    var date = document.createTextNode(input.created_at);

    var p = document.createElement('p');
    p.appendChild(social);
    p.appendChild(thumbs);
    p.appendChild(date);
    p.appendChild(document.createElement('br'));
    p.appendChild(document.createElement('hr'));
    p.appendChild(user);
    p.appendChild(caption);

    var pin = document.createElement('a');
    pin.href = input.link;
    pin.target = '_blank';
    pin.className = 'pin highlight';
    pin.appendChild(img);
    pin.appendChild(p);

    return pin;
};

/**
 * Draws pins to screen in a particular order sorted by date
 * 
 * @param {type} response
 * @returns {undefined}
 */
var drawToScreen = function (response) {

    var columns = document.getElementById('columns');

    var keys = Object.keys(response);
    if (keys.length == 0) {
        return;
    }

    keys.sort(function (a, b) {
        return b - a;
    });

    for (var i = 0; i < keys.length; i++) {
        var pin = pinFactory(response[keys[i]]);
        columns.insertBefore(pin, columns.childNodes[0]);
    }

    // Get latest item's date to send it as marker to server
    lastdate = response[1].created_at;
};

/**
 * Gets new feed from server
 * 
 * @returns {undefined}
 */
var getNewJson = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            response = JSON.parse(xhttp.responseText);
            drawToScreen(response);
        }
    };

    setInterval(function () {
        xhttp.open("GET", "https://livefeed.urbanladder.com/api/getfeed?lastdate=" + lastdate, true);
        xhttp.send();
    }, REFRESH_INTERVAL);

};

window.onload = function () {
    getNewJson();
};
