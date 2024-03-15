var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('room-type-table', 'table-search');
    updateModal = initializeModal("#update-room-type-modal");
    addModal = initializeModal("#add-room-type-modal");
    
    $(".fees").select2({
        placeholder: "Select fees",
        allowClear: true,
    });

    $(".select2-container").addClass("bg-gray-50");
    $(".select2-container").addClass("border");
    $(".select2-container").addClass("border-gray-300");
    $(".select2-container").addClass("text-gray-900");
    $(".select2-container").addClass("text-sm");
    $(".select2-container").addClass("rounded-lg");
    $(".select2-container").addClass("focus:ring-primary-600");
    $(".select2-container").addClass("focus:border-primary-600");
    $(".select2-container").addClass("block");
    $(".select2-container").addClass("w-full");
    $(".select2-container").addClass("p-1");
    $(".select2-container").addClass("dark:bg-gray-600");
    $(".select2-container").addClass("dark:border-gray-500");
    $(".select2-container").addClass("dark:placeholder-gray-400");
    $(".select2-container").addClass("dark:text-white");
    $(".select2-container").addClass("dark:focus:ring-primary-500");
    $(".select2-container").addClass("dark:focus:border-primary-500");
    $(".select2-container").addClass("cursor-pointer");
});

$(document).on('click', '#add-room-type-button', function(e){
    e.preventDefault();
    addModal.show();
});
$(document).on('submit', '#form-add-room-types', function(e){
    e.preventDefault();
    
    var form = $(this);
    var data = form.serialize();
    axios.post(addRoomTypeURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data;
                $(".room-types-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 fee-row-${data.data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-index">
                                ${$('.room-types-tbody tr').length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-hours">
                                ${data.data.name}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap room-type-fees-td-${data.data.id}">
                            
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-fee" data-room-type-id="${data.data.id}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-fee" data-room-type-id="${data.data.id}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

                data.data.fees.forEach(fee => {
                    $(`.room-type-fees-td-${data.data.id}`).append(`
                        <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-amount">
                            ${fee.hours} - ${fee.amount}
                        </span>
                    `);
                });

                closeModals();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        });
});

$(document).on('click', '.button-update-room-type', function(e){
    e.preventDefault();
    $("#room-type-id-update").val($(this).data('room-type-id'));
    $("#room-type-update").val($(this).data('room-type-name'));
    $('#fees-update').val($(this).data('room-type-fee-ids'));
    $('#fees-update').trigger('change');
    updateModal.show();
});
$(document).on('submit', '#form-update-room-types', function(e){
    e.preventDefault();
    
    var form = $(this);
    var data = form.serialize();
    axios.post(updateRoomTypeURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data;
                const unformattedData = response.data.unformatted_data;
                const rowSelector = `.room-type-row-${data.data.id}`;
                 
                $(`${rowSelector} .room-type-name`).text(data.data.name);

                var feesHtml = '';

                data.data.fees.forEach(fee => {
                    feesHtml += `
                        <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] room-type-fees">
                            ${fee.hours} - ${fee.amount}
                        </span>
                    `;
                });

                $(`${rowSelector} .room-type-fees`).html(feesHtml);

                $(".button-update-room-type").data('room-type-name', data.data.name);
                $(".button-update-room-type").data('room-type-fee-ids', unformattedData.fees);

                closeModals();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        });
});

$(document).on('click', '.button-delete-room-type', function(e){
    e.preventDefault();
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${$(this).data('room-type-name')}?</span>`,
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
            const roomTypeId = $(this).data('room-type-id');
            axios.post("{% url 'delete-room-type' %}", {id: roomTypeId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        $(`.room-type-row-${roomTypeId}`).remove();
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

$(document).on('click', '.close-modal-button', function(e){
    e.preventDefault();
    if(updateModal.isVisible()){
        updateModal.hide();
    }
    else if(addModal.isVisible()){
        addModal.hide();
    }
});