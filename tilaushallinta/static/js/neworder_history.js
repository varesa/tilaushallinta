/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014
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

        $('#table_history').append("<tr class=\"row_data\">" +
            "<td><input type=\"radio\" name=\"history_selector\" value=" + i + "></td>" +
            "<td>" + namerow + "</td>" +
            "<td>" + addressrow +  "</td>" +
            "</tr>")
    }
}

function show_history(type) {
    /*
    Show the popup window for choosing from existing objects
    triggered by a user click in the form
     */
    $('.row_data').remove();

    selection_type = type;

    var url = "";
    if(type == "tilaaja") {
        url = '/json/tilaajat'
    } else {
        url = '/json/kohteet'
    }

    $.get(url, populate_modal);
    $('.modal').modal();

}

function load_order() {
    /*
    Load the data from an object and insert it into the form,
    triggered by user selecting an item in the modal
     */
    console.log(selection_type);

    var radiobutton = $('input[name="history_selector"]:checked');
    if(radiobutton.length < 1) {
        return; // No order selected
    }
    var value = radiobutton.val();
    var order = orders[parseInt(value)];

    console.log(order);


    // Load data and set to read-only
    for(var i = 0; i < fields.length; i++) {
        $('input[name="' + selection_type + "_" + fields[i] + '"]').val(order[fields[i]]);
        $('input[name="' + selection_type + "_" + fields[i] + '"]').prop("readonly", true);
    }

    // Save the id of the original
    $('input[name="' + selection_type + '_id"]').val(order['id']);

    // Make sure edit is 0
    $('input[name="' + selection_type + '_edit"]').val('0');

    // Hide the selection box
    $('.modal').modal('hide');

    // Show the 'edit'/'create new based on' controls
    $('#old_' + selection_type + '_controls').css("display", "table-cell");
}

/*
Editing the existing object / creating a new one based on it
 */

function edit_existing(type) {
    // Remove read-only property
    for(var i = 0; i < fields.length; i++) {
        $('input[name="' + type + "_" + fields[i] + '"]').prop("readonly", false);
    }

    // Set 'edit' to true
    $('input[name="' + type + '_edit"]').val('1');

    // Remove controls
    $('#old_' + type + '_controls').css("display", "none");

    // set message
    var target;
    if(type == 'tilaaja')
        target = 'tilaajaa';
    else
        target = 'kohdetta';
    $('#old_' + type + '_state').html("Muokataan aikaisempaa " + target);
}

function create_new_based_on(type) {
    // Remove read-only property
    for(var i = 0; i < fields.length; i++) {
        $('input[name="' + type + "_" + fields[i] + '"]').prop("readonly", false);
    }

    // Reset the "existing id"
    $('input[name="' + type + '_id"]').val('');

    // Remove controls
    $('#old_' + type + '_controls').css("display", "none");
}