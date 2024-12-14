// Exemple de validation de formulaire (si nécessaire)
document.querySelector('form').onsubmit = function(e) {
    let email = document.querySelector('input[name="email"]');
    if (!email.value.includes('@')) {
        alert('Veuillez entrer un email valide.');
        e.preventDefault();
    }
};
