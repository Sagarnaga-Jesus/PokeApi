from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key='1z2x2c3v4b5n6m7,8.9-01a2s3d4fg5h6j7k8l9ñ0'
API = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    
    pokemon_name = request.form.get('name','').strip().lower()
    if not pokemon_name:
        flash('Por favor ingresa un nombre de Pokémon válido.','danger')
        return redirect(url_for('index.html'))
    
    try:
        response = requests.get(f"{API}{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()
            return render_template('pokmon.html', pokemon=pokemon_data)
        else:
            flash('Pokémon no encontrado. Intenta con otro nombre.','warning')
            return redirect(url_for('base'))
        
    except requests.exceptions.RequestException as e:
        flash('Error al conectar con la API de Pokémon. Intenta más tarde.','danger')
        return redirect(url_for('base'))
        
        pokemon_info = {
            'name': data['name'].title(),
            'id': data['id'],
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'].title() for t in data['types']],
            'abilities': [a['ability']['name'].title() for a in data['abilities']],
            'sprite': data['sprites']['front_default']
        }
        
        return render_template('results.html', pokemon=pokemon_info)
        
    
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)