
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://desercion-uninorte.onrender.com';

document.addEventListener('DOMContentLoaded', () => {
    console.log('Sistema inicializado');
    
    cargarProgramas();
    setupFormSubmit();
    verificarConexion();
});

// CARGAR API

async function cargarProgramas() {
    try {
        const response = await fetch(`${API_URL}/programas`);
        const data = await response.json();
        
        const selectPrograma = document.getElementById('programa');
        selectPrograma.innerHTML = '<option value="">Seleccionar programa...</option>';
        
        data.programas.forEach(programa => {
            const option = document.createElement('option');
            option.value = programa.codigo;
            option.textContent = programa.nombre;
            selectPrograma.appendChild(option);
        });
        
        console.log(`${data.programas.length} programas cargados`);
        
    } catch (error) {
        console.error('Error cargando programas:', error);
        const selectPrograma = document.getElementById('programa');
        selectPrograma.innerHTML = '<option value="">Error cargando programas</option>';
    }
}

// FORMULARIO

function setupFormSubmit() {
    const form = document.getElementById('prediction-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const formData = {
            edad_ingreso: parseInt(document.getElementById('edad_ingreso').value),
            sexo: document.getElementById('sexo').value,
            estrato: parseInt(document.getElementById('estrato').value),
            programa: document.getElementById('programa').value,
            promedio_historico: parseFloat(document.getElementById('promedio_historico').value),
            creditos_maximos: parseInt(document.getElementById('creditos_maximos').value),
            total_periodos: parseInt(document.getElementById('total_periodos').value),
            tasa_aprobacion_media: parseFloat(document.getElementById('tasa_aprobacion_media').value),
            rezago_final: parseFloat(document.getElementById('rezago_final').value),
            ha_estado_fuera: parseInt(document.getElementById('ha_estado_fuera').value),
            tiene_beca: parseInt(document.getElementById('tiene_beca').value),
            naturaleza_colegio: document.getElementById('naturaleza_colegio').value,
            calendario: document.getElementById('calendario').value
        };
        
        mostrarEstado('loading');
        
        // Realizar predicción
        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const resultado = await response.json();
            
            // Mostrar resultados
            mostrarResultados(resultado);
            
        } catch (error) {
            console.error('Error en predicción:', error);
            alert('Error al conectar con el servidor. Verifique que el backend esté ejecutándose.');
            mostrarEstado('form');
        }
    });
}
function mostrarEstado(estado) {
    document.getElementById('form-card').classList.add('hidden');
    document.getElementById('results-card').classList.add('hidden');
    document.getElementById('loading-state').classList.add('hidden');
    
    if (estado === 'loading') {
        document.getElementById('loading-state').classList.remove('hidden');
    } else if (estado === 'results') {
        document.getElementById('results-card').classList.remove('hidden');
    } else {
        document.getElementById('form-card').classList.remove('hidden');
    }
}

// MOSTRAR RESULTADOS

function mostrarResultados(resultado) {
    console.log('Resultado:', resultado);
    
    const { prediccion, recomendacion, factores_riesgo, perfil } = resultado;
    
    actualizarMedidor(prediccion.probabilidad);
    
    actualizarBadgeRiesgo(prediccion.nivel_riesgo);
    
    document.getElementById('risk-recommendation').textContent = recomendacion;
    
    actualizarFactoresRiesgo(factores_riesgo);
    
    actualizarPerfil(perfil);
    
    mostrarEstado('results');
    
    document.getElementById('results-card').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

// GRAFICO (GAUGE)

function actualizarMedidor(probabilidad) {
    const needle = document.getElementById('gauge-needle');
    const probabilityValue = document.getElementById('probability-value');
    
    probabilityValue.textContent = `${probabilidad.toFixed(1)}%`;
    
    const angle = -90 + (probabilidad * 1.8);
    
    needle.style.transform = `translateX(-50%) rotate(${angle}deg)`;
}

// ACTUALIZAR BADGE DE RIESGO

function actualizarBadgeRiesgo(nivel) {
    const badge = document.getElementById('risk-badge');
    
    badge.classList.remove('bajo', 'medio', 'alto');
    
    if (nivel === 'BAJO') {
        badge.classList.add('bajo');
        badge.textContent = 'RIESGO BAJO';
    } else if (nivel === 'MEDIO') {
        badge.classList.add('medio');
        badge.textContent = 'RIESGO MEDIO';
    } else {
        badge.classList.add('alto');
        badge.textContent = 'RIESGO ALTO';
    }
}

// FACTORES DE RIESGO

function actualizarFactoresRiesgo(factores) {
    const factorsList = document.getElementById('risk-factors-list');
    
    if (factores.length === 0) {
        factorsList.innerHTML = '<p class="no-factors">No se detectaron factores de riesgo críticos</p>';
    } else {
        factorsList.innerHTML = factores.map(factor => `
            <div class="factor-item">
                <div class="factor-name">${factor.factor}</div>
                <div class="factor-value">Valor: ${factor.valor}</div>
                <div class="factor-description">${factor.descripcion}</div>
            </div>
        `).join('');
    }
}

// PERFIL DEL ESTUDIANTE
function actualizarPerfil(perfil) {
    const profileGrid = document.getElementById('student-profile');
    
    profileGrid.innerHTML = `
        <div class="profile-item">
            <div class="profile-label">Edad</div>
            <div class="profile-value">${perfil.edad} años</div>
        </div>
        <div class="profile-item">
            <div class="profile-label">Promedio</div>
            <div class="profile-value">${perfil.promedio.toFixed(2)}</div>
        </div>
        <div class="profile-item">
            <div class="profile-label">Tasa Aprobación</div>
            <div class="profile-value">${perfil.tasa_aprobacion}</div>
        </div>
        <div class="profile-item">
            <div class="profile-label">Rezago</div>
            <div class="profile-value">${perfil.rezago.toFixed(1)} periodos</div>
        </div>
        <div class="profile-item">
            <div class="profile-label">Periodos Cursados</div>
            <div class="profile-value">${perfil.periodos}</div>
        </div>
        <div class="profile-item">
            <div class="profile-label">Programa</div>
            <div class="profile-value">${perfil.programa}</div>
        </div>
    `;
}


function resetForm() {
    document.getElementById('prediction-form').reset();
    mostrarEstado('form');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// VERIFICAR CONEXIÓN BACKEND

async function verificarConexion() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy' && data.modelo_cargado) {
            console.log('Conexión con backend exitosa');
            console.log('Modelo cargado correctamente');
        } else {
            console.warn('Backend conectado pero modelo no cargado');
        }
    } catch (error) {
        console.error('Error de conexión con backend:', error);
        console.log('Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:5000');
    }
}
