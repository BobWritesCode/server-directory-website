// DOM Ready
$(document).ready(function() {
    $('#profile-form').find('#id_email').prop("readonly", "readonly").addClass("form-control-plaintext text-light border border-light ps-2").css('pointer-events', 'none');
});