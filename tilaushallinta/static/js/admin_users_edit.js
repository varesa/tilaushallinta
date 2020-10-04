/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2016
 */

var fields = ["id", "nimi", "yritys", "ytunnus", "osoite", "postinumero", "postitoimipaikka", "puhelin", "email"];

/*
Selecting objects from the history
 */

var selection_type = "";
var orders = [];

function populate_modal(data) {
    /*
    Populate the modal list from data coming from the server,
    to be used as a callback
     */
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

        $('#history-table').append("<tr class=\"row_data\">" +
            "<td><input type=\"radio\" name=\"client_select\" value=" + i + "></td>" +
            "<td>" + namerow + "</td>" +
            "<td>" + addressrow +  "</td>" +
            "</tr>")
    }
}

function show_clients() {
    /*
    Show the popup window for choosing from existing objects
    triggered by a user click in the form
     */
    $('.row_data').remove();


    var url = "";
    var data = {};
    url = '/json/tilaajat';

    $.get(url, data, populate_modal);
    $('.modal').modal();
}

function set_client() {
    var radiobutton = $('input[name="client_select"]:checked');
    var row = radiobutton.parent().parent();
    var name = row.children()[1].innerHTML;

    $("#client_name").html("Tilaaja: " + name + " (ei tallennettu)");
    $("#client_id").val(radiobutton.val())
}
