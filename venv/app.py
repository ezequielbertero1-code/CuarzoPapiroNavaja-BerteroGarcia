# Ver dsp que realmente nos sirve de este import de flask.
from flask import Flask, render_template, request, session, redirect, url_for 

app = Flask(__name__)
# pide una clave secreta si o si, como va a ser local y no se va a hacer nada puse clave.
app.secret_key = 'clave'

#routes, post nose si es necesario realmente
@app.route('/', methods=['GET', 'POST'])
def juego():

    # si no inicio el juego todavia, lo inicializo
    if 'jugando' not in session:
        session['jugando'] = True
        session['ganadas'] = 0
        session['perdidas'] = 0
        session['empates'] = 0
        session['msj'] = "Juega al famoso Piedra papel o tijera."

        #aca iria la logica del juego

    #Paso variables a HTML
    return render_template(
        'index.html',
        msj=session['msj'],
        ganadas=session['ganadas'],
        perdidas=session['perdidas'],
        empates=session['empates'],
        juego_terminado=session.get('juego_terminado', False)
    )

# route para reiniciar juego
@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('juego'))

if __name__ == '__main__':
    app.run(debug=True)