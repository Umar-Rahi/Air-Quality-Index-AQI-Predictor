// Air Quality Index Predictor - Frontend JavaScript

class AQIPredictor {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.chart = null;
        this.sampleData = [];
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.initChart();
        this.loadSampleData();
        this.showInitialState();
    }

    bindEvents() {
        // Form submission
        document.getElementById('aqiForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.predictAQI();
        });

        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearForm();
        });

        // Load sample data button
        document.getElementById('loadSampleBtn').addEventListener('click', () => {
            this.showSampleDataModal();
        });

        // Input validation
        this.addInputValidation();
    }

    addInputValidation() {
        const inputs = document.querySelectorAll('#aqiForm input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.validateInput(e.target);
            });
        });
    }

    validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);

        // Remove previous validation classes
        input.classList.remove('is-valid', 'is-invalid');

        if (input.value === '') {
            return;
        }

        if (isNaN(value) || value < min || value > max) {
            input.classList.add('is-invalid');
        } else {
            input.classList.add('is-valid');
        }
    }

    async predictAQI() {
        try {
            this.showLoading();

            // Get form data
            const formData = this.getFormData();
            
            // Validate form data
            if (!this.validateFormData(formData)) {
                this.showError('Please fill in all fields with valid values.');
                return;
            }

            // Make API request
            const response = await fetch(`${this.apiBaseUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Prediction failed');
            }

            const result = await response.json();
            this.displayResults(result);
            this.updateChart(result.input_data);

        } catch (error) {
            console.error('Prediction error:', error);
            this.showError(error.message || 'Failed to predict AQI. Please check your connection and try again.');
        }
    }

    getFormData() {
        return {
            pm25: parseFloat(document.getElementById('pm25').value) || 0,
            pm10: parseFloat(document.getElementById('pm10').value) || 0,
            no2: parseFloat(document.getElementById('no2').value) || 0,
            so2: parseFloat(document.getElementById('so2').value) || 0,
            co: parseFloat(document.getElementById('co').value) || 0,
            o3: parseFloat(document.getElementById('o3').value) || 0,
            temperature: parseFloat(document.getElementById('temperature').value) || 0,
            humidity: parseFloat(document.getElementById('humidity').value) || 0
        };
    }

    validateFormData(data) {
        return Object.values(data).every(value => 
            !isNaN(value) && value >= 0 && value !== null
        );
    }

    displayResults(result) {
        this.hideLoading();
        this.hideError();

        // Update AQI value
        document.getElementById('aqiValue').textContent = result.aqi;

        // Update category
        const categoryElement = document.getElementById('aqiCategory');
        categoryElement.textContent = result.category;
        categoryElement.style.backgroundColor = result.color;
        categoryElement.style.color = this.getContrastColor(result.color);

        // Update description
        document.getElementById('aqiDescription').textContent = this.getAQIDescription(result.aqi);

        // Show results
        document.getElementById('resultsContainer').classList.remove('d-none');
        document.getElementById('resultsContainer').classList.add('fade-in');
    }

    getAQIDescription(aqi) {
        if (aqi <= 50) {
            return "Air quality is satisfactory, and air pollution poses little or no risk.";
        } else if (aqi <= 100) {
            return "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.";
        } else if (aqi <= 150) {
            return "Members of sensitive groups may experience health effects. The general public is less likely to be affected.";
        } else if (aqi <= 200) {
            return "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.";
        } else if (aqi <= 300) {
            return "Health alert: The risk of health effects is increased for everyone.";
        } else {
            return "Health warning of emergency conditions: everyone is more likely to be affected.";
        }
    }

    getContrastColor(hexColor) {
        // Convert hex to RGB
        const r = parseInt(hexColor.substr(1, 2), 16);
        const g = parseInt(hexColor.substr(3, 2), 16);
        const b = parseInt(hexColor.substr(5, 2), 16);
        
        // Calculate luminance
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        
        return luminance > 0.5 ? '#000000' : '#ffffff';
    }

    initChart() {
        const ctx = document.getElementById('pollutantChart').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['PM2.5', 'PM10', 'NO₂', 'SO₂', 'CO', 'O₃', 'Temp', 'Humidity'],
                datasets: [{
                    label: 'Pollutant Levels',
                    data: [0, 0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: [
                        'rgba(231, 76, 60, 0.8)',   // PM2.5 - Red
                        'rgba(230, 126, 34, 0.8)',  // PM10 - Orange
                        'rgba(241, 196, 15, 0.8)',  // NO2 - Yellow
                        'rgba(155, 89, 182, 0.8)',  // SO2 - Purple
                        'rgba(52, 152, 219, 0.8)',  // CO - Blue
                        'rgba(46, 204, 113, 0.8)',  // O3 - Green
                        'rgba(26, 188, 156, 0.8)',  // Temperature - Teal
                        'rgba(52, 73, 94, 0.8)'     // Humidity - Dark Blue
                    ],
                    borderColor: [
                        'rgba(231, 76, 60, 1)',
                        'rgba(230, 126, 34, 1)',
                        'rgba(241, 196, 15, 1)',
                        'rgba(155, 89, 182, 1)',
                        'rgba(52, 152, 219, 1)',
                        'rgba(46, 204, 113, 1)',
                        'rgba(26, 188, 156, 1)',
                        'rgba(52, 73, 94, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Current Pollutant Levels',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            font: {
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    updateChart(data) {
        const chartData = [
            data['PM2.5'],
            data['PM10'],
            data['NO2'],
            data['SO2'],
            data['CO'],
            data['O3'],
            data['Temperature'],
            data['Humidity']
        ];

        this.chart.data.datasets[0].data = chartData;
        this.chart.update('active');
    }

    async loadSampleData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/sample-data`);
            if (response.ok) {
                this.sampleData = await response.json();
            }
        } catch (error) {
            console.error('Failed to load sample data:', error);
        }
    }

    showSampleDataModal() {
        const container = document.getElementById('sampleDataContainer');
        container.innerHTML = '';

        this.sampleData.forEach((sample, index) => {
            const card = this.createSampleDataCard(sample, index);
            container.appendChild(card);
        });

        const modal = new bootstrap.Modal(document.getElementById('sampleDataModal'));
        modal.show();
    }

    createSampleDataCard(sample, index) {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';

        const card = document.createElement('div');
        card.className = 'card sample-card h-100';
        card.style.cursor = 'pointer';

        card.innerHTML = `
            <div class="card-body">
                <h6 class="card-title text-center">${sample.name}</h6>
                <div class="sample-values">
                    <small>
                        <strong>PM2.5:</strong> ${sample.data.pm25} μg/m³ |
                        <strong>PM10:</strong> ${sample.data.pm10} μg/m³<br>
                        <strong>NO₂:</strong> ${sample.data.no2} ppb |
                        <strong>SO₂:</strong> ${sample.data.so2} ppb<br>
                        <strong>CO:</strong> ${sample.data.co} ppm |
                        <strong>O₃:</strong> ${sample.data.o3} ppb<br>
                        <strong>Temp:</strong> ${sample.data.temperature}°C |
                        <strong>Humidity:</strong> ${sample.data.humidity}%
                    </small>
                </div>
            </div>
        `;

        card.addEventListener('click', () => {
            this.loadSampleIntoForm(sample.data);
            bootstrap.Modal.getInstance(document.getElementById('sampleDataModal')).hide();
        });

        col.appendChild(card);
        return col;
    }

    loadSampleIntoForm(data) {
        document.getElementById('pm25').value = data.pm25;
        document.getElementById('pm10').value = data.pm10;
        document.getElementById('no2').value = data.no2;
        document.getElementById('so2').value = data.so2;
        document.getElementById('co').value = data.co;
        document.getElementById('o3').value = data.o3;
        document.getElementById('temperature').value = data.temperature;
        document.getElementById('humidity').value = data.humidity;

        // Add visual feedback
        const inputs = document.querySelectorAll('#aqiForm input[type="number"]');
        inputs.forEach(input => {
            input.classList.add('is-valid');
            setTimeout(() => {
                input.classList.remove('is-valid');
            }, 2000);
        });
    }

    clearForm() {
        document.getElementById('aqiForm').reset();
        
        // Remove validation classes
        const inputs = document.querySelectorAll('#aqiForm input[type="number"]');
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
        });

        this.showInitialState();
        this.updateChart({
            'PM2.5': 0, 'PM10': 0, 'NO2': 0, 'SO2': 0,
            'CO': 0, 'O3': 0, 'Temperature': 0, 'Humidity': 0
        });
    }

    showLoading() {
        document.getElementById('resultsContainer').classList.add('d-none');
        document.getElementById('errorContainer').classList.add('d-none');
        document.getElementById('loadingContainer').classList.remove('d-none');
    }

    hideLoading() {
        document.getElementById('loadingContainer').classList.add('d-none');
    }

    showError(message) {
        this.hideLoading();
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorContainer').classList.remove('d-none');
        document.getElementById('resultsContainer').classList.add('d-none');
    }

    hideError() {
        document.getElementById('errorContainer').classList.add('d-none');
    }

    showInitialState() {
        document.getElementById('resultsContainer').classList.add('d-none');
        document.getElementById('loadingContainer').classList.add('d-none');
        document.getElementById('errorContainer').classList.add('d-none');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AQIPredictor();
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add tooltips to info icons
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add smooth scrolling for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});