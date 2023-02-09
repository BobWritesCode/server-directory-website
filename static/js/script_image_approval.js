"use strict";

// Globals
const btnApprove = $("#btnApprove");
const btnReject = $("#btnReject");
const btnBan = $("#btnBan");
const btnNext = $("#btnNext");

// Listeners
window.addEventListener("DOMContentLoaded", function () {

    btnApprove.on("click", function () {
        action('image_approval_approve', $('#current_id').text());
    });
    btnReject.on("click", function () {
        action('image_approval_reject', $('#current_id').text());
    });
    btnBan.on("click", function () {
        action('image_approval_ban', $('#current_id').text());
    });
    btnNext.on("click", function () {
        action('image_approval_next');
    });
});

function action(arg) {
    askServer("/call_server", { arguments: arguments }).then((data) => {
        if (data.result) {
            if (arguments[0]=='image_approval_next'){
                window.location.href = String(data.result.text);
            }else{
                $('#status_txt').text(data.result.text)
                btnNext.removeAttr('disabled')
            }

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