/**
 * Created by mjafar on 2015/01/01.
 */

var $messages_container;
var $me_too_link;

function showMessages(messages) {
    // Clean
    $messages_container.children().remove();

    // Create
    for (var i = 0; i < messages.length; ++i) {
        // Clone
        var item = messages[i];
        var htmlrepr = $("div[mj-message-template='true']").clone();
        htmlrepr.attr('mj-message-template', 'false');

        // Fill html
        htmlrepr
            .attr('mj-dataid', item.data_id)
            .attr('mj-category-id', item.category_id);

        htmlrepr.find('[mj-request-id]').html(item.data_id);
        htmlrepr.find('.panel-heading a[data-toggle="collapse"]').attr('href', '#collapse-' + item.data_id);
        htmlrepr.find('.panel-heading a.metoo').attr('mj-dataid', item.data_id);
        htmlrepr.find('.panel-collapse').attr('id','collapse-' + item.data_id);
        htmlrepr.find('[mj-message-container]').html(item.message);
        if (item.reply) {
            htmlrepr.find('[mj-reply-wrapper').removeClass('hide');
            htmlrepr.find('[mj-reply-text').html(item.reply);
            htmlrepr.find('[mj-reply-name]').html(item.reply_by);
        }

        //htmlrepr.find('[mj-category!=else]').hide();
        for (var j = 0; j < 5; ++j) {
            if (item.category_id == j) {
                htmlrepr.find('[mj-category="' + j + '"]').show();
                htmlrepr.find('[mj-category="else"]').hide();
            }
        }
        if (item.category_id == 3) {
            htmlrepr.find('[mj-course-1]').html(item.course_name);
        } else {
            htmlrepr.find('[mj-course-1]').html(item.offered_course);
        }
        htmlrepr.find('[mj-course-2]').html(item.second_course);
        htmlrepr.find('[mj-conflict-category]').html(item.category);


        htmlrepr.find('[mj-metoo-number]').html(item.metoos);
        if (item.metooed) {
            htmlrepr.find('[mj-metoo-link]').hide();
            htmlrepr.find('[mj-metoo-number]').addClass('metooed');
        }

        $messages_container.append(htmlrepr);
    }

    var $me_too_link = $('[mj-metoo-link]');
    var $un_me_too = $('[mj-metoo-number]');

    $me_too_link.on('click', function(e) {
        e.preventDefault();

        var $me_too_badge = $(this).parent().find('[mj-metoo-number]'); // TOFF
        $(this).hide(300);
        $.ajax({
            url: window.$ajax_metoo,
            type: 'post',
            dataType: 'json',
            data: {
                data_id: $(this).attr('mj-dataid')
            }
        }).success(function (response) {
            console.log(response);
            var response_parsed = json_parse(response);
            $me_too_badge.html(response_parsed['meetoos']);
            if (response_parsed['meetoed']) {
                $me_too_badge.removeClass('metooed');
                $(this).show(300);
            } else {
                $me_too_badge.addClass('metooed');
            }
        }).error(function () {
            $(this).show(300);
        })
    });


    $un_me_too.on('click', function (e) {
        e.preventDefault();

        console.log('un me too clicked!');

        $(this).removeClass('metooed');
        var $me_too_link = $(this).parent().find('[mj-metoo-link]');
        $.ajax({
            url: window.$ajax_metoo,
            type: 'post',
            dataType: 'json',
            data: {
                data_id: $(this).attr('mj-dataid')
            }
        }).success(function (response) {
            console.log(response);
            var response_parsed = json_parse(response);
            $me_too_badge.html(response_parsed['meetoos']);
            if (response_parsed['meetoed']) {
                $me_too_badge.addClass('metooed');
                $me_too_link.hide(300);
            } else {
                $me_too_badge.removeClass('metooed');
                $me_too_link.show(300);
            }
        }).error(function () {
            $(this).addClass('metooed');
        })
    });


    $window.trigger('messages.lazyShow');
}

$window.on('messages.lazyShow', function () {
    var first_hide = $messages_container.children('div.panel.hide:first');
    if (first_hide && first_hide.length) {
        first_hide.removeClass('hide').hide().fadeIn(100, function () {
            $(window).trigger('messages.lazyShow');
        });
    }
});

$window.on('load', function() {
    $messages_container = $('div#messages-container');

    $.ajax({
        url: window.$ajax_search,
        type: 'get',
        dataType: 'json'
    }).success(function (response) {
        // TODO (mjafar)
        console.log(response);
        showMessages(response);
    }).error(function () {
        // TODO (mjafar)
        alert("Refresh kon :D");
    });
});


