/**
* Created by mjafar on 2015/01/01.
*/
var $searchables = $('.searchable');

$searchables.bind('change', function () {
    $window.trigger('search.do', [{
            category: $('select[name=category]').find(':selected').val(),
            offered_course: $('select[name=offered_course]').find(':selected').val(),
            second_course: $('select[name=second_course]').find(':selected').val(),
            course_name: $('input[name=course_name]').val()
    }]);
});

/** A'min code: **/
$('.collapse').collapse();
$('#id_offered_course').select2();
$('#id_second_course').select2();
$('#id_category').bind('change', function () {
    a_value = $(this).val();
    showDefaultForm(a_value);
});
var c_value = $('#id_category > *[selected=selected]').attr('value');
showDefaultForm(c_value);
function showDefaultForm(value){
    console.log("hi");
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
        data: {csrfmiddlewaretoken: csrf_token, courseId: t.val()}
    }).success(function (r) {
        t.parent().parent().parent().find('.details').html('<p class="course-details">' + r.details + '</p>');
    }).error(function () {
    });
}
