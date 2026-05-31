document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    if (!form) {
        console.error("Formulario no encontrado");
        return;
    }
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const response = await fetch('/predict', { method: 'POST', body: formData });
        const data = await response.json();
        if (data.error) {
            document.getElementById('error').innerText = data.error;
            document.getElementById('result').style.display = 'none';
        } else {
            document.getElementById('error').innerText = '';
            document.getElementById('quantity').innerText = data.Cantidad_Predecida;
            document.getElementById('recommendation').innerText = data.Recomendacion;
            document.getElementById('result').style.display = 'block';
        }
    });
});