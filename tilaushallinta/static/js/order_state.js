/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2016
 */

var tilaus = {
    baseurl: "/tilaukset/"
};

var huoltosopimus = {
    baseurl: "/huoltosopimukset/"
};

var huolto = {
    baseurl: "/huoltosopimukset/-1/huolto/"
}

function state_changed() {
    var oldstate = $("input[name='state_original']").val();
    var newstate = $("#state_select").val();

    if(oldstate != newstate) {
        $("#state_change").prop('disabled', false);
        $("#state_change").val("Vaihda");
    } else {
        $("#state_change").prop('disabled', true);
    }
}

function order_change_state() {
    var tilaus_id = $("input[name='tilaus_id']").val();
    change_state(tilaus, tilaus_id);
}

function huoltosopimus_change_state() {
    var sopimus_id = $("input[name='huoltosopimus_id']").val();
    change_state(huoltosopimus, sopimus_id);
}

function huolto_change_state() {
    var huolto_id = $("input[name='huolto_id']").val();
    change_state(huolto, huolto_id);
}

var button_id = "#state_change";
var original_state = "state_original";

function change_state(type, id) {
    var newstate = $("#state_select").val();

    $.post(type.baseurl + id + "/setstate", {newstate: newstate});
    $("input[name='" + original_state + "']").val(newstate);

    $(button_id).val("Vaihdettu");
    $(button_id).prop('disabled', true);
}