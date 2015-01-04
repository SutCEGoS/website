/**
 * Created by mjafar on 2015/01/01.
 */

var $messages_container;
var $loading;
var $no_result;
var $messages = [];
var $course_list = [];
/*
{
    course.id: {
        'course_name': course.course.name,
        'course_number': course.course.course_number,
        'professor': course.professor.name,
        'group_number': course.group_number,
        'exam_time': course.exam_time,
        'capacity': course.capacity,
        'details': course.details,
    }
}
 */

$(document).ready(function() {
    $messages_container = $('div#messages-container');
    $loading = $('#loading');
    $no_result = $('#no_result');

    $.ajax({
        url: window.$course_list_url,
        type: 'get',
        dataType: 'json'
    })
        .success(function(response) {
            $course_list = response;


            var $offered_course = $('#id_offered_course');
            var $second_course = $('#id_second_course');
/*
            $offered_course.html('');
            $second_course.html('');
            $.each($course_list, function(course_id, course_details)
            {
                var new_option = $('<option>', { value:course_id, text:course_details.course_name });
                $offered_course.append(new_option);
                $second_course.append(new_option);
            });
            */

            $offered_course.select2();
            $second_course.select2();
        })
        .error(function() {
            alert("Failed to load courses list, please refresh the page.");
        });
});

$window.on('load', function () {
    var location_parts = window.location.search.split('&');
    var has_id = false;
    var id;
    $.each(location_parts, function(index,value) {
        var index_of_id = value.indexOf('id=');
        if (index_of_id == 0 || (index_of_id == 1 && value[0] == '?')) {
            id = value.substr(index_of_id + 'id='.length);
            has_id = true;
            console.log(id);
        }
    });
    if (has_id) {
        $window.trigger('search.do', [
            {id:id}
        ]);
    } else {
        $window.trigger('search.do', [
            {}
        ]);
    }
});

$window.on('search.do', function (e, data) {
    $window.trigger('search.started');
    $.ajax({
        url: window.$load_url,
        type: 'get',
        dataType: 'json',
        data: data
    }).success(function (response) {
            $window.trigger('search.finished');
            if (response.length == 0) {
                $window.trigger('search.no_result');
            } else {
                $window.trigger('search.result', [response]);
            }
        }).error(function () {
            $window.trigger('search.finished');
            alert("Error occurred, please check your connection or refresh the page.");
        });
});

$window.on('search.started', function (e) {
    $no_result.hide();
    $no_result.removeClass("hide");
    $loading.show();
    $add_message_button.addClass('disabled');

});

$window.on('search.no_result', function (e) {
    $messages_container.children().remove();

    setTimeout(function(){
        //$no_result.fadeIn(100);
        $no_result.show();
    },1000);
    //$no_result.show();
});

$window.on('search.finished', function (e) {
    $add_message_button.removeClass('disabled');
    setTimeout(function(){
        $loading.fadeOut(200);
        //$loading.hide();
    },900);
//    $loading.hide();
});

$window.on('search.result', function (e, messages) {
    $messages_container.children().remove();
    $messages = messages;
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
        htmlrepr.find('a[mj-permanent-link]').attr('href', '?id=' + item.data_id).on('click', function(e) {
            e.preventDefault();
            $window.trigger('search.do', [{
                id: item.data_id
            }]);
        });
        htmlrepr.find('.panel-heading a[data-toggle="collapse"]').attr('href', '#collapse-' + item.data_id);
        htmlrepr.find('.panel-heading a.metoo').attr('mj-dataid', item.data_id);
        htmlrepr.find('.panel-collapse').attr('id', 'collapse-' + item.data_id);
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

    $me_too_link.on('click', function (e) {
        e.preventDefault();
        var $this = $(this);
        var $me_too_badge = $this.parent().find('[mj-metoo-number]'); // TOFF

        $this.hide(300);
        $.ajax({
            url: window.$ajax_metoo,
            type: 'post',
            dataType: 'json',
            data: {
                data_id: $this.attr('mj-dataid'),
                csrfmiddlewaretoken: window.csrf_token
            }
        }).success(function (response) {
                $me_too_badge.html(response.metoos);
                if (response.meetoed) {
                    $me_too_badge.removeClass('metooed');
                    $this.show(300);
                } else {
                    $me_too_badge.addClass('metooed');
                }
            }).error(function () {
                $this.show(300);
            });
    });


    $un_me_too.on('click', function (e) {
        e.preventDefault();
        var $this = $(this);

        if (!$this.hasClass('metooed')) {
            return;
        }

        $this.removeClass('metooed');
        var $me_too_link = $this.parent().find('[mj-metoo-link]');
        $.ajax({
            url: window.$ajax_metoo,
            type: 'post',
            dataType: 'json',
            data: {
                data_id: $this.attr('mj-dataid'),
                csrfmiddlewaretoken: window.csrf_token
            }
        }).success(function (response) {
                $this.html(response.metoos);
                if (response.metooed) {
                    $this.addClass('metooed');
                    $me_too_link.filter(':visible').hide(300);
                } else {
                    $this.removeClass('metooed');
                    $me_too_link.show(300);
                }
            }).error(function () {
                $this.addClass('metooed');
            });
    });


    $window.trigger('messages.lazyShow');
});

$window.on('messages.lazyShow', function () {
    var first_hide = $messages_container.children('div.panel.hide:first');
    if (first_hide && first_hide.length) {
        first_hide.removeClass('hide').hide().fadeIn(100, function () {
            $(window).trigger('messages.lazyShow');
        });
    }
});
