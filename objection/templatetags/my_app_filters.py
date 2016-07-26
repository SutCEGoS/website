__author__ = 'Amin'

from django import template

register = template.Library()


@register.filter
def get_form_field_as_div(field,css_class=""):
    if type(css_class) is int:
        size = css_class
        css_class = ''
    else:
        s = css_class.split('$')
        size = s[0]
        css_class=s[1]
    obj = '<div class="' + css_class + ' col-lg-' + str(size) + ' col-md-' + str(size) + ' col-sm-' + str(size) + '">'
    if field.errors:
        obj += '<div class="control-group error"><label class="control-label">' + str(field.label)
        if field.field.required:
            obj += '<span style="font-size: 16px;color: red;">*</span>'
        obj += '</label><div class="controls">' + str(field) + '<span class="help-inline">'
        for error in field.errors:
            obj += str(error)
        obj += '</span></div></div>'
    else:
        obj += '<div class ="control-group"><label class ="control-label">' + str(field.label)

        if field.field.required:
            obj += '<span style="font-size: 16px;color: red;">*</span>'
        obj += '</label><div class="controls">' + str(field)
        obj += '</div></div>'
    obj += '<div class="details"></div></div>'
    return obj