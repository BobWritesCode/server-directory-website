/* global $ */

// Globals
const btnApprove = $('#btnApprove');
const btnReject = $('#btnReject');
const btnBan = $('#btnBan');
const btnNext = $('#btnNext');
const banForm = $('#user-ban-form');

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

function action(...args) {
  askServer('/call_server', {
    args,
  }).then((data) => {
    if (data.result) {
      if (args[0] === 'image_approval_next') {
        window.location.href = String(data.result.text);
      } else {
        $('#status_txt').text(data.result.text);
        btnNext.removeAttr('disabled');
      }
    }
  });
}

/**
 * Check user input matches expected input before ban, then bans user.
 */
function UserBanConfirm() {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check user has input correct string.
  if ($('#ban_confirm').val() !== 'ban') {
    $('#ban_confirm').after(
      "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>",
    );
  }
  // If no error messages then send request to server.
  if ($('.error-message').length === 0) {
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'id')
      .val(banForm.find('#ban_confirm_id').val());
    banForm.append(input);
    action('image_approval_ban', $('#current_id').text());
    banForm.submit();
  }
}

// Listeners
window.addEventListener('DOMContentLoaded', () => {
  btnApprove.on('click', () => {
    action('image_approval_approve', $('#current_id').text());
  });
  btnReject.on('click', () => {
    action('image_approval_reject', $('#current_id').text());
  });
  btnBan.on('click', () => {
    UserBanConfirm();
  });
});
