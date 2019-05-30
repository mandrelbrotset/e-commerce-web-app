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
    var data = "<div class='list-group cart-group'>";

    for (i = 0; i < products.length; i++) {
        console.log(products[i])

        data = data + `<a href="item/` + products[i][0] + `" class="list-group-item list-group-item-action flex-column align-items-start">
                            <img src="static/images/` + products[i][6] + `" style="width:320px;height:250px;" />
                            <div class="side-content">
                                <div class="d-inline-flex p-3">
                                   <div class="p-2" style="width:700px;"><h4>` + products[i][1] + `</h4></div>
                                   <div class="p-2"><h4>$` + products[i][5] + `</h4></div>
                                </div>
                                <p class="card-text">` + products[i][4] + `</p>
                                <small>` + products[i][3] + `</small>
                            </div>
                       </a>`
    }

    data = data + "</div>"

    var x = document.getElementById('product')
    x.innerHTML = data;
}