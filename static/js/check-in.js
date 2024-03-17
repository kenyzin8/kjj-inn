var updateModal = null,
    addModal = null,
    timers = {};

function formatTime(seconds) {
    let parts = [];
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secondsLeft = seconds % 60;

    if (hours > 0) {
        parts.push(`${hours}hr${hours !== 1 ? 's' : ''}`);
    }
    if (hours > 0 || minutes > 0) {
        parts.push(`${minutes}min${minutes !== 1 ? 's' : ''}`);
    }
    parts.push(`${secondsLeft}sec${secondsLeft !== 1 ? 's' : ''}`);

    return parts.join(' ');
}

function initializeTimer(element) {
    var $this = $(element);
    var customerId = $this.data('customer-id');
    var remainingTime = $this.data('remaining-time');
    var expectedCheckOutTime = $this.data('expected-check-out-time');

    if(remainingTime === 'end'){
        $this.text("Waiting for check-out");
        return;
    }

    var timeParts = remainingTime.match(/(\d+)hr[s]? (\d+)min[s]? (\d+)sec[s]?/);

    if (timeParts && timeParts.length === 4) {
        var totalSeconds = (parseInt(timeParts[1]) || 0) * 3600 + (parseInt(timeParts[2]) || 0) * 60 + (parseInt(timeParts[3]) || 0);

        var interval = setInterval(function() {
            totalSeconds -= 1;
            $this.text(formatTime(totalSeconds));

            if (totalSeconds <= 0) {
                clearInterval(interval);
                delete timers[customerId];
                $this.text("Waiting for check-out");
            }

        }, 1000);

        timers[customerId] = interval;
    } else {
        showError(`Invalid time format:, ${remainingTime}`);
    }
}

$(document).ready(function() {
    addModal = initializeModal("#add-check-in-modal");

    $(".remaining-time").each(function() {
        initializeTimer(this);
    });
});

$(document).on('click', '.check-out-customer', function(e) {
    e.stopPropagation();
    const roomName = $(this).data('room-name');

    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to check out Room ${roomName}?</span>`,
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
            const customerId = $(this).data('customer-id');
            axios.post(customerCheckOutURL, {id: customerId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        $('.customer-index-' + response.data.data.id).remove();
                        
                        if(response.data.data.building_active_count <= 0){
                            $('.building-index-' + response.data.data.building_id).addClass('hidden');
                        }
                        else{
                            $('.building-active-count-' + response.data.data.building_id).text(response.data.data.building_active_count_text);
                        }

                        if (timers[customerId]) {
                            clearInterval(timers[customerId]);
                            delete timers[customerId]; 
                        }
                    
                        $("#select-room").append(`<option value="${response.data.data.room_id}" data-room-type-id="${response.data.data.room_type_id}">${response.data.data.room_get_room_for_dropdown}</option>`);

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

$(document).on('click', '#add-check-in-button', function() {
    addModal.show();
});

$(document).on('change', '#select-room', function() {
    var selectedRoom = $(this).val();
    var roomTypeId = $(this).find(':selected').data('room-type-id');

    axios.get(getRoomPricesURL, {
        params: {
            room_type_id: roomTypeId
        }})
        .then(function (response) {
            const data = response.data;
            if (data.success === true) {
                var selectHours = $('#select-hours');
                selectHours.empty();
                selectHours.append('<option value="" selected disabled>Select Fee</option>');
                data.data.forEach(function(item) {
                    selectHours.append('<option value="' + item.id + '">' + item.hours + ' hours - ₱' + item.amount + '</option>');
                });
            }
            else {
                showError(data.message);
            }
        })
        .catch(function (error) {
            showError(error);
        })
});

$(document).on('submit', '#form-add-check-in', function(e) {
    e.preventDefault();

    var form = $(this);
    var data = form.serialize();

    axios.post(addCustomerCheckInURL, data)
        .then(function (response) {
            if(response.data.success === true) {
                var buildingIndex = $('.building-index-' + response.data.data.building_id);

                if(buildingIndex.hasClass('hidden')){
                    buildingIndex.removeClass('hidden');
                }

                var buildingActiveCount = $('.building-active-count-' + response.data.data.building_id);
                buildingActiveCount.text(response.data.data.building_active_count);

                var customersList = $('.customers-list-' + response.data.data.building_id);

                var customerId = response.data.data.id;

                customersList.prepend(`
                    <li class="py-3 sm:py-4 customer-index-${customerId}">
                        <div class="flex items-center hover:bg-gray-700 hover:rounded-lg p-1 cursor-pointer view-customer-summary" data-customer-slug="${response.data.data.slug}">
                            <div id="tooltip-${customerId}" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-black transition-opacity duration-300 rounded-lg shadow-sm opacity-0 tooltip bg-[orange]">
                                Check-Out Customer
                                <div class="tooltip-arrow" data-popper-arrow></div>
                            </div>
                            <div class="flex-1 min-w-0">
                                <div class="inline-flex flex-col text-start font-medium">
                                    <span class="truncate text-md room-name dark:text-[orange]">
                                        ${response.data.data.room_name}
                                    </span>
                                    <span class="text-xs truncate text-gray-400">
                                        ${response.data.data.room_hours}
                                    </span>
                                    <span class="text-xs truncate text-gray-400">
                                        ${response.data.data.formatted_check_in_date}
                                    </span>
                                </div>
                            </div>
                            <div class="inline-flex items-center">
                                <div class="inline-flex flex-col text-end">
                                    <span class="text-md font-medium dark:text-[orange] remaining-time" data-remaining-time="${response.data.data.unformatted_get_remaining_time}" data-customer-id="${customerId}" data-expected-check-out-time="${response.data.data.expected_check_out_date}">
                                        ${response.data.data.remaining_time}
                                    </span>
                                    <span class="text-xs font-medium text-gray-500 truncate dark:text-gray-400">
                                        ${response.data.data.formatted_check_out_date}
                                    </span>
                                    <p class="p-0">
                                        <button class="check-out-customer" data-customer-id="${customerId}" data-room-name="${response.data.data.room_number}">
                                            <span class="text-xs font-semibold dark:text-[red] px-2.5 py-0.5 rounded dark:bg-gray-900 room-name">
                                                Check Out
                                                <i class="fa-solid fa-caret-up"></i>
                                            </span>
                                        </button>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </li>                
                `);

                var newCustomerElement = $(`.customer-index-${customerId} .remaining-time`)[0];
                initializeTimer(newCustomerElement);

                $("#select-room option[value='" + response.data.data.room_id + "']").remove();

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

$(document).on('click', '.view-customer-summary', function() {
    const customerSlug = $(this).attr('data-customer-slug');
    const viewSummaryURL = viewCheckInSummaryURL.replace('0', customerSlug);
    window.location.replace(viewSummaryURL);
});