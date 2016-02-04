/*
 * This source code is licensed under the terms of the
 * Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2016
 */

var MUOKKAA = "Muokkaa";
var TALLENNA = "Tallenna";

function order_update(type) {
    var prefix = type + "_";
    var elements = $("[name^=" + prefix + "]");

    var values = {};
    elements.each(function() {
        values[$(this).attr('name')] = $(this).val();
    });
    $.post("/update/" + type + "/" + values[type + '_id'], values);
}

function order_muokkaa(type) {
    var prefix = type + "_";
    var button = $("#" + prefix + "muokkaa");
    var elements = $("[name^=" + prefix + "]");

    if(button.text() == MUOKKAA) {
        button.text(TALLENNA);
        elements.prop('readonly', false);
    } else {
        order_update(type);
        button.text(MUOKKAA);
        elements.prop('readonly', true);
    }
}
