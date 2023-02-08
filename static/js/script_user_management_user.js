"use strict";

// Globals
const form = $('#update-user-form');
const deleteForm = $("#user-delete-form")
const btnUpdate = $('button[name="user_management_save"]');
const btnDelete = $('button[name="btnDelete"]');
const btnDeleteConfirm = deleteForm.find('button[name="user-delete-confirm"]');

// Listeners
window.addEventListener("DOMContentLoaded", function() {
    btnUpdate.on("click", function(e) {
        e.preventDefault()
        $(".error-message").remove();
        const formData = {}
        if ($(".error-message").length == 0) {
            // Convert form data into an object with correct values.
            for (const i of form[0]) {
                if (i.type == 'checkbox') {
                    formData[i.name] = i.checked
                } else {
                    formData[i.name] = i.value
                }
            }
            action("user_management_save", formData);
        }
    });
    btnDeleteConfirm.on("click", function(e) {
        UserDeleteConfirm()
    });
});

// DOM Ready
$(document).ready(function() {
    form.find('#id_id').prop("readonly", "readonly").addClass("form-control-plaintext text-light border border-light ps-2").css('pointer-events', 'none');
});

/**
 * Call BootStrap toast to show
 */
function showToast() {
    $("#liveToast").toast({
        delay: 3000
    });
    $("#liveToast").toast("show");
}

/**
 * Call BootStrap toast to hide
 */
function hideToast() {
    $("#liveToast").toast("hide");
}

/**
 * Check user input matches expected input
 */
function UserDeleteConfirm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check user has input correct string.
    if ($("#id_delete_confirm").val() != "delete") {
        $("#id_delete_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>"
            );
    }
    // If no error messages then send request to server.
    if ($(".error-message").length == 0) {
        let input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "id")
            .val(form.find('#id_id').val());
        deleteForm.append(input);
        deleteForm.submit();
    }
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
            if (data.result.success) {
                // Show BootStrap toast
                showToast();
            } else {
                switch (data.result.reason) {

                    case "Username already taken":
                        form.find('#id_username')
                            .after(
                                "<div class='error-message alert alert-danger mt-1' role='alert'>Username already taken</div>"
                            );
                        break

                    case "No spaces allowed":
                        form.find('#id_username')
                            .after(
                                "<div class='error-message alert alert-danger mt-1' role='alert'>No spaces allowed</div>"
                            );
                        break

                    case "Must be at least 5 characters long":
                        form.find('#id_username')
                            .after(
                                "<div class='error-message alert alert-danger mt-1' role='alert'>Must be at least 5 characters long</div>"
                            );
                        break

                    case "Must be at 20 characters or less":
                        form.find('#id_username')
                            .after(
                                "<div class='error-message alert alert-danger mt-1' role='alert'>Must be at 20 characters or less</div>"
                            );
                        break

                    case "Email address already taken":
                        form.find('#id_email')
                            .after(
                                "<div class='error-message alert alert-danger mt-1' role='alert'>Email address already taken</div>"
                            );
                        break

                    case "Email address not valid":
                        form.find('#id_email')
                            .after(
                                "<div class='error-message alert alert-warning mt-1' role='alert'>Email address not valid</div>"
                            );
                        break
                };
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