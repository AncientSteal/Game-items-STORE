document.addEventListener('DOMContentLoaded', function() {
    const shade = document.getElementById('shade');
    const orderButton = document.getElementById('order_button');
    const orderModal = document.getElementById('order_modal');
    const closeButton = document.getElementById('close_button');
    const successModal = document.getElementById('success_modal');
    const closeSuccess = successModal.querySelector('.close_button');

    orderButton.addEventListener('click', () => {
        orderModal.style.display = 'block';
        shade.classList.add('active');
    });

    orderModal.addEventListener('submit', () => {
        event.preventDefault();
        orderModal.style.display = 'none';
        successModal.style.display = 'block';
    });

    closeSuccess.addEventListener('click', () => {
        successModal.style.display = 'none';
        shade.classList.remove('active');
    });

    closeButton.addEventListener('click', () => {
        orderModal.style.display = 'none';
        shade.classList.remove('active');
    });

    window.addEventListener('click', (event) => {
        if (event.target === shade) {
            orderModal.style.display = 'none';
            successModal.style.display = 'none';
            shade.classList.remove('active');
        }
    });
});
