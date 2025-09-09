// Hapus atau komentari alert jika tidak diperlukan lagi
// alert('Haii');

const menuHamburger = document.getElementById("menu-hamburger");
const navMenu = document.getElementById("nav-menu");

menuHamburger.addEventListener("click", function () {
  // Toggle class untuk animasi hamburger
  menuHamburger.classList.toggle("active");

  // Toggle class untuk menampilkan/menyembunyikan menu
  navMenu.classList.toggle("translate-x-full");
});

// Tambahkan style untuk animasi hamburger icon jika diperlukan
const style = document.createElement("style");
style.innerHTML = `
    #menu-hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    #menu-hamburger.active span:nth-child(2) {
        transform: scale(0);
    }
    #menu-hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(5px, -5px);
    }
`;
document.head.appendChild(style);
