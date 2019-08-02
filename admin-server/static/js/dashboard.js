// for edit item
function saveItem(item_id){
    let xhr = new XMLHttpRequest();
    let formData = new FormData();

    let name = document.getElementById("name-" + item_id).value;
    let price = document.getElementById("price-" + item_id).value;
    let quantity = document.getElementById("quantity-" + item_id).value;
    let description = document.getElementById("description-" + item_id).value;
    let tags = document.getElementById("tags-" + item_id).value;
    let file = document.getElementById("file-" + item_id);
    let image_name = document.getElementById("img-name-" + item_id).value;
    
    if(file.files[0]){
        formData.append("image", file.files[0]);
    }

    formData.append("item_id", item_id);
    formData.append("name", name)
    formData.append("price", price);
    formData.append("quantity", quantity);
    formData.append("description", description);
    formData.append("tags", tags);
    formData.append("image_name", image_name);
    
    xhr.onreadystatechange = state => { 
        console.log(xhr.status); 
        // return to Edit Item section after reloading the page
        sessionStorage.setItem("page", "edit_item");
        // reload page
        window.location.reload(true);
    }
    let apiURL = "/edit_item";
    xhr.open("POST", apiURL);
    xhr.send(formData);
}
// end

function saveOrder(obj){
    let inputField = document.getElementById('fulfilled-' + obj.id)

    if(inputField.value === "True"){
        let xhr = new XMLHttpRequest();
        let formData = new FormData();

        formData.append("order_id", obj.id);
        
        console.log("id: " + obj.id)

        xhr.onreadystatechange = state => { 
            console.log(xhr.status); 
            // return to Orders section after reloading the page
            sessionStorage.setItem("page", "orders");
            // reload page
            window.location.reload(true);
        }
        
        let apiURL = "/fulfill_order";
        xhr.open("POST", apiURL);
        xhr.send(formData);
    }
}


// to close alert boxes
function hide_message(x) {
    x = this.parentNode;

    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

// end

function showAddItemPage(){
    document.getElementById('add-item').style.display = "block";
    document.getElementById('edit-item').style.display = "none";
    document.getElementById('item-listing').style.display = "none";
    document.getElementById('orders').style.display = "none";
}

function showEditPage(){
    document.getElementById('add-item').style.display = "none";
    document.getElementById('edit-item').style.display = "block";
    document.getElementById('item-listing').style.display = "none";
    document.getElementById('orders').style.display = "none";
}

function showListings(){
    document.getElementById('add-item').style.display = "none";
    document.getElementById('edit-item').style.display = "none";
    document.getElementById('item-listing').style.display = "block";
    document.getElementById('orders').style.display = "none";
}

function showOrders(){
    document.getElementById('add-item').style.display = "none";
    document.getElementById('edit-item').style.display = "none";
    document.getElementById('item-listing').style.display = "none";
    document.getElementById('orders').style.display = "block";
}

if(sessionStorage.getItem("page")){
    page = sessionStorage.getItem("page");

    if(page === "edit_item"){
        showEditPage();
    }else if(page === "orders"){
        showOrders();
    }
}else{
    showListings();
}
