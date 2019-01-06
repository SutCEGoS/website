/**
 * Created by mjafar on 2015/01/01.
 */

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
        message: $('textarea[name="message"]').val(),
        title: $('input[name=title]').val()
    };
}

$window.on('load', function () {

    /** A'min code: **/
    $('.collapse').collapse();
    $('#id_category').bind('change', function () {
        a_value = $(this).val();
        showDefaultForm(a_value);
    });
    var c_value = $('#id_category > *[selected=selected]').attr('value');
    showDefaultForm(c_value);
    function showDefaultForm(value) {
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