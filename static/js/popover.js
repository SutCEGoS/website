/**
 * Created by seyed on 1/1/15.
 */


(function ($) {
    var state = false;
    $.fn.popConfirm = function (options) {

        var $this = this;
        var settings = $.extend({
            title: 'Are you sure?',
            content: '',
            container: 'body',
            placement: 'top',
            yes: 'yes',
            no: 'no',
            callback_yes: function () {
            },
            callback_no: function () {
            }
        }, options);
        var yes = $('<button class="btn btn-danger" data-delete-yes></button>').text(settings.yes);
        var no = $('<button class="btn btn-default" data-delete-yes></button>').text(settings.no);

        yes.on('click', function () {
            $this.popover('hide');
            $this.popover('destroy');
            settings.callback_yes();
        });
        no.on('click', function () {
            $this.popover('hide');
            $this.popover('destroy');
            settings.callback_no();
        });

        var group = $('<div class="btn-group"></div>');
        group.append(no).append(yes);
        var div = $('<div class=""></div>');
        div.text(settings.content);
        if (settings.content !== '') {
            div.append('<br>');
        }
        div.append(group);
        $this.popover('hide');
        $this.popover('destroy');
        $this.popover({
            trigger: 'manual',
            html: true,
            placement: settings.placement,
            title: settings.title,
            container: settings.container,
            content: div
        });
        if(state == true)
        {
            $this.popover('hide');
            state = false;
        }
        else
        {
            $this.popover('show');
            state = true;
        }

        return this;
    };

}(jQuery));