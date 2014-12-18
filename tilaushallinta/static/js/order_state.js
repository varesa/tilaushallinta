/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014
 */

function order_state_changed() {
    var oldstate = $("input[name='tilaus_originalstate']").val();
    var newstate = $("#order_state_select").val();

    if(oldstate != newstate) {
        $("#table_order_status input").prop('disabled', false);
        $("#table_order_status input").val("Vaihda");
    } else {
        $("#table_order_status input").prop('disabled', true);
    }
}

function order_change_state() {
    var tilaus_id = $("input[name='tilaus_id']").val();
    var newstate = $("#order_state_select").val();

    $.post("/tilaukset/" + tilaus_id + "/setstate", {newstate: newstate});

    $("input[name='tilaus_originalstate']").val(newstate);

    $("#table_order_status input").val("Vaihdettu");
    $("#table_order_status input").prop('disabled', true);

}