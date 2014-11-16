/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014
 */

var selection_type = "";
var orders = [];

function populate_modal(data) {
    for(var i = 0; i < data.length; i++) {
        orders[i] = data[i];
        var namerow = "";
        if(data[i]['yritys'].length > 0) {
            namerow += data[i]['yritys'];
            if(data[i]['nimi'].length > 0) {
                namerow += ", " + data[i]['nimi'];
            }
        } else {
            namerow = data[i]['nimi'];
        }

        var addressrow = data[i]['osoite'] + ", " + data[i]['postinumero'] + ' ' + data[i]['postitoimipaikka'];

        $('#table_history').append("<tr class=\"row_data\">" +
            "<td><input type=\"radio\" name=\"history_selector\" value=" + i + "></td>" +
            "<td>" + namerow + "</td>" +
            "<td>" + addressrow +  "</td>" +
            "</tr>")
    }
}

function show_history(type) {
    $('.row_data').remove();

    selection_type = type;

    var url = "";
    if(type == "tilaaja") {
        url = '/json/tilaajat_newest'
    } else {
        url = '/json/kohteet_newest'
    }

    $.get(url, populate_modal);
    $('.modal').modal();

}

function load_order() {
    console.log(selection_type);

    var radiobutton = $('input[name="history_selector"]:checked');
    if(radiobutton.length < 1) {
        return; // No order selected
    }
    var value = radiobutton.val();
    var order = orders[parseInt(value)];

    console.log(order);

    var fields = ["uuid", "nimi", "yritys", "ytunnus", "osoite", "postinumero", "postitoimipaikka", "puhelin", "email"];
    for(var i = 0; i < fields.length; i++) {
        $('input[name="' + selection_type + "_" + fields[i] + '"]').val(order[fields[i]]);
        $('input[name="' + selection_type + "_" + fields[i] + '"]').prop("readonly", true);
    }
    $('input[name="' + selection_type + '_uuid"]').val(order['uuid']);

    $('.modal').modal('hide');
}