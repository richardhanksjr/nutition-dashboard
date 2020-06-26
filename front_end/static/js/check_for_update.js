let storage = window.localStorage;

let date = storage.getItem("last_updated_time");
if (!date){
    console.log(new Date().getTime())
    console.log("plus 10", new Date().getTime() + (10*60))
}
 console.log(date)
