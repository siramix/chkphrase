/*global Slick*/
/*global window*/
/*global alert*/
/*global jQuery*/

(function ($) {
    'use strict';

    function RemoteModel() {

        var PAGESIZE = 50,
            data = {length: 0},
            searchstr = "apple",
            sortcol = null,
            sortdir = 1,
            h_request = null,
            req = null,
            onDataLoading = new Slick.Event(),
            onDataLoaded = new Slick.Event(),
            onSuccess;


        function init() {}


        function isDataLoaded(from, to) {
            var i;
            for (i = from; i <= to; i += 1) {
                if (data[i] === undefined || data[i] === null) {
                    return false;
                }
            }

            return true;
        }

        function clear() {
            var key;
            for (key in data) {
                if (data.hasOwnProperty(key)) {
                    delete data[key];
                }
            }
            data.length = 0;
        }

        function onError(fromPage, toPage) {
            alert("error loading pages " + fromPage + " to " + toPage);
        }

        function ensureData(from, to) {
            var i,
                fromPage,
                toPage,
                url;
            if (req) {
                req.abort();
                for (i = req.fromPage; i <= req.toPage; i += 1) {
                    data[i * PAGESIZE] = undefined;
                }
            }

            if (from < 0) {
                from = 0;
            }

            console.log('From: ' + from);
            console.log('To: ' + to);
            fromPage = Math.floor(from / PAGESIZE);
            toPage = Math.floor(to / PAGESIZE);

            while (data[fromPage * PAGESIZE] !== undefined && fromPage <= toPage) {
                fromPage += 1;
            }

            while (data[toPage * PAGESIZE] !== undefined && fromPage < toPage) {
                toPage -= 1;
            }

            if (fromPage > toPage || ((fromPage === toPage) && data[fromPage * PAGESIZE] !== undefined)) {
                // TODO:  look-ahead
                return;
            }

            console.log(fromPage);
            console.log(toPage);
            url = "{{app_root}}/phrases?offset=" + (fromPage * PAGESIZE) +
                "&count=" + (((toPage - fromPage) * PAGESIZE) + PAGESIZE);
            console.log(url);

            if (h_request !== null) {
                clearTimeout(h_request);
            }

            h_request = setTimeout(function () {
                var i;
                for (i = fromPage; i <= toPage; i += 1) {
                    data[i * PAGESIZE] = null; // null mes'req'd but not available'
                }
                onDataLoading.notify({from: from, to: to});

                req = $.ajax({ url: url,
                               dataType: 'json',
                               success: onSuccess,
                               error: function () {} //onError(fromPage, toPage); }
                             });
                req.fromPage = fromPage;
                req.toPage = toPage;
            }, 50);
        }

        onSuccess = function (resp, textStatus, jqXHR) {
            var from = req.fromPage * PAGESIZE,
                to = from + resp.count,
                i,
                curObj;
            data.length = parseInt(resp.total, 10);
            console.log(resp);

            for (i = 0; i < resp.count; i += 1) {
                curObj = resp[from + i];
                data[from + i] = {};
                data[from + i].id = resp[from + i].id;
                data[from + i].phrase = resp[from + i].phrase;
                data[from + i].approved = resp[from + i].approved;
                data[from + i].buzzworthy = resp[from + i].buzzworthy;
//                data[from + i].category = resp[from + i].catgory.name;
                if (curObj.hasOwnProperty("difficulty")) {
                    if (curObj.difficulty.hasOwnProperty("name")) {
                        data[from + i].difficulty = curObj.difficulty.name;
                        console.log('FOOOO');
                    }
                }
/*                data[from + i].genre = resp[from + i].genre.name;
                data[from + i].pack = resp[from + i].pack.name;
                data[from + i].user = resp[from + i].user.name; */
                data[from + i].source = resp[from + i].source;
                data[from + i].index = from + i;
            }

            req = null;

            onDataLoaded.notify({from: from, to: to});
        };


        function reloadData(from, to) {
            var i;
            for (i = from; i <= to; i += 1) {
                delete data[i];
            }

            ensureData(from, to);
        }

        function setSort(column, dir) {
            sortcol = column;
            sortdir = dir;
            clear();
        }

        function setSearch(str) {
            searchstr = str;
            clear();
        }

        init();

        return {
            // properties
            "data": data,

            // methods
            "clear": clear,
            "isDataLoaded": isDataLoaded,
            "ensureData": ensureData,
            "reloadData": reloadData,
            "setSort": setSort,
            "setSearch": setSearch,

            // events
            "onDataLoading": onDataLoading,
            "onDataLoaded": onDataLoaded
        };
    }

    // Slick.Data.RemoteModel
    $.extend(true, window, { Slick: { Data: { RemoteModel: RemoteModel }}});
}(jQuery));
