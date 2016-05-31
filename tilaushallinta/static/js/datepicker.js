/*
 * This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2016
 */

// Enable date pickers
$(document).ready(function() {
    var date_inputs = $('.input-group.date');
    if(date_inputs.length) {
        date_inputs.datepicker({language: 'fi'});
    }
});