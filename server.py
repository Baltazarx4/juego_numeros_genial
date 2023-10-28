from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ruta raíz: Inicializa el número aleatorio y muestra el formulario de adivinanza
@app.route('/', methods=['GET'])
def index():
    if 'target_number' not in session:
        session['target_number'] = random.randint(1, 100)
        session['attempts'] = 0  # Contador de intentos
        session['message'] = ''  # Mensaje para el usuario
    return render_template('index.html', message=session['message'])

# Ruta para manejar el intento del usuario
@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    session['attempts'] += 1

    if guess == session['target_number']:
        session['message'] = f'¡Felicidades! Adivinaste el número {session["target_number"]} en {session["attempts"]} intentos.'
        session.pop('target_number')  # Resetea el juego
        return render_template('index.html', message=session['message'], result='correct')
    elif guess < session['target_number']:
        session['message'] = 'Demasiado bajo. ¡Inténtalo de nuevo!'
        return render_template('index.html', message=session['message'], result='incorrect')
    else:
        session['message'] = 'Demasiado alto. ¡Inténtalo de nuevo!'
        return render_template('index.html', message=session['message'], result='incorrect')


@app.route('/reset', methods=['POST'])
def reset_game():
    session.clear()  # Borra todos los datos de la sesión
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
