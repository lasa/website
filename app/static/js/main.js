$(document).ready(function () {

var menu = $('.navbar');
var origOffsetY = menu.offset().top;

function scroll() {
    if ($(window).scrollTop() >= origOffsetY) {
        $('.navbar').addClass('sticky');
        $('.content').addClass('menu-padding');
    } else {
        $('.navbar').removeClass('sticky');
        $('.content').removeClass('menu-padding');
    }


   }

  document.onscroll = scroll;

});