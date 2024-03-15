var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('building-table', 'table-search');
    addModal = initializeModal("#add-building-modal");
    updateModal = initializeModal("#update-building-modal");
});

$(document).on('click', '#add-building-button', function() {
    addModal.show();
});

$(document).on('submit', '#form-add-buildings', function(e){
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(addBuildingURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data;
                $(".buildings-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 building-row-${data.data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-index">
                                ${$(".buildings-tbody tr").length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] fee-index">
                                ${data.data.name}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] ">
                                No rooms
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-building" data-building-id="${data.data.id}" data-building-name="${data.data.name}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-building" data-building-id="${data.data.id}" data-building-name="${data.data.name}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

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
})

$(document).on('click', '.button-update-building', function() {
    $("#building-id-update").val($(this).data('building-id'));
    $("#building-name-update").val($(this).data('building-name'));
    updateModal.show();
});

$(document).on('submit', '#form-update-buildings', function(e){
    e.preventDefault();
    const form = $(this);
    var data = form.serialize();

    axios.post(updateBuildingURL, data)
    .then(function (response) {
        if(response.data.success === true) {
            const data = response.data;

            $(`.building-row-${data.data.id} .building-name`).text(data.data.name);
            
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
})

$(document).on('click', '.button-delete-building', function() {
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${$(this).data('building-name')}?</span>`,
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
            const buildingId = $(this).data('building-id');
            axios.post(deleteBuildingURL, {id: buildingId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        $(`.building-row-${buildingId}`).remove();
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
})