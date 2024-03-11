function showError(message){
    var errorModal = document.getElementById('error-modal')
    errorModal.querySelector('.modal-body').textContent = message
    errorModal.showModal()
}

function showSuccess(message){
    var successModal = document.getElementById('success-modal')
    successModal.querySelector('.modal-body').textContent = message
    successModal.showModal()
}

function toggleDropdown(element) {
    var dropdown = document.getElementById(element.getAttribute('aria-controls'))
    if(dropdown.classList.contains('hidden')){
        element.querySelector('.arrow-indicator').classList.remove('rotate-90')
    }else{
        element.querySelector('.arrow-indicator').classList.add('rotate-90')
    }
}