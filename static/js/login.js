/**
 * Created by seyed on 1/1/15.
 */

var $window = $(window);
$window.on('load', function(){
    var $username = $('#username');
    var $password = $('#password');
    var maxWidth = Math.max($username.width() , $password.width());

    $username.css("width",maxWidth);
    $password.css("width",maxWidth);
     //$username.width(maxWidth);
     //$password.width(maxWidth);

});