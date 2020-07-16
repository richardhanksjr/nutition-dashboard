// Update the app every n minutes
let num_minutes_to_update = 5;
setInterval(function(){
    window.location.href = index_url;
}, 1000 * 60 * num_minutes_to_update);
