/**
 * Created by seyed on 1/4/15.
 */
$(document).ready(function() {
    $("#remove_search_filter").on('click', function(){
        $("#remove_search_filter").hide();
        $window.trigger('searchform.resetform');
    });
});


$window.on('searchform.resetform', function() {
    $('form[name=search_form]')[0].reset();
    $window.trigger('search.do', [{}]);
});