document.addEventListener('DOMContentLoaded', function() {
    // Retrieve data from the DOM
    var positivePercentage = parseFloat(document.getElementById('positive-percentage').textContent);
    var negativePercentage = parseFloat(document.getElementById('negative-percentage').textContent);

    var ctx = document.getElementById("resultsChart").getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Positive Tests", "Negative Tests"],
            datasets: [{
                label: 'Percentage (%)',
                data: [positivePercentage, negativePercentage],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                        }
                    }
                }
            }
        }
    });
});