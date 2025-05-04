let navToggle = document.querySelector('.fa-bars');
let navList = document.querySelector('.nav-list');

navToggle.addEventListener('click', function() {
    navToggle.classList.toggle('fa-times');
    navList.classList.toggle('active');
})