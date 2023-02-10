"use strict";

// Globals
const form = $('#update-user-form');
const userDeleteForm = $("#user-delete-form")
const listingDeleteForm = $("#listing-delete-form")
const banForm =$('#user-ban-form')
const verifyForm =$('#user-ban-form')
const promoteForm =$('#user-promote-form')
const demoteForm =$('#user-demote-form')

const btnUpdate = $('button[name="user_management_save"]');
const btnDelete = $('button[name="btnDelete"]');
const btnBan = $('button[name="user_management_ban"]');
const btnUnban = $('#btnUnban');

const btnDeleteConfirm = userDeleteForm.find('button[name="user-delete-confirm"]');
const btnListingDeleteConfirm = listingDeleteForm.find('button[name="listing-delete-confirm"]');
const btnBanConfirm = banForm.find('button[name="user-ban-confirm"]');
const btnVerifyConfirm =$('button[name="user-verify-confirm"]')
const btnPromoteConfirm = promoteForm.find('button[name="user-promote-confirm"]')
const btnDemoteConfirm = demoteForm.find('button[name="user-demote-confirm"]')


let lastDeleteBtnID = null

// Listeners
window.addEventListener("DOMContentLoaded", function() {
    // Keep track of last item id pressed.
    $("button[data-target='#listing-delete-modal']").on("click", function() {
        if ($(this).attr("data-item")) {
            lastDeleteBtnID = $(this).attr("data-item");
        }
    });

    btnUnban.on("click", function(e) {
        e.preventDefault()
        let input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "unban")
            .val(true);
        form.append(input).submit();
    });

    btnVerifyConfirm.on("click", function(e) {
        e.preventDefault()
        let input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "email-verify")
            .val(true);
        form.append(input).submit();
    });

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
    btnListingDeleteConfirm.on("click", function(e) {
        ListingDeleteConfirm();
    });
    btnDeleteConfirm.on("click", function(e) {
        UserDeleteConfirm();
    });
    btnBanConfirm.on("click", function(e) {
        UserBanConfirm();
    });
    btnPromoteConfirm.on("click", function(e) {
        e.preventDefault()
        promoteUserToStaff();
    });
    btnDemoteConfirm.on("click", function(e) {
        e.preventDefault()
        demoteUserFromStaff();
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
 * Check user input matches expected input before deletion, then deletes listing.
 */
function ListingDeleteConfirm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check user has input correct string.
    if ($("#delete_listing_confirm").val() != "delete") {
        $("#delete_listing_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>"
            );
    }
    // If no error messages then send request to server.
    if ($(".error-message").length == 0) {
        let input = $("<input>")
            .attr("type", "hidden")
            .attr("name", "id")
            .val(lastDeleteBtnID);
        let input2 = $("<input>")
            .attr("type", "hidden")
            .attr("name", "user_id")
            .val(form.find('#id_id').val());
        listingDeleteForm.append(input).append(input2).submit();
    }
}

/**
 * Check user input matches expected input before ban, then bans user.
 */
function UserBanConfirm() {
    // Clear any current error messages from screen.
    $(".error-message").remove();
    // Check user has input correct string.
    if ($("#ban_confirm").val() != "ban") {
        $("#ban_confirm")
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
        banForm.append(input);
        banForm.submit();
    }
}


/**
 * Check user input matches expected input before deletion, then deletes user.
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
        userDeleteForm.append(input);
        userDeleteForm.submit();
    }
}

/**
 * Promotes user to staff member.
 */
function promoteUserToStaff() {
    let input = $("<input>")
        .attr("type", "hidden")
        .attr("name", "promote")
        .val(true);
    form.append(input);
    form.submit();
}

/**
 * Promotes user to staff member.
 */
function demoteUserFromStaff() {
    let input = $("<input>")
        .attr("type", "hidden")
        .attr("name", "demote")
        .val(true);
    form.append(input);
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
