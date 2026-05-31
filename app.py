from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

with open('modelo.pkl', 'rb') as f:
    modelo = pickle.load(f)
with open('preprocesamiento.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

regiones = list(label_encoders['region'].classes_)
categorias = list(label_encoders['category'].classes_)
sub_categorias = list(label_encoders['sub-category'].classes_)
segmentos = list(label_encoders['segment'].classes_)
modos_entregas = list(label_encoders['ship_mode'].classes_)
meses = list(range(1,13))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def formulario():
    return render_template('form.html',
                           regiones=regiones,
                           categorias=categorias,
                           sub_categorias=sub_categorias,
                           segmentos=segmentos,
                           modos_entregas=modos_entregas,
                           meses=meses)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/predict', methods=['POST'])
def predict():
    region = request.form['region']
    categoria = request.form['category']
    sub_categoria = request.form['sub_category']
    mes = int(request.form['month'])
    descuento = float(request.form['discount'])
    segmento = request.form['segment']
    modo_entrega = request.form['ship_mode']
    ventas = float(request.form['sales'])

    region_enc = label_encoders['region'].transform([region])[0]
    categoria_enc = label_encoders['category'].transform([categoria])[0]
    sub_categoria_enc = label_encoders['sub-category'].transform([sub_categoria])[0]
    segmento_enc = label_encoders['segment'].transform([segmento])[0]
    modo_entrega_enc = label_encoders['ship_mode'].transform([modo_entrega])[0]

    features = np.array([[region_enc, categoria_enc, sub_categoria_enc, mes, descuento, segmento_enc, modo_entrega_enc, ventas]])
    prediccion = modelo.predict(features)[0]
    pred_qty = max(0, round(prediccion))

    if pred_qty < 2:
        reco = "Baja Demanda"
    elif pred_qty < 5:
        reco = "Demanda Moderada"
    else:
        reco = "Alta Demanda"

    return jsonify({'Cantidad_Predecida': pred_qty,
                    'Recomendacion': reco})


if __name__ == '__main__':
    app.run(debug=True)