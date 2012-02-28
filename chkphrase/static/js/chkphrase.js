/**
 * This is the javascript heart of chkphrase. The convention I've adopted is
 * to have a separate namespace for each page of the application. This assumes
 * that JQuery 1.6.4 and JQuery Mobile 1.0.1 have been included in the page
 * prior to the inclusion of this script.
 */

// Namespaces
var $ = $ || {};
var document = document || {};
var chkphrase = chkphrase || {};

// Home
chkphrase.home = chkphrase.home || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.home.load = function () {
    'use strict';
    $.getJSON('phrases/count', function (data) {
        $('#count').val(data.count);
    });
};

/**
 * We attach all of our handy listeners in the document.ready such that we
 * know that our DOM elements are where we'd expect them to be.
 */
$(document).ready(function () {
    'use strict';
    chkphrase.home.load();
});
