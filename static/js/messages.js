/**
 * Created by mjafar on 2015/01/01.
 */

function showMessages(messages) {
    $('#messages-container').children().remove();
    for (var i = 0; i < messages.length; ++i) {
        var item = messages[i];
        var htmlrepr = $("div[mj-message-template='true']").clone();
        htmlrepr.attr('mj-message-template', 'false');

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
        if (!item.metooed) {
            htmlrepr.find('[mj-metoo-link]').hide();
            htmlrepr.find('[mj-metoo-number]').addClass('metooed');
        }

        $('#messages-container').append(htmlrepr);
    }

    $window.trigger('lazyShow');
}

$window.on('messages.lazyShow', function () {
    var firsthide = $('#messages-container').children('div.panel.hide:first');
    if (firsthide && firsthide.length) {
        firsthide.removeClass('hide').hide().fadeIn(100, function () {
            $(window).trigger('messages.lazyShow');
        });
    }
});

$window.on('load', function() {
    $.ajax({
        url: window.$ajax_search,
        type: 'get',
        dataType: 'json'
    }).success(function (response) {
        // TODO (mjafar)
        showMessages(response);
    }).error(function () {
        // TODO (mjafar)
        alert("Refresh kon :D");
    });
});