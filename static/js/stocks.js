var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('stock-table', 'table-search');
    updateModal = initializeModal("#update-stock-modal");
    addModal = initializeModal("#add-stock-modal");

    $("#add-product, #update-product").select2({
        placeholder: "Select a product",
        allowClear: true,
    });
   
    $(".select2-container").addClass("bg-gray-50");
    $(".select2-container").addClass("border");
    $(".select2-container").addClass("border-gray-300");
    $(".select2-container").addClass("text-gray-900");
    $(".select2-container").addClass("text-sm");
    $(".select2-container").addClass("rounded-lg");
    $(".select2-container").addClass("focus:ring-gray-700");
    $(".select2-container").addClass("block");
    $(".select2-container").addClass("w-full");
    $(".select2-container").addClass("p-2.5");
    $(".select2-container").addClass("dark:bg-gray-700");
    $(".select2-container").addClass("dark:border-gray-700");
    $(".select2-container").addClass("dark:placeholder-gray-700");
    $(".select2-container").addClass("dark:text-white");
});

$(document).on('click', '#add-stock-button', function() {
    addModal.show();
});

$(document).on('submit', '#form-add-stock', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(addStockURL, data)
        .then(function (response) {
            if(response.data.stock_exists === true) {
                showError('Stock already exists');
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;

                $(".stocks-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 stock-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] stock-index">
                                ${$(".stocks-tbody tr").length}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] stock-name">
                                ${data.product}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] stock-quantity">
                                ${data.quantity}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] stock-price">
                                ${data.price}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-stock" data-stock-id="${data.id}" data-product-id="${data.product_id}" data-stock-quantity="${data.quantity}" data-stock-price="${data.price_unformatted}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-stock" data-stock-id="${data.id}" data-product-name="${data.product}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                                <a href="${barcodesURL}?product=${data.product_id}" class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-product-barcodes">
                                    <i class="fa-solid fa-barcode"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

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

$(document).on('click', '.button-update-stock', function() {
    var stockId = $(this).data('stock-id');
    var productId = $(this).data('product-id');
    var quantity = $(this).data('stock-quantity');
    var price = $(this).data('stock-price');

    $("#update-stock-id").val(stockId);
    $("#update-product").val(productId).trigger('change');
    $("#update-quantity").val(quantity);
    $("#update-price").val(price);

    updateModal.show();
});

$(document).on('submit', '#form-update-stock', function(e){
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(updateStockURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                const data = response.data.data;
                var row = $(".stock-row-" + data.id);
                row.find('.stock-name').html(data.product);
                row.find('.stock-quantity').html(data.quantity);
                row.find('.stock-price').html(data.price);

                row.find('.button-update-stock').data('stock-quantity', data.quantity);
                row.find('.button-update-stock').data('stock-price', data.price_unformatted);

                closeModals();
                showSuccess('Stock updated successfully');
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

$(document).on('click', '.button-delete-stock', function() {
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
            var stockId = $(this).data('stock-id');
            const stockRow = `.stock-row-${stockId}`;
            axios.post(deleteStockURL, {id: stockId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        $(stockRow).remove();
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