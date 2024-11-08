# Importamos las clases y métodos
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def aritmetica():
    if request.method == "POST":
        # Valores que recibo del form n1, n2 son pasados
        num1 = float(request.form.get("n1"))
        num2 = float(request.form.get("n2"))
        
        # Realizamos operaciones aritméticas
        suma = num1 + num2
        resta = num1 - num2
        multiplicacion = num1 * num2
        division = num1 / num2
        return render_template('index.html', total_suma=suma,
                                             total_resta=resta,
                                             total_multiplicacion=multiplicacion,
                                             total_division=division)

    return render_template('index.html')

@app.route('/divisas', methods=['GET', 'POST'])
def divisas():
    pesos = None
    dolares = None
    if request.method == "POST":
        # Tasa de cambio actual de USD a COP
        tasa_cambio = 4390.0
        
        # Valor recibido del formulario
        dolares = float(request.form.get("dolares"))
        
        # Convertimos dólares a pesos
        pesos = dolares * tasa_cambio
        
    return render_template('divisas.html', total_pesos=pesos, dolares=dolares)

if __name__ == "__main__":
    app.run(debug=True)
