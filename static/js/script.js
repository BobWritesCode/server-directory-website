"use strict";

// Global HTML Elements
const btnDeleteAccount = $("button[data-target='#delete-account-modal']");
const btnEmailUpdateConfirm = $("#email-update-form").find(
    "button[name='email-address-update-confirm']"
);
const btnServerListingDeleteConfirm = $("#server-listing-delete-form").find(
    "button[name='server-listing-delete-confirm']"
);

let lastIDBtn = 0;

window.addEventListener("DOMContentLoaded", function () {
    // Keep track of last item id pressed.
    $("button").on("click", function () {
        if ($(this).attr("data-item")) {
            lastIDBtn = $(this).attr("data-item");
        }
    });

    $("button[data-name='Bump Button']").on("click", function () {
        if ($(this).text() != "Bumped") {
            $(this).text("Bumped")
            bump($(this).attr("data-item"));
        }
    });

    btnDeleteAccount.on("click", function () {
        clearRemoveInput();
    });
    btnEmailUpdateConfirm.on("click", function () {
        userEmailUpdate();
    });
    btnServerListingDeleteConfirm.on("click", function () {
        ServerListingDeleteConfirm();
    });
});

/**
 * Check user input matches expected input
 * @return {None} No  return
 */
function ServerListingDeleteConfirm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check user has input correct string.
    if ($("#id_server_listing_delete_confirm").val() != "delete") {
        $("#server-listing-delete-form")
            .find("#id_server_listing_delete_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>"
            );
    }
    // If no error messages then send request to server.
    if ($(".error-message").length == 0) {
        var input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "itemID")
            .val(lastIDBtn);
        $("#server-listing-delete-form").append(input);
        $("#server-listing-delete-form").submit();
    }
}

/**
 * Clears input box where user will need to type 'remove' to confirm
 * account deletion.
 * @return {None} No  return
 */
function clearRemoveInput() {
    $("#div_id_confirm").find("input[name=confirm]").val("");
}

/**
 * Validate form before submit.
 * Validation to see both vales are valid emails addresses and match.
 */
function userEmailUpdate() {
    const val1 = $("#email-update-form").find("#id_email").val();
    const val2 = $("#email-update-form").find("#id_email_confirm").val();

    $(".error-message").remove();

    // Check if email is correct format.
    if (!validateEmail(val1)) {
        $("#email-update-form")
            .find("#id_email")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'> Not a valid email address </div>"
            );
        return;
    }

    // Check if both inputs match.
    if (val1 !== val2) {
        $("#email-update-form")
            .find("#id_email_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'> Must match. </div>"
            );
        return;
    }

    // If no error messages then send request to server to check input email address does not already exist.
    if ($(".error-message").length == 0) {
        checkEmailInUse("/request", { email: val1 }).then((data) => {
            if (data.result) {
                $("#email-update-form")
                    .find("#id_email")
                    .after(
                        "<div class='error-message alert alert-warning mt-1' role='alert'> Email address already registered </div>"
                    );
            } else {
                $("#email-update-form").submit();
            }
        });
    }
}

/**
 * Returns true/false if arg is a valid email address.
 */
function validateEmail(email) {
    const atPosition = email.indexOf("@");
    const dotPosition = email.lastIndexOf(".");
    return !(
        atPosition < 1 ||
        dotPosition < atPosition + 2 ||
        dotPosition + 2 >= email.length
    );
}

/**
 * Send a request to the server to check if user input email address is already registered.
 * @returns True or False
 */
async function checkEmailInUse(url = "", data = {}) {
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


function bump(server_id) {
    addBump("/bump_server", { server_id: server_id }).then((data) => {
        if (data.result) {
            // return true
            console.log(data.result);
        } else {
            // return false
            console.log(data.result);
        }
    });
}



async function addBump(url = "", data = {}) {
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