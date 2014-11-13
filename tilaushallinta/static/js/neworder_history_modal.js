/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014
 */

var selection_type = "";

function show_history(type) {
    $('.row_data').remove();

    selection_type = type;

    var url = "";
    if(type == "tilaaja") {
        url = '/json/tilaajat_newest'
    } else {
        url = '/json/kohteet_newest'
    }
    $.get(url, function(data) {
        console.log(type);
        for(var i = 0; i < data.length; i++) {
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
                "<td><input type=\"radio\"></td>" +
                "<td>" + namerow + "</td>" +
                "<td>" + addressrow +  "</td>" +
                "</tr>")
        }
    });
    $('.modal').modal(/*options?*/);

}