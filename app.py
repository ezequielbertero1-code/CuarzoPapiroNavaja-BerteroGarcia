from flask import Flask, render_template, request, session, redirect, url_for
from automata.fa.dfa import DFA
import os , secrets  # para elegir aleatorio de forma segura

app = Flask(__name__)
# Mejor tomarla de variable de entorno; si no existe, usa un fallback (solo local)
app.secret_key = secrets.token_hex(16)

dfa = DFA(
                states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'},
                input_symbols={'C', 'P', 'N'},
                transitions={
                    'q0': {'C': 'q1', 'P': 'q2', 'N': 'q3'},
                    'q1': {'C': 'q6', 'P': 'q5', 'N': 'q4'},
                    'q2': {'C': 'q4', 'P': 'q6', 'N': 'q5'},
                    'q3': {'C': 'q5', 'P': 'q4', 'N': 'q6'},
                    'q4': {'C': 'q4', 'P': 'q4', 'N': 'q4'},
                    'q5': {'C': 'q5', 'P': 'q5', 'N': 'q5'},
                    'q6': {'C': 'q6', 'P': 'q6', 'N': 'q6'}
                },
                initial_state='q0',
                final_states={'q4', 'q5', 'q6'}
            )

OPCIONES = ("C", "P", "N")
EMOJIS = {
    'C': 'Cuarzo 🪨',
    'N': 'Navaja ✂️',
    'P': 'Papiro 📄',
}

def init_sesion():
    session.setdefault("jugando", True)
    session.setdefault("ganadas", 0)
    session.setdefault("perdidas", 0)
    session.setdefault("empates", 0)
    session.setdefault("msj", "Jugá al famoso Piedra, Papel o Tijera.")

@app.route("/", methods=["GET", "POST"])
def juego():
    init_sesion()
    if request.method == "POST":
        eleccion = request.form.get("eleccion", "")
        if eleccion not in OPCIONES:
            session["msj"] = "Elección inválida. Probá con piedra, papel o tijera."
            return redirect(url_for("juego"))

        comp = secrets.choice(OPCIONES)
        
        if dfa.read_input(eleccion+comp) == 'q6':
            session["empates"] += 1
            resultado = "Empate"
            
        elif dfa.read_input(eleccion+comp) == 'q4':
            session["ganadas"] += 1
            resultado = "Ganaste!"
        else:
            session["perdidas"] += 1
            resultado = "Perdiste!"

        session["msj"] = f"Elegiste {EMOJIS[eleccion]} y la compu {EMOJIS[comp]}: {resultado}."

        
    return render_template(
        "index.html",
        msj=session["msj"],
        ganadas=session["ganadas"],
        perdidas=session["perdidas"],
        empates=session["empates"],
        juego_terminado=session.get("juego_terminado", False),
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("juego"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
