const navbar = document.querySelector('#navbar');
const main = document.querySelector('#main_body')
let navTop = navbar.offsetTop;
function stickynavbar() {
  if (window.scrollY >= navTop) {    
    navbar.classList.add('sticky');
    main.classList.add('sticky_main');
  } else {
    navbar.classList.remove('sticky');
    main.classList.remove('sticky_main');
  }
}
window.addEventListener('scroll', stickynavbar);
console.log("Hello world!"); 