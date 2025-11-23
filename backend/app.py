from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MODELO 

class ModeloPredictorDesercion:

    def __init__(self, model, threshold, discretizer, imputer_num,
                 imputer_cat, label_encoders, num_cols, cat_cols, feature_names):
        self.model = model
        self.threshold = threshold
        self.discretizer = discretizer
        self.imputer_num = imputer_num
        self.imputer_cat = imputer_cat
        self.label_encoders = label_encoders
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.feature_names = feature_names

    def predict_proba(self, X):
        #[P(no desertor), P(desertor)]
        X_proc = self._preprocess(X)
        return self.model.predict_proba(X_proc)

    def predict(self, X):
        proba = self.predict_proba(X)[:, 1]
        return (proba >= self.threshold).astype(int)

    def _preprocess(self, X):
        X_proc = X.copy()

        X_proc[self.num_cols] = self.imputer_num.transform(X_proc[self.num_cols])
        X_proc[self.cat_cols] = self.imputer_cat.transform(X_proc[self.cat_cols])

        for col in self.cat_cols:
            if col in self.label_encoders:
                X_proc[col] = self.label_encoders[col].transform(X_proc[col].astype(str))
            else:
                X_proc[col] = X_proc[col].astype(int)

        X_proc[self.num_cols] = self.discretizer.transform(X_proc[self.num_cols]).astype(int)

        return X_proc
app = Flask(__name__)
CORS(app)  
        
# CARGAR MODELO Y MAPEOS

try:
    with open('model_results.pkl', 'rb') as f:
        results = pickle.load(f)
    
    pipeline = results['pipeline']
    threshold = results['threshold']
    metrics = results['metrics']
    
    logger.info("✓ Modelo cargado exitosamente")
    logger.info(f"  Threshold: {threshold:.2f}")
    logger.info(f"  Recall: {metrics['recall']*100:.1f}%")
    
except Exception as e:
    logger.error(f"Error cargando modelo: {e}")
    pipeline = None
    metrics = {}

try:
    with open('mapeos_nombres.pkl', 'rb') as f:
        mapeos = pickle.load(f)
    
    mapeo_programas = mapeos['programas']
    
    logger.info("✓ Mapeos cargados exitosamente")
    logger.info(f"  Programas disponibles: {len(mapeo_programas)}")

    
except Exception as e:
    logger.warning(f"Error cargando mapeos: {e}")
    mapeo_programas = {}

# RUTA API

