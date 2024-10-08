let errorTimeoutId;
let successTimeoutId;
var modals = [];

var errorIndex = 0;
var successIndex = 0;

function playErrorAudio(){
    var beepAudio = $("#error-audio")[0];
    beepAudio.pause(); 
    beepAudio.currentTime = 0; 
    beepAudio.volume = 0.5;
    beepAudio.play(); 
}

function playSuccessAudio(){
    var beepAudio = $("#success-audio")[0];
    beepAudio.pause();
    beepAudio.currentTime = 0;
    beepAudio.play();
}

function showError(message) {
    if (errorTimeoutId) {
        clearTimeout(errorTimeoutId);
    }

    errorIndex++;

    $(".toast-error-message").html(`${errorIndex} - ${message}`);

    if ($(".toast-error").is(":hidden")) {
        $(".toast-error").fadeIn();
        $(".toast-error").css('display', 'inline-flex');
    } else {
        $(".toast-error").css('display', 'inline-flex');
    }
    errorTimeoutId = setTimeout(function() {
        $(".toast-error").fadeOut();
    }, 5000);

    playErrorAudio();
}

function showSuccess(message) {
    if (successTimeoutId) {
        clearTimeout(successTimeoutId);
    }

    successIndex++;

    $(".toast-success-message").html(`${successIndex} - ${message}`);

    if ($(".toast-success").is(":hidden")) {
        $(".toast-success").fadeIn();
        $(".toast-success").css('display', 'inline-flex');
    } else {
        $(".toast-success").css('display', 'inline-flex');
    }

    successTimeoutId = setTimeout(function() {
        $(".toast-success").fadeOut();
    }, 5000);

    playSuccessAudio();
}

function toggleDropdown(element) {
    var dropdown = document.getElementById(element.getAttribute('aria-controls'))
    if(dropdown.classList.contains('hidden')){
        element.querySelector('.arrow-indicator').classList.remove('rotate-90')
    }else{
        element.querySelector('.arrow-indicator').classList.add('rotate-90')
    }
}

function initializeModal(modalId) {
    var modalElement = document.querySelector(modalId);
    if (!modalElement) {
        console.error('Modal element not found:', modalId);
        return null;
    }

    var modalOptions = {
        placement: 'bottom-right',
        backdrop: 'static',
        backdropClasses: 'bg-gray-900/50 dark:bg-gray-900/80 fixed inset-0 z-40',
        closable: true,
        onHide: function(e) {
            
        },
        onShow: function(e) {

        }
    };

    var modalInstanceOptions = {
        id: modalElement.getAttribute('id'),
        override: true
    };

    var modalInstance = new Modal(modalElement, modalOptions, modalInstanceOptions);

    modals.push(modalInstance);

    return modalInstance;
}

function closeModals() {
    modals.forEach(modal => {
        if(modal.isVisible()) {
            modal.hide();
        }
    });
}

$(document).on('click', '.close-modal-button', function() {
    closeModals();
});

function setupTableSearch(tableId, searchInputId) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');

    const noDataRow = tbody.insertRow();
    noDataRow.classList.add('border-b');
    noDataRow.classList.add('border-gray-700');
    noDataRow.classList.add('bg-gray-800');
    noDataRow.style.display = 'none'; 
    const cell = noDataRow.insertCell();

    searchInput.addEventListener('keyup', function(e) {
        const searchValue = e.target.value.toLowerCase().trim().replace(/\u00A0/g, ' ').replace(/,/g, '');
        cell.innerHTML = `<div class="my-5 ms-2 font-semibold italic">Oops, no data available for ${e.target.value}<div>`;
        cell.colSpan = tbody.rows[0].cells.length; 
        const tableRows = tbody.querySelectorAll('tr');
        let visibleRowCount = 0;

        tableRows.forEach(row => {
            if (row !== noDataRow) {
                const rowText = row.innerText.toLowerCase().replace(/\u00A0/g, ' ').replace(/,/g, '');
                if (rowText.includes(searchValue)) {
                    row.style.display = '';
                    visibleRowCount++;
                } else {
                    row.style.display = 'none';
                }
            }
        });

        noDataRow.style.display = visibleRowCount === 0 ? '' : 'none';
    });
}

function getCSRFTokenFromCookies(){
    const cookie = document.cookie;
    const csrfToken = cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    return csrfToken;
}

let showColon = true;

function updateTimer() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();

    const hoursAngle = ((hours % 12) + minutes / 60) * 30;
    const minutesAngle = minutes * 6;

    document.getElementById('hour-hand').style.transform = `rotate(${hoursAngle}deg)`;
    document.getElementById('minute-hand').style.transform = `rotate(${minutesAngle}deg)`;

    let options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    let formattedDateTime = now.toLocaleString('en-US', options);
    if (showColon) {
        formattedDateTime = formattedDateTime.replace(/:/g, '<span>:</span>');
    } else {
        formattedDateTime = formattedDateTime.replace(/:/g, '<span style="visibility: hidden;">:</span>');
    }
    showColon = !showColon;

    formattedDateTime = formattedDateTime.replace("at", "-");

    document.querySelector('.timer-text').innerHTML = formattedDateTime;
}

updateTimer();
setInterval(updateTimer, 1000);