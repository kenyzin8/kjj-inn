let errorTimeoutId;
let successTimeoutId;

function showError(message) {
    if (errorTimeoutId) {
        clearTimeout(errorTimeoutId);
    }

    $(".toast-error-message").text(message);
    
    if ($(".toast-error").is(":hidden")) {
        $(".toast-error").fadeIn();
        $(".toast-error").css('display', 'inline-flex');
    } else {
        $(".toast-error").css('display', 'inline-flex');
    }
    errorTimeoutId = setTimeout(function() {
        $(".toast-error").fadeOut();
    }, 5000);
}

function showSuccess(message) {
    if (successTimeoutId) {
        clearTimeout(successTimeoutId);
    }

    $(".toast-success-message").text(message);

    if ($(".toast-success").is(":hidden")) {
        $(".toast-success").fadeIn();
        $(".toast-success").css('display', 'inline-flex');
    } else {
        $(".toast-success").css('display', 'inline-flex');
    }

    successTimeoutId = setTimeout(function() {
        $(".toast-success").fadeOut();
    }, 5000);
}

function hideModal(element) {
    element.find('.close-modal-button').click();
}

function toggleDropdown(element) {
    var dropdown = document.getElementById(element.getAttribute('aria-controls'))
    if(dropdown.classList.contains('hidden')){
        element.querySelector('.arrow-indicator').classList.remove('rotate-90')
    }else{
        element.querySelector('.arrow-indicator').classList.add('rotate-90')
    }
}