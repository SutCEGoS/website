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
                    'If you forgot your password really, you can press on the Yes button and we will send you an email. Then you can go and change your password!'
                ,
//                yes: 'بله',
//                no: 'خیر',
                callback_yes: function () {
                    window.location = forgot_link;
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