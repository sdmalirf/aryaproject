// Konfirmasi file JS terhubung
console.log("File scripts.js berhasil terhubung!");

// Smooth scrolling untuk anchor link
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Validasi form sederhana
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        const name = document.querySelector("#name").value;
        const email = document.querySelector("#email").value;

        if (!name || !email) {
            e.preventDefault();
            alert("Harap isi semua field di form!");
        }
    });
});

// Efek klik tombol
document.querySelectorAll("button").forEach(button => {
    button.addEventListener("click", () => {
        button.style.transform = "scale(1.1)";
        setTimeout(() => button.style.transform = "scale(1)", 200);
    });
});
