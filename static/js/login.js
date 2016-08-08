/**
 * Created by seyed on 1/1/15.
 */

var $forgot_link;
$window.on('load', function(){
    $forgot_link = $('#forgot');

    $forgot_link.on('click', function(e) {

        var $this = $(this);
        $this.popConfirm({
                placement: 'bottom',
                title: 'Are you sure?',
                content:
                    'اگر شما واقعاً گذرواژه‌تان را گم کردید، می‌توانید دکمه «بله» را فشار دهید و ما برای شما یک رایانامه با دستورالعملهای لازم برای بازتنظیم گذرواژه‌تان را برایتان ارسال کنیم.',
                yes: 'بله',
                no: 'خیر',
                container: false,
                callback_yes: function () {
                    window.location = window.forgot_link;
                    //TODO
                }
            });
    });
    var $username = $('#username');
    var $password = $('#password');
    var maxWidth = Math.max($username.width() , $password.width());

    $username.css("width",maxWidth);
    $password.css("width",maxWidth);
     //$username.width(maxWidth);
     //$password.width(maxWidth);

});