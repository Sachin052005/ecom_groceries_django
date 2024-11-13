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
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Assuming this is the quantity element
    console.log("pid=", id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data = ", data);
            // Update the quantity in the specific element
            $(eml).text(data.quantity); // Use jQuery to update the text
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});


$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Assuming this is the quantity element
    console.log("pid=", id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data = ", data);
            // Update the quantity in the specific element
            $(eml).text(data.quantity); // Use jQuery to update the text
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});


$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Get the product ID
    var cartItem = $(this).closest('.row'); // Get the closest row (cart item)
    
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: { prod_id: id },
        success: function(data) {
            // Update displayed amounts
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
            // Remove the cart item from the DOM
            cartItem.remove();
            // Check if the cart is empty after removal
            if ($('.row').length === 0) {
                $('.container').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});




// Voice Search Functionality
const voiceSearchBtn = document.getElementById('voiceSearchBtn');
const searchInput = document.querySelector('input[name="search"]');

voiceSearchBtn.addEventListener('click', function() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US'; // Set language here

        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript; // Set the input value to the recognized text
            recognition.stop();
            // Optionally, submit the form if you want to search immediately
            document.querySelector('form[role="search"]').submit();
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
        };
    } else {
        alert('Sorry, your browser does not support voice search.');
    }
});





