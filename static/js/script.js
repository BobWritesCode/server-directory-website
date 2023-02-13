/* global $ */

// Global HTML Elements
const footerYear = $('#footer-year');

// DOM Ready
$(document).ready(() => {
  footerYear.text(new Date().getFullYear());
  $('[data-bs-toggle="tooltip"]').tooltip();
});
