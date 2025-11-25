from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
try:
    with open('model_results.pkl', 'rb') as f:
        results = pickle.load(f)
    
    pipeline = results['pipeline']
    threshold = results['threshold']
    metrics = results['metrics']
    
    logger.info("Modelo cargado exitosamente")
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
    
    logger.info("Mapeos cargados ")
    logger.info(f"Programas disponibles: {len(mapeo_programas)}")

    
except Exception as e:
    logger.warning(f"Error cargando mapeos: {e}")
    mapeo_programas = {}


def identificar_factores_riesgo(data, probabilidad):
    factores = []
    
    if probabilidad < 0.30:
        return []
    
    elif probabilidad < 0.60:
        if data['promedio_historico'] < 3.2:
            factores.append({
                'factor': 'Promedio moderado',
                'valor': f"{data['promedio_historico']:.2f}",
                'descripcion': 'Por debajo de 3.2 - requiere atención'
            })
        
        if data['tasa_aprobacion_media'] < 0.75:
            factores.append({
                'factor': 'Tasa de aprobación moderada',
                'valor': f"{data['tasa_aprobacion_media']*100:.0f}%",
                'descripcion': 'Menos del 75% de materias aprobadas'
            })
        
        if data['rezago_final'] > 0.5:
            factores.append({
                'factor': 'Rezago académico',
                'valor': f"{data['rezago_final']:.1f} períodos",
                'descripcion': 'Retraso en el plan de estudios'
            })
        
        if data['tiene_beca'] == 0 and data['estrato'] <= 3:
            factores.append({
                'factor': 'Sin apoyo de beca',
                'valor': 'No',
                'descripcion': 'Podría beneficiarse de apoyo financiero'
            })
        
        if data['creditos_maximos'] < 16:
            factores.append({
                'factor': 'Carga académica reducida',
                'valor': f"{data['creditos_maximos']} créditos",
                'descripcion': 'Menos de 16 créditos por período'
            })
    
    else:
        if data['promedio_historico'] < 3.0:
            factores.append({
                'factor': 'Promedio bajo crítico',
                'valor': f"{data['promedio_historico']:.2f}",
                'descripcion': 'Por debajo del mínimo aprobatorio (3.0)'
            })
        elif data['promedio_historico'] < 3.5:
            factores.append({
                'factor': 'Promedio bajo',
                'valor': f"{data['promedio_historico']:.2f}",
                'descripcion': 'Rendimiento académico por debajo del promedio'
            })
        
        if data['tasa_aprobacion_media'] < 0.70:
            factores.append({
                'factor': 'Baja tasa de aprobación',
                'valor': f"{data['tasa_aprobacion_media']*100:.0f}%",
                'descripcion': 'Pérdida recurrente de materias - riesgo crítico'
            })
        
        if data['rezago_final'] > 1.0:
            factores.append({
                'factor': 'Rezago académico significativo',
                'valor': f"{data['rezago_final']:.1f} períodos",
                'descripcion': 'Atraso considerable en el plan de estudios'
            })
        
        if data['ha_estado_fuera'] == 1:
            factores.append({
                'factor': 'Inactividad previa',
                'valor': 'Sí',
                'descripcion': 'Ha tenido períodos de inactividad académica'
            })
        
        if data['tiene_beca'] == 0:
            factores.append({
                'factor': 'Sin apoyo financiero',
                'valor': 'No',
                'descripcion': 'Factor de vulnerabilidad económica'
            })
        
        if data['creditos_maximos'] < 15:
            factores.append({
                'factor': 'Carga académica muy baja',
                'valor': f"{data['creditos_maximos']} créditos",
                'descripcion': 'Menos de 15 créditos - señal de dificultad'
            })
        
        if data['edad_ingreso'] > 22:
            factores.append({
                'factor': 'Edad de ingreso elevada',
                'valor': f"{data['edad_ingreso']} años",
                'descripcion': 'Factor de riesgo adicional según literatura'
            })
        
        if data['total_periodos'] > 10:
            factores.append({
                'factor': 'Exceso de períodos cursados',
                'valor': f"{data['total_periodos']} períodos",
                'descripcion': 'Tiempo prolongado sin graduarse'
            })
    
    return factores


def generar_recomendacion(nivel_riesgo, factores, data):
    if nivel_riesgo == "ALTO":
        return (
            "INTERVENCIÓN URGENTE: (1) Contacto inmediato con el estudiante, "
            "(2) Reunión con coordinador académico esta semana, "
            "(3) Evaluar plan de nivelación y tutorías intensivas, "
            "(4) Considerar apoyo psicosocial y evaluación de becas, "
            "(5) Seguimiento semanal obligatorio durante todo el período."
        )
    elif nivel_riesgo == "MEDIO":
        return (
            "MONITOREO PREVENTIVO: (1) Contacto con el estudiante en las próximas 2 semanas, "
            "(2) Ofrecer tutorías en materias críticas, "
            "(3) Seguimiento mensual del progreso académico, "
            "(4) Evaluar necesidad de apoyo adicional (financiero, académico, psicológico), "
            "(5) Mantener canal de comunicación abierto."
        )
    else:  # BAJO
        return (
            "SEGUIMIENTO ESTÁNDAR: (1) Mantener protocolo de seguimiento semestral regular, "
            "(2) Reconocer y reforzar logros académicos, "
            "(3) Mantener motivación y sentido de pertenencia institucional, "
            "(4) Recursos de apoyo disponibles si los necesita en el futuro."
        )


# RUTAS API

@app.route('/')
def home():
    return jsonify({
        'nombre': 'SADE - Sistema de Alerta de Deserción Estudiantil',
        'version': '2.0',
        'institucion': 'Universidad del Norte',
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
        'tecnica_balanceo': 'SMOTE',
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
            'filosofia': "Prioriza detectar desertores sobre evitar falsas alarmas"
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
        
        probabilidad = pipeline.predict_proba(input_data)[0][1]
        prediccion = pipeline.predict(input_data)[0]
        
        if probabilidad < 0.30:
            nivel_riesgo = 'BAJO'
            color = '#10b981'  
        elif probabilidad < 0.60:
            nivel_riesgo = 'MEDIO'
            color = '#f59e0b'  
        else:
            nivel_riesgo = 'ALTO'
            color = '#ef4444'  
        
        factores_riesgo = identificar_factores_riesgo(data, probabilidad)
        
        recomendacion = generar_recomendacion(nivel_riesgo, factores_riesgo, data)
        
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
                'modelo': 'Naive Bayes + SMOTE',
                'version': '2.0'
            }
        }
        
        logger.info(f" Predicción: {probabilidad*100:.1f}% - {nivel_riesgo} - {len(factores_riesgo)} factores")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({
            'error': 'Error al procesar predicción',
            'detalle': str(e)
        }), 500


# SERVIDOR

if __name__ == '__main__':
    print(f"\nEstado del modelo: {' Cargado' if pipeline else ' Error'}")
    print(f"Recall (detección): {metrics.get('recall', 0)*100:.1f}%" if metrics else "N/A")
    print(f"Programas disponibles: {len(mapeo_programas)}")
    print("Servidor iniciado en http://localhost:5000")
    print("\nEndpoints disponibles:")
    print("  GET  /           - Información general del sistema")
    print("  GET  /health     - Estado del servidor")
    print("  GET  /programas  - Lista de programas académicos")
    print("  GET  /info       - Métricas del modelo")
    print("  POST /predict    - Realizar predicción de riesgo")
    
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)