@app.route('/')
def home():
    return jsonify({
        'nombre': 'API de Predicción de Deserción Estudiantil',
        'version': '1.0',
        'estado': 'activo' if pipeline else 'error',
        'threshold': threshold if pipeline else None,
        'metricas': metrics if metrics else None,
        'endpoints': {
            '/predict': 'POST - Realizar predicción',
            '/health': 'GET - Estado del servidor',
            '/programas': 'GET - Lista de programas disponibles',
            '/info': 'GET - Información del modelo'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'modelo_cargado': pipeline is not None,
        'mapeos_cargados': len(mapeo_programas) > 0
    })

@app.route('/programas')
def get_programas():
    programas_list = [
        {'codigo': codigo, 'nombre': nombre}
        for codigo, nombre in sorted(mapeo_programas.items(), key=lambda x: x[1])
    ]
    return jsonify({'programas': programas_list})

@app.route('/info')
def get_info():
    if not pipeline:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    return jsonify({
        'modelo': 'Naive Bayes Categórico',
        'tecnica_balanceo': 'SMOTE (sampling_strategy=0.43)',
        'threshold': threshold,
        'metricas': {
            'accuracy': f"{metrics['accuracy']*100:.2f}%",
            'precision': f"{metrics['precision']*100:.2f}%",
            'recall': f"{metrics['recall']*100:.2f}%",
            'f1_score': f"{metrics['f1']*100:.2f}%",
            'roc_auc': f"{metrics['roc_auc']*100:.2f}%"
        },
        'interpretacion': {
            'recall': f"Detecta {metrics['recall']*100:.0f}% de los desertores reales",
            'precision': f"De cada 100 alertas, {metrics['precision']*100:.0f} son correctas",
            'filosofia': "Prioriza detectar desertores (recall) sobre evitar falsas alarmas"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    
    if not pipeline:
        return jsonify({'error': 'Modelo no disponible'}), 500
    
    try:
        data = request.get_json()

        if data['naturaleza_colegio'].upper() in ['PUBLICO', 'PÚBLICO']:
            data['naturaleza_colegio'] = 'PÚBLICO'
        elif data['naturaleza_colegio'].upper() == 'PRIVADO':
            data['naturaleza_colegio'] = 'PRIVADO'
        
        required_fields = [
            'edad_ingreso', 'sexo', 'estrato', 'programa',
            'promedio_historico', 'creditos_maximos', 'total_periodos',
            'tasa_aprobacion_media', 'rezago_final', 'ha_estado_fuera',
            'tiene_beca', 'naturaleza_colegio', 'calendario'
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': 'Campos faltantes',
                'campos': missing_fields
            }), 400
        
        programa = data['programa']
        escuela_map = {
            'PRMEDICINA12': 'CS', 'PROFEDERECHO': 'JU', 'PINGSISTEMAS': 'IN',
            'PADMEMPRESAS': 'AD', 'PINGINDUSTRL': 'IN', 'PRPSICOLOGIA': 'HU',
            'PNEGINTNALES': 'AD', 'PINGENICIVIL': 'IN', 'PCOMUNSOCIAL': 'HU',
            'PINGMECANICA': 'IN', 'PARQUITECTUR': 'AQ', 'PDISENOGRAFI': 'AQ',
            'PLENGMODCULT': 'II', 'PRELINTERNAC': 'JU', 'PINGELECTRON': 'IN',
            'PRCONTADURIA': 'AD', 'PRODONTOLOGI': 'CS', 'PRENFERMERIA': 'CS',
            'PROFGEOLOGIA': 'BA', 'PROFECONOMIA': 'AD', 'PINGELECTRIC': 'IN',
            'PCIENPOLIGOB': 'JU', 'PDISENOINDUS': 'AQ', 'PRCIENCIADAT': 'IN',
            'PROFESMUSICA': 'VA', 'PLICPEDAGINF': 'IE', 'PMATEMATICAS': 'BA',
            'PRLICEDUINFA': 'IE', 'PFILOSOHUMAN': 'HU', 'PLICFILOSOHU': 'HU',
            'PLICMATEMATI': 'BA'
        }
        escuela = escuela_map.get(programa, 'IN')
        
        input_data = pd.DataFrame({
            'EDAD_INGRESO': [data['edad_ingreso']],
            'SEXO': [data['sexo']],  
            'ESTRATO': [data['estrato']],
            'PROGRAMA': [programa],
            'ESCUELA': [escuela],
            'PROMEDIO_HISTORICO': [data['promedio_historico']],
            'CREDITOS_MAXIMOS': [data['creditos_maximos']],
            'TOTAL_PERIODOS': [data['total_periodos']],
            'TASA_APROBACION_MEDIA': [data['tasa_aprobacion_media']],
            'REZAGO_FINAL': [data['rezago_final']],
            'HA_ESTADO_FUERA': [data['ha_estado_fuera']],
            'TIENE_BECA': [data['tiene_beca']],
            'NATURALEZA_DEL_COLEGIO': [data['naturaleza_colegio']],
            'CALENDARIO': [data['calendario']]
})
        
        # Realizar predicción
        probabilidad = pipeline.predict_proba(input_data)[0][1]
        prediccion = pipeline.predict(input_data)[0]
        
        if probabilidad < 0.30:
            nivel_riesgo = 'BAJO'
            color = '#10b981'  
            recomendacion = 'Seguimiento estándar. El estudiante muestra señales positivas.'
        elif probabilidad < 0.60:
            nivel_riesgo = 'MEDIO'
            color = '#f59e0b'  
            recomendacion = 'Monitoreo preventivo recomendado. Ofrecer apoyo académico.'
        else:
            nivel_riesgo = 'ALTO'
            color = '#ef4444'  
            recomendacion = 'Intervención urgente necesaria. Contactar al estudiante de inmediato.'
        
        # Factores de riesgo
        factores_riesgo = []
        if data['promedio_historico'] < 3.0:
            factores_riesgo.append({
                'factor': 'Promedio bajo',
                'valor': f"{data['promedio_historico']:.2f}",
                'descripcion': 'Por debajo de 3.0'
            })
        if data['tasa_aprobacion_media'] < 0.70:
            factores_riesgo.append({
                'factor': 'Baja tasa de aprobación',
                'valor': f"{data['tasa_aprobacion_media']*100:.0f}%",
                'descripcion': 'Menos del 70% de materias aprobadas'
            })
        if data['rezago_final'] > 1.0:
            factores_riesgo.append({
                'factor': 'Rezago académico',
                'valor': f"{data['rezago_final']:.1f}",
                'descripcion': 'Rezago superior a 1 periodo'
            })
        if data['tiene_beca'] == 0:
            factores_riesgo.append({
                'factor': 'Sin apoyo de beca',
                'valor': 'No',
                'descripcion': 'No cuenta con beca financiera'
            })
        if data['edad_ingreso'] > 22:
            factores_riesgo.append({
                'factor': 'Edad de ingreso elevada',
                'valor': f"{data['edad_ingreso']} años",
                'descripcion': 'Superior al promedio (18-20 años)'
            })
        if data['ha_estado_fuera'] == 1:
            factores_riesgo.append({
                'factor': 'Inactividad previa',
                'valor': 'Sí',
                'descripcion': 'Ha estado fuera de la universidad'
            })
        
        # Respuesta
        response = {
            'prediccion': {
                'desertor': bool(prediccion),
                'probabilidad': round(probabilidad * 100, 2),
                'nivel_riesgo': nivel_riesgo,
                'color': color
            },
            'recomendacion': recomendacion,
            'factores_riesgo': factores_riesgo,
            'perfil': {
                'edad': data['edad_ingreso'],
                'promedio': data['promedio_historico'],
                'tasa_aprobacion': f"{data['tasa_aprobacion_media']*100:.0f}%",
                'rezago': data['rezago_final'],
                'periodos': data['total_periodos'],
                'programa': mapeo_programas.get(programa, programa)
            },
            'metadata': {
                'threshold': threshold,
                'modelo': 'Naive Bayes + SMOTE'
            }
        }
        
        logger.info(f"Predicción exitosa: {probabilidad*100:.1f}% - {nivel_riesgo}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({
            'error': 'Error al procesar predicción',
            'detalle': str(e)
        }), 500

# SERVIDOR

if __name__ == '__main__':
    print(f"Estado del modelo: {' Cargado' if pipeline else '✗ Error'}")
    print(f"Threshold: {threshold:.2f}" if pipeline else "N/A")
    print(f"Recall: {metrics.get('recall', 0)*100:.1f}%" if metrics else "N/A")
    print("\nServidor iniciado en http://localhost:5000")
    print("Endpoints:")
    print("  GET  / - Información general")
    print("  GET  /health - Estado del servidor")
    print("  GET  /programas - Lista de programas")
    print("  GET  /info - Información del modelo")
    print("  POST /predict - Realizar predicción")
    
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
