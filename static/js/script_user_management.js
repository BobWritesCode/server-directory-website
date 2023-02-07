"use strict";

const btnUserSearch = $("#btnUserSearch");
const userSearchForm = $("#user-search-form")

// Listeners
window.addEventListener("DOMContentLoaded", function() {

    btnUserSearch.on("click", function(e) {
        e.preventDefault()
        validateForm()
        if ($(".error-message").length == 0) {
            action('search_users', $('#search-name').val());
        }
    });
});


function validateForm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check game name field is not black.
    if (!userSearchForm.find("#search-name").val()) {
        userSearchForm.find("#search-name")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Must not be blank</div>"
            );
    };
};

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
                if (arguments[0] == 'search_users') {
                    displayUsers(JSON.parse(data.result.users));
                };
            };
        });
}

function displayUsers(obj) {
    $('#user-search-display-table').find('tbody').html('')
    for (let i = 0; i < obj.length; i++) {
        let newTr = document.createElement("tr")
        $(newTr).append('<th scope="row">'+(i+1)+'</th>')
            .append('<td>'+obj[i].pk+'</td>')
            .append('<td>'+obj[i].fields.username+'</td>')
            .append('<td>'+obj[i].fields.email+'</td>');
        $('#user-search-display-table').find('tbody').append(newTr)
    }
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