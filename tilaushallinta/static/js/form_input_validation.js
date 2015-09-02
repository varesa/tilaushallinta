/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2015
 */


// Enable date pickers
$(document).ready(function() {
    $('.input-group.date').datepicker({language: 'fi'});
});

// Add asterisks to fields that have been marked as required
$(document).ready(function() {
    var pattern =  /([^<]*)(.*)/;
    var lines = $(".required");
    lines.each(function(index, element) {
        if($(element).children("label").length) {
            $(element).children("label").append('<span class="asterisk">*</span>');
        } else {
            var matches = pattern.exec($(element).html());
            var label = matches[1];
            var rest = matches[2];
            $(element).html(label + '<span class="asterisk">*</span>' + rest);
        }
    });
});

// Called whem submitting the form, checks if input data is valid
function check_input() {
    var invalid = false;
    $(".required input, .required textarea").each(function(index, element) {
        if($(element).prop("type") == 'checkbox') {
            console.log("checkbox found")
            if(!$(element).prop("checked")) {
                invalid = true;
                console.log("Checkbox empty");
            }
        } else if($(element).prop("type") == 'textarea') {
            console.log("textarea found");
            if($(element).val().length == 0) {
                invalid = true;
                console.log("Textarea empty");
            }
        } else if($(element).prop("type") == 'text') {
            console.log("textfield found");
            if($(element).val().length == 0) {
                invalid = true;
                console.log("Text field empty");
            }
        }
    });
    return !invalid;
}