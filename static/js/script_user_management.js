/* global $ */

const btnUsernameSearch = $('#btnUserSearch');
const btnEmailSearch = $('#btnEmailSearch');
const btnIDSearch = $('#btnIDSearch');
const userSearchForm = $('#user-search-form');
const inputSearch = $('#search-name');

/**
 * Validates the form and provides error messages to the user if any.
 */
function validateForm(btnType) {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check game name field is not blank.
  if (!inputSearch.val()) {
    userSearchForm
      .find('#search-name')
      .after(
        "<div class='error-message alert alert-warning mt-1' role='alert'>Must not be blank</div>",
      );
    return;
  }
  if (btnType === 'id' && !Number.isInteger(parseInt(inputSearch.val(), 10))) {
    userSearchForm
      .find('#search-name')
      .after(
        "<div class='error-message alert alert-warning mt-1' role='alert'>Must be whole number when searching by ID</div>",
      );
  }
}

/**
 * Updates the number of results in the DOM.
 * @param {object} num The number of results in the array of users received from the server.
 */
function updateResultCount(num) {
  $('#id_results_number').text(`Results found: ${num}`);
}

/**
 * Performs a promise using askServer() to return a json.
 * @param {object} users Receives users as an object from action(). Then converts
 * them into rows and appends them into a html table.
 */
function displayUsers(users) {
  const tableBody = $('#user-search-display-table tbody');
  tableBody.empty();
  for (let i = 0; i < users.length; i += 1) {
    const user = users[i];
    const row = $('<tr>').appendTo(tableBody);
    $('<th>', { scope: 'row', text: i + 1 }).appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.pk,
        }),
      )
      .appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.fields.username,
        }),
      )
      .appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.fields.email,
        }),
      )
      .appendTo(row);
  }
}

/**
 * Performs callback from server
 * @async
 * @param  {string} url URL to call in website.urls.py
 * @param  {object} data Check  website.views.py call_server() for options
 * @returns {json}
 */
async function askServer(url = '', data = {}) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data),
  });
  return response.json();
}

/**
 * Performs a promise using askServer() to return a json.
 * @param {string} arg [1] The action you wish to call. See website.views.py call_server().
 * Currently on set up to use 'get_game_details'
 * @param {*} arg... [...] Any other data you wish to send to server.
 */
function action(...args) {
  askServer('/call_server', {
    args,
  }).then((data) => {
    if (data.result) {
      const results = JSON.parse(data.result.users);
      displayUsers(results);
      updateResultCount(results.length);
    }
  });
}

// Listeners
window.addEventListener('DOMContentLoaded', () => {
  btnUsernameSearch.on('click', (e) => {
    e.preventDefault();
    validateForm('username');
    if ($('.error-message').length === 0) {
      action('search_users_username', $('#search-name').val());
    }
  });

  btnEmailSearch.on('click', (e) => {
    e.preventDefault();
    validateForm('email');
    if ($('.error-message').length === 0) {
      action('search_users_email', $('#search-name').val());
    }
  });

  btnIDSearch.on('click', (e) => {
    e.preventDefault();
    validateForm('id');
    if ($('.error-message').length === 0) {
      action('search_users_id', $('#search-name').val());
    }
  });
});
