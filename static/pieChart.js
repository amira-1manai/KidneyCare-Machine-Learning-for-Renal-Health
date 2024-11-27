document.addEventListener('DOMContentLoaded', function() {
    // Retrieve data from the DOM
    var positivePercentage = parseFloat(document.getElementById('positive-percentage').textContent);
    var negativePercentage = parseFloat(document.getElementById('negative-percentage').textContent);

    var ctx = document.getElementById("resultsChart1").getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'pie', // Change to 'pie' for a pie chart
        data: {
            labels: ["Positive Tests", "Negative Tests"],
            datasets: [{
                label: 'Percentage (%)',
                data: [positivePercentage, negativePercentage],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)', // Color for positive tests
                    'rgba(255, 99, 132, 0.2)'  // Color for negative tests
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)', // Border color for positive tests
                    'rgba(255, 99, 132, 1)'  // Border color for negative tests
                ],
                borderWidth: 1
            }]
        },
        options: {
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