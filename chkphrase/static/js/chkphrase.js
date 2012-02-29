/**
 * This is the javascript heart of chkphrase. The convention I've adopted is
 * to have a separate namespace for each page of the application. This assumes
 * that JQuery 1.6.4 has been included in the page prior to the inclusion of
 * this script.
 * 
 * IMPORTANT: JQuery Mobile 1.0.1 should be included AFTER this script.
 */

// Namespaces
var $ = $ || {};
var document = document || {};
var chkphrase = chkphrase || {};

// General --------------------------------------------------------------------
chkphrase.listToChooser = function (list, parent) {
    'use strict';
    var index,
        html,
        curId,
        curName;
    parent.empty();
    html = '<fieldset data-role="controlgroup">';
    for (index in list) {
        if (list.hasOwnProperty(index)) {
            curId = list[index].id;
            curName = list[index].name;
            html += '<input class="radio_input" ';
            html += '       type="radio"';
            html += '       name="radio-choice" ';
            html += '       id="radio-choice-' + curId + '" ';
            html += '       value="' + curId + '" />';
            html += '<label class="radio_input_label" ';
            html += '       for="radio-choice-' + curId + '">';
            html += curName + '</label>';
        }
    }
    html += '</fieldset>';
    $(html).appendTo(parent).trigger('create');
};


// Main -----------------------------------------------------------------------
chkphrase.main = chkphrase.main || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.main.pageshow = function () {
    'use strict';
    $.getJSON('phrases/count', function (data) {
        $('#phrase_count_value').html(data.count);
    });
};

// Users ----------------------------------------------------------------------
chkphrase.users = chkphrase.users || {};
chkphrase.users.data = chkphrase.users.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.users.pageshow = function () {
    'use strict';
    $.getJSON('users', function (data) {
        chkphrase.listToChooser(data, $('#user_list'));
        $('#user_list input').unbind('change').change(function () {
            $('#users .ui-disabled').removeClass('ui-disabled');
            chkphrase.users.data.selectedId = $(this).val();
        });
        $('#user_delete_button').unbind('click').click(function () {
            $.post('users/delete/' + chkphrase.users.data.selectedId,
                      function (data) {
                    $('#user_edit_button').addClass('ui-disabled');
                    $('#user_delete_button').addClass('ui-disabled');
                    chkphrase.users.pageshow();
                });
        });
        $('#user_add_button').unbind('click').click(function () {
            chkphrase.users.data.selectedId = null;
            $('#user_name').val('');
            $('#user_full_name').val('');
            $('#user_password').val('');
        });
    });
};

chkphrase.users.dialogshow = function () {
    'use strict';
    if (chkphrase.users.data.selectedId !== null) {
        $.getJSON('users/' + chkphrase.users.data.selectedId,
                  function (data) {
                $('#user_name').val(data.name);
                $('#user_full_name').val(data.full_name);
            });
    }
    $('#user_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#user_name').val();
        params.full_name = $('#user_full_name').val();
        params.password = $('#user_password').val();
        if (chkphrase.users.data.selectedId !== null) {
            $.post('users/edit/' + chkphrase.users.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('users/add', params, function (data) {});
        }
    });
};

// Categories -----------------------------------------------------------------
chkphrase.categories = chkphrase.categories || {};
chkphrase.categories.data = chkphrase.categories.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.categories.pageshow = function () {
    'use strict';
    $.getJSON('categories', function (data) {
        chkphrase.listToChooser(data, $('#category_list'));
        $('#category_list input').unbind('change').change(function () {
            $('#categories .ui-disabled').removeClass('ui-disabled');
            chkphrase.categories.data.selectedId = $(this).val();
        });
        $('#category_delete_button').unbind('click').click(function () {
            $.post('categories/delete/' + chkphrase.categories.data.selectedId,
                      function (data) {
                    $('#category_edit_button').addClass('ui-disabled');
                    $('#category_delete_button').addClass('ui-disabled');
                    chkphrase.categories.pageshow();
                });
        });
        $('#category_add_button').unbind('click').click(function () {
            chkphrase.categories.data.selectedId = null;
            $('#category_name').val('');
        });
    });
};

chkphrase.categories.dialogshow = function () {
    'use strict';
    if (chkphrase.categories.data.selectedId !== null) {
        $.getJSON('categories/' + chkphrase.categories.data.selectedId,
                  function (data) {
                $('#category_name').val(data.name);
            });
    }
    $('#category_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#category_name').val();
        if (chkphrase.categories.data.selectedId !== null) {
            $.post('categories/edit/' + chkphrase.categories.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('categories/add', params, function (data) {});
        }
    });
};

// Precategories --------------------------------------------------------------
chkphrase.precategories = chkphrase.precategories || {};
chkphrase.precategories.data = chkphrase.precategories.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.precategories.pageshow = function () {
    'use strict';
    $.getJSON('precategories', function (data) {
        chkphrase.listToChooser(data, $('#precategory_list'));
        $('#precategory_list input').unbind('change').change(function () {
            $('#precategories .ui-disabled').removeClass('ui-disabled');
            chkphrase.precategories.data.selectedId = $(this).val();
        });
        $('#precategory_delete_button').unbind('click').click(function () {
            $.post('precategories/delete/' + chkphrase.precategories.data.selectedId,
                      function (data) {
                    $('#precategory_edit_button').addClass('ui-disabled');
                    $('#precategory_delete_button').addClass('ui-disabled');
                    chkphrase.precategories.pageshow();
                });
        });
        $('#precategory_add_button').unbind('click').click(function () {
            chkphrase.precategories.data.selectedId = null;
            $('#precategory_name').val('');
        });
    });
};

chkphrase.precategories.dialogshow = function () {
    'use strict';
    if (chkphrase.precategories.data.selectedId !== null) {
        $.getJSON('precategories/' + chkphrase.precategories.data.selectedId,
                  function (data) {
                $('#precategory_name').val(data.name);
            });
    }
    $('#precategory_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#precategory_name').val();
        if (chkphrase.precategories.data.selectedId !== null) {
            $.post('precategories/edit/' + chkphrase.precategories.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('precategories/add', params, function (data) {});
        }
    });
};

$(document).bind('mobileinit', function () {
    'use strict';
    $('#main').live('pageshow', chkphrase.main.pageshow);

    $('#users').live('pageshow', chkphrase.users.pageshow);
    $('#user_dialog').live('pageshow', chkphrase.users.dialogshow);

    $('#categories').live('pageshow', chkphrase.categories.pageshow);
    $('#category_dialog').live('pageshow', chkphrase.categories.dialogshow);

    $('#precategories').live('pageshow', chkphrase.precategories.pageshow);
    $('#precategory_dialog').live('pageshow',
                                  chkphrase.precategories.dialogshow);

/**    $('#genres').live('pageshow', chkphrase.genres.pageshow);
    $('#genre_dialog').live('pageshow', chkphrase.genres.dialogshow);

    $('#difficulties').live('pageshow', chkphrase.difficulties.pageshow);
    $('#difficulty_dialog').live('pageshow', chkphrase.difficulties.dialogshow);

    $('#packs').live('pageshow', chkphrase.packs.pageshow);
    $('#pack_dialog').live('pageshow', chkphrase.packs.dialogshow);**/
});