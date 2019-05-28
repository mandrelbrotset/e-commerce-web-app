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
                <img src="images/` + products[i][5] + `" style="height:120px;">
                <h2>` + products[i][0] + ` $` + products[i][4] + `</h2>
                <p>` + products[i][3] + `</p>
                <small>` + products[i][2] + `</small>
            </div>`;

        data = data + x;
    }

    var x = document.getElementById('product')
    x.innerHTML = data;
}