/* global $ */

// Globals
const btnNewTag = $('#btnNewTag');
const btnDeleteTag = $('#btnDeleteTag');
const form = $('#tag-management-form');
const btnSubmit = form.find('button[type="submit"]');
const formInternalContainer = $('#form-internal-container');
const btnTagDeleteConfirm = $('#tag-delete-form').find(
  "button[name='tag-delete-confirm']",
);

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

// Functions

/**
 * Validates the user form for either adding or updating a tag.
 * Shows errors to the user if any.
 */
function validateForm() {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check tag name field is not black.
  if (!form.find('#id_name').val()) {
    form
      .find('#id_name')
      .after(
        "<div class='error-message alert alert-warning mt-1' role='alert'>Must not be blank</div>",
      );
  }
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
    if (data.result) {
      if (args[0] === 'get_tag_details') {
        // Turn tag json into object
        const obj = JSON.parse(data.result.tag);
        // Pre-fill inputs in form
        form.find('#id_id').val(obj.id);
        form.find('#id_name').val(obj.name);
        form.find('#id_slug').val(obj.slug);
      }
    }
  });
}

/**
 * Clears html form when choose to update or add tag
 */
function clearForm() {
  $('input:not([name=csrfmiddlewaretoken])').val('');
  btnSubmit.prop('disabled', true);
}

/**
 * Prepare html form ready to input a new tag
 */
function prepareFormForNewTag() {
  $('#form-header').text('Adding New Tag').removeClass('d-none');
  formInternalContainer.removeClass('d-none');
  form.find('#div_id_id').addClass('d-none');
  btnSubmit.html('<i class="bi bi-save"></i>');
  btnSubmit.prop('disabled', false);
  btnDeleteTag.addClass('d-none');
  btnDeleteTag.prop('disabled', true);
}

/**
 * Prepare html form ready to update selected tag
 */
function prepareFormForUpdateTag() {
  $('#form-header').text('Update Tag').removeClass('d-none');
  formInternalContainer.removeClass('d-none');
  form.find('#div_id_id').removeClass('d-none');
  form.find('#div_id_slug').removeClass('d-none');
  btnSubmit.html('<i class="bi bi-save"></i>');
  btnSubmit.prop('disabled', false);
  btnDeleteTag.removeClass('d-none');
  btnDeleteTag.prop('disabled', false);
}

/**
 * Submits form via Post
 */
function submitForm() {
  form.submit();
}

/**
 * Check user input matches expected input
 * @return {None} No  return
 */
function TagDeleteConfirm() {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check user has input correct string.
  if ($('#id_tag_delete_confirm').val() !== 'delete') {
    $('#id_tag_delete_confirm').after(
      "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>",
    );
  }
  // If no error messages then send request to server.
  if ($('.error-message').length === 0) {
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'itemID')
      .val(form.find('#id_id').val());
    $('#tag-delete-form').append(input);
    $('#tag-delete-form').submit();
  }
}

// DOM Ready
$(document).ready(() => {
  $('.tag-select-drop-down').select2().val(null).trigger('change');
  form
    .find('#id_id')
    .prop('readonly', 'readonly')
    .addClass('form-control-plaintext text-light border border-light ps-2')
    .css('pointer-events', 'none');
  form
    .find('#id_slug')
    .prop('readonly', 'readonly')
    .addClass('form-control-plaintext text-light border border-light ps-2')
    .css('pointer-events', 'none');
  $('#tag-delete-form').find('#div_id_id').addClass('d-none');
});

// Listeners
window.addEventListener('DOMContentLoaded', () => {
  $('#tag-select-drop-down').on('select2:select', () => {
    clearForm();
    $('.error-message').remove();
    prepareFormForUpdateTag();
    action('get_tag_details', $('#tag-select-drop-down').val());
  });

  btnNewTag.on('click', () => {
    clearForm();
    $('.error-message').remove();
    prepareFormForNewTag();
  });

  btnSubmit.on('click', (e) => {
    e.preventDefault();
    validateForm();
    if ($('.error-message').length === 0) {
      submitForm();
    }
  });

  btnTagDeleteConfirm.on('click', () => {
    TagDeleteConfirm();
  });
});

window.addEventListener('keyup', () => {
  form
    .find('#id_slug')
    .val(form.find('#id_name').val().replace(/\s+/g, '-').toLowerCase());
});
