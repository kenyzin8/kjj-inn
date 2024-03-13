var updateModal = null,
    addModal = null;
var isUpdating = false;

$(document).ready(function(e) {
    setupTableSearch('room-table', 'table-search');
    updateModal = initializeModal("#update-room-modal");
    addModal = initializeModal("#add-room-modal");
});

$(document).on('change', '#room-type, #room-type-update', function(e) {
    var room_type_id = $(this).val();

    var roomTbody = isUpdating ? '.room-type-fee-tbody-update' : '.room-type-fee-tbody';

    axios.get(getRoomTypePricesURL, {
        params: {
            room_type_id: room_type_id
        }
    })
    .then(function (response) {

        if(response.data.success === false) {
            $('.table-room-type-price-wrapper').hide();
            return;
        }

        const data = response.data.data;
        $(roomTbody).empty();
        data.forEach(function (item) {
            $(roomTbody).append(`
                <tr class="odd:bg-white odd:dark:bg-gray-700 even:bg-gray-50 even:dark:bg-gray-900 border-b dark:border-gray-700">
                    <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        ${item.hours}
                    </td>
                    <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        ${item.amount}
                    </td>
                </tr>
            `);
        });
        $('.table-room-type-price-wrapper').show();
    })
    .catch(function (error) {
        showError(error);
    })
});

$(document).on('submit', '#form-add-room', function(e) {
    e.preventDefault();

    if($('#building').val() === null) {
        showError('Please select a building');
        return;
    }
    else if($('#room-type').val() === null) {
        showError('Please select a room type');
        return;
    }

    var form = $(this);
    var data = form.serialize();
    axios.post(addRoomURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data.data;
                const unformatted_data = response.data.unformatted_data;
                $('.rooms-tbody').prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 room-row-${data.id}">
                        <th class="px-6 py-4">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] room-index">
                                ${$('.rooms-tbody tr').length + 1}
                            </span>
                        </th>
                        <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] room-number">
                                ${data.room_number}
                            </span>
                        </th>
                        <td class="px-6 py-4">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] room-type-name">
                                ${data.room_type}
                            </span>
                        </td>
                        <td class="px-6 py-4">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] good-for">
                                ${data.good_for}
                            </span>  
                        </td>
                        <td class="px-6 py-4">  
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] building-name">
                                ${data.building}
                            </span>  
                        </td>
                        <td class="px-6 py-4">  
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] date-updated">
                                ${data.date_updated}
                            </span>  
                        </td>
                        <td class="px-6 py-4">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a data-modal-target="update-room-modal" data-modal-toggle="update-room-modal" class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-room" data-room-id="${unformatted_data.id}" data-room-number="${unformatted_data.room_number}" data-building="${unformatted_data.building}" data-room-type="${unformatted_data.room_type}" data-good-for="${unformatted_data.good_for}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-room" data-room-name="${data.room_number}" data-room-id="${data.id}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);
                
                closeModals();
                showSuccess('Room added successfully');
            }
            else{
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error);
        })
});

$(document).on('submit', '#form-update-form', function(e) {
    e.preventDefault();

    if($('#building-update').val() === null) {
        showError('Please select a building');
        return;
    }
    else if($('#room-type-update').val() === null) {
        showError('Please select a room type');
        return;
    }

    var form = $(this);
    var data = form.serialize();
    axios.post(updateRoomURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const updatedRoom = response.data.data;
                const unformatted_data = response.data.unformatted_data;
                const roomRowSelector = `.room-row-${updatedRoom.id}`;
                $(`${roomRowSelector} .room-number`).html(updatedRoom.room_number);
                $(`${roomRowSelector} .building-name`).html(updatedRoom.building);
                $(`${roomRowSelector} .room-type-name`).html(updatedRoom.room_type);
                $(`${roomRowSelector} .good-for`).html(updatedRoom.good_for);
                $(`${roomRowSelector} .date-updated`).html(updatedRoom.date_updated);
                $(`${roomRowSelector} .button-update-room`).data('room-number', unformatted_data.room_number);
                $(`${roomRowSelector} .button-update-room`).data('building', unformatted_data.building);
                $(`${roomRowSelector} .button-update-room`).data('room-type', unformatted_data.room_type);
                $(`${roomRowSelector} .button-update-room`).data('good-for', unformatted_data.good_for);
                
                closeModals();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error);
        });
});

$(document).on('click', '.button-delete-room', function(e) {
    var room_name = $(this).data('room-name');
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${room_name}?</span>`,
        icon: "warning",
        showDenyButton: true,
        confirmButtonColor: "orange",
        confirmButtonTextColor: "black",
        denyButtonColor: "#232323",
        confirmButtonText: "Yes",
        denyButtonText: `No`,
        allowOutsideClick: false,
        animation: true
        }).then((result) => {
        if (result.isConfirmed) {
            var room_id = $(this).data('room-id');
            axios.post(deleteRoomURL, {
                    room_id: room_id
                }, {
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}' 
                    }
                })
                .then(function (response) {
                    if(response.data.success === true) {
                        showSuccess('Room deleted successfully');
                        $(`.button-delete-room[data-room-id=${room_id}]`).closest('tr').remove();
                    }
                    else{
                        showError(response.data.message);
                    }
                })
                .catch(function (error) {
                    showError(error);
                })
        }
    });

});

$(document).on('click', '#add-room-button', function(e) {
    isUpdating = false;
    $("#room-type").val('');
    $("#room-type").trigger('change');
    $('.table-room-type-price-wrapper').hide();

    addModal.show();
});

$(document).on('click', '.button-update-room', function(e) {
    isUpdating = true;
    $("#room-id-update").val($(this).data('room-id'));
    $("#room-number-update").val($(this).data('room-number'));
    $("#building-update").val($(this).data('building'));
    $("#good-for-update").val($(this).data('good-for'));
    $("#room-type-update").val($(this).data('room-type'));
    $("#room-type-update").trigger('change');
    $('.table-room-type-price-wrapper').hide();

    updateModal.show();
});