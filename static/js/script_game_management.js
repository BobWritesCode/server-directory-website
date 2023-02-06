"use strict";

// Globals
const btnLoadGame = $("#btnLoadGame");
const btnNewGame = $("#btnNewGame");
const form = $('#game-management-form');
const btnSubmit = form.find('button[type="submit"]');
const formInternalContainer = $('#form-internal-container');

// Listeners
window.addEventListener("DOMContentLoaded", function() {

    btnLoadGame.on("click", function() {
        clearForm();
        $(".error-message").remove();
        prepareFormForUpdateGame();
        action('get_game_details', $('#game-select-drop-down').val());
    });

    btnNewGame.on("click", function() {
        clearForm();
        $(".error-message").remove();
        prepareFormForNewGame();
    });

    btnSubmit.on("click", function(e) {
        e.preventDefault()
        validateForm()
        if ($(".error-message").length == 0) {
            submitForm();
        }
    });

});

// DOM Ready
$(document)
    .ready(function() {
        $('.game-select-drop-down').select2();
        $(".tags-multiple").select2({
            placeholder: "Select tags",
            allowClear: true,
            closeOnSelect: false,
        });
        form.find('#id_id').prop("readonly", "readonly");
        form.find('#id_slug').prop("readonly", "readonly");
    });

// Functions

/**
 * Validates the user form for either adding or updating a game.
 * Shows errors to the user if any.
 */
function validateForm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();

    // Check game name field is not black.
    if (!form.find("#id_name").val()) {
        form.find("#id_name")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must not be blank</div>"
            );
    }

    // Check at least 1 tag is selected.
    if ($(".select2-selection__choice").length == 0) {
        form.find(".select2-container")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Select at least 1 tag</div>"
            );
    }

    // Check user has chosen a status.
    if (!form.find("input[type='radio']:checked").val()) {
        form.find("#div_id_status")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must select 1 option</div>"
            );
    }

}

/**
 * Performs a promise using askServer() to return a json.
 * @param {string} arg [1] The action you wish to call. See website.views.py call_server(). Currently on set up to use 'get_game_details'
 * @param {*} arg... [...] Any other data you wish to send to server.
 */
function action(...args) {
    askServer("/call_server", {
            arguments: arguments
        })
        .then((data) => {

            if (data.result) {
                if (arguments[0] == 'get_game_details') {
                    // Turn game json into object
                    const obj = JSON.parse(data.result.game);
                    // Turn tags json into an object
                    const obj2 = JSON.parse(data.result.game_tags);
                    // Pre-fill inputs in form
                    form.find('#id_id').val(obj.id);
                    form.find('#id_name').val(obj.name);
                    form.find('#id_slug').val(obj.slug);
                    if (obj.image) {
                        // Image found, show image
                        form.find('#game-cover-container').removeClass('d-none');
                        form.find('#no-game-cover-container').addClass('d-none');
                        $("#game-cover-container").html(
                            "<img id='game_cover' src='" + obj.image.public_id + "' class='img-fluid mt-3 mb-2' style='max-height: 500px;' alt='Game cover'>");
                    } else {
                        // Image not found, show placeholder
                        form.find('#game-cover-container').addClass('d-none');
                        form.find('#no-game-cover-container').removeClass('d-none');
                        $("#game-cover-container").html('');
                    }
                    form.find('input[name="status"][value="' + obj.status + '"]').prop("checked", true);

                    // Create an array from tags linked to game selected.
                    const tags = Array.from(Object.values(obj2), x => x.pk)
                    // Populate multi choice dropdown with correct tags
                    $('#tags-multiple').val(tags).trigger('change')
                };
            };
        });
}

/**
 * Clears html form when choose to update or add game
 */
function clearForm() {
    $('input:not([name=csrfmiddlewaretoken],[name="status"])').val('')
    form.find('#game-cover-container').addClass('d-none');
    form.find('#no-game-cover-container').addClass('d-none');
    $("#game-cover-container").html('');
    $('#tags-multiple').val('').trigger('change');
    form.find('input[name="status"]').prop("checked", false);
    btnSubmit.prop("disabled", true);
}

/**
 * Prepare html form ready to input a new game
 */
function prepareFormForNewGame() {
    $('#form-header').text('Adding New Game');
    formInternalContainer.removeClass('d-none');
    form.find("#div_id_id").addClass("d-none");
    form.find("#div_id_slug").addClass("d-none");
    btnSubmit.text("Add new game");
    btnSubmit.prop("disabled", false);
}

/**
 * Prepare html form ready to update selected game
 */
function prepareFormForUpdateGame() {
    $('#form-header').text('Updating Game');
    formInternalContainer.removeClass('d-none');
    form.find("#div_id_id").removeClass("d-none");
    form.find("#div_id_slug").removeClass("d-none");
    btnSubmit.text("Save Changes");
    btnSubmit.prop("disabled", false);
}

/**
 * Submits form via Post
 */
function submitForm() {
    form.submit();
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