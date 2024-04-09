import firebase from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js';
import "https://www.gstatic.com/firebasejs/10.10.0/firebase-database.js";



var Config = {

  apiKey: "AIzaSyCVDRhmU_ps8O0GNI9FjqmR6oh67ariS3s",
  authDomain: "eirq-solutions.firebaseapp.com",
  databaseURL: "https://eirq-solutions-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "eirq-solutions",
  storageBucket: "eirq-solutions.appspot.com",
  messagingSenderId: "931290153741",
  appId: "1:931290153741:web:d8edcb6428ff83a5352644",
  measurementId: "G-KRKNJRRQMY"

  };
        
// Initialize Firebase
firebase.initializeApp(Config);
var database = firebase.database();

// Get the canvas element
var ctx = document.getElementById('airQualityChart').getContext('2d');

// Define the initial data for the chart
var initialData = {
    labels: ['Temperature', 'eCO2'],
    datasets: [{
        label: 'Air Quality',
        data: [17, 400], // Initial sample data
        backgroundColor: [
            'rgba(0, 0, 255, 0.5)', // Slightly dark blue for Temperature
            'rgba(138, 43, 226, 0.5)' // Slightly dark purple for Temperature
        ],
        borderWidth: 0
    }]
};

// Define the options for the chart
var options = {
    responsive: false, // Make the chart non-responsive
    cutout: '50%', // Make a hole in the middle of the doughnut chart
    plugins: {
        legend: {
            position: 'bottom' // Position the legend at the bottom
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    var label = '';
                    if (context.dataset.label) {
                        label += context.dataset.label + ': ';
                    }
                    if (context.parsed) {
                        label += context.parsed;
                        if (context.datasetIndex === 0) {
                            label += ' °C'; // Add Celsius unit for temperature
                        } else if (context.datasetIndex === 1) {
                            label += ' ppm'; // Add ppm unit for eCO2
                        }
                    }
                    return label;
                }
            }
        }
    }
};

// Create the doughnut chart
var airQualityChart = new Chart(ctx, {
    type: 'doughnut',
    data: initialData,
    options: options
});

// Function to update chart with retrieved data
function updateChart(snapshot) {
    var data = snapshot.val();
    var eco2 = data.eCO2;
    var temperature = data.temperature;
    console.log("eCO2:", eco2);
    console.log("Temperature:", temperature);

    // Update chart with retrieved data
    airQualityChart.data.datasets[0].data = [temperature, eco2];
    airQualityChart.update();
}

// Retrieve data from Firebase Realtime Database
var databaseRef = database.ref("air_quality");
  databaseRef.once('value', updateChart).catch((error) => {
     console.error("Error retrieving data:", error);
});

// Event listener for update button
document.getElementById('updateButton').addEventListener('click', function() {
    databaseRef.once('value', updateChart).catch((error) => {
        console.error("Error retrieving data:", error);
    });
});