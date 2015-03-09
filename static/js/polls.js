/**
 * Created by Amin on 3/8/2015.
 */


$('.poll-link').on('click', function () {
    var poll_id = this.getAttribute('data-id');
    $.ajax({
        url: window.$get_poll_url,
        type: 'post',
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': window.csrf_token,
            'poll_id': poll_id
        }
    }).success(function (response) {
    }).error(function (response) {
        if (response.status == 200)
            $("#poll-form").html(response.responseText);
    });
});

$('#poll-form').ajaxForm({
    beforeSend: function () {
    },
    complete: function (xhr) {
        var e = xhr.responseJSON.error;
        if (e != '') {
            alert(e);
        } else {
            $('#poll-form').html('');
            $('.poll-link[data-id=' + xhr.responseJSON.id.toString() + ']').click();
        }
    }
});