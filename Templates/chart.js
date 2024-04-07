function getAirQualityData() {
    // Replace this with your actual function to fetch air quality data
    // For example, you can use AJAX to fetch data from a backend server
    const eCO2 = 400; // Example eCO2 value
    const temperature = 25; // Example temperature value

    return { eCO2, temperature };
}

function displayGraph() {
    const airQualityData = getAirQualityData();

    const ctx = document.getElementById('airQualityChart').getContext('2d');
    const airQualityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['eCO2', 'Temperature'],
            datasets: [{
                label: 'Air Quality',
                data: [airQualityData.eCO2, airQualityData.temperature],
                backgroundColor: ['#8A2BE2', '#4169E1'],
                borderWidth: 1
            }]
        }
    });
}