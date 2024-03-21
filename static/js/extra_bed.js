var updateModal = null

$(document).ready(function() {
    updateModal = initializeModal("#update-extra-bed-modal");
});

$(document).on('click', '#update-extra-bed-button', function() {
    var extraBedId = $(this).data('extra-bed-id');
    var extraBedPrice = $(this).data('extra-bed-price');
    $('#extra-bed-id-update').val(extraBedId);
    $('#update-extra-bed-fee').val(extraBedPrice);
    updateModal.show();
});

$(document).on('submit', '#form-update-extra-bed', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();

    axios.post(updateExtraBedURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                console.log(response.data);
                $(".extra-bed-fee").html(response.data.data.price);
                $("#update-extra-bed-button").data('extra-bed-price', response.data.data.price_unformatted);
                updateModal.hide();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            closeModals();
            showError(error);
        });
});