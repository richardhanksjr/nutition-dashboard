let progress, display;
const original_seconds = seconds_since_first_meal;

function startTimer(duration, display) {
    var timer = duration, minutes, seconds, hours;
    setInterval(function () {

        hours = parseInt(timer / 3600, 10);
        minutes = parseInt((timer % 3600) / 60, 10);
        seconds = parseInt(timer % 60, 10);


        hours = hours < 10 ? "0" + hours: hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = hours + ":" + minutes + ":" + seconds;
        // console.log(seconds_since_first_meal, timer)
        // progress.style.width = timer / original_seconds;
        if (--timer < 0) {
            clearInterval(startTimer);
            location.reload();

        }
    }, 1000);
}

window.onload = function () {
    var timer = seconds_since_first_meal;
        if (timer === 0){
            return;
    }
    display = document.getElementById('clock');
    progress = document.getElementById('fasting_progress');
    startTimer(timer, display);
};