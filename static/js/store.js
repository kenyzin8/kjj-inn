var inCart = [];

// function playBeepAudio(){
//     var beepAudio = $("#beep-audio")[0];
//     beepAudio.pause(); 
//     beepAudio.currentTime = 0; 
//     beepAudio.play(); 
// }

function updateSubtotal(){
    var totalPriceDisplay = 0;
    $(".subtotal-prices").each(function(){
        var price = $(this).text().replace('₱', '').trim();
        
        totalPriceDisplay += parseFloat(price);
    });
    $(".total-subtotal").text(`₱ ${$(".subtotal-prices").length == 0 ? 0 : totalPriceDisplay.toFixed(2)}`);
}

function resetFields(){
    $("#add-to-cart-product-barcode").val('');
    $("#add-to-cart-quantity-input").val(1);
    $("#room-number").val('');
    $("#room-number").trigger('change');
    $("#no-room-check-box").prop('checked', false);
    $("#room-number").prop('disabled', false);
    $("#cart-tbody").empty();
    $(".total-quantity").text(0);
    $(".total-subtotal").text(0);
    inCart = [];
    $("#add-to-cart-product-barcode").focus();
}

function selectCustomerByURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const customerId = urlParams.get('customer');

    if (customerId) {
        const exists = $("#room-number option[value='" + customerId + "']").length > 0;

        if (exists) {
            $("#room-number").val(customerId);
            $("#no-room-check-box").prop('checked', false);
        } else {
            $("#room-number").val('');
            urlParams.delete('customer');
            window.history.replaceState({}, document.title, window.location.pathname);
        }
        $("#room-number").trigger('change');
    }
}

$(document).ready(function(){
    $("#add-to-cart-product-barcode").focus();

    selectCustomerByURL();
})

