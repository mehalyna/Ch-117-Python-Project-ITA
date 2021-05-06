'use strict'

const top_swiper = new Swiper('.first-container', {
  // Optional parameters
  direction: 'horizontal',
  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: '.first-next',
    prevEl: '.first-prev',
  },

  slidesPerView: 5,
  spaceBetween: 20,
  speed: 600,
});


const new_slider = new Swiper('.second-container', {
  // Optional parameters
  direction: 'horizontal',
  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: '.second-next',
    prevEl: '.second-prev',
  },

  slidesPerView: 5,
  spaceBetween: 20,
  speed: 600,
});

setTimeout(function () {
    if ($('#msg').length > 0) {
        $('#msg').fadeTo(500, 0, function () {})
    }
}, 2000)
