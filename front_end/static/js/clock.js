
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
    startTimer(timer, display);
};