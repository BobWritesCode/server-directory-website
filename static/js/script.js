"use strict";

// DOM Ready
$(document).ready(function() {
    $('#footer-year').text(new Date().getFullYear())
    $('[data-bs-toggle="tooltip"]').tooltip();
});
