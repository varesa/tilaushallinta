/*
 * This source code is licensed under the terms of the
 * Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
 * To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
 * Copyright Esa Varemo 2014-2016
 */

var index;
var orders = [];

function create_index() {
    index = lunr(function () {
        this.ref('id');
        this.field('id2');
        this.field('reference');
        this.field('tila');
        
        this.field('tilaaja_nimi');
        this.field('tilaaja_yritys');
        this.field('tilaaja_osoite');
        this.field('tilaaja_postinumero');
        this.field('tilaaja_postitoimipaikka');
        
        this.field('kohde_nimi');
        this.field('kohde_yritys');
        this.field('kohde_osoite');
        this.field('kohde_postinumero');
        this.field('kohde_postitoimipaikka');
    });
    index.pipeline.reset();
}

function index_order(order) {
    if(order.id === 211) {
        var x = 0;
    }
    index.add({
        id:  order.id,
        id2: order.id2,
        reference: order.reference,
        date: order.date,
        tila: order.tila,

        'tilaaja_nimi': order.tilaaja.nimi,
        'tilaaja_yritys': order.tilaaja.yritys,
        'tilaaja_osoite': order.tilaaja.osoite,
        'tilaaja_postinumero': order.tilaaja.postinumero,
        'tilaaja_postitoimipaikka': order.tilaaja.postitoimipaikka,

        'kohde_nimi': order.kohde.nimi,
        'kohde_yritys': order.kohde.yritys,
        'kohde_osoite': order.kohde.osoite,
        'kohde_postinumero': order.kohde.postinumero,
        'kohde_postitoimipaikka': order.kohde.postitoimipaikka
    });
}

function get_orders() {
    $.get("/tilaukset/json", function (data) {
       var obj = JSON.parse(data);
       for(var x = 0; x < obj.length; x++) {
           var order = obj[x];
           orders[order.id] = order;
           index_order(order);
       }
   });
}

$(document).ready(function () {
    create_index();
    get_orders();

    $("#order_search_field").keyup(function () {
        var text = $(this).val();

        if(text.length) {
            var results = index.search(text);
            results.sort(function (a, b) {
                if(a.ref < b.ref) {
                    return 1;
                } else {
                    return -1;
                }
            });
            if(results.length) {
                $("#search-results tr").remove();
                $("#search-panel-body").css("display", "");
                $("#search-results").append("<tr><th>#</th><th>Tila</th><th>Tilaaja</th><th>Kohteen osoite</th></tr>");
                for(var x = 0; x < results.length; x++) {
                    var order = orders[results[x].ref];

                    var nimi;
                    if(order.tilaaja.nimi.length && order.tilaaja.yritys.length) {
                        nimi = order.tilaaja.nimi + ", " + order.tilaaja.yritys;
                    } else {
                        nimi = order.tilaaja.nimi + order.tilaaja.yritys;
                    }

                    var osoite = order.kohde.osoite + ", " + order.kohde.postinumero + " " + order.kohde.postitoimipaikka;

                    $("#search-results").append("<tr onclick='window.location.href=\"/tilaukset/" + order.id + "\"'>" +
                        "<td>" + order.id2 + "</td>" +
                        "<td><span class='tilaus_tila tila_" + order.tila.toLowerCase() + "'>" + order.tila[0] + order.tila.substring(1).toLowerCase() +  "</span></td>" +
                        "<td>" + nimi + "</td>" +
                        "<td>" + osoite + "</td>" +
                        "</tr>");
                }
            } else {
                $("#search-panel-body").css("display", "none");
            }

            $(".panel").css("display", "none");
            $("#search-panel").css("display", "");
        } else {
            $(".panel").css("display", "");
            $("#search-panel-body").css("display", "none");
        }
    })
});