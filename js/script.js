const navbar = document.querySelector('#navbar');
let navTop = navbar.offsetTop;
function stickynavbar() {
  if (window.scrollY >= navTop) {    
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');    
  }
}
window.addEventListener('scroll', stickynavbar);
console.log("Hello world!"); 