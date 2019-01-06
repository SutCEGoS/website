/**
 * Created by seyed on 1/1/15.
 */

$window.on('load', function(){
    $('#forgot').on('click', function(e) {
        $(this).popConfirm({
            placement: 'bottom',
            title: 'رمزتان را فراموش کردید؟',
            content: 'لطفا نام کاربریتان را در فرم ورود به سایت (بالا) وارد کنید و روی دکمهٔ ادامه کلیک کنید.',
            yes: 'ادامه',
            no: 'بستن',
            container: false,
            callback_yes: function () {
                forgot_form = $('form[name=forgot_password_form]');
                forgot_form.find('input#id_username_or_email').val($('input[name=username]').val());
                forgot_form.submit();
            }
        });
    });
    var $username = $('#username');
    var $password = $('#password');
    var maxWidth = Math.max($username.width() , $password.width());

    $username.css("width",maxWidth);
    $password.css("width",maxWidth);
});