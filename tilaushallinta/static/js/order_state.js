/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2015
 */

var tilaus = {
    original_state: "state_original",
    button_id: "#state_change",
    baseurl: "/tilaukset/"
};

var huoltosopimus = {
    original_state: "state_original",
    button_id: "#state_change",
    baseurl: "/huoltosopimukset/"
};

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
    var newstate = $("#state_select").val();

    change_state(tilaus, tilaus_id, newstate);
}

function huoltosopimus_change_state() {
    var sopimus_id = $("input[name='huoltosopimus_id']").val();
    var newstate = $("#state_select").val();

    change_state(huoltosopimus, sopimus_id, newstate);
}

function change_state(type, id, newstate) {
    $.post(type.baseurl + id + "/setstate", {newstate: newstate});
    $("input[name='" + type.original_state + "']").val(newstate);

    $(type.button_id).val("Vaihdettu");
    $(type.button_id).prop('disabled', true);
}