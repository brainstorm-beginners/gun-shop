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
      });
    }, 1000);

    menuExtendable.addEventListener("mouseout", function() {
        isMenuVisible = false;
    });

    menuExtendable.addEventListener("mousemove", function() {
        isMenuVisible = true;
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

    window.openGunPage = function(gunId, categoryId) {
        window.location.href = "/gun/" + categoryId + "/" + gunId;
    }

    window.openGunByCategoryPage = function(categoryId) {
        window.location.href = "/gun/" + categoryId;
    }

    window.searchGun = function () {
        let searchText = document.getElementById('searchBarTextBox').value;
        window.location.href = "/gun/" + searchText;
    }
});
