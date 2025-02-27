document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("weather-form");
    let formContainer = document.getElementById("form-container");
    let weatherInfo = document.getElementById("weather-info");
    let tempElement = document.getElementById("temperature");

    function getTemperatureColor(temp) {
        if (temp <= -30) return "#1B1F7A";
        if (temp <= -20) return "#1E3A8A";
        if (temp <= -10) return "#2563EB";
        if (temp <= 0) return "#3B82F6";
        if (temp <= 10) return "#22A7F0";
        if (temp <= 20) return "#F59E0B";
        if (temp <= 30) return "#DC2626";
        return "#9B1C1C";
    }

    function updateTemperatureColor() {
        if (!tempElement) return;
        let temp = parseFloat(tempElement.innerText);
        let color = getTemperatureColor(temp);
        tempElement.style.color = color;
    }

    if (weatherInfo && weatherInfo.innerHTML.trim() !== "") {
        setTimeout(() => {
            weatherInfo.classList.add("show");
            formContainer.classList.add("expanded");
            updateTemperatureColor();
        }, 100);
    }

    form.addEventListener("submit", function (event) {
        if (weatherInfo && weatherInfo.classList.contains("show")) {
            event.preventDefault();
            weatherInfo.classList.remove("show");
            setTimeout(() => { form.submit(); }, 600);
        }
    });
});
