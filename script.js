document.getElementById('nameForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const input = document.getElementById('nombreInput');
    const nombre = input.value.trim();
    const nombreMinuscula = nombre.toLowerCase();

    // Lista de frases que activan el easter egg
    const frasesEasterEgg = ['que te importa', 'qué te importa', 'que te importa?', 'qué te importa?'];

    if (frasesEasterEgg.includes(nombreMinuscula)) {
        activarEasterEgg();
        input.value = '';
        return;
    }

    // Muestra el saludo normal
    document.getElementById('saludoResultado').textContent = `¡Un gusto conocerte, ${nombre}!`;

    // Envío al servidor local
    try {
        const response = await fetch('http://localhost:3000/api/guardar-nombre', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre: nombre })
        });

        if (response.ok) {
            console.log('Nombre enviado al backend.');
        } else {
            console.error('Error al responder el backend.');
        }
    } catch (error) {
        console.error('Error al conectar con el servidor local:', error);
    }

    input.value = '';
});

// Función para activar la imagen en pantalla completa
function activarEasterEgg() {
    const overlay = document.getElementById('easterEggOverlay');
    overlay.classList.remove('hidden');
}

// Cierra la pantalla completa haciendo clic en cualquier parte
document.getElementById('easterEggOverlay').addEventListener('click', function() {
    this.classList.add('hidden');
});