$(document).on('submit', '#add-to-cart-form', function(e){
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();

    const productBarcode = $('#add-to-cart-product-barcode').val();
    const quantity = $('#add-to-cart-quantity-input').val();

    axios.get(fetchProductURL, {
        params: {
            product_barcode: productBarcode,
            quantity: quantity,
        }
    })
    .then(function (response) {
        const data = response.data.data;

        $("#add-to-cart-product-barcode").val('');

        if(!response.data.success){
            showError(response.data.message);
            return;
        }

        const currentQuantity = parseInt($(`#product-${data.identifier}`).val());

        if(currentQuantity + parseInt(quantity) > data.stocks){
            showError(`Only ${data.stocks} stocks left for ${data.product_name}`);
            return;
        }

        $(".total-quantity").text(parseInt($(".total-quantity").text()) + parseInt(quantity));
        $(`.subtotal-${data.identifier}`).text(parseFloat($(`#product-${data.identifier}`).val()) * parseFloat(data.price_unformatted));
        updateSubtotal();

    
        // playBeepAudio();

        if(inCart.includes(data.identifier)){
            $(`#product-${data.identifier}`).val(currentQuantity + parseInt(quantity));
            $(`.subtotal-${data.identifier}`).text(`₱ ${parseFloat(parseFloat($(`#product-${data.identifier}`).val()) * parseFloat(data.price_unformatted)).toFixed(2)}`);
            updateSubtotal();
            showSuccess(`${data.product_name} added to cart`);
            return;
        }

        $("#cart-tbody").append(`
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <input type="hidden" name="product-identifiers[]" value="${data.identifier}" />
                <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white whitespace-nowrap">
                    ${data.product_name}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                        <button id="product-decrement-${data.identifier}" class="inline-flex items-center justify-center p-1 text-sm font-medium h-6 w-6 text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" type="button">
                            <span class="sr-only">Quantity button</span>
                            <i class="fa-solid fa-minus w-3 h-3"></i>
                        </button>
                        <div class="ms-3">
                            <input type="number" id="product-${data.identifier}" name="cart-products-quantity[]" data-input-counter value="${quantity}" class="disabled bg-gray-50 w-14 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block px-2.5 py-1 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="1" required />
                        </div>
                        <button id="product-increment-${data.identifier}" class="inline-flex items-center justify-center h-6 w-6 p-1 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" type="button">
                            <span class="sr-only">Quantity button</span>
                            <i class="fa-solid fa-plus w-3 h-3"></i>
                        </button>
                    </div>
                </td>
                <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white cart-prices whitespace-nowrap">
                    ${data.price}
                </td>
                <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white subtotal-${data.identifier} subtotal-prices whitespace-nowrap">
                    ₱ ${data.subtotal}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="#" class="font-medium text-red-600 dark:text-red-500 hover:underline remove-product-from-cart" data-product-identifer="${data.identifier}" data-product-price="${data.price_unformatted}">Remove</a>
                </td>
            </tr>
        `);

        updateSubtotal();

        $(`#product-decrement-${data.identifier}`).on('click', function(){
            var currentQuantity = parseInt($(`#product-${data.identifier}`).val());
            if(currentQuantity > 1){
                $(`#product-${data.identifier}`).val(currentQuantity - 1);
                $(".total-quantity").text(parseInt($(".total-quantity").text()) - 1);
                $(`.subtotal-${data.identifier}`).text(`₱ ${parseFloat(parseFloat($(`#product-${data.identifier}`).val()) * parseFloat(data.price_unformatted)).toFixed(2)}`);
                updateSubtotal();
                $("#add-to-cart-product-barcode").focus();
            }
        });

        $(`#product-increment-${data.identifier}`).on('click', function(){
            var currentQuantity = parseInt($(`#product-${data.identifier}`).val());
            if(currentQuantity < data.stocks){
                $(`#product-${data.identifier}`).val(currentQuantity + 1);
                $(".total-quantity").text(parseInt($(".total-quantity").text()) + 1);
                $(`.subtotal-${data.identifier}`).text(`₱ ${parseFloat(parseFloat($(`#product-${data.identifier}`).val()) * parseFloat(data.price_unformatted)).toFixed(2)}`);
                updateSubtotal();
                $("#add-to-cart-product-barcode").focus();
            }
        });
        
        inCart.push(data.identifier);

        showSuccess(`${data.product_name} added to cart`);
    })
    .catch(function (error) {
        showError(error);
    })
})

$(document).on('click', '.remove-product-from-cart', function(e){
    e.preventDefault();
    const identifier = $(this).data('product-identifer');
    const price = $(this).data('product-price');
    inCart = inCart.filter(item => item !== identifier);
    $(".total-quantity").text(parseInt($(".total-quantity").text()) - parseInt($(`#product-${identifier}`).val()));
    $(this).closest('tr').remove();
    $("#add-to-cart-product-barcode").focus();
    updateSubtotal();
})

$(document).on('click', '#decrement-button', function(){
    const quantity = $(this).val();
    if(quantity < 1){
        $("#add-to-cart-quantity-input").val(1);
    }
    $("#add-to-cart-product-barcode").focus();
})

$(document).on('click', '#increment-button', function(){
    const quantity = $(this).val();
    $("#add-to-cart-product-barcode").focus();
})

$(document).on('change', '#room-number', function(){
    const customerId = $(this).val();
    $("#customer-id-to-submit").val(customerId);
    $("#add-to-cart-product-barcode").focus();
})

$(document).on('click', '#no-room-check-box', function(){
    
    if($(this).is(':checked')){
        $("#room-number").val('');
        $("#room-number").trigger('change');
        $("#room-number").prop('disabled', true);
        $("#customer-id-to-submit").val('walk-in');
    }else{
        $("#room-number").prop('disabled', false);
    }
    $("#add-to-cart-product-barcode").focus();
})

$(document).on('click', '.submit-purchase-button', function(){
    
    if($("#room-number").val() == null && !$("#no-room-check-box").is(':checked')){
        $("#add-to-cart-product-barcode").focus();
        showError("Missing customer or room");
        return;
    }

    if($("#cart-tbody").children().length == 0){
        $("#add-to-cart-product-barcode").focus();
        showError("Your cart is empty");
        return;
    }

    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to submit the purchase?</span>`,
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
            $("#to-submit-form").submit();
        }
    });
    
})

$(document).on('submit', '#to-submit-form', function(e){
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();

    axios.post(submitPurchaseURL, formData)
        .then(function (response) {
            const data = response.data;

            if(!data.success){
                showError(data.message);
                return;
            }

            resetFields();

            showSuccess(data.message);
            
        })
        .catch(function (error) {
            showError(error.message);
        })
})

$(document).on('click', '.add-to-cart-button', function(){
    $("#add-to-cart-product-barcode").focus();
})

$(document).on('keydown', 'html', function(e){
    $("#add-to-cart-product-barcode").focus();
})