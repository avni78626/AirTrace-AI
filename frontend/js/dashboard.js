const days = [
    "Sep 28",
    "Sep 29",
    "Sep 30",
    "Oct 1",
    "Oct 2",
    "Oct 3",
    "Oct 4"
];


const riskData = [
    55,
    62,
    68,
    72,
    78,
    81,
    85
];


const temperatureData = [
    32,
    33,
    34,
    35,
    36,
    37,
    38
];


new Chart(
    document.getElementById("predictionChart"),
    {
        type: "line",

        data: {

            labels: days,

            datasets: [
                {
                    label: "Risk Score",

                    data: riskData,

                    tension: 0.3
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {
                    beginAtZero: true,

                    max: 100
                }

            }
        }
    }
);



new Chart(
    document.getElementById("temperatureChart"),
    {
        type: "line",

        data: {

            labels: days,

            datasets: [
                {
                    label: "Temperature °C",

                    data: temperatureData,

                    tension: 0.3
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {
                    beginAtZero: false
                }

            }
        }
    }
);