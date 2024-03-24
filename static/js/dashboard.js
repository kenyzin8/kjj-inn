// https://flowbite.com/docs/plugins/charts/
const options1 = {
    chart: {
        type: "area",
        fontFamily: "Inter, sans-serif",
        dropShadow: {
            enabled: false,
        },
        toolbar: {
            show: false,
        },
    },
    tooltip: {
        enabled: true,
        x: {
            show: false,
        },
    },
    fill: {
        type: "gradient",
        gradient: {
            opacityFrom: 0.55,
            opacityTo: 0,
            shade: "#1C64F2",
            gradientToColors: ["#1C64F2"],
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 6,
    },
    grid: {
        show: false,
        strokeDashArray: 4,
        padding: {
            left: 2,
            right: 2,
            top: -26
        },
    },
    series: [{
        name: "Room Sales",
        data: roomSalesData,
        color: "#1A56DB",
    }, {
        name: "Walk-In Sales",
        data: walkInSalesData,
        color: "#7E3BF2",
    }, ],
    xaxis: {
        categories: monthData,
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        show: false,
        labels: {
            formatter: function(value) {
                return '₱' + value;
            }
        }
    },
}
const options2 = {
    chart: {

        type: "area",
        fontFamily: "Inter, sans-serif",
        dropShadow: {
            enabled: false,
        },
        toolbar: {
            show: false,
        },
    },
    tooltip: {
        enabled: true,
        x: {
            show: false,
        },
    },
    fill: {
        type: "gradient",
        gradient: {
            opacityFrom: 0.55,
            opacityTo: 0,
            shade: "#1C64F2",
            gradientToColors: ["#1C64F2"],
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 6,
    },
    grid: {
        show: false,
        strokeDashArray: 4,
        padding: {
            left: 2,
            right: 2,
            top: 0
        },
    },
    series: [{
        name: "Customers",
        data: customerData,
        color: "#1A56DB",
    }, ],
    xaxis: {
        categories: monthData,
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        show: false,
    },
}

if (document.getElementById("area-chart") && typeof ApexCharts !== 'undefined') {
    const chart1 = new ApexCharts(document.getElementById("size-chart"), options1);
    chart1.render();
    const chart2 = new ApexCharts(document.getElementById("area-chart"), options2);
    chart2.render();
}
$(document).on('submit', '#shoutbox-input-form', function(e) {
    e.preventDefault();
    $("#shoutbox-input").val("");
});