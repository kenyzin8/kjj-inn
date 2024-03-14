var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('fee-table', 'table-search');
    updateModal = initializeModal("#update-fee-modal");
    addModal = initializeModal("#add-fee-modal");
});

$(document).on('submit', '#form-add-fees', function(e){
    e.preventDefault();

    var form = $(this);
    var data = form.serialize();
    axios.post(addFeeURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data.data;
                const unformatted_data = response.data.unformatted_data;
                $(".fees-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 fee-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">${$('.fees-tbody tr').length + 1}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-hours">${data.hours}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-amount">${data.amount}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">N/A</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] date-updated">${data.date_updated}</span>
                        </td>
                        <td class="px-6 py-4">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a data-modal-target="update-fee-modal" data-modal-toggle="update-fee-modal" class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-fee" data-fee-id="${unformatted_data.id}" data-fee-hours="${unformatted_data.hours}" data-fee-amount="${unformatted_data.amount}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-fee" data-fee-id="${data.id}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

                $("#add-fee").val('');
                $("#add-hours").val('');

                closeModals();
                showSuccess('Room added successfully');
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        })
});

$(document).on('submit', '#form-update-fees', function(e){
    e.preventDefault();

    var form = $(this);
    var data = form.serialize();

    axios.post(updateFeeURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const updatedFee = response.data.data;
                const unformatted_data = response.data.unformatted_data;
                const roomRowSelector = `.fee-row-${updatedFee.id}`;

                $(`${roomRowSelector} .fee-hours`).html(updatedFee.hours);
                $(`${roomRowSelector} .fee-amount`).html(updatedFee.amount);
                $(`${roomRowSelector} .date-updated`).html(updatedFee.date_updated);

                $(`${roomRowSelector} .button-update-fee`).data('fee-hours', unformatted_data.hours);
                $(`${roomRowSelector} .button-update-fee`).data('fee-amount', unformatted_data.amount);
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

$(document).on('click', '.button-update-fee', function(e){
    e.preventDefault();
    updateModal.show();

    const feeAmount = $(this).data('fee-amount');
    $("#fee-id-update").val($(this).data('fee-id'));
    $("#update-fee").val($(this).data('fee-amount').replace(/,/g, ''));
    $("#update-hours").val($(this).data('fee-hours'));
});

$(document).on('click', '.close-modal-button', function(e){
    e.preventDefault();
    if(updateModal.isVisible()){
        updateModal.hide();
    }
    else if(addModal.isVisible()){
        addModal.hide();
    }
});

$(document).on('click', '#add-fee-button', function(e){
    e.preventDefault();
    addModal.show();
});

$(document).on('click', '.button-delete-fee', function(e){
    e.preventDefault();
    const fee_hours = $(this).data('fee-hours');
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${fee_hours}?</span>`,
        icon: "warning",
        showDenyButton: true,
        confirmButtonColor: "orange",
        denyButtonColor: "#232323",
        confirmButtonText: "Yes",
        denyButtonText: `No`,
        allowOutsideClick: false,
        animation: true
        }).then((result) => {
        if (result.isConfirmed) {
            const feeId = $(this).data('fee-id');
            const feeRowSelector = `.fee-row-${feeId}`;
            axios.post(deleteFeeURL, {id: feeId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        $(feeRowSelector).remove();
                        showSuccess(response.data.message);
                    }
                    else{
                        showError(response.data.message);
                    }
                })
                .catch(function (error) {
                    showError(error.message);
                });
        }
    });

});
