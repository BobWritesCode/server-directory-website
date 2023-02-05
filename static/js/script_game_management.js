"use strict";

// Globals
const btnLoadGame = $("#btnLoadGame");
const btnSubmit = $('#game-management-form').find("button[type='button']");

// Listeners
window.addEventListener("DOMContentLoaded", function () {

    btnLoadGame.on("click", function () {
        action('get_game_details', $('#game-select-drop-down').val());
    });

    btnSubmit.on("click", function () {
        $('#game-management-form').find('#id_id').prop( "disabled", false)
        $('#game-management-form').find('#id_slug').prop( "disabled", false)
        $("#game-management-form").submit();
        $('#game-management-form').find('#id_id').prop( "disabled", true)
        $('#game-management-form').find('#id_slug').prop( "disabled", true)
    });

});

// DOM Ready
$(document).ready(function() {
    $('.game-select-drop-down').select2();
    $('.tag-select-drop-down-multiple').select2();
});

// Functions
function action(arg) {
    console.log(arguments[1]);
    addBump("/call_server", { arguments: arguments }).then((data) => {

        if (data.result) {

            if (arguments[0]=='get_game_details'){
                const obj = JSON.parse(data.result.game);
                const obj2 = JSON.parse(data.result.game_tags);
                console.log(obj2);
                $('#game-management-form').find('#id_id').val(obj.id);
                $('#game-management-form').find('#id_name').val(obj.name);
                $('#game-management-form').find('#id_slug').val(obj.slug);
                $('#game-management-form').find('button[type="button"]').prop( "disabled", false );
            };

        };
    });
}


async function askServer(url = "", data = {}) {
    const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
    const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: { "X-CSRFToken": csrftoken },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify(data),
    });
    return response.json();
}