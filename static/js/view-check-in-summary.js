var timers = {};

function parseDateTime(dateTimeString) {
    var dateTimeParts = dateTimeString.match(/(\w+ \d+, \d{4}), (\d+):(\d+) (a.m.|p.m.)/);
    if (dateTimeParts) {
        var datePart = dateTimeParts[1];
        var hour = parseInt(dateTimeParts[2], 10);
        var minute = parseInt(dateTimeParts[3], 10);
        var amPm = dateTimeParts[4];

        if (amPm === 'p.m.' && hour < 12) {
            hour += 12;
        } else if (amPm === 'a.m.' && hour === 12) {
            hour = 0;
        }

        var formattedDateTime = `${datePart} ${hour}:${minute}`;
        return new Date(formattedDateTime);
    } else {
        return null;
    }
}

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
    var checkInTime = parseDateTime($this.data('check-in-time'));
    var checkOutTime = parseDateTime($this.data('check-out-time'));

    if(remainingTime === 'end'){
        $this.text("Waiting for check-out");
        $('.time-progress').css('width', '100%');
        $('.time-progress').text('100%');
        $('.time-progress').css('background', `red`);
        $('.time-progress').css('color', `white`);
        return;
    }

    var timeParts = remainingTime.match(/(\d+)hr[s]? (\d+)min[s]? (\d+)sec[s]?/);
    var totalDurationSeconds = (checkOutTime - checkInTime) / 1000;

    if (timeParts && timeParts.length === 4) {
        var totalSeconds = (parseInt(timeParts[1]) || 0) * 3600 + (parseInt(timeParts[2]) || 0) * 60 + (parseInt(timeParts[3]) || 0);
        var remainingPercentage = 100 - ((totalSeconds / totalDurationSeconds) * 100);
        $('.time-progress').css('width', `${remainingPercentage}%`);
        $('.time-progress').text(`${remainingPercentage.toFixed(2)}%`);

        var interval = setInterval(function() {
            totalSeconds -= 1;
            $this.text(formatTime(totalSeconds));

            remainingPercentage = 100 - ((totalSeconds / totalDurationSeconds) * 100);
            $('.time-progress').css('width', `${remainingPercentage}%`);
            $('.time-progress').text(`${remainingPercentage.toFixed(2)}%`);

            if (totalSeconds <= 0) {
                clearInterval(interval);
                delete timers[customerId];
                $this.text("Waiting for check-out");
                $('.time-progress').css('background', `red`);
                $('.time-progress').css('color', `white`);
            }

        }, 1000);

        timers[customerId] = interval;
    } else {
        showError(`Invalid time format:, ${remainingTime}`);
    }
}

$(document).ready(function() {
    initializeTimer($(".remaining-time"));
});
$(document).on('click', '.check-out-customer', function() {
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
            axios.post(customerCheckOutUrl, {id: customerId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        showSuccess(response.data.message);
                        setTimeout(() => {
                            window.location.replace('/customer/check-in/');
                        }, 1000);
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