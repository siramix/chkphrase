/**
 * This is the javascript heart of chkphrase. The convention I've adopted is
 * to have a separate namespace for each page of the application. This assumes
 * that JQuery 1.6.4 has been included in the page prior to the inclusion of
 * this script.
 *
 * IMPORTANT: JQuery Mobile 1.0.1 should be included AFTER this script.
 */

/*global $*/
/*global document*/

// Namespaces
var chkphrase = chkphrase || {};

// General --------------------------------------------------------------------
chkphrase.listToRadioButtons = function (list, parent) {
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

chkphrase.listToChooser = function (list, parent) {
    'use strict';
    var index,
        html,
        curId,
        curName,
        value;
    parent.empty();
    html += '<option value="null">None Selected</option>';
    for (index in list) {
        if (list.hasOwnProperty(index)) {
            curId = list[index].id;
            curName = list[index].name;
            html += '<option value="' + curId + '">' + curName + '</option>';
        }
    }
    $(html).appendTo(parent).trigger('create');
};

// Main -----------------------------------------------------------------------
chkphrase.main = chkphrase.main || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.main.pageshow = function () {
    'use strict';
    $.getJSON('{{app_root}}/phrases/count', function (data) {
        $('#phrase_count_value').html(data.count);
    });
    $.getJSON('{{app_root}}/phrases/count/approved', function (data) {
        $('#phrase_approved_count').html(data.count);
    });
    $.getJSON('{{app_root}}/phrases/count/buzzworthy', function (data) {
        $('#phrase_buzzworthy_count').html(data.count);
    });
    $.getJSON('{{app_root}}/phrases/count/rejected', function (data) {
        $('#phrase_rejected_count').html(data.count);
    });
    $.getJSON('{{app_root}}/phrases/count/unseen', function (data) {
        $('#phrase_unseen_count').html(data.count);
    });
    $.getJSON('{{app_root}}/phrases/counts/per_user', function (data) {
        var user;
        $('.user_count').remove();
        for (user in data) {
            if (data.hasOwnProperty(user)) {
                $('#phrase_count').append('<span class="user_count count_container"><span>' + user + ':&nbsp;</span>' + '<span>' + data[user] + '</span></span>');
            }
        }
    });
    $.getJSON('{{app_root}}/badwords/counts/per_user', function (data) {
        var user;
        $('.user_badword_count').remove();
        for (user in data) {
            if (data.hasOwnProperty(user)) {
                $('#phrase_count').append('<span class="user_badword_count count_container"><span>' + user + ' (bad words):&nbsp;</span>' + '<span>' + data[user] + '</span></span>');
            }
        }
    });
};

// Add Phrase -----------------------------------------------------------------
chkphrase.addphrase = chkphrase.phrase || {};

chkphrase.addphrase.add = function () {
    'use strict';
    var params,
        phrase,
        category_val,
        genre_val,
        difficulty_val,
        pack_val,
        id;
    category_val = $('#addphrase_category_chooser').val();
    genre_val = $('#addphrase_genre_chooser').val();
    difficulty_val = $('#addphrase_difficulty_chooser').val();
    pack_val = $('#addphrase_pack_chooser').val();
    phrase = $('#cur_add_phrase').val();
    params = {
        'phrase' : phrase,
        'approved' : '1',
        'buzzworthy' : '-1',
        'source' : 'custom'
    };

    if (category_val) {
        params.category_id = category_val;
    }
    if (genre_val) {
        params.genre_id = genre_val;
    }
    if (difficulty_val) {
        params.difficulty_id = difficulty_val;
    }
    if (pack_val) {
        params.pack_id = pack_val;
    }

    return $.post('{{app_root}}/phrases/add', params);
};

/**
 * The things to do when showing the phrase page.
 * We load a random unapproved item and display stats about it.
 */
chkphrase.addphrase.pageshow = function () {
    'use strict';
    var cur_phrase,
        category_chooser,
        genre_chooser,
        difficulty_chooser,
        pack_chooser,
        precategory_div;
    category_chooser = $('#addphrase_category_chooser');
    genre_chooser = $('#addphrase_genre_chooser');
    difficulty_chooser = $('#addphrase_difficulty_chooser');
    pack_chooser = $('#addphrase_pack_chooser');
    $.getJSON('{{app_root}}/categories', function (categories) {
        chkphrase.listToChooser(categories, category_chooser);
    });
    $.getJSON('{{app_root}}/genres', function (genres) {
        chkphrase.listToChooser(genres, genre_chooser);
    });
    $.getJSON('{{app_root}}/difficulties', function (difficulties) {
        chkphrase.listToChooser(difficulties, difficulty_chooser);
    });
    $.getJSON('{{app_root}}/packs', function (packs) {
        chkphrase.listToChooser(packs, pack_chooser);
    }).then(function () {
        $('#addphrase_add_button').unbind('click').click(function () {
            chkphrase.addphrase.add().success(function () {
                $('#cur_add_phrase').val('');
            }).error(function () {
                alert('Something went wrong! Maybe you entered a duplicate?');
            }).complete(function () {
                $('#addphrase').trigger('pageshow');
            });
        }).removeClass('ui-btn-active');
        $('#addphrase_clear_button').unbind('click').click(function () {
            $('#cur_add_phrase').val('');
            $('#addphrase').trigger('pageshow');
        }).removeClass('ui-btn-active');
    });
};

// Phrases --------------------------------------------------------------------
chkphrase.phrases = chkphrase.phrases || {};
chkphrase.phrases.cur_phrase = chkphrase.phrases.cur_phrase || {};

/**
 * Sets the phrase data for an approved word.  In the process this
 * rejects the word from Buzzwords as we don't want to reuse the
 * same words, i.e. a phrase can only be Approved for Phrasecraze 
 * or Buzzworthy
 */
chkphrase.phrases.approve = function (approval) {
    'use strict';
    var params,
        category_val,
        genre_val,
        difficulty_val,
        pack_val,
        id;
    category_val = $('#phrase_category_chooser').val();
    genre_val = $('#phrase_genre_chooser').val();
    difficulty_val = $('#phrase_difficulty_chooser').val();
    pack_val = $('#phrase_pack_chooser').val();
    id = chkphrase.phrases.cur_phrase.id;
    params = {
        'phrase' : chkphrase.phrases.cur_phrase.phrase,
        'approved' : approval,
        'buzzworthy' : -1,
        'category_id' : category_val,
        'genre_id' : genre_val,
        'difficulty_id' : difficulty_val,
        'pack_id' : pack_val
    };

    return $.post('{{app_root}}/phrases/edit/' + id, params);
};

/**
 * Sets the phrase data for a word that we might want to use
 * for Buzzwords, rejecting the word for phrasecraze.  
 * Phrase state after function:
 *   Approval: -1
 *   Buzzworthy: 1
 */
chkphrase.phrases.setbuzzworthy = function (buzzworthy) {
    'use strict';
    var params,
        category_val,
        genre_val,
        difficulty_val,
        pack_val,
        id;
    category_val = $('#phrase_category_chooser').val();
    genre_val = $('#phrase_genre_chooser').val();
    difficulty_val = $('#phrase_difficulty_chooser').val();
    pack_val = $('#phrase_pack_chooser').val();
    id = chkphrase.phrases.cur_phrase.id;
    params = {
        'phrase' : chkphrase.phrases.cur_phrase.phrase,
        'approved' : -1,
        'buzzworthy' : buzzworthy,
        'category_id' : category_val,
        'genre_id' : genre_val,
        'difficulty_id' : difficulty_val,
        'pack_id' : pack_val
    };

    return $.post('{{app_root}}/phrases/edit/' + id, params);
};

/**
 * The things to do when showing the phrase page.
 * We load a random unapproved item and display stats about it.
 */
chkphrase.phrases.pageshow = function () {
    'use strict';
    var cur_phrase,
        category_chooser,
        genre_chooser,
        difficulty_chooser,
        pack_chooser,
        precategory_div;
    precategory_div = $('#precategory');
    category_chooser = $('#phrase_category_chooser');
    genre_chooser = $('#phrase_genre_chooser');
    difficulty_chooser = $('#phrase_difficulty_chooser');
    pack_chooser = $('#phrase_pack_chooser');
    $.ajax({
        'url' : '{{app_root}}/phrases/random/unapproved',
        'cache' : false,
        'success' : function (phrase) {
            cur_phrase = phrase;
            chkphrase.phrases.cur_phrase = phrase;
            $('#cur_phrase').html(phrase.phrase);
            $('#phrase_source').html(phrase.source);
        }
    }).then(function () {
        $.getJSON('{{app_root}}/categories', function (categories) {
            chkphrase.listToChooser(categories, category_chooser);
        });
    }).then(function () {
        $.getJSON('{{app_root}}/genres', function (genres) {
            chkphrase.listToChooser(genres, genre_chooser);
        });
    }).then(function () {
        $.getJSON('{{app_root}}/difficulties', function (difficulties) {
            chkphrase.listToChooser(difficulties, difficulty_chooser);
        });
    }).then(function () {
        $.getJSON('{{app_root}}/packs', function (packs) {
            chkphrase.listToChooser(packs, pack_chooser);
        });
        if (!$.isEmptyObject(cur_phrase.pre_category)) {
            precategory_div.html(cur_phrase.pre_category.name);
        } else {
            precategory_div.html('No Precategory Provided');
        }
    }).then(function () {
        $('#phrase_approve_button').unbind('click').click(function () {
            chkphrase.phrases.approve(1).success(function () {
                $('#phrases').trigger('pageshow');
            });
        }).removeClass('ui-btn-active');
        $('#phrase_buzzworthy_button').unbind('click').click(function () {
            chkphrase.phrases.setbuzzworthy(1).success(function () {
                $('#phrases').trigger('pageshow');
            });
        }).removeClass('ui-btn-active');
        $('#phrase_reject_button').unbind('click').click(function () {
            chkphrase.phrases.approve(-1).success(function () {
                chkphrase.phrases.pageshow();
            });
        }).removeClass('ui-btn-active');
        $('#phrase_skip_button').unbind('click').click(function () {
            chkphrase.phrases.pageshow();
        }).removeClass('ui-btn-active');
    });
};

// Add Bad Words --------------------------------------------------------------
chkphrase.addbadwords = chkphrase.addbadwords || {};

chkphrase.addbadwords.create_delete = function (cur_element, cur_index) {
    'use strict';
    return function () {
        var ret;
        $.post('{{app_root}}/badwords/delete/' + cur_index,
               null,
               function (data) {},
               'json');
        cur_element.remove();
        return ret;
    };
};

chkphrase.addbadwords.add_badword = function (cur_word) {
    'use strict';
    var delete_button,
        badword;
    delete_button = $('<a href="#addbadwords" data-role="button" data-icon="delete" data-inline="true">Delete</a>');
    badword = $('<div>' + cur_word.word + '</div>');
    delete_button
        .appendTo(badword)
        .trigger('create')
        .button()
        .unbind('click').click(chkphrase.addbadwords.create_delete(badword, cur_word.id));
    return badword;
};

chkphrase.addbadwords.get_bad_words = function (phrase_id) {
    'use strict';
    $.ajax({
        'url' : '{{app_root}}/badwords/forphrase/' + phrase_id,
        'success' : function (badwords) {
            var index, cur_word;
            for (index in badwords) {
                if (badwords.hasOwnProperty(index)) {
                    cur_word = chkphrase.addbadwords.add_badword(badwords[index]);
                    $('#cur_bad_container').append(cur_word);
                }
            }
        }
    });
};

/**
 * Shows the page for adding bad words to a buzzword
 */
chkphrase.addbadwords.pageshow = function () {
    'use strict';
    var cur_phrase;
    $.ajax({
        'url' : '{{app_root}}/phrases/random/buzzworthy',
        'cache' : false,
        'success' : function (phrase) {
            chkphrase.phrases.cur_phrase = phrase;
            chkphrase.addbadwords.get_bad_words(phrase.id);
            $('#cur_word').html(phrase.phrase);
            $('#phrase_source').html(phrase.source);

            $('#addbadwords_add_button').unbind('click').click(function () {
                var params = {};
                params.word = $('#cur_bad_word').val();
                params.phrase_id = phrase.id;
                $.post('{{app_root}}/badwords/add',
                       params,
                       function (data) {
                        var badword;
                        badword = chkphrase.addbadwords.add_badword(data);
                        $('#cur_bad_container').append(badword);
                    });
            });
        }
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
    $.getJSON('{{app_root}}/users', function (data) {
        chkphrase.listToRadioButtons(data, $('#user_list'));
        $('#user_list input').unbind('change').change(function () {
            $('#users .ui-disabled').removeClass('ui-disabled');
            chkphrase.users.data.selectedId = $(this).val();
        });
        $('#user_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/users/delete/' + chkphrase.users.data.selectedId,
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
        $.getJSON('{{app_root}}/users/' + chkphrase.users.data.selectedId,
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
            $.post('{{app_root}}/users/edit/' + chkphrase.users.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/users/add', params, function (data) {});
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
    $.getJSON('{{app_root}}/categories', function (data) {
        chkphrase.listToRadioButtons(data, $('#category_list'));
        $('#category_list input').unbind('change').change(function () {
            $('#categories .ui-disabled').removeClass('ui-disabled');
            chkphrase.categories.data.selectedId = $(this).val();
        });
        $('#category_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/categories/delete/' + chkphrase.categories.data.selectedId,
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
        $.getJSON('{{app_root}}/categories/' + chkphrase.categories.data.selectedId,
                  function (data) {
                $('#category_name').val(data.name);
            });
    }
    $('#category_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#category_name').val();
        if (chkphrase.categories.data.selectedId !== null) {
            $.post('{{app_root}}/categories/edit/' + chkphrase.categories.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/categories/add', params, function (data) {});
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
    $.getJSON('{{app_root}}/precategories', function (data) {
        chkphrase.listToRadioButtons(data, $('#precategory_list'));
        $('#precategory_list input').unbind('change').change(function () {
            $('#precategories .ui-disabled').removeClass('ui-disabled');
            chkphrase.precategories.data.selectedId = $(this).val();
        });
        $('#precategory_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/precategories/delete/' + chkphrase.precategories.data.selectedId,
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
        $.getJSON('{{app_root}}/precategories/' + chkphrase.precategories.data.selectedId,
                  function (data) {
                $('#precategory_name').val(data.name);
            });
    }
    $('#precategory_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#precategory_name').val();
        if (chkphrase.precategories.data.selectedId !== null) {
            $.post('{{app_root}}/precategories/edit/' + chkphrase.precategories.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/precategories/add', params, function (data) {});
        }
    });
};

// Genres --------------------------------------------------------------
chkphrase.genres = chkphrase.genres || {};
chkphrase.genres.data = chkphrase.genres.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.genres.pageshow = function () {
    'use strict';
    $.getJSON('{{app_root}}/genres', function (data) {
        chkphrase.listToRadioButtons(data, $('#genre_list'));
        $('#genre_list input').unbind('change').change(function () {
            $('#genres .ui-disabled').removeClass('ui-disabled');
            chkphrase.genres.data.selectedId = $(this).val();
        });
        $('#genre_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/genres/delete/' + chkphrase.genres.data.selectedId,
                      function (data) {
                    $('#genre_edit_button').addClass('ui-disabled');
                    $('#genre_delete_button').addClass('ui-disabled');
                    chkphrase.genres.pageshow();
                });
        });
        $('#genre_add_button').unbind('click').click(function () {
            chkphrase.genres.data.selectedId = null;
            $('#genre_name').val('');
        });
    });
};

chkphrase.genres.dialogshow = function () {
    'use strict';
    if (chkphrase.genres.data.selectedId !== null) {
        $.getJSON('{{app_root}}/genres/' + chkphrase.genres.data.selectedId,
                  function (data) {
                $('#genre_name').val(data.name);
            });
    }
    $('#genre_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#genre_name').val();
        if (chkphrase.genres.data.selectedId !== null) {
            $.post('{{app_root}}/genres/edit/' + chkphrase.genres.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/genres/add', params, function (data) {});
        }
    });
};

// Difficulties --------------------------------------------------------------
chkphrase.difficulties = chkphrase.difficulties || {};
chkphrase.difficulties.data = chkphrase.difficulties.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.difficulties.pageshow = function () {
    'use strict';
    $.getJSON('{{app_root}}/difficulties', function (data) {
        chkphrase.listToRadioButtons(data, $('#difficulty_list'));
        $('#difficulty_list input').unbind('change').change(function () {
            $('#difficulties .ui-disabled').removeClass('ui-disabled');
            chkphrase.difficulties.data.selectedId = $(this).val();
        });
        $('#difficulty_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/difficulties/delete/' + chkphrase.difficulties.data.selectedId,
                      function (data) {
                    $('#difficulty_edit_button').addClass('ui-disabled');
                    $('#difficulty_delete_button').addClass('ui-disabled');
                    chkphrase.difficulties.pageshow();
                });
        });
        $('#difficulty_add_button').unbind('click').click(function () {
            chkphrase.difficulties.data.selectedId = null;
            $('#difficulty_name').val('');
        });
    });
};

chkphrase.difficulties.dialogshow = function () {
    'use strict';
    if (chkphrase.difficulties.data.selectedId !== null) {
        $.getJSON('{{app_root}}/difficulties/' + chkphrase.difficulties.data.selectedId,
                  function (data) {
                $('#difficulty_name').val(data.name);
            });
    }
    $('#difficulty_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#difficulty_name').val();
        if (chkphrase.difficulties.data.selectedId !== null) {
            $.post('{{app_root}}/difficulties/edit/' + chkphrase.difficulties.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/difficulties/add', params, function (data) {});
        }
    });
};

// Packs --------------------------------------------------------------
chkphrase.packs = chkphrase.packs || {};
chkphrase.packs.data = chkphrase.packs.data || {};

/**
 * Load the phrase count each time the home screen is visited.
 */
chkphrase.packs.pageshow = function () {
    'use strict';
    $.getJSON('{{app_root}}/packs', function (data) {
        chkphrase.listToRadioButtons(data, $('#pack_list'));
        $('#pack_list input').unbind('change').change(function () {
            $('#packs .ui-disabled').removeClass('ui-disabled');
            chkphrase.packs.data.selectedId = $(this).val();
        });
        $('#pack_delete_button').unbind('click').click(function () {
            $.post('{{app_root}}/packs/delete/' + chkphrase.packs.data.selectedId,
                      function (data) {
                    $('#pack_edit_button').addClass('ui-disabled');
                    $('#pack_delete_button').addClass('ui-disabled');
                    chkphrase.packs.pageshow();
                });
        });
        $('#pack_add_button').unbind('click').click(function () {
            chkphrase.packs.data.selectedId = null;
            $('#pack_name').val('');
        });
    });
};

chkphrase.packs.dialogshow = function () {
    'use strict';
    if (chkphrase.packs.data.selectedId !== null) {
        $.getJSON('{{app_root}}/packs/' + chkphrase.packs.data.selectedId,
                  function (data) {
                $('#pack_name').val(data.name);
            });
    }
    $('#pack_edit_okay_button').unbind('click').click(function () {
        var params = {};
        params.name = $('#pack_name').val();
        if (chkphrase.packs.data.selectedId !== null) {
            $.post('{{app_root}}/packs/edit/' + chkphrase.packs.data.selectedId,
                   params,
                   function (data) {});
        } else {
            $.post('{{app_root}}/packs/add', params, function (data) {});
        }
    });
};

$(document).bind('mobileinit', function () {
    'use strict';
    $.mobile.defaultPageTransition = 'slide';
    $('#main').live('pageshow', chkphrase.main.pageshow);

    $('#addphrase').live('pageshow', chkphrase.addphrase.pageshow);

    $('#phrases').live('pageshow', chkphrase.phrases.pageshow);

    $('#addbadwords').live('pageshow', chkphrase.addbadwords.pageshow);

    $('#users').live('pageshow', chkphrase.users.pageshow);
    $('#user_dialog').live('pageshow', chkphrase.users.dialogshow);

    $('#categories').live('pageshow', chkphrase.categories.pageshow);
    $('#category_dialog').live('pageshow', chkphrase.categories.dialogshow);

    $('#precategories').live('pageshow', chkphrase.precategories.pageshow);
    $('#precategory_dialog').live('pageshow',
                                  chkphrase.precategories.dialogshow);

    $('#genres').live('pageshow', chkphrase.genres.pageshow);
    $('#genre_dialog').live('pageshow', chkphrase.genres.dialogshow);

    $('#difficulties').live('pageshow', chkphrase.difficulties.pageshow);
    $('#difficulty_dialog').live('pageshow', chkphrase.difficulties.dialogshow);

    $('#packs').live('pageshow', chkphrase.packs.pageshow);
    $('#pack_dialog').live('pageshow', chkphrase.packs.dialogshow);
});
