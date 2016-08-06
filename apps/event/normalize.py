# -*- coding: utf-8 -*-
def replace_persian_numbers(string):
    arr = [u'۰', u'۱', u'۲', u'۳', u'۴', u'۵', u'۶', u'۷', u'۸', u'۹']
    if not isinstance(string, basestring):
        return string
    for i in range(0, 10):
        string = string.replace(arr[i], str(i))
    return string


def unicode_normalize(string):
    if not string:
        return u''
    return replace_persian_numbers(string)
