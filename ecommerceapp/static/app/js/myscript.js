// Initialize OwlCarousel for sliders
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
});

// Plus Cart Button
$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Span element for quantity display

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: { prod_id: id },
        success: function(data) {
            eml.innerText = data.quantity; // Update quantity
            document.getElementById("amount").innerText = data.amount; // Update cart total
            document.getElementById("totalamount").innerText = data.totalamount; // Update final amount
        }
    });
});

// Minus Cart Button
$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Span element for quantity display

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: { prod_id: id },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

// Remove Cart Item
$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: { prod_id: id },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            this.closest('.row').remove(); // Remove item row from UI
        }
    });
});

// Add to Wishlist
$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: { prod_id: id },
        success: function(data) {
            window.location.href = `http://localhost:8000/product-detail/${id}`;
        }
    });
});

// Remove from Wishlist
$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: { prod_id: id },
        success: function(data) {
            window.location.href = `http://localhost:8000/product-detail/${id}`;
        }
    });
});