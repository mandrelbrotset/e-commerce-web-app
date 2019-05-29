var xhr = new XMLHttpRequest();
var url = "http://localhost:5000/get_products";

xhr.open("GET", url, true);
xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            showProducts(xhr.responseText);
        } else {
            console.error(xhr.statusText);
        }
    }
};

xhr.onerror = function (e) {
    console.error(xhr.statusText);
};
xhr.send(null);



function showProducts(products) {
    var elem = document.getElementById('loading');
    elem.style.display = 'hidden';

    var products = JSON.parse(products);
    console.log(products);
    var data = "";

    for (i = 0; i < products.length; i++) {
        console.log(products[i])

        x = `<div>
                <img src="images/` + products[i][6] + `" style="height:120px;" alt="item">
                <h2>` + products[i][1] + ` $` + products[i][5] + `</h2>
                <p>` + products[i][4] + `</p>
                <small>` + products[i][3] + `</small>
                <a href="item/` + products[i][0] + `">View item</a>
            </div>`;

        data = data + x;
    }

    var x = document.getElementById('product')
    x.innerHTML = data;
}

/*
function add_to_cart(item_id){
    async load() {
        let url =  'https://finance.yahoo.com/webservice/v1/symbols/goog/quote?format=json';
        try {
            let response = await fetch(url);
//          ^^^^
            return await response.text();
//                                ^^^^^^
        } catch (e) {
            return e.message;
        }
    }
}
*/