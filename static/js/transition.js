function visible(el) {
    var bottom_of_object = $(el).offset().top + $(el).outerHeight();
    var bottom_of_window = $(window).scrollTop() + $(window).height();

    /* If the object is completely visible in the window, fade it in */

    return( bottom_of_window > bottom_of_object );
}
function halfVisible(el) {
    var bottom_of_object = $(el).offset().top + $(el).outerHeight()*2/3;
    var bottom_of_window = $(window).scrollTop() + $(window).height();

    /* If the object is completely visible in the window, fade it in */

    return( bottom_of_window > bottom_of_object );
}

function showAnnouncements(event)
{
    var win = $(window);
    var notifs = $(".entry");
    notifs.each(function(i, el) {
        if (visible($(el))) {
            $(el).css("visibility","visible");
            $(el).addClass("show-notif");
        }
    });
}
$(window).scroll(showAnnouncements);
function showMembers(event) {
    var win = $(window);
    var members = $(".memberHidden");
    members.each(function(i, el) {
        if (halfVisible($(el))) {
            $(el).css("visibility","visible");
            $(el).hide().fadeIn();
            $(el).removeClass("memberHidden");
        }
    });
}