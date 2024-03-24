// Litepicker
// 
// The date pickers in Material Admin Pro
// are powered by the Litepicker plugin.
// Litepicker is a lightweight, no dependencies
// date picker that allows for date ranges
// and other options. For more usage details
// visit the Litepicker docs.
// 
// Litepicker Documentation
// https://wakirin.github.io/Litepicker

window.addEventListener('DOMContentLoaded', event => {
    const startInput = document.getElementById('salesStart');
    const endInput = document.getElementById('salesEnd');
    var picker = null;
    if (startInput && endInput) {
        new Litepicker({
            element: startInput,
            elementEnd: endInput,
            singleMode: false,
            allowRepick: true,
            startDate: new Date(),
            endDate: new Date(),
            format: 'MMM DD, YYYY',
            numberOfMonths: 2,
            numberOfColumns: 2,
            autoApply: true,
            showWeekNumbers: false,
            plugins: ['ranges', 'mobilefriendly'],
            ranges: {
                customRanges: {
                    'Today': [new Date(), new Date()],
                    'Yesterday': [new Date(new Date().setDate(new Date().getDate() - 1)), new Date(new Date().setDate(new Date().getDate() - 1))],
                    'This Week': [new Date(new Date().setDate(new Date().getDate() - new Date().getDay())), new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 6))],
                    'Last Week': [
                        new Date(new Date().setDate(new Date().getDate() - new Date().getDay() - 7)), 
                        new Date(new Date().setDate(new Date().getDate() - new Date().getDay() - 1))
                    ],
                    'This Month': [
                        new Date(new Date().setFullYear(new Date().getFullYear(), new Date().getMonth(), 1)), 
                        new Date(new Date().setFullYear(new Date().getFullYear(), new Date().getMonth() + 1, 0))
                    ],
                    'Last Month': [
                        new Date(new Date().setFullYear(new Date().getFullYear(), new Date().getMonth() - 1, 1)), 
                        new Date(new Date().setFullYear(new Date().getFullYear(), new Date().getMonth(), 0))
                    ],
                    'This Year': [
                        new Date(new Date().setFullYear(new Date().getFullYear(), 0, 1)), 
                        new Date(new Date().setFullYear(new Date().getFullYear(), 11, 31))
                    ],
                }
            },
            setup: (picker) => {
                const urlParams = new URLSearchParams(window.location.search);
                const startDateString = urlParams.get('startDate');
                const endDateString = urlParams.get('endDate');

                picker.on('render', (ui) => {
                    if (startDateString && endDateString){
                        const startDate = new Date(startDateString);
                        const endDate = new Date(endDateString);
                        picker.setDateRange(startDate, endDate); 
                    }
                });

                picker.on('selected', (date1, date2) => {
                    const newStartDate = date1.format('YYYY-MM-DD');
                    const newEndDate = date2.format('YYYY-MM-DD');
                    if (newStartDate !== startDateString || newEndDate !== endDateString) {
                        const url = new URL(window.location.href);
                        url.searchParams.set('startDate', newStartDate);
                        url.searchParams.set('endDate', newEndDate);
                        window.location.href = url;
                    }
                });
            },
        });
    }
});
