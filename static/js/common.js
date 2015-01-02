/**
 * Created by mjafar on 2014/12/31.
 */

var $window = $(window);

$window.on('load', function() {
    var $forgot_link = $('#forgot');

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
});
