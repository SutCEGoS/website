/**
 * Created by mjafar on 2015/01/01.
 */

var $messages_container;
var $loading;
var $no_result;
var $messages = [];
var $course_list = [];
var fade_in_time = 350;

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
                $window.trigger('search.result', [response, false]);
            }
        }).error(function () {
            $window.trigger('search.finished');
            alert("Error occurred, please check your connection or refresh the page.");
        });
});

$window.on('search.started', function (e) {
    $no_result.hide().removeClass("hide");
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
    if (!parseInt($('select[name=category]').find(':selected').val())) {
        $add_message_button.addClass('disabled');
    }
});

$window.on('search.result', function (e, messages, append) {
    var to_add;
    if (!append) {
        $messages_container.children().remove();
        $messages = messages;
        to_add = $messages;
    } else {
        $messages.push(messages);
        to_add = [messages];
    }

    if (append || messages.length < 10) {
        fade_in_time = 350;
    } else {
        fade_in_time = 120;
    }

    // Create
    $.each(to_add, function (i, item) {
        // Clone
        var item_dom = $("div[mj-message-template='true']").clone();
        item_dom.attr('mj-message-template', 'false');

        // Fill html
        item_dom
            .attr('mj-dataid', item.data_id)
            .attr('mj-category-id', item.category_id);

        item_dom.find('[mj-request-id]').html(item.data_id);
        item_dom.find('a[mj-permanent-link]').attr('href', '?id=' + item.data_id).on('click', function(e) {
            e.preventDefault();
            $window.trigger('search.do', [{
                id: item.data_id
            }]);
        });
        item_dom.find('.panel-heading a[data-toggle="collapse"]').attr('href', '#collapse-' + item.data_id);
        item_dom.find('.panel-heading a.metoo').attr('mj-dataid', item.data_id);
        item_dom.find('.panel-collapse').attr('id', 'collapse-' + item.data_id);
        item_dom.find('[mj-message-container]').html(item.message);
        if (item.reply && item.reply.length) {
            item_dom.addClass('filter_replied');
            item_dom.find('[mj-reply-wrapper]').removeClass('hide');
            item_dom.find('[mj-reply-text]').html(item.reply);
            item_dom.find('[mj-reply-name]').html(item.reply_by);
        }

        //htmlrepr.find('[mj-category!=else]').hide();
        //item_dom.find('[mj-category]').filter('[mj-category!="else"]').hide();
        item_dom.find('[mj-category]').hide();
        for (var j=1; j<=6; ++j) {
            if (item.category_id == j) {
                item_dom.find('[mj-category="' + j + '"]').show();
                //item_dom.find('[mj-category="else"]').hide();
            }
        }
        if (item.category_id == 3) {
            item_dom.find('[mj-course-1]').html(item.course_name);
        } else {
            item_dom.find('[mj-course-1]').html(item.offered_course);
        }
        item_dom.find('[mj-course-2]').html(item.second_course);
        item_dom.find('[mj-conflict-category]').html(item.category_name);

//        var abs_url = window.location + '?id=' + item.data_id;
//        item_dom.find('param[name=FlashVars]').attr('value', 'text='+ abs_url);
//        item_dom.find('embed').attr('FlashVars', 'text='+ abs_url);

        item_dom.find('[mj-metoo-number]').html(item.metoos);
        if (item.metooed) {
            item_dom.addClass('filter_metooed');
            item_dom.find('[mj-metoo-link]').hide();
            item_dom.find('[mj-metoo-number]').addClass('metooed');
        }
        if (!item.can_me_too) {
            item_dom.addClass('filter_mine');
            item_dom.find('[mj-metoo-link]').remove();
        }

        $messages_container.append(item_dom);
    });

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
        first_hide.removeClass('hide').hide().fadeIn(fade_in_time, function () {
            $(window).trigger('messages.lazyShow');
        });
    }
});
