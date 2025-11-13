from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = '1z2x2c3v4b5n6m7,8.9-01a2s3d4fg5h6j7k8l9ñ0'
API = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/search', methods=['POST'])
def search():
    pokemon_name = request.form.get('name', '').strip().lower()
    
    if not pokemon_name:
        flash('Por favor ingresa un nombre de Pokémon válido.', 'error')
        return redirect(url_for('base'))
    
    try:
        response = requests.get(f"{API}{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()

            pokemon_info = {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height'] / 10,
                'weight': pokemon_data['weight'] / 10,
                'imagen': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']],
            }
            
            return render_template('pokemon.html', pokemon=pokemon_info)
        else:
            flash(f'Pokémon "{pokemon_name}" no encontrado.', 'error')
            return redirect(url_for('index'))
        
    except requests.exceptions.RequestException:
        flash('Error al conectar con la API de Pokémon. Inténtalo de nuevo más tarde.', 'error')
        return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)