const carousel = document.querySelector('.carousel');
  const items = document.querySelectorAll('.carousel-item');
  const leftButton = document.querySelector('.carousel-control-left');
  const rightButton = document.querySelector('.carousel-control-right');
  let currentScroll = 0;
  let scrollWidth = carousel.scrollWidth - carousel.clientWidth;

  function updateButtons() {
    if (currentScroll === 0) {
      leftButton.disabled = true;
    } else {
      leftButton.disabled = false;
    }
    if (currentScroll === scrollWidth) {
      rightButton.disabled = true;
    } else {
      rightButton.disabled = false;
    }
  }

  leftButton.addEventListener('click', function() {
    currentScroll = Math.max(currentScroll - carousel.clientWidth, 0);
    carousel.scrollTo({left: currentScroll, behavior: 'smooth'});
    updateButtons();
  });

  rightButton.addEventListener('click', function() {
    currentScroll = Math.min(currentScroll + carousel.clientWidth, scrollWidth);
    carousel.scrollTo({left: currentScroll, behavior: 'smooth'});
    updateButtons();
  });

  updateButtons();