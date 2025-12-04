// var swiper = new Swiper('.blog-slider', {
//     spaceBetween: 30,
//     effect: 'fade',
//     loop: true,
//     mousewheel: {
//         invert: false,
//     },
//     // autoHeight: true,
//     pagination: {
//         el: '.blog-slider__pagination',
//         clickable: true,
//     }
// });
//
// $(".custom-carousel").owlCarousel({
//     autoWidth: true,
//     loop: true
// });
// $(document).ready(function () {
//     $(".custom-carousel .item").click(function () {
//         $(".custom-carousel .item").not($(this)).removeClass("active");
//         $(this).toggleClass("active");
//     });
// });

"use strict";

let next = document.querySelector(".next");
let prev = document.querySelector(".prev");

next.addEventListener("click", function () {
    let items = document.querySelectorAll(".item");
    document.querySelector(".slide").appendChild(items[0]);
});

prev.addEventListener("click", function () {
    let items = document.querySelectorAll(".item");
    document.querySelector(".slide").prepend(items[items.length - 1]);
});
