const navbar = document.querySelector('#navbar');
const main = document.querySelector('#main_body')
let navTop = navbar.offsetTop;
function stickynavbar() {
  if (window.scrollY >= navTop) {    
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');
  }
}
window.addEventListener('scroll', stickynavbar);
