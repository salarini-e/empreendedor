/*Definindo a lógica por trás do dropdown do nav:*/
document.addEventListener("click", e=>{
    const isDropDownButton = e.target.matches("[data-dropdown-button]");
    if(!isDropDownButton && e.target.closest("[data-dropdown]") != null) return;
    
    let currentDropDown = null;
    if(isDropDownButton){
        currentDropDown = e.target.closest("[data-dropdown]");
        currentDropDown.classList.toggle("activate");
    }

    document.querySelectorAll("[data-dropdown].activate").forEach(dropDown=>{
        if(dropDown == currentDropDown) return;
        dropDown.classList.remove("activate");
    })
});
/* Definindo a lógica por trás do offcanvas do nav */
document.querySelector(".menu-open").addEventListener("click", ()=>{
    document.querySelector(".menu-wrapper").style.width = "240px";
    document.querySelector("body").style.marginRight = "240px";
});
document.querySelector(".menu-close").addEventListener("click", ()=>{
    document.querySelector(".menu-wrapper").style.width = "0";
    document.querySelector("body").style.width = "0";
});