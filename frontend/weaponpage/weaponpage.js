window.addEventListener("DOMContentLoaded", (event) => {
    // 'navigationMenu' elements' hover-pointer effect
    let menuElements = document.querySelectorAll(".navigationElement");
    for (let menuElement of menuElements) {
      menuElement.addEventListener("mouseover", function() {
        menuElement.style.cursor = "pointer";
      });
    };

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
    };

    let secondaryWeaponImage = document.querySelectorAll(".secondaryWeaponImage");
    for (let image of secondaryWeaponImage) {
        image.addEventListener("mouseover", function() {
        image.style.cursor = "pointer";
        image.style.transform = "scale(1.05)";
        });

        image.addEventListener("mouseout", function() {
          image.style.transform = "scale(1)";
        });
    };

    let bottomWeaponImage = document.getElementById("bottomWeaponImage");
    bottomWeaponImage.addEventListener("mouseover", function() {
      bottomWeaponImage.style.cursor = "pointer";
      bottomWeaponImage.style.transform = "scale(1.015)";
      bottomWeaponImage.style.transition = "all 0.3s ease-in-out";
      bottomWeaponImage.style.backgroundSize = "105%";
    });

    bottomWeaponImage.addEventListener("mouseout", function() {
      bottomWeaponImage.style.transition = "all 0.3s ease-in-out";
      bottomWeaponImage.style.transform = "scale(1)";
      bottomWeaponImage.style.backgroundSize = "100%";
    });
});
