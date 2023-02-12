// Global HTML Elements
const footerYear = $('#footer-year');

// DOM Ready
$(document).ready(function() {
    'use strict';
    footerYear.text(new Date().getFullYear());
    $('[data-bs-toggle="tooltip"]').tooltip();
});
