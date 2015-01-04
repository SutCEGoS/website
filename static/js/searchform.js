/**
* Created by mjafar on 2015/01/01.
*/
var $searchables = $('.searchable');
var $add_message_button;

$window.on('message_add.do', function (e, data) {
    $window.trigger('message_add.started');
    data.csrfmiddlewaretoken = window.csrf_token;
    $.ajax({
        url: window.$message_add_url,
        type: 'post',
        dataType: 'json',
        data: data
    }).success(function (response) {
        $window.trigger('message_add.finished', [response]);
    }).error(function (response) {
        $window.trigger('message_add.error', [response.responseJSON]);
    });
});

$window.on('message_add.finished', function(e, response) {
    toastr.success("Your message have been sent.", "Message sent");
    $window.trigger('search.result', [response, true]);
});

$window.on('message_add.error', function(e, response) {
    if (response == undefined) {
        toastr.error("We're sorry, an unexpected error occurred while sending your message.", "Error :-(");
    } else {
        toastr.error('<p dir="rtl">' + response + '</p>', "Error :-(");
    }
});

$window.on('message_add.started', function(e) {
    toastr.info("Hold on...", "Sending message");
});

$window.on('load', function() {
    $add_message_button = $('#add_message');
    $searchables = $('.searchable');

    $searchables.bind('change', function () {
        $window.trigger('search.do', [{
                category: $('select[name=category]').find(':selected').val(),
                offered_course: $('select[name=offered_course]').find(':selected').val(),
                second_course: $('select[name=second_course]').find(':selected').val(),
                course_name: $('input[name=course_name]').val()
        }]);
    });

    $add_message_button.on('click', function(e) {
        var $this = $(this);
        if ($this.hasClass('disabled')) {
            return;
        }
        e.preventDefault();

        $window.trigger('message_add.do', [{
            category: $('select[name=category]').find(':selected').val(),
            offered_course: $('select[name=offered_course]').find(':selected').val(),
            second_course: $('select[name=second_course]').find(':selected').val(),
            course_name: $('input[name=course_name]').val(),
            message: $('textarea[name="message"]').val()
        }]);
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
    }


    $('#id_offered_course').bind('change', function () {
        appendDetails($(this));
    });
    $('#id_second_course').bind('change', function () {
        appendDetails($(this));
    });
    function appendDetails(t) {
        $.ajax({
            url: "/get-course-details/",
            type: 'POST',
            dataType: 'json',
            data: {csrfmiddlewaretoken: window.csrf_token, courseId: t.val()}
        }).success(function (r) {
            t.parent().parent().parent().find('.details').html('<p class="course-details">' + r.details + '</p>');
        }).error(function () {
        });
    }
});