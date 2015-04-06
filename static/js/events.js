/**
 * Created by Amin on 3/8/2015.
 */


$('.event-link').on('click', function () {
    var poll_id = this.getAttribute('data-id');
    var t = $(this).find('.panel-title').html();
    $.ajax({
        url: window.$get_event_url,
        type: 'post',
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': window.csrf_token,
            'event-id': poll_id
        }
    }).success(function (response) {
    }).error(function (response) {
        if (response.status == 200)
            $("#events-form").html(response.responseText);
        $('#form-heading').html(t);
    });
});

$('#events-form').ajaxForm({
    beforeSend: function () {
    },
    complete: function (xhr) {
        var e = xhr.responseJSON.error;
        if (e != '') {
            alert(e);
        } else {
            $('#event-form').html('<p>' +
            'ثبت نام شما با موفقیت انجام شد! تعداد ثبت نامی : ' +
             xhr.responseJSON.count.toString() +
            '</p>');
        }
    }
});
