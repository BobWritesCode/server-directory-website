"use strict";

// Global HTML Elements
const form = $('#listing-form');
const btnSubmit = form.find('button[type="submit"]');

// DOM Ready
$(document).ready(function() {
    $("#tags-multiple").select2({
        placeholder: "Select tags",
        allowClear: true,
        closeOnSelect: false,
    });
});

// Listeners
window.addEventListener("DOMContentLoaded", function() {
    btnSubmit.on("click", function(e) {
        e.preventDefault()
        validateForm()
        if ($(".error-message").length == 0) {
            submitForm();
        }
    });
});

/**
 * Validates the form.
 * Shows errors to the user if any.
 */
function validateForm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check game picked
    if (!form.find("#id_game").val()) {
        form.find("#id_game")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must select a game</div>"
            );
    }
    // Check name given
    if (!form.find("#id_title").val()) {
        form.find("#id_title")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must provide a name</div>"
            );
    }
    // Check name given is long enough
    if (form.find("#id_title").text().length > 0 && form.find("#id_title").text().length < 5 ) {
        form.find("#id_title")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must be at least 5 characters long</div>"
            );
    }
    // Check at least 1 tag is selected.
    if ($(".select2-selection__choice").length == 0) {
        form.find(".select2-container")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Select at least 1 tag</div>"
            );
    }
    // Check no more then tags selected.
    if ($(".select2-selection__choice").length > 10) {
        form.find(".select2-container")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Maximum tags allowed is 10, please remove some.</div>"
            );
    }
    // Check short description is long enough.
    if ($(tinyMCE.get('id_short_description').getBody()).text().length < 100) {
        $('#div_id_short_description')
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must be at least 100 characters long</div>"
            );
    }
    // Check short description is not too long.
    if ($(tinyMCE.get('id_short_description').getBody()).text().length > 200) {
        console.log( "error");
        $('#div_id_short_description')
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must be under 200 characters long</div>"
            );
    }
    // Check long description is long enough.
    if ($(tinyMCE.get('id_long_description').getBody()).text().length < 200) {
        console.log( "error");
        $('#div_id_long_description')
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must be at least 200 characters long</div>"
            );
    }
    // Check long description is not too long.
    if ($(tinyMCE.get('id_long_description').getBody()).text().length > 2000) {
        console.log( "error");
        $('#div_id_long_description')
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must be under 2000 characters long</div>"
            );
    }
    // Check has discord server
    if (!form.find("#id_discord").val()) {
        form.find("#id_discord")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must provide discord invite code</div>"
            );
    }
}

/**
 * Submits form via Post
 */
function submitForm() {
    form.submit();
}