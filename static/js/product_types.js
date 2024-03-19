var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('product-type-table', 'table-search');
    updateModal = initializeModal("#update-product-type-modal");
    addModal = initializeModal("#add-product-type-modal");
});

$(document).on('click', '#add-product-type-button', function() {
    addModal.show();
});
$(document).on('submit', '#form-add-product-type', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(addProductTypeURL, data)
        .then(function (response) {

            if(response.data.product_type_exists === true){
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;

                $(".product-types-tbody").append(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 product-type-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] product-type-index">
                                ${$(".product-types-tbody tr").length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] product-type-name">
                                ${data.name}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-product-type" data-product-type-id="${data.id}" data-product-type-name="${data.id}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-product-type" data-product-type-id="${data.id}" data-product-type-name="${data.name}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

                $("#add-product-type").val("");

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
        })
});

$(document).on('click', '.button-update-product-type', function() {
    var productTypeId = $(this).data('product-type-id');
    var productTypeName = $(this).data('product-type-name');
    $("#update-product-type-id").val(productTypeId);
    $("#update-product-type").val(productTypeName);
    updateModal.show();
});
$(document).on('submit', '#form-update-product-type', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(updateProductTypeURL, data)
        .then(function (response) {

            if(response.data.product_type_exists === true){
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;
                $(`.product-type-row-${data.id} .product-type-name`).text(data.name);
                $(`.product-type-row-${data.id} .button-update-product-type`).data('product-type-name', data.name);
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
        })
});

$(document).on('click', '.button-delete-product-type', function() {
    var productTypeName = $(this).data('product-type-name');
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${productTypeName}?</span>`,
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
            var productTypeId = $(this).data('product-type-id');
            const productTypeRow = $(this).closest('tr');
            axios.post(deleteProductTypeURL, {id: productTypeId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        productTypeRow.remove();
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