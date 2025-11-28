const toggleBtn = document.getElementById('toggleMenu');
const menu = document.getElementById('sideMenu');
const shade = document.getElementById('shade');
const arrow = toggleBtn.querySelector('.arrow');
const artImage = document.getElementById('art_image');

let isOpen = false;

toggleBtn.onclick = () => {

    if (!isOpen) {
        // Открыть меню
        menu.style.left = '0px';
        toggleBtn.style.left = '250px';
        shade.classList.add('active');
        arrow.style.transform = 'rotate(180deg)';
        artImage.style.left = '-400px';
        artImage.style.bottom = '-300px';


    } else {
        // Закрыть меню
        menu.style.left = '-250px';
        toggleBtn.style.left = '-6px';
        shade.classList.remove('active');
        arrow.style.transform = 'rotate(0deg)';
        artImage.style.left = '-800px';
        artImage.style.bottom = '-1100px';
    }
    isOpen = !isOpen;
};
