"use strict";

window.addEventListener("DOMContentLoaded", function() {
    // As Anchor goes over whole listing, it also covers the button.
    // This will check to see if the button has been clicked and if so
    // prevent the anchor loading the next page.
    // We also check the text inside the button has not been clicked
    // as that is a different event target.
    $(document).on('click', 'a', function(e) {
        let target = $( e.target );
        if (target.is('button') || target.parent().is('button')) {
            e.preventDefault();
        }
    });

    $("button[data-name='Bump Button']").on("click", function() {
        if ($(this).hasClass('btn-dark')) {
            bump.call(this);
            return "";
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
            $(this).removeClass('btn-dark').addClass('btn-light')
                .attr('data-original-title', 'Bumped')
                .tooltip("hide").tooltip("show");
            let x = parseInt($(this).parent().find('p').text()) + 1;
            $(this).parent().find('p').text(x)
        };
        // Disable remaining bump buttons if user used max bumps.
        if (data.result >= 5) {
            $('html').find('.btn-dark[data-name="Bump Button"]')
                .removeClass('btn-dark')
                .addClass('btn-danger')
                .addClass('opacity-50')
                .attr('data-original-title', 'Out of bumps');
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
