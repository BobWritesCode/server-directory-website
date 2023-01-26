"use strict";

// Global HTML Elements
const btnDeleteAccount = $("button[data-target='#delete-account-modal']");

window.addEventListener("DOMContentLoaded", function () {
    btnDeleteAccount.on("click", function () {
        clearRemoveInput();
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
