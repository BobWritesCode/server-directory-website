"use strict";

// Global HTML Elements
const btnDeleteAccount = $("button[data-target='#delete-account-modal']");
const btnEmailUpdateConfirm = $("#email-update-form").find(
    "button[name='email-address-update-confirm']"
);

window.addEventListener("DOMContentLoaded", function () {
    btnDeleteAccount.on("click", function () {
        clearRemoveInput();
    });
    btnEmailUpdateConfirm.on("click", function () {
        userEmailUpdate();
    });
});

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

    if (val1 !== val2) {
        $("#email-update-form")
            .find("#id_email_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'> Must match. </div>"
            );
    }

    if (!validateEmail(val1)) {
        $("#email-update-form")
            .find("#id_email")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'> Not a valid email address </div>"
            );
    }

    if (!validateEmail(val2)) {
        $("#email-update-form")
            .find("#id_email_confirm")
            .after(
                "<div class='error-message alert alert-warning mt-1' role='alert'> Not a valid email address </div>"
            );
    }

    if ($(".error-message").length == 0) {
        $("#email-update-form").submit();
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
