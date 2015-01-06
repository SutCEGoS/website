/**
 * Created by seyed on 1/4/15.
 */
$(document).ready(function() {
    $("#remove_search_filter").on('click', function(){
        $("#remove_search_filter").hide();
        $window.trigger('searchform.resetform');
    });


    $("#mine_checkbox").on('change',function(){
        $others_objections=$( "div[mj-message-template='false']").not(".filter_mine_or_metooed");
        if($("#mine_checkbox").prop('checked') == true)
        {
            $others_objections.fadeOut(300);
        }
        else
        {
           $others_objections.fadeIn(300);
        }
        //console.log($("#mine_checkbox").prop('checked'));
    });
});


$window.on('searchform.resetform', function() {
    $('form[name=search_form]')[0].reset();
    $window.trigger('search.do', [{}]);
});