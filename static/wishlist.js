let wishlist = [];

function updateWishlist(url, csrftoken, productid) {
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({productid: productid})
    })
}

async function getWishlist(url) {
    let response = await fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    });
    let data = await response.json();
    return data['wishlist'].map(e => String(e));;
}

function updateWishlistButtons(selector) {
    wishlistButtons = document.querySelectorAll(selector);
    wishlistButtons.forEach(element => {
        if (wishlist.includes(element.value)) {
            element.innerText = '♥';
        }
    });
}