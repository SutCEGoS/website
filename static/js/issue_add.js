/**
 * Created by mjafar on 2015/01/01.
 */
var $searchables = $('.searchable');
var $add_message_button;

$window.on('issue_add.do', function (e, data) {
    $window.trigger('issue_add.started');
    data.csrfmiddlewaretoken = window.csrf_token;
    $.ajax({
        url: window.$message_add_url,
        type: 'post',
        dataType: 'json',
        data: data
    }).success(function (response) {
        $window.trigger('issue_add.finished', [response]);
    }).error(function (response) {
        $window.trigger('issue_add.error', [response.responseJSON]);
    });
});

$window.on('issue_add.finished', function (e, response) {
    toastr.success("Your message have been sent.", "Message sent");
    $no_result.hide();
    $window.trigger('search.result', [response], true);
    $window.trigger('searchform.resetform');
});

$window.on('issue_add.error', function (e, response) {
    if (response == undefined) {
        toastr.error("We're sorry, an unexpected error occurred while sending your message.", "Error :-(");
    } else {
        toastr.error('<p dir="rtl">' + response + '</p>', "Error :-(");
    }
});

$window.on('issue_add.started', function (e) {
    toastr.info("Hold on...", "Sending message");
});

$window.on('load', function () {
    $add_message_button = $('#add_issue');
    $searchables = $('.searchable');

    $searchables.bind('change', function () {
        var category_id = $('select[name=category]').find(':selected').val();
        if (parseInt(category_id)) {
            $window.trigger('search.do', [
                {
                    category: category_id
                }
            ]);
        } else {
            $window.trigger('search.do', [{}]);
        }
    });

    $add_message_button.on('click', function (e) {
        var $this = $(this);
        if ($this.hasClass('disabled')) {
            return;
        }
        e.preventDefault();

        $window.trigger('issue_add.do', [{
            category: $('select[name=category]').find(':selected').val(),
            message: $('textarea[name="message"]').val(),
            title: $('input[name=title]').val()
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