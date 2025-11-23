# 🎓 Sistema de Predicción de Deserción Estudiantil

Aplicación web completa para predicción temprana de deserción estudiantil usando Naive Bayes + SMOTE.

## 📋 Características

- ✨ **Interfaz moderna y profesional** con diseño responsive
- 🎯 **Medidor visual de riesgo** estilo velocímetro con aguja animada
- 📊 **Dashboard interactivo** con análisis detallado
- ✅ **Validación completa** de todos los campos del formulario
- ℹ️ **Tooltips informativos** para cada variable
- 🔄 **API REST** con Flask para comunicación frontend-backend
- 📱 **Responsive design** compatible con móviles y tablets

## 🏗️ Estructura del Proyecto

```
desercion-detector/
├── backend/
│   ├── app.py                 # API Flask
│   ├── model_results.pkl      # Modelo entrenado
│   ├── mapeos_nombres.pkl     # Mapeos de programas/escuelas
│   └── requirements.txt       # Dependencias Python
├── frontend/
│   ├── index.html            # Página principal
│   ├── css/
│   │   └── styles.css        # Estilos CSS
│   └── js/
│       └── main.js           # Lógica JavaScript
└── README.md
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Paso 1: Clonar/Descargar el Proyecto

Descarga la carpeta `desercion-detector` completa en tu máquina.

### Paso 2: Copiar los Archivos del Modelo

**IMPORTANTE:** Debes copiar los siguientes archivos desde tu Google Colab a la carpeta `backend/`:

1. `model_results.pkl` - El modelo entrenado
2. `mapeos_nombres.pkl` - Los mapeos de programas y escuelas

```bash
# En la carpeta backend/ deben estar estos archivos:
backend/
├── app.py
├── model_results.pkl          ← COPIAR DESDE COLAB
├── mapeos_nombres.pkl         ← COPIAR DESDE COLAB
└── requirements.txt
```

### Paso 3: Instalar Dependencias del Backend

Abre una terminal en la carpeta `backend/` y ejecuta:

```bash
cd backend
pip install -r requirements.txt
```

**Nota para Windows:** Si tienes problemas, prueba con:
```bash
pip install --break-system-packages -r requirements.txt
```

**Dependencias instaladas:**
- Flask 3.0.0
- Flask-CORS 4.0.0
- pandas 2.1.4
- numpy 1.26.2
- scikit-learn 1.3.2
- imbalanced-learn 0.11.0
- gunicorn 21.2.0

## ▶️ Ejecución

### Paso 1: Iniciar el Backend

En la carpeta `backend/`, ejecuta:

```bash
python app.py
```

Deberías ver algo como:

```
======================================================================
🎓 SERVIDOR DE PREDICCIÓN DE DESERCIÓN ESTUDIANTIL
======================================================================
Estado del modelo: ✓ Cargado
Threshold: 0.35
Recall: 62.9%
======================================================================

🚀 Servidor iniciado en http://localhost:5000
📝 Endpoints disponibles:
  GET  / - Información general
  GET  /health - Estado del servidor
  GET  /programas - Lista de programas
  GET  /info - Información del modelo
  POST /predict - Realizar predicción

⏸️  Presiona Ctrl+C para detener
```

**⚠️ NO CIERRES ESTA TERMINAL** - El servidor debe estar corriendo.

### Paso 2: Abrir el Frontend

Abre el archivo `frontend/index.html` en tu navegador web:

- **Opción 1:** Doble clic en `index.html`
- **Opción 2:** Arrastrar el archivo al navegador
- **Opción 3 (VS Code):** Click derecho → "Open with Live Server"

La aplicación debería abrirse en tu navegador.

## 📖 Uso de la Aplicación

### 1. Completar el Formulario

Llena todos los campos del formulario con los datos del estudiante:

**Información Demográfica:**
- Edad de Ingreso (16-35 años)
- Sexo (M/F)
- Estrato Socioeconómico (1-6)

**Información Académica:**
- Programa Académico (seleccionar de la lista)
- Promedio Acumulado (0.0-5.0)
- Créditos Máximos (6-24)
- Total de Periodos (1-15)
- Tasa de Aprobación (0-100%)
- Rezago Académico (0.0-3.0)
- Ha Estado Fuera (Sí/No)

**Información Socioeconómica:**
- Tiene Beca (Sí/No)
- Tipo de Colegio (Privado/Público/Otro)
- Calendario (A/B/Otro)

### 2. Tooltips Informativos

Haz clic en el ícono ℹ️ junto a cada campo para ver información detallada sobre qué significa esa variable.

### 3. Realizar Predicción

Haz clic en el botón **"🎯 Realizar Predicción"**.

### 4. Interpretar Resultados

La aplicación mostrará:

**Medidor de Riesgo:**
- Aguja que indica el nivel de probabilidad (0-100%)
- Zonas coloreadas: Verde (bajo), Amarillo (medio), Rojo (alto)

**Nivel de Riesgo:**
- 🟢 RIESGO BAJO (< 30%)
- 🟡 RIESGO MEDIO (30-60%)
- 🔴 RIESGO ALTO (> 60%)

**Factores de Riesgo:**
- Lista de factores detectados que aumentan el riesgo

**Perfil del Estudiante:**
- Resumen de las características ingresadas

## 🧪 Ejemplos de Prueba

### Estudiante de Bajo Riesgo 🟢

```
Edad: 18
Sexo: Femenino
Estrato: 4
Programa: Ingeniería Sistemas
Promedio: 4.3
Créditos: 18
Periodos: 3
Tasa Aprobación: 95%
Rezago: 0.0
Ha Estado Fuera: No
Tiene Beca: Sí
Tipo Colegio: Privado
Calendario: A

Resultado esperado: 8-15% probabilidad, RIESGO BAJO
```

### Estudiante de Riesgo Medio 🟡

```
Edad: 20
Sexo: Masculino
Estrato: 3
Programa: Derecho
Promedio: 3.3
Créditos: 18
Periodos: 4
Tasa Aprobación: 75%
Rezago: 0.8
Ha Estado Fuera: No
Tiene Beca: No
Tipo Colegio: Público
Calendario: A

Resultado esperado: 35-50% probabilidad, RIESGO MEDIO
```

### Estudiante de Alto Riesgo 🔴

```
Edad: 25
Sexo: Masculino
Estrato: 2
Programa: Medicina
Promedio: 2.2
Créditos: 15
Periodos: 7
Tasa Aprobación: 50%
Rezago: 2.5
Ha Estado Fuera: Sí
Tiene Beca: No
Tipo Colegio: Público
Calendario: B

Resultado esperado: 60-75% probabilidad, RIESGO ALTO
```

## 🐛 Solución de Problemas

### Error: "Cannot connect to backend"

**Problema:** El frontend no puede conectarse al servidor Flask.

**Solución:**
1. Verifica que el servidor esté corriendo (debes ver el mensaje de inicio)
2. Asegúrate de que esté en `http://localhost:5000`
3. Revisa la consola del navegador (F12) para ver errores

### Error: "Modelo no cargado"

**Problema:** Los archivos `.pkl` no están en la carpeta correcta.

**Solución:**
1. Verifica que `model_results.pkl` y `mapeos_nombres.pkl` estén en `backend/`
2. Reinicia el servidor Flask
3. Revisa el output del servidor para ver si hay errores al cargar

### Error: "ModuleNotFoundError"

**Problema:** Faltan dependencias de Python.

**Solución:**
```bash
cd backend
pip install -r requirements.txt
```

### La página se ve rota (sin estilos)

**Problema:** Los archivos CSS/JS no se cargan correctamente.

**Solución:**
1. Verifica que la estructura de carpetas sea correcta
2. Asegúrate de que `css/styles.css` y `js/main.js` existan
3. Abre la consola del navegador (F12) y revisa errores

### El select de programas está vacío

**Problema:** La API no está devolviendo los programas.

**Solución:**
1. Verifica que `mapeos_nombres.pkl` esté cargado
2. Prueba acceder a `http://localhost:5000/programas` en el navegador
3. Revisa los logs del servidor Flask

## 📊 API Endpoints

### GET /

Información general de la API

```json
{
  "nombre": "API de Predicción de Deserción Estudiantil",
  "version": "1.0",
  "estado": "activo"
}
```

### GET /health

Estado del servidor

```json
{
  "status": "healthy",
  "modelo_cargado": true,
  "mapeos_cargados": true
}
```

### GET /programas

Lista de programas disponibles

```json
{
  "programas": [
    {
      "codigo": "PINGSISTEMAS",
      "nombre": "Ingeniería Sistemas Y Computac"
    },
    ...
  ]
}
```

### GET /info

Información del modelo

```json
{
  "modelo": "Naive Bayes Categórico",
  "threshold": 0.35,
  "metricas": {
    "recall": "62.85%",
    "precision": "21.00%",
    ...
  }
}
```

### POST /predict

Realizar predicción

**Request Body:**
```json
{
  "edad_ingreso": 20,
  "sexo": "M",
  "estrato": 3,
  "programa": "PINGSISTEMAS",
  "promedio_historico": 3.5,
  "creditos_maximos": 18,
  "total_periodos": 4,
  "tasa_aprobacion_media": 0.85,
  "rezago_final": 0.5,
  "ha_estado_fuera": 0,
  "tiene_beca": 1,
  "naturaleza_colegio": "PRIVADO",
  "calendario": "A"
}
```

**Response:**
```json
{
  "prediccion": {
    "desertor": false,
    "probabilidad": 25.3,
    "nivel_riesgo": "BAJO",
    "color": "#10b981"
  },
  "recomendacion": "Seguimiento estándar...",
  "factores_riesgo": [...],
  "perfil": {...}
}
```

## 🎯 Métricas del Modelo

- **Modelo:** Naive Bayes Categórico
- **Técnica de Balanceo:** SMOTE (sampling_strategy=0.43)
- **Threshold:** 0.35
- **Recall:** 62.85% (detecta 63 de cada 100 desertores)
- **Precision:** 21.00% (1 de cada 5 alertas es correcta)
- **F1-Score:** 31.49%
- **ROC-AUC:** 73.60%

## 🚢 Deployment (Opcional)

### Opción 1: Heroku

```bash
# En la carpeta backend/
echo "web: gunicorn app:app" > Procfile
git init
git add .
git commit -m "Initial commit"
heroku create nombre-app
git push heroku master
```

### Opción 2: Render

1. Sube el código a GitHub
2. Conecta con Render
3. Configura como "Web Service"
4. Comando de inicio: `gunicorn app:app`

### Opción 3: Local Network

Para acceder desde otros dispositivos en tu red local:

```python
# En app.py, cambiar:
app.run(debug=False, host='0.0.0.0', port=5000)
```

Luego accede desde `http://TU_IP:5000`

## 📝 Notas para la Defensa

1. **Demostrar con casos reales:** Usa los ejemplos de prueba
2. **Explicar el medidor:** Muestra cómo la aguja se mueve según riesgo
3. **Mostrar factores:** Destaca que el sistema identifica causas específicas
4. **Enfatizar usabilidad:** Tooltips, validaciones, diseño intuitivo
5. **Mencionar escalabilidad:** API REST lista para integración

## 🤝 Créditos

Desarrollado para Tesis de Grado - Sistema de Alerta Temprana

---

**¿Problemas? Revisa la sección de Solución de Problemas o contacta al desarrollador.**
