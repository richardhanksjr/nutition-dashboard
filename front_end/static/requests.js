let pe_ratio = document.getElementById("pe_ratio");
let pe_ratio_content = document.getElementById("pe_ratio_content");

function fetchHTMLandAppend(parent_id, route){
    fetch(route)
        .then(function(response) {
            return response.text();
        })
        .then(function(html){
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            let pe_element = doc.getElementById(parent_id);
            pe_ratio_content.innerHTML = pe_element.innerHTML;
        })
}


pe_ratio.addEventListener("click", () => fetchHTMLandAppend('pe_ratio_parent', "api/pe_ratio"));