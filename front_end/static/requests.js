let pe_ratio = document.getElementById("pe_ratio");
let pe_ratio_content = document.getElementById("pe_ratio_content");


pe_ratio.addEventListener("click", function(){
    fetch("/pe_ratio")
        .then(function(response) {
            return response.text();
        })
        .then(function(html){
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            let pe_element = doc.getElementById('pe_ratio_parent');
            pe_ratio_content.innerHTML = pe_element.innerHTML;
        })
});