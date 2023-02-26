/* global $ */

// Globals
const form = $('#update-user-form');
const userDeleteForm = $('#user-delete-form');
const listingDeleteForm = $('#listing-delete-form');
const banForm = $('#user-ban-form');
const promoteForm = $('#user-promote-form');
const demoteForm = $('#user-demote-form');

// const btnUpdate = $('button[name="user_management_save"]');
const btnUnban = $('#btnUnban');

const btnDeleteConfirm = userDeleteForm.find(
  'button[name="user-delete-confirm"]',
);
const btnListingDeleteConfirm = listingDeleteForm.find(
  'button[name="listing-delete-confirm"]',
);
const btnBanConfirm = banForm.find('button[name="user-ban-confirm"]');
const btnVerifyConfirm = $('button[name="user-verify-confirm"]');
const btnPromoteConfirm = promoteForm.find(
  'button[name="user-promote-confirm"]',
);
const btnDemoteConfirm = demoteForm.find('button[name="user-demote-confirm"]');

let lastDeleteBtnID = null;

/**
 * Check user input matches expected input before deletion, then deletes listing.
 */
function ListingDeleteConfirm() {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check user has input correct string.
  if ($('#delete_listing_confirm').val() !== 'delete') {
    $('#delete_listing_confirm').after(
      "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>",
    );
  }
  // If no error messages then send request to server.
  if ($('.error-message').length === 0) {
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'id')
      .val(lastDeleteBtnID);
    const input2 = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'user_id')
      .val(form.find('#id_id').val());
    listingDeleteForm.append(input).append(input2).submit();
  }
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
      .val(form.find('#id_id').val());
    banForm.append(input);
    banForm.submit();
  }
}

/**
 * Check user input matches expected input before deletion, then deletes user.
 */
function UserDeleteConfirm() {
  // Clear any current error messages from screen.
  $('.error-message').remove();
  // Check user has input correct string.
  if ($('#id_delete_confirm').val() !== 'delete') {
    $('#id_delete_confirm').after(
      "<div class='error-message alert alert-warning mt-1' role='alert'>Follow instructions above</div>",
    );
  }
  // If no error messages then send request to server.
  if ($('.error-message').length === 0) {
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'id')
      .val(form.find('#id_id').val());
    userDeleteForm.append(input);
    userDeleteForm.submit();
  }
}

/**
 * Promotes user to staff member.
 */
function promoteUserToStaff() {
  const input = $('<input>')
    .attr('type', 'hidden')
    .attr('name', 'promote')
    .val(true);
  form.append(input);
  form.submit();
}

/**
 * Promotes user to staff member.
 */
function demoteUserFromStaff() {
  const input = $('<input>')
    .attr('type', 'hidden')
    .attr('name', 'demote')
    .val(true);
  form.append(input);
  form.submit();
}

// DOM Ready
$(document).ready(() => {
  form
    .find('#id_id')
    .prop('readonly', 'readonly')
    .addClass('form-control-plaintext text-light border border-light ps-2')
    .css('pointer-events', 'none');
});

// Listeners
window.addEventListener('DOMContentLoaded', () => {
  // Keep track of last item id pressed.
  $("button[data-target='#listing-delete-modal']").on(
    'click',
    function getID() {
      if ($(this).attr('data-item')) {
        lastDeleteBtnID = $(this).attr('data-item');
      }
    },
  );

  btnUnban.on('click', (e) => {
    e.preventDefault();
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'unban')
      .val(true);
    form.append(input).submit();
  });

  btnVerifyConfirm.on('click', (e) => {
    e.preventDefault();
    const input = $('<input>')
      .attr('type', 'hidden')
      .attr('name', 'email-verify')
      .val(true);
    form.append(input).submit();
  });
  btnListingDeleteConfirm.on('click', () => {
    ListingDeleteConfirm();
  });
  btnDeleteConfirm.on('click', () => {
    UserDeleteConfirm();
  });
  btnBanConfirm.on('click', () => {
    UserBanConfirm();
  });
  btnPromoteConfirm.on('click', (e) => {
    e.preventDefault();
    promoteUserToStaff();
  });
  btnDemoteConfirm.on('click', (e) => {
    e.preventDefault();
    demoteUserFromStaff();
  });
});
