var updateModal = null,
    addModal = null;

function addBarcodeByURL(){
    var url = window.location.href;
    var urlParams = new URLSearchParams(window.location.search);
    var product = urlParams.get('product');

    if(product){
        addModal.show();
        $("#add-product").val(product).trigger('change');
    }

    window.history.replaceState({}, document.title, window.location.pathname);
}

$(document).ready(function() {
    setupTableSearch('barcode-table', 'table-search');
    updateModal = initializeModal("#update-barcode-modal");
    addModal = initializeModal("#add-barcode-modal");

    $("#add-product").select2({
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

    addBarcodeByURL();
});

$(document).on('click', '#add-barcode-button', function() {
    addModal.show();
    $("#add-barcode").focus();
    $("#add-barcode").val("");
    $(".submitted-barcodes-tbody").empty();

});

$(document).on('change', '#add-product', function() {
    $("#add-barcode").val("");
    var product = $(this).val();
    if (product) {
        $("#add-barcode").focus();
    }
});

$(document).on('keydown', 'html', function(e){
    $("#add-barcode").focus();
})

$(document).on('submit', '#form-add-barcode', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();

    axios.post(addBarcodeURL, data)
        .then(function (response) {
            
            $("#add-barcode").val("");

            if(response.data.product_exists === true){
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;

                $(".submitted-barcodes-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                ${data.product}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                ${data.barcode}
                            </span>
                        </td>
                    </tr>
                `);

                $(".barcodes-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 barcode-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] barcode-index">
                                ${$(".barcodes-tbody tr").length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] barcode-name">
                                ${data.barcode}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <svg id="bc-${data.id}" ></svg>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] barcode-product">
                                ${data.product}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-barcode" data-barcode-id="${data.id}" data-barcode-name="${data.barcode}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-barcode" data-barcode-id="${data.id}" data-barcode-name="${data.barcode}" data-product-id="${data.product_id}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

                JsBarcode(`#bc-${data.id}`, `${data.barcode}`, {
                    width:1,
                    height: 30,
                    displayValue: true,
                    fontSize: 13
                });

                $("#add-barcode").focus();

                showSuccess(response.data.message);
            }
            else{
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        })
});

$(document).on('click', '.button-update-barcode', function() {
    var barcodeId = $(this).data('barcode-id');
    var barcodeName = $(this).data('barcode-name');
    var productName = $(this).data('product-name');

    $("#update-barcode-id").val(barcodeId);
    $("#display-product").val(productName);
    $("#update-barcode").val(barcodeName);

    updateModal.show();
    $("#update-barcode").focus();
});

$(document).on('submit', '#form-update-barcode', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();

    axios.post(updateBarcodeURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                var barcodeId = response.data.data.id;
                var barcodeName = response.data.data.barcode;
                var productName = response.data.data.product.name;

                $(".barcode-row-" + barcodeId + " .barcode-name").text(barcodeName);
                $(".barcode-row-" + barcodeId + " .barcode-product").text(productName);

                $(".button-update-barcode[data-barcode-id='" + barcodeId + "']").data('barcode-name', barcodeName);

                closeModals();
                showSuccess(response.data.message);
            }
            else{
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        })
});


$(document).on('click', '.button-delete-barcode', function(e){
    e.preventDefault();
    var barcodeName = $(this).data('barcode-name');

    Swal.fire({
        title: 'Are you sure?',
        text: `You are about to delete the barcode ${barcodeName}.`,
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
            var barcodeId = $(this).data('barcode-id');
            axios.post(deleteBarcodeURL, {id: barcodeId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
            .then(function (response) {
                if(response.data.success === true) {
                    $(".barcode-row-" + barcodeId).remove();
                    showSuccess(response.data.message);
                }
                else{
                    showError(response.data.message);
                }
            })
            .catch(function (error) {
                showError(error.message);
            })
        }
    });
});