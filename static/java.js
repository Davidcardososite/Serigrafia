// efeito clean
  const elements = document.querySelectorAll('.links,.tecidos,.plastico,.papel,.galeria,.galeria_sobre');

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0 });

  elements.forEach(element => {
    observer.observe(element);
  });


document.addEventListener('DOMContentLoaded', function() {
    const hamburgerIcon = document.querySelector('.hamburger-icon');
    const navList = document.querySelector('.nav_list');

    // Adiciona um evento de clique ao ícone do hambúrguer
    hamburgerIcon.addEventListener('click', function(event) {
        event.stopPropagation();
        hamburgerIcon.classList.toggle('open');
        navList.classList.toggle('open');
    });

    // Adiciona um evento de clique ao documento inteiro
    document.addEventListener('click', function(event) {
        if (!navList.contains(event.target) && navList.classList.contains('open')) {
            navList.classList.remove('open');
            hamburgerIcon.classList.remove('open');
        }
    });
});
