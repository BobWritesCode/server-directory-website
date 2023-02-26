/* global $ */
/* eslint default-case: ["error", { "commentPattern": "^skip\\sdefault" }] */

// Global HTML Elements
const emailForm = $('#email_update_form');
const btnDeleteAccount = $("button[data-target='#delete-account-modal']");
const btnEmailUpdateConfirm = $('#email_update_form').find(
  'button[name="email_address_update_confirm"]',
);
const btnServerListingDeleteConfirm = $('#server-listing-delete-form').find(
  'button[name="server-listing-delete-confirm"]',
);

let lastDeleteBtnID = null;

// DOM Ready
$(document).ready(() => {
  $('#profile-form')
    .find('#id_email')
    .prop('readonly', 'readonly')
    .addClass('form-control-plaintext text-light border border-light ps-2')
    .css('pointer-events', 'none');
});

/**
 * Call BootStrap toast to show.
 */
// eslint-disable-next-line no-unused-vars
function showToast() {
  $('#liveToast').toast({
    delay: 3000,
  });
  $('#liveToast').toast('show');
}

/**
 * Check user input matches expected input
 * @param {integer} id Taken from data attribute in button.
 */
function ServerListingDeleteConfirm(id) {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check user has input correct string.
  if ($('#id_server_listing_delete_confirm').val() !== 'delete') {
    $('#server-listing-delete-form')
      .find('#id_server_listing_delete_confirm')
      .after(
        '<div class="error-message alert alert-warning mt-1" role="alert">Follow instructions above</div>',
      );
  }
  // If no error messages then send request to server.
  if ($('.error-message').length === 0) {
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'itemID')
      .val(id);
    $('#server-listing-delete-form').append(input);
    $('#server-listing-delete-form').submit();
  }
}

/**
 * Clears input box where user will need to type 'remove' to confirm
 * account deletion.
 * @return {None} No  return
 */
function clearRemoveInput() {
  $('#div_id_confirm').find('input[name="confirm"]').val('');
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
 * @param {string} arg [1] The action you wish to call. See website.views.py
 * call_server(). Currently on set up to use 'get_tag_details'
 * @param {*} arg... [...] Any other data you wish to send to server.
 */
function action(...args) {
  askServer('/call_server', {
    args,
  }).then((data) => {
    if (data.result.success) {
      // Show BootStrap toast
      window.location.href = 'my_account';
    } else {
      switch (data.result.reason) {
        case 'Email address not valid':
          emailForm
            .find('#email_update')
            .after(
              '<div class="error-message alert alert-danger mt-1" role="alert">Email address not valid</div>',
            );
          break;
        case 'Does not match':
          emailForm
            .find('#email_update_confirm')
            .after(
              '<div class="error-message alert alert-danger mt-1" role="alert">Email does not match</div>',
            );
          break;
        case 'Email address already taken':
          emailForm
            .find('#email_update')
            .after(
              '<div class="error-message alert alert-danger mt-1" role="alert">Email address already taken</div>',
            );
          break;

        default:
          emailForm
            .find('#email_update')
            .after(
              `<div class="error-message alert alert-danger mt-1" role="alert"> ${data.result.reason} </div>`,
            );
        // skip default case
      }
    }
  });
}

/**
 * Validate form before submit.
 * Validation to see both vales are valid emails addresses and match.
 */
function userEmailUpdate() {
  const formData = {};
  formData.email1 = $('#email_update_form').find('#email_update').val();
  formData.email2 = $('#email_update_form').find('#email_update_confirm').val();
  action('update_email', formData);
}

window.addEventListener('DOMContentLoaded', () => {
  // Keep track of last item id pressed.
  $('button[data-target="#server-listing-delete-modal"]').on(
    'click',
    function getID() {
      if ($(this).attr('data-item')) {
        lastDeleteBtnID = $(this).attr('data-item');
      }
    },
  );
  btnDeleteAccount.on('click', () => {
    clearRemoveInput();
  });
  btnEmailUpdateConfirm.on('click', (e) => {
    e.preventDefault();
    $('.error-message').remove();
    userEmailUpdate();
  });
  btnServerListingDeleteConfirm.on('click', () => {
    ServerListingDeleteConfirm(lastDeleteBtnID);
  });
});
