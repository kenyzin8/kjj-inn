var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('product-table', 'table-search');
    updateModal = initializeModal("#update-product-modal");
    addModal = initializeModal("#add-product-modal");
});

$(document).on('click', '#add-product-button', function() {
    addModal.show();
});

$(document).on('submit', '#form-add-product', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();

    if($("#add-product-type").val() === null){
        showError("Please select a product type.");
        return;
    }

    axios.post(addProductURL, data)
        .then(function (response) {

            if(response.data.product_exists === true){
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;
                barcodesURL = barcodesURL.replace('0', data.id);

                $(".products-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 product-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] product-index">
                                ${$(".products-tbody tr").length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] product-name">
                                ${data.name}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] product-type">
                                ${data.product_type}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-product" data-product-id="${data.id}" data-product-name="${data.name}" data-product-type-name="${data.product_type}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-product" data-product-id="${data.id}" data-product-name="${data.name}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                                <a href="${barcodesURL}" class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-product-barcodes">
                                <i class="fa-solid fa-barcode"></i>
                            </a>
                            </span>
                        </td>
                    </tr>
                `);

                $("#add-product").val("");
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

$(document).on('click', '.button-update-product', function() {
    var productId = $(this).data('product-id');
    var productName = $(this).data('product-name');
    var productTypeId = $(this).data('product-type-id');

    $("#update-product-id").val(productId);
    $("#update-product").val(productName);
    $("#update-product-type").val(productTypeId);

    updateModal.show();
});

$(document).on('submit', '#form-update-product', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();

    if($("#update-product-type").val() === null){
        showError("Please select a product type.");
        return;
    }

    axios.post(updateProductURL, data)
        .then(function (response) {
            if(response.data.product_exists === true){
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;
                $(`.product-row-${data.id} .product-name`).text(data.name);
                $(`.product-row-${data.id} .product-type`).text(data.product_type);
                $(`.product-row-${data.id} .button-update-product`).data('product-name', data.name);
                $(`.product-row-${data.id} .button-update-product`).data('product-type-id', data.product_type_id);
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

$(document).on('click', '.button-delete-product', function() {
    var productName = $(this).data('product-name');
    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${productName}?</span>`,
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
            var productId = $(this).data('product-id');
            const row = $(this).closest('tr');
            axios.post(deleteProductURL, {id: productId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        row.remove();
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