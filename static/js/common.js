/**
 * Created by mjafar on 2014/12/31.
 */

var $window = $(window);

$window.on('load', function() {
    var $forgot_link = $('#forgot');
    var $forgot_popup = $('#forgot_popup');

    $forgot_link.on('click', function(e) {
        $forgot_popup.fadeToggle(300);
        e.preventDefault();
    });
});
