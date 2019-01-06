/**
* Created by mjafar on 2015/01/01.
*/
var $searchables = $('.searchable');
var $add_message_button;

$window.on('message_add.do', function (e, data) {
    $window.trigger('message_add.started');
    data.csrfmiddlewaretoken = window.csrf_token;
    $.ajax({
        url: $('form[name=search_form]').attr('action'),
        type: 'post',
        dataType: 'json',
        data: data
    }).success(function (response) {
        $window.trigger('message_add.finished', [response]);
    }).error(function (response) {
        $window.trigger('message_add.error', [response.responseJSON]);
    }).complete(function() {
        $add_message_button.removeClass('disabled').removeAttr('disabled');
    });
});

$window.on('message_add.finished', function(e, response) {
    toastr.success("پیام شما با موفقیت ثبت شد.", "ارسال پیام");
    $no_result.hide();
    $window.trigger('search.result', [response, true]);
    $window.trigger('searchform.resetform');
});

$window.on('message_add.error', function(e, response) {
    if (response == undefined) {
        toastr.error("متأسفیم، اشکالی در ارسال پیامتان پیش آمد.", "خطا :(");
    } else {
        toastr.error('<p dir="rtl">' + response + '</p>', "خطا :(");
    }
});

$window.on('message_add.started', function(e) {
    toastr.info("چند لحظه صبر کنید...", "در حال ارسال پیام");
    $add_message_button.addClass('disabled').attr('disabled', 'disabled');
});


var _get_search_items = function (category_id) {
    return {
        category: category_id,
        offered_course: $('select[name=offered_course]').find(':selected').val(),
        second_course: $('select[name=second_course]').find(':selected').val(),
        course_name: $('input[name=course_name]').val()
    };
}

var _get_message_data = function () {
    return {
        category: $('select[name=category]').find(':selected').val(),
        offered_course: $('select[name=offered_course]').find(':selected').val(),
        second_course: $('select[name=second_course]').find(':selected').val(),
        course_name: $('input[name=course_name]').val(),
        message: $('textarea[name="message"]').val()
    };
}

$window.on('load', function() {
    $add_message_button = $('#add_message');
    $searchables = $('.searchable');

    $searchables.bind('change', function () {
        var category_id = $('select[name=category]').find(':selected').val();
        if (parseInt(category_id)) {
            $window.trigger('search.do', [
                _get_search_items(category_id)
            ]);
        } else {
            $window.trigger('search.do', [{}]);
        }
    });

    $add_message_button.on('click', function(e) {
        var $this = $(this);
        if ($this.hasClass('disabled')) {
            return;
        }
        e.preventDefault();

        $window.trigger('message_add.do', [_get_message_data()]);
    });

    /** A'min code: **/
    $('.collapse').collapse();
    $('#id_category').bind('change', function () {
        a_value = $(this).val();
        showDefaultForm(a_value);
    });
    var c_value = $('#id_category > *[selected=selected]').attr('value');
    showDefaultForm(c_value);
    function showDefaultForm(value){
        if (value == 1) {
            $('.offered-course-div').fadeIn();
            $('.second-course-div').fadeIn();
            $('.course-name-div').fadeOut();
        } else if (value == 3) {
            $('.offered-course-div').fadeOut();
            $('.second-course-div').fadeOut();
            $('.course-name-div').fadeIn();
        } else if (value > 0) {
            $('.offered-course-div').fadeIn();
            $('.second-course-div').fadeOut();
            $('.course-name-div').fadeOut();
        } else {
            $('.offered-course-div').fadeOut();
            $('.second-course-div').fadeOut();
            $('.course-name-div').fadeOut();
        }
        var $remove_search_filter = $("#remove_search_filter");
        $("#mine_checkbox").prop('checked', false)
                .closest("label").removeClass("active");
        $("#replied_checkbox").prop('checked', false)
                .closest("label").removeClass("active");
        if (value > 0) {
            $remove_search_filter.show();
            $remove_search_filter.removeClass("hide");
        }
        else {
            $remove_search_filter.hide();
        }
    }
});