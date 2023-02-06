"use strict";

// Globals
const btnLoadGame = $("#btnLoadGame");
const btnNewGame = $("#btnNewGame");
const form = $('#game-management-form');
const formInternalContainer = $('#form-internal-container');

// Listeners
window.addEventListener("DOMContentLoaded", function() {

    btnLoadGame.on("click", function() {
        clearForm();
        prepareFormForUpdateGame();
        action('get_game_details',$('#game-select-drop-down').val());
    });

    btnNewGame.on("click", function() {
        clearForm();
        prepareFormForNewGame();
    });
});

// DOM Ready
$(document)
    .ready(function() {
        $('.game-select-drop-down').select2();
        $('.tags-multiple').select2();
        $(".tags-multiple").select2({
            placeholder: "Select tags",
            allowClear: true
            });
        form.find('#id_id').prop("readonly", "readonly");
        form.find('#id_slug').prop("readonly", "readonly");
    });

// Functions
function action(arg) {
    addBump("/call_server", {
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

                    if (obj.image_public_id) {
                        // Image found, show image
                        form.find('#game-cover-container').removeClass('d-none');
                        form.find('#no-game-cover-container').addClass('d-none');
                        $("#game-cover-container").html(
                            "<img id='game_cover' src='" + obj.image['public_id'] + "' class='img-fluid mt-3 mb-2' style='max-height: 500px;' alt='Game cover'>");
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
                    // Allow submit button now to be clicked
                    form.find('button[type="submit"]').prop("disabled", false);
                };
            };
        });
}

function clearForm(){
    $('input:not([name=csrfmiddlewaretoken],[name="status"])').val('')
    form.find('#game-cover-container').addClass('d-none');
    form.find('#no-game-cover-container').addClass('d-none');
    $("#game-cover-container").html('');
    $('#tags-multiple').val('').trigger('change');
    form.find('input[name="status"]').prop("checked", false);
    form.find('button[type="submit"]').prop("disabled", true);
}

function prepareFormForNewGame() {
    $('#form-header').text('Adding New Game');
    formInternalContainer.removeClass('d-none');
    form.find("#div_id_id").addClass("d-none");
    form.find("#div_id_slug").addClass("d-none");
    form.find('button[type="submit"').text("Add new game");
    form.find('button[type="submit"]').prop("disabled", false);
}

function prepareFormForUpdateGame() {
    $('#form-header').text('Updating Game');
    formInternalContainer.removeClass('d-none');
    form.find('button[type="submit"').text("Save Changes");
    form.find("#div_id_id").removeClass("d-none");
    form.find("#div_id_slug").removeClass("d-none");
}


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