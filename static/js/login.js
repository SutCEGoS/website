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
                content: 'If you are sure press on yes button?',
                yes: 'Yes',
                no: 'No',
                container: false,
                callback_yes: function () {
                    window.location.replace(window.forgot_link);
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