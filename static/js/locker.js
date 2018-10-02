var lockerLetter = 'M';

function changeLetter(ch) {
    $("#locker-title").html("کمد "+ch);
    lockerLetter = ch;
    $(".locker > .row > .col ").each(function () {
        var my  = $(this).html();
        my = my.slice(my.length-2,my.length);
        $(this).html(lockerLetter+my);
    });
}
$(".locker > .row > .col ").click(function () {
        $("#chosen-locker").val($(this).html());
        $("#lockerModal").modal('toggle');
    }
);