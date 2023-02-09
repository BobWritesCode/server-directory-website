"use strict";

// Global HTML Elements
const form = $('#listing-form');
const btnSubmit = form.find('button[type="submit"]');
const dropDownGame = form.find('#id_game');

// DOM Ready
$(document).ready(function() {
    $("#tags-multiple").select2({
        placeholder: "Select tags",
        allowClear: true,
        closeOnSelect: false,
        theme: "classic"});
    get_tags();
    // Parse selected tags twice to create JS object.
    const obj = JSON.parse($('#selected_tags').text());
    const obj2 = JSON.parse(obj)
    // Create an array from tags linked to game selected.
    const tags = Array.from(obj2, x => x.pk)
    // Populate multi choice dropdown with correct tags
    $('#tags-multiple').val(tags).trigger('change');
});

// Listeners
window.addEventListener("DOMContentLoaded", function() {
    btnSubmit.on("click", function(e) {
        e.preventDefault()
        validateForm();
        if ($(".error-message").length == 0) {
            submitForm();
        }
    });

    dropDownGame.on("input", function(e) {
        $('#tags-multiple').val(null)
            .trigger('change')
            .html("");

        $("#tags-multiple").select2({
            placeholder: "Choose game first"})
            .prop("disabled", true);

        if (dropDownGame.val() != 0) {
            get_tags();
        }
    });
});

async function get_tags() {
    action('get_game_tags', dropDownGame.val());
    $("#tags-multiple").select2({
        placeholder: "Select tags"})
        .prop("disabled", false);
    return true
}

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

/**
 * Performs a promise using askServer() to return a json.
 * @param {string} arg [1] The action you wish to call. See website.views.py
 * call_server(). Currently on set up to use 'get_tag_details'
 * @param {*} arg... [...] Any other data you wish to send to server.
 */
function action(...args) {
    askServer("/call_server", {
            arguments: arguments
        })
        .then((data) => {
            if (data.result.success == "tags") {
                    const tags = data.result.reason
                    for (const tag of tags) {
                        let newOption = new Option(tag[1], tag[0], false, false);
                        $('#tags-multiple').append(newOption).trigger('change');
                    }
            };
        });
}

/**
 * Performs callback from server
 * @async
 * @param  {string} url URL to call in website.urls.py
 * @param  {object} data Check  website.views.py call_server() for options
 * @returns {json}
 */
async function askServer(url = "", data = {}) {
    const csrftoken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
        )
        .value;
    const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrftoken
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify(data),
    });
    return response.json();
}