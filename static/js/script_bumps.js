"use strict";

window.addEventListener("DOMContentLoaded", function() {
    $("button[data-name='Bump Button']").on("click", function() {
        if ($(this).text() != "Bumped") {
            $(this).text("Bumped")
            bump.call(this);
        }
    });
});

/**
 * Check user bump status and then change bump button styles based on response.
 */
function bump() {
    addBump("/bump_server", {
        server_id: $(this).attr("data-item")
    }).then((data) => {
        // Change bump button to bumped and disable.
        if (data.result <= 5) {
            // Change button style and disable.
            $(this).attr("disabled", true)
                .removeClass('btn-primary')
                .addClass('btn-success')
                .text('BUMPED!')
        };
        // Disable remaining bump buttons if user used max bumps.
        if (data.result >= 5) {
            $('html').find('.btn-primary[data-name="Bump Button"]')
                .attr("disabled", true)
                .removeClass('btn-primary')
                .addClass('btn-warning')
                .text('No more bumps!')
        };
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
        headers: {
            "X-CSRFToken": csrftoken
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify(data),
    });
    return response.json();
}
