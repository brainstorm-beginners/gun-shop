window.addEventListener("DOMContentLoaded", (event) => {
  // 'navigationMenu' elements' hover-pointer effect
  let menuElements = document.querySelectorAll(".navigationElement");
  for (let menuElement of menuElements) {
    menuElement.addEventListener("mouseover", function() {
      menuElement.style.cursor = "pointer";
    });
  }

  let menuElement = document.getElementById("navigationElementExtendable");
  menuElement.addEventListener("mouseover", function() {
      menuElement.style.cursor = "pointer";
  });

  // 'searchIcon' element's hover-pointer effect
  let searchIcon = document.getElementById("searchIcon");
  searchIcon.addEventListener("mouseover", function() {
      searchIcon.style.cursor = "pointer";
  });

  // 'extendableMenu' element's hover-appearing effect
  let menuElementExtendable = document.getElementById("navigationElementExtendable");
  let menuExtendable = document.getElementById("extendableMenu");
  let isMenuVisible = false;

  menuElementExtendable.addEventListener("mouseover", function() {
      isMenuVisible = true;
  });

  setTimeout(function() {
    menuElementExtendable.addEventListener("mouseout", function() {
      isMenuVisible = false;
      document.getElementById("navigationElementExtendable").style.backgroundColor = "#3F3F3F";
      document.getElementById("navigationElementExtendable").style.borderTop = "2px solid inherit";
      document.getElementById("navigationElementExtendable").style.borderBottom = "2px solid inherit";
      document.getElementById("navigationElementExtendable").style.color = "aliceblue";
    });
  }, 500);

  menuExtendable.addEventListener("mouseout", function() {
      isMenuVisible = false;
      document.getElementById("navigationElementExtendable").style.backgroundColor = "#3F3F3F";
      document.getElementById("navigationElementExtendable").style.borderTop = "2px solid inherit";
      document.getElementById("navigationElementExtendable").style.borderBottom = "2px solid inherit";
      document.getElementById("navigationElementExtendable").style.color = "aliceblue";
  });

  menuExtendable.addEventListener("mousemove", function() {
      isMenuVisible = true;
      document.getElementById("navigationElementExtendable").style.backgroundColor = "aliceblue";
      document.getElementById("navigationElementExtendable").style.borderTop = "2px solid #3F3F3F";
      document.getElementById("navigationElementExtendable").style.borderBottom = "2px solid #3F3F3F"
      document.getElementById("navigationElementExtendable").style.color = "#3F3F3F";
  });

  setInterval(function() {
  if (isMenuVisible) {
      menuExtendable.style.display = "block";
  } else {
      menuExtendable.style.display = "none";
  }
  }, 1);

  let extendableMenuElements = document.querySelectorAll(".extendableMenuElement");
  for (let extendableMenuElement of extendableMenuElements) {
      extendableMenuElement.addEventListener("mouseover", function() {
      extendableMenuElement.style.cursor = "pointer";
    });
  }

  window.getCart = function() {
    return JSON.parse(localStorage.getItem("cart")) || { items: [] };
  };

  window.closeCart = function() {
    document.querySelector(".cart").classList.remove("active");
    document.querySelector("body").style.overflowY = "auto";
    document.querySelector("body").style.paddingRight = "0";

    document.querySelector(".cartInfoText").innerHTML = `<b>Корзина:</b> 0 товаров - 0$`
  }

  window.getCartQuantity = function() {
    const cart = window.getCart();
  
    return cart.items.reduce((sum, item) => sum + item.quantity, 0);
  };
  
  window.getCartTotal = function() {
    const cart = window.getCart();
  
    return cart.items.reduce((sum, item) => sum + item.quantity * item.price, 0);
  };

  window.addItemToCart = function(productId, productImage, productPrice, productName, HTMLelementId) {
    const cart = localStorage.getItem("cart") ? JSON.parse(localStorage.getItem("cart")) : { items: [] };
  
    console.log("cart: ");
    console.table(cart.items);
  
    const itemInCart = cart.items.find(item => item.id === productId);
  
    if (itemInCart) {
      itemInCart.quantity++;
      console.log("QUANTITY++");
    } else {
      cart.items.push({
        id: productId,
        quantity: 1,
        image_url: productImage,
        price: productPrice,
        name: productName
      });
      console.log("ADDED TO THE CART\n\n\n-------------------------------");
    }
  
    localStorage.setItem("cart", JSON.stringify(cart));

    document.querySelector(".cartInfoText").innerHTML = `<b>Корзина:</b> ${getCartQuantity()} товаров - ${getCartTotal()}$`
  };    

  document.querySelector(".cartInfoText").innerHTML = `<b>Корзина:</b> ${getCartQuantity()} товаров - ${getCartTotal()}$`
  
  window.renderCart = function() {
    const cart = window.getCart();
    const items = cart.items.map((item) => ({
      id: item.id,
      quantity: item.quantity,
      image_url: item.image_url,
      price: item.price,
      name: item.name
    }));

    const cartEl = document.querySelector(".cart");
    cartEl.classList.add("active");

    document.querySelector("body").style.overflowY = "hidden";
    document.querySelector("body").style.paddingRight = "14px";

    cartEl.innerHTML = `
      <div class="closeCartButton" id="closeCartButton"><span class="horizontalLine"></span><span class="verticalLine"></span></div>
      <h1 style="margin-top: 50px;"> КОРЗИНА </h1>
      <div class="totalSumBox">
        <h2 style="padding: 0px 30px;"> Full price: <span style="color: green;">${window.getCartTotal(cart)}$</span> for ${window.getCartQuantity(cart)} chosen products</h2>
      </div>
      <ul class="cart-items">
        ${items.map((item) => `
          <li class="cart-item">
            <img src="/static_weapon_page/images/${item.image_url}" alt="">
            <p class="cart-item-name" style="text-align: center;"><b>Name</b>:<br><br>${item.name}</p>
            <p class="cart-item-price" style="text-align: center;"><b>Price</b>:<br><br>${item.price}$</p>
            <p class="cart-item-quantity" style="text-align: center;"><b>Quantity</b>:<br><br>${item.quantity}</p>
          </li>
        `).join("")}
      </ul>
      <div class="cartButtonsBox">
        <button id="clearCartButton">ИЛИ ОЧИСТИТЬ КОРЗИНУ</button>
        <button id="buyButton">ЗАКАЗАТЬ</button>
      </div>
    `;

    document.getElementById("closeCartButton").addEventListener("click", () => {
      closeCart();
    })

    document.getElementById("clearCartButton").addEventListener("click", () => {
      localStorage.removeItem("cart");
      renderCart();
    })
  };

  window.openGunPage = function(gunId, categoryId) {
      window.location.href = "/gun/" + categoryId + "/" + gunId;
  }

  window.openGunByCategoryPage = function(categoryId) {
      window.location.href = "/gun/" + categoryId;
  }

  window.searchGun = function () {
      let searchText = document.getElementById('searchBarTextBox').value;
      window.location.href = "/gun/search/" + searchText;
  }
});
