/**
 * Date: 6/26/12
 * Time: 3:50 PM
 *   Iranian (Jalali) calendar:
 *         http://en.wikipedia.org/wiki/Iranian_calendar
 *   Gregorian calendar:
 *         http://en.wikipedia.org/wiki/Gregorian_calendar
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2, or (at your option)
 *   any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.

 */


MONTHS = ["فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند"];
MILADI_MONTH_IN_PERSIAN = ["ژانویه", "فوریه", "مارس", "آوریل", "مه", "ژوئن", "ژوئیه", "اوت", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"];
JALALI_WEEKDAYS = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه"];

var GREGORIAN_EPOCH = 1721425.5;
var JALALI_EPOCH = 1948320.5;

//*******************************************************Base Function************************************************************************
function jalali_to_jd(year, month, day) {
//    "JALALI_TO_JD: Determine Julian day from Jalali date"
    var rm, epbase, mm, epyear;
    if (year >= 0)
        rm = 474;
    else
        rm = 473;
    epbase = year - (rm);
    //epbase = year - 474 if year>=0 else 473
    epyear = 474 + (epbase % 2820);
    if (month <= 7)
        mm = (month - 1) * 31;
    else
        mm = ((month - 1) * 30) + 6;
    var a = Number(Math.floor((epyear * 682 - 110) / 2816).toFixed(1));
    var b = Number(Math.floor(epbase / 2820).toFixed(1));

    return day + mm + a + (epyear - 1) * 365 + b * 1029983 + (JALALI_EPOCH - 1);
}
function jwday(j) {
    /*
     "JWDAY: Calculate day of week from Julian day"
     */
    return Number(Math.floor((j + 1.5)) % 7)
}

function leap_gregorian(year) {
//"LEAP_GREGORIAN: Is a given year in the Gregorian calendar a leap year ?"

    return ((year % 4) == 0) && (!(((year % 100) == 0) && ((year % 400) != 0)))
}


function gregorian_to_jd(year, month, day) {
    //"GREGORIAN_TO_JD: Determine Julian day number from Gregorian calendar date"
    var tm;

    if (month <= 2)
        tm = 0;
    else if (leap_gregorian(year))
        tm = -1;
    else
        tm = -2;

//tm = 0 if month <= 2 else (-1 if self.leap_gregorian(year) else -2)

    return (GREGORIAN_EPOCH - 1) + (365 * (year - 1)) + Number(Math.floor((year - 1) / 4).toFixed(1)) + (-Number(Math.floor((year - 1) / 100).toFixed(1))) + Number(Math.floor((year - 1) / 400).toFixed(1)) + Number(Math.floor((((367 * month) - 362) / 12) + tm + day).toFixed(1))
}

function jd_to_gregorian(jd) {
    //"JD_TO_GREGORIAN: Calculate Gregorian calendar date from Julian day"
    var wjd, depoch, quadricent, dqc, cent, dcent, quad, dquad, yindex, year, yearday, leapadj, month, day;
    wjd = Number(Math.floor(jd - 0.5).toFixed(1)) + 0.5;
    depoch = wjd - GREGORIAN_EPOCH;
    quadricent = Number(Math.floor(depoch / 146097).toFixed(1));
    dqc = depoch % 146097;
    cent = Number(Math.floor(dqc / 36524).toFixed(1));
    dcent = dqc % 36524;
    quad = Number(Math.floor(dcent / 1461).toFixed(1));
    dquad = dcent % 1461;
    yindex = Number(Math.floor(dquad / 365).toFixed(1));
    year = Math.floor(Number((quadricent * 400) + (cent * 100) + (quad * 4) + yindex));
    if (!((cent == 4) || (yindex == 4))) {
        year += 1;
    }


    yearday = wjd - gregorian_to_jd(year, 1, 1);
    if (wjd < gregorian_to_jd(year, 3, 1)) {
        leapadj = 0;
    }
    else if (leap_gregorian(year)) {
        leapadj = 1;
    }
    else {
        leapadj = 2;
    }


//leapadj = 0 if() wjd < self.gregorian_to_jd(year, 3, 1) else (1 if() self.leap_gregorian(year) else 2)

    month = Math.floor((((yearday + leapadj) * 12) + 373) / 367);
    day = wjd - gregorian_to_jd(year, month, 1) + 1;
    var greg;
    greg = [year, month, day];
    return greg
}


function gregorian_to_jd(year, month, day) {
    /*
     "GREGORIAN_TO_JD: Determine Julian day number from Gregorian calendar date"
     */
    var tm;
    if (month <= 2)
        tm = 0;
    else if (leap_gregorian(year))
        tm = -1;
    else
        tm = -2;
    var a = Number(Math.floor((year - 1) / 4).toFixed(1));
    var b = Number(Math.floor((year - 1) / 100).toFixed(1));
    var c = Number(Math.floor((year - 1) / 400).toFixed(1));
    var d = Number(Math.floor((((367 * month) - 362) / 12) + tm + day).toFixed(1));

//tm = 0 if month <= 2 else (-1 if self.leap_gregorian(year) else -2)

    return (GREGORIAN_EPOCH - 1) + (365 * (year - 1)) + a - b + c + d
}

function jd_to_jalali(jd) {
    /*
     "JD_TO_JALALI: Calculate Jalali date from Julian day"
     */
    var jdj, depoch, cycle, cyear, ycycle, aux1, aux2, yday, year, month, day;

    jd = Number(Math.floor(jd).toFixed(1)) + 0.5;
    depoch = jd - jalali_to_jd(475, 1, 1);
    cycle = Number(Math.floor(depoch / 1029983).toFixed(1));
    cyear = depoch % 1029983;
    if (cyear == 1029982)
        ycycle = 2820;
    else {
        aux1 = Number(Math.floor(cyear / 366).toFixed(1));
        aux2 = cyear % 366;
        ycycle = Number(Math.floor(((2134 * aux1) + (2816 * aux2) + 2815) / 1028522).toFixed(1)) + aux1 + 1;
    }
    year = Number(Math.floor(ycycle + (2820 * cycle) + 474).toFixed(1));
    if (year <= 0)
        year -= 1;
    yday = (jd - self.jalali_to_jd(year, 1, 1)) + 1;
    if (yday <= 186)
        month = Number(Math.floor(Math.ceil(yday / 31)).toFixed(1));
    else
        month = Number(Math.floor(Math.ceil((yday - 6) / 30)).toFixed(1));

    day = Number(Math.floor(jd - jalali_to_jd(year, month, 1)).toFixed(1)) + 1;
    var jalali;
    jalali = [year, month, day];
    return jalali

}

//*******************************************************Aplied Function***************************************************************************


function get_greg_date(shamsi_str,format) {
    var shamsi, year, month, day, jd, greg, date;
    shamsi = shamsi_str.split('-');
    year = Number(shamsi[0]);
    month = Number(shamsi[1]);
    day = Number(shamsi[2]);
    jd = jalali_to_jd(year, month, day);
    greg = jd_to_gregorian(jd);
    date = new Date(greg[0], greg[1] - 1, greg[2]);
    return date.format(format)
}



//................................................................................
function apply_datepicker(selector) {
    selector = (typeof selector == 'undefined') ? '.dateinput input' : selector;
    $(selector).each(function () {
        var old_value = $(this).val();
        $(this).datepicker({
            showOn: 'button',
            buttonImage: '/static/images/calendar-green.png',
            buttonImageOnly: true,
            changeMonth:true,
            changeYear:true,
            dateFormat:"yy-mm-dd",
            onSelect:function (dateStr, inst) {
                var month;
                var day;
                if (inst.selectedDay < 10) {
                    day = '0' + inst.selectedDay;
                } else {
                    day = inst.selectedDay;
                }
                if (inst.selectedMonth < 10) {
                    month = '0' + (inst.selectedMonth + 1);
                } else {
                    month = inst.selectedMonth + 1;
                }
                $(this).val(inst.selectedYear + "-" + month + "-" + day);
            }
        });
        $(this).attr("autocomplete", "off");
        $(this).click(function () {
            $(this).focus();
        });
        $(this).datepicker("option", "yearRange", "1320:1400");
        $(this).val(old_value);
    });
}
function apply_timepicker(selector){
    selector = (typeof selector == 'undefined') ? '.timeinput input' : selector;
    $(selector).each(function(){
        $(this).timepicker({
            currentText: 'اکنون',
            closeText: 'انجام',
            timeOnlyTitle: 'انتخاب زمان',
            timeText: 'زمان',
            hourText: 'ساعت',
            minuteText: 'دقیقه'});
    })
}


function get_jalali(str) {
    /*
     str:string like:"2012-07-03".
     return jalali date in array format like [1391,4,13].

     example: get_jalali("2012-07-03") return [1391,4,13].
     */
    var miladi, jd, jalali, arr;
    miladi = false;
    str = str.trim();
    arr = str.split('-');
    if (arr.length == 3 && (0 < Number(arr[1]) < 13) && (0 < Number(arr[2]) < 32)) {
        miladi = arr;
    }
    if (miladi) {
        jd = gregorian_to_jd(Number(miladi[0]), Number(miladi[1]), Number(miladi[2]));
        jalali = jd_to_jalali(jd);
        return jalali;
    }
    else
        return false;
}


function get_jalali_date(str) {
    /*
     get string like "2012-07-03" and return jalali date in string format like: "1391-4-13"
     example: get_jalali_date("2012-07-03") return "1391-4-13".
     */
    var jalali, month, day;
    str = str.trim();
    if (jalali = get_jalali(str)) {
        month = (jalali[1] > 9) ? jalali[1].toString() : '0' + jalali[1].toString();
        day = (jalali[2] > 9) ? jalali[2].toString() : '0' + jalali[2].toString();
        return jalali[0].toString() + '-' + month + '-' + day;
    }
    else
        return false;
}


function get_jalali_long_date(str) {
    /*
     str:string like:"2012-07-03".
     return jalali date in string format like: "13 تير 1391"

     example: get_jalali_long_date("2012-07-03") return "13 تير 1391"
     */
    var jalali;
    str = str.trim();
    if (jalali = get_jalali(str))
        return jalali[2].toString() + " " + MONTHS[jalali[1] - 1] + " " + (jalali[0]).toString();
    else
        return false;
}

function get_time_stamp(str) {
    /*
     get a string and return a unix time stamp that "strtotime" is product
     */
    var arr , month, day;
    arr = str.split('-');
    if (arr.length == 3 && (0 < Number(arr[1]) < 13) && (0 < Number(arr[2]) < 32)) {
        month = (arr[1].length == 1) ? '0' + arr[1] : arr[1];
        day = (arr[2].length == 1) ? '0' + arr[2] : arr[2];
        return strtotime(arr[0] + '-' + month + '-' + day);
    }
    else return strtotime(str);

}

function get_jalali_date_with_format(text, format) {
    /*
    یک رشته را که نشان دهنده ی یک تاریخ میلادی است میگیرد و با توجه به فرمتی که به آن داده میشود
    تاریخ شمسی را برمیگرداند.

    فرمت باید یکی از موارد
     "longDateTime", "longDate", "fullDate", "isoDate", "isoDateTime"
     باشد و به طور پیش فرض
     "isoDate"
          است.

          در زیر نوع تاریخ شمسی بازگشت داده شده را با توجه به فرمت ارسالی مشاهده مینمایید

     longDateTime:   "ddd mmm dd yyyy HH:MM:ss",   //  "سه‌شنبه 13 تير 1391 15:36:48"
     longDate:       "mmmm d, yyyy",               //  "13 تير 1391"
     fullDate:       "dddd, mmmm d, yyyy",         //  "سه‌شنبه 13 تير 1391"
     isoDate:        "yyyy-mm-dd",                 //  "1391-4-13"
     isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",      //  "1391-4-13 15:36:48"
به مثالهای زیر توجه نمایید

     example:2012 8 22
         get_jalali_date_with_format("2012-9-22", "longDate") return "1 مهر 1391"
         get_jalali_date_with_format("2012-9-22", "isoDate") return "1391-07-01"
         get_jalali_date_with_format("2012 september 22", "fullDate") return "شنبه 1 مهر 1391"
         get_jalali_date_with_format("2012 september 22", "isoDate") return "1391-07-01"
         get_jalali_date_with_format("2012/9/22", "isoDate") return "1391-07-01"
         get_jalali_date_with_format("2012 8 22", "longDateTime") return "شنبه 1 مهر 1391 0:0:0"

     */
    var date, time, jd, week_day, pdate;
    format = format.trim();
    format = (typeof format == 'undefined') ? "isoDate" : format;
    format = format.trim();
    time_stamp = get_time_stamp(text);
    if (!time_stamp) return false;
    date = new Date(time_stamp * 1000);
    switch (format) {
        case "longDateTime"://"ddd mmm dd yyyy HH:MM:ss"
            time = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
            //time = (time == "4:30:0") ? "00:00" : time;
            jd = gregorian_to_jd(date.getFullYear(), date.getMonth() + 1, date.getDate());
            week_day = JALALI_WEEKDAYS[jwday(jd)];
            pdate = get_jalali_long_date(date.format("isoDate"));
            return week_day + ' ' + pdate + ' ' + time;

        case "longDate"://"mmmm d, yyyy"
            return get_jalali_long_date(date.format("isoDate"));

        case "fullDate"://"dddd, mmmm d, yyyy"
            jd = gregorian_to_jd(date.getFullYear(), date.getMonth() + 1, date.getDate());
            week_day = JALALI_WEEKDAYS[jwday(jd)];
            pdate = get_jalali_long_date(date.format("isoDate"));
            return week_day + ' ' + pdate;

        case "isoDate"://"yyyy-mm-dd"
            return get_jalali_date(date.format("isoDate"));

        case "isoDateTime"://"yyyy-mm-dd'T'HH:MM:ss"
            var sp = date.format(format).split('T');
            time = (sp[1] == "04:30:00") ? "00:00" : sp[1];
            pdate = get_jalali_date(sp[0]);
            return pdate + ' ' + time;
        default:
            return false;
    }
}


function persian_miladi_to_jalali(str) {
    /*
    تاریخ های میلادی که شبیه به
     3 ژوئیه 2012
          باشند را به تاریخ شمسی به شکل
     13 تير 1391
     در می آورند

     example:
     persian_miladi_to_jalali( 3 ژوئیه 2012 ) return 13 تير 1391
     persian_miladi_to_jalali( 3 ژوئیه 2012، ساعت 18:04:34  ) return 13 تير 1391 ساعت 18:04:49

     */
    var a, month_number, day;
    str = str.trim();
    a = str.split(' ');
    month_number = MILADI_MONTH_IN_PERSIAN.indexOf(a[1]);
    if (month_number != -1) {
        if (a.indexOf("ساعت") != -1) {
            month_number = (month_number + 1 > 9) ? (month_number + 1).toString() : '0' + (month_number + 1).toString();
            var year = a[2].replace('،', '');
            day = (a[0].length == 1) ? '0' + a[0] : a[0];
            var miladi = year + '-' + month_number + '-' + day;
            return get_jalali_long_date(miladi) + ' ساعت ' + a[4];
        }
        else {
            month_number = (month_number + 1 > 9) ? (month_number + 1).toString() : '0' + (month_number + 1).toString();
            day = (a[0].length == 1) ? '0' + a[0] : a[0];
            var miladi = a[2] + '-' + month_number + '-' + day;
            return get_jalali_date_with_format(miladi, "longDate");
        }

    }
    else {
        return false;
    }
}


function convert_miladi_dates_to_shamsi(selector, format) {
    /*
     تاریخ های میلادی که با
     selector
     مشخص شده اند را به تاریخ شمسی با فرمت داده شده تبدیل مینمایند.

     توجه:
     selector
     از قوانین
     jquery
     پیروی میکند و چناچه به تابع ارسال نشود به طور پیش فرض
     ".dateinput input"
     می باشد.
     فرمت به طور پیش فرض
     "isoDate"
     است و فرمت های دیگر در تابع
     "get_jalali_date_with_format"
     شرح داده شده است

     */

    format = (typeof format == 'undefined') ? "isoDate" : format;
    selector = (typeof selector == 'undefined') ? '.dateinput input' : selector;
    $(selector).each(function () {
        var value, text, miladi, temp;
        value = $(this).val();
        text = $(this).text().trim();
        if (value && $(this).get(0).tagName == 'INPUT') {
            $(this).val(get_jalali_date(value));
        }
        else if (text) {
            if (temp = get_jalali_date_with_format(text, format)) {
                $(this).text(temp);
            }
            else if (miladi = persian_miladi_to_jalali(text))
                $(this).text(miladi);
            else
                $(this).text("invali date format");
        }
    });
}


var date_format;
function convert_shamsi_dates_to_miladi_in_submit(selector, format) {
    /*
    تاریخ های شمسی که با
     selector
    مشخص شده اند را به تاریخ میلادی با فرمت داده شده تبدیل مینمایند.

    توجه:
     selector
    از قوانین
     jquery
    پیروی میکند و چناچه به تابع ارسال نشود به طور پیش فرض
     ".dateinput input"
     می باشد.
     فرمت به طور پیش فرض
     "isoDate"
     است و فرمت های دیگر درفایل
     "js/datepicker/date.format.js" line "95".
     شرح داده شده است
    تبدیل تاریخ ها زمانی انجام میشود که نزدیکترین فرم به
     selector
سابمیت شود
     */
    var form;
    selector = (typeof selector == 'undefined') ? '.dateinput input' : selector;
    date_format = (typeof format == 'undefined') ? "isoDate" : format;
    form = $(selector).closest("form");
    if (form != "undefined") {
        form.submit(function () {
            $(selector).each(function () {
                if ($(this).val())
                    $(this).val(get_greg_date($(this).val(),date_format));
            });
        })
    }
}


function convert_shamsi_date_to_miladi(selector, format) {
    /*
یک
     selector
که دارای تاریخ شمسی است را گرفته و با توجه به فرمت داده شده
آن را به تاریخ میلادی تبدیل میکند

     توجه:
     selector
     از قوانین
     jquery
     پیروی میکند
     فرمت به طور پیش فرض
     "isoDate"
     است و فرمت های دیگر درفایل
     "js/datepicker/date.format.js" line "95".
     شرح داده شده است
     */
    date_format = (typeof format == 'undefined') ? "isoDate" : format;
    var value;
    if ($(selector).val()!='undefined')
        value = $(selector).val();
    else if($(selector).text()!='undefined')
        value = $(selector).text();
    return get_greg_date(value,date_format);
}