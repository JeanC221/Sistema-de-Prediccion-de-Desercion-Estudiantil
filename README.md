#  Sistema de Predicción de Deserción Estudiantil

Aplicación web completa para predicción temprana de deserción estudiantil usando Naive Bayes + SMOTE.

##  Características

-  **Interfaz moderna y profesional** con diseño responsive
-  **Medidor visual de riesgo** estilo velocímetro con aguja animada
-  **Dashboard interactivo** con análisis detallado
-  **Validación completa** de todos los campos del formulario
-  **Tooltips informativos** para cada variable
-  **API REST** con Flask para comunicación frontend-backend
-  **Responsive design** compatible con móviles y tablets

##  Instalación

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

##  Ejecución

### Paso 1: Iniciar el Backend

En la carpeta `backend/`, ejecuta:

```bash
python app.py
```

### Paso 2: Abrir el Frontend

Abre el archivo `frontend/index.html` en tu navegador web:

- **Opción 1:** Doble clic en `index.html`
- **Opción 2:** Arrastrar el archivo al navegador
- **Opción 3 (VS Code):** Click derecho → "Open with Live Server"

La aplicación debería abrirse en tu navegador.

##  Uso de la Aplicación

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

Haz clic en el ícono  junto a cada campo para ver información detallada sobre qué significa esa variable.

### 3. Realizar Predicción

Haz clic en el botón **" Realizar Predicción"**.

### 4. Interpretar Resultados

La aplicación mostrará:

**Medidor de Riesgo:**
- Aguja que indica el nivel de probabilidad (0-100%)
- Zonas coloreadas: Verde (bajo), Amarillo (medio), Rojo (alto)

**Nivel de Riesgo:**
-  RIESGO BAJO (< 30%)
-  RIESGO MEDIO (30-60%)
-  RIESGO ALTO (> 60%)

**Factores de Riesgo:**
- Lista de factores detectados que aumentan el riesgo

**Perfil del Estudiante:**
- Resumen de las características ingresadas

##  Ejemplos de Prueba

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


##  Métricas del Modelo

- **Modelo:** Naive Bayes Categórico
- **Técnica de Balanceo:** SMOTE (sampling_strategy=0.43)
- **Threshold:** 0.35
- **Recall:** 62.85% (detecta 63 de cada 100 desertores)
- **Precision:** 21.00% (1 de cada 5 alertas es correcta)
- **F1-Score:** 31.49%
- **ROC-AUC:** 73.60%

Para acceder desde otros dispositivos en tu red local:

```python
# En app.py, cambiar:
app.run(debug=False, host='0.0.0.0', port=5000)
```

Luego accede desde `http://TU_IP:5000`

