const renderChart = (data, labels) => {
   var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 255, 0, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 165, 0, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 255, 0, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 165, 0, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
        title: {
            display:true,
            legend: {
                position: 'left',
                labels: {
                    boxWidth: 10,
                    padding: 10,
                    fontSize: 16
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        }
    });
};
