const ctx = document.getElementById('lineChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['12:00 PM','1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM','6:00 PM','7:00 PM','8:00 PM'],
        datasets: [{
            label: 'Heart Rate (in BPM)',
            data: [72, 70, 84, 54, 76, 88, 58, 72],
            backgroundColor: [
                'rgba(85, 85, 85, 1)',
            ],
            borderColor: [
                'rgba(41, 255, 99)',
            ],
            borderWidth: 1
        }]
    },
    options: {
       responsive: true
    }
});