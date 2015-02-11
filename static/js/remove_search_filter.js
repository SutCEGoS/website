/**
 * Created by seyed on 1/4/15.
 */
$(document).ready(function () {
    $("#remove_search_filter").on('click', function () {
        $("#remove_search_filter").hide();
        $window.trigger('searchform.resetform');
    });


    $("#mine_checkbox").on('change', function () {
        $others_objections = $("div[mj-message-template='false']").not(".filter_mine_or_metooed");
        if ($("#mine_checkbox").prop('checked') == true) {
            $others_objections.fadeOut(300);
        }
        else {
            $others_objections.removeClass("hide");
            $others_objections.fadeIn(300);
        }
    });

    $(document).tooltip({'selector': '.metooed', 'title': 'Un me too!', 'placement': 'top'});


    $("input:radio[name=sort]").on('change', function () {
          $window.trigger('search.result', [window.last_response], false);
          var $items = $("div[mj-message-template='false']");
        $items.sort(function(a,b){
        });
    });
});


$window.on('searchform.resetform', function () {
    $('form[name=search_form]')[0].reset();
    $window.trigger('search.do', [
        {}
    ]);
});

window.item_compare = function (a,b) {
    if (sort_type == "metoo") {
        if (a.metoos == b.metoos) {
            return a.data_id < b.data_id ? 1 : -1;
        }
        return a.metoos < b.metoos ? 1 : -1;
    }
    else {
        return a.data_id < b.data_id ? 1 : -1;
    }
};