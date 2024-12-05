document.getElementById("predictBtn").addEventListener("click", async function() {
    // Get input values
    const temperature = document.getElementById("temperature").value;
    const rainfall = document.getElementById("rainfall").value;
    const humidity = document.getElementById("humidity").value;
    const soilType = document.getElementById("soilType").value;

    // Validate input values
    if (temperature < -50 || temperature > 60 || isNaN(temperature)) {
        document.getElementById("result").innerHTML = "Error: Temperature should be between -50°C and 60°C.";
        return;
    }
    if (rainfall < 0 || rainfall > 5000 || isNaN(rainfall)) {
        document.getElementById("result").innerHTML = "Error: Rainfall should be between 0mm and 5000mm.";
        return;
    }
    if (humidity < 0 || humidity > 100 || isNaN(humidity)) {
        document.getElementById("result").innerHTML = "Error: Humidity should be between 0% and 100%.";
        return;
    }

    // Prepare data to send to the backend
    const inputData = {
        Temperature: parseFloat(temperature),
        Rainfall: parseFloat(rainfall),
        Humidity: parseFloat(humidity),
        SoilType: parseInt(soilType)
    };

    try {
        // Send data to the backend API
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputData)
        });

        const result = await response.json();
        
        // Display the result
        if (response.ok) {
            // Show both predicted crop and sustainable farming method on separate lines
            document.getElementById("result").innerHTML = 
                `Suggested Crop: ${result.predicted_crop} <br><br> Sustainable Methods: ${result.sustainable_method}`;
        } else {
            document.getElementById("result").innerHTML = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = `Error: ${error.message}`;
    }
});

