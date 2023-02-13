/* global $ */

async function askServer(url, data) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const response = await fetch(url, {
    body: JSON.stringify(data),
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    method: 'POST',
    mode: 'cors',
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });
  return response.json();
}

/**
 * Check user bump status and then change bump button styles based on response.
 */
function action() {
  askServer('/bump_server', {
    server_id: $(this).attr('data-item'),
  }).then((data) => {
    // Change bump button to bumped and disable.
    if (data.result <= 5) {
      // Change button style and disable.
      $(this)
        .removeClass('btn-dark')
        .addClass('btn-light')
        .attr('data-original-title', 'Bumped')
        .tooltip('hide')
        .tooltip('show');
      const x = parseInt($(this).parent().find('p').text(), 10) + 1;
      $(this).parent().find('p').text(x);
    }
    // Disable remaining bump buttons if user used max bumps.
    if (data.result >= 5) {
      $('html')
        .find('.btn-dark[data-name="Bump Button"]')
        .removeClass('btn-dark')
        .addClass('btn-danger')
        .addClass('opacity-50')
        .attr('data-original-title', 'Out of bumps');
    }
  });
  return '';
}

/**
 * As Anchor goes over whole listing div, it also covers the button element.
 * This will check to see if the button has been clicked and if so
 * prevent the anchor loading the next page.
 * We also check the text inside the button has not been clicked
 * as that is a different event target.
 */
function clickA(e) {
  const target = $(e.target);
  if (target.is('button') || target.parent().is('button')) {
    e.preventDefault();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  $(document).on('click', 'a', (e) => {
    clickA(e);
  });

  $('button[data-name="Bump Button"]').on('click', function bump() {
    if ($(this).hasClass('btn-dark')) {
      action.call(this);
    }
  });
});
