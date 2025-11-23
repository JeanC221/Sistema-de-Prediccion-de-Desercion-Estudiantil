/**
 * Sistema de Predicción de Deserción Estudiantil
 * JavaScript - Lógica del Frontend
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

const API_URL = 'http://localhost:5000';

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎓 Sistema de Alerta Temprana inicializado');
    
    // Cargar programas
    cargarProgramas();
    
    // Setup de tooltips
    setupTooltips();
    
    // Setup del formulario
    setupFormValidation();
    setupFormSubmit();
});

// ============================================================================
// CARGAR PROGRAMAS DESDE API
// ============================================================================

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
        
        console.log(`✓ ${data.programas.length} programas cargados`);
        
    } catch (error) {
        console.error('Error cargando programas:', error);
        const selectPrograma = document.getElementById('programa');
        selectPrograma.innerHTML = '<option value="">Error cargando programas</option>';
    }
}

// ============================================================================
// TOOLTIPS INFORMATIVOS
// ============================================================================

function setupTooltips() {
    const infoBtns = document.querySelectorAll('.info-btn');
    
    infoBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const infoId = 'info-' + btn.getAttribute('data-info');
            const tooltip = document.getElementById(infoId);
            
            // Cerrar todos los tooltips
            document.querySelectorAll('.tooltip').forEach(t => {
                if (t !== tooltip) t.classList.remove('active');
            });
            
            // Toggle tooltip actual
            tooltip.classList.toggle('active');
        });
    });
    
    // Cerrar tooltips al hacer click fuera
    document.addEventListener('click', (e) => {
        if (!e.target.classList.contains('info-btn')) {
            document.querySelectorAll('.tooltip').forEach(t => {
                t.classList.remove('active');
            });
        }
    });
}

// ============================================================================
// VALIDACIÓN DEL FORMULARIO
// ============================================================================

function setupFormValidation() {
    // Edad de ingreso (16-35)
    const edadInput = document.getElementById('edad_ingreso');
    edadInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (val < 16 || val > 35) {
            e.target.setCustomValidity('La edad debe estar entre 16 y 35 años');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    // Promedio (0.0-5.0)
    const promedioInput = document.getElementById('promedio_historico');
    promedioInput.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (val < 0 || val > 5) {
            e.target.setCustomValidity('El promedio debe estar entre 0.0 y 5.0');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    // Créditos (6-24)
    const creditosInput = document.getElementById('creditos_maximos');
    creditosInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (val < 6 || val > 24) {
            e.target.setCustomValidity('Los créditos deben estar entre 6 y 24');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    // Tasa de aprobación (0-100)
    const tasaInput = document.getElementById('tasa_aprobacion_media');
    tasaInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (val < 0 || val > 100) {
            e.target.setCustomValidity('La tasa debe estar entre 0 y 100%');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    // Rezago (0-3)
    const rezagoInput = document.getElementById('rezago_final');
    rezagoInput.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (val < 0 || val > 3) {
            e.target.setCustomValidity('El rezago debe estar entre 0 y 3 periodos');
        } else {
            e.target.setCustomValidity('');
        }
    });
    
    // Periodos (1-15)
    const periodosInput = document.getElementById('total_periodos');
    periodosInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (val < 1 || val > 15) {
            e.target.setCustomValidity('Los periodos deben estar entre 1 y 15');
        } else {
            e.target.setCustomValidity('');
        }
    });
}

// ============================================================================
// ENVÍO DEL FORMULARIO
// ============================================================================

function setupFormSubmit() {
    const form = document.getElementById('prediction-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validar formulario
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Recopilar datos
        const formData = {
            edad_ingreso: parseInt(document.getElementById('edad_ingreso').value),
            sexo: document.getElementById('sexo').value,
            estrato: parseInt(document.getElementById('estrato').value),
            programa: document.getElementById('programa').value,
            promedio_historico: parseFloat(document.getElementById('promedio_historico').value),
            creditos_maximos: parseInt(document.getElementById('creditos_maximos').value),
            total_periodos: parseInt(document.getElementById('total_periodos').value),
            tasa_aprobacion_media: parseInt(document.getElementById('tasa_aprobacion_media').value) / 100,
            rezago_final: parseFloat(document.getElementById('rezago_final').value),
            ha_estado_fuera: parseInt(document.getElementById('ha_estado_fuera').value),
            tiene_beca: parseInt(document.getElementById('tiene_beca').value),
            naturaleza_colegio: document.getElementById('naturaleza_colegio').value,
            calendario: document.getElementById('calendario').value
        };
        
        // Mostrar estado de carga
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
            mostrarError('Error al conectar con el servidor. Verifique que el backend esté ejecutándose.');
        }
    });
}

// ============================================================================
// MOSTRAR ESTADOS
// ============================================================================

function mostrarEstado(estado) {
    // Ocultar todos
    document.getElementById('initial-state').classList.add('hidden');
    document.getElementById('results-card').classList.add('hidden');
    document.getElementById('loading-state').classList.add('hidden');
    document.getElementById('error-state').classList.add('hidden');
    
    // Mostrar el apropiado
    if (estado === 'loading') {
        document.getElementById('loading-state').classList.remove('hidden');
    } else if (estado === 'results') {
        document.getElementById('results-card').classList.remove('hidden');
    } else if (estado === 'error') {
        document.getElementById('error-state').classList.remove('hidden');
    } else {
        document.getElementById('initial-state').classList.remove('hidden');
    }
}

function mostrarError(mensaje) {
    document.getElementById('error-message').textContent = mensaje;
    mostrarEstado('error');
}

// ============================================================================
// MOSTRAR RESULTADOS
// ============================================================================

function mostrarResultados(resultado) {
    console.log('Resultado:', resultado);
    
    const { prediccion, recomendacion, factores_riesgo, perfil } = resultado;
    
    // Actualizar medidor (gauge)
    actualizarMedidor(prediccion.probabilidad);
    
    // Actualizar badge de riesgo
    actualizarBadgeRiesgo(prediccion.nivel_riesgo, prediccion.color);
    
    // Actualizar recomendación
    document.getElementById('risk-recommendation').textContent = recomendacion;
    
    // Actualizar factores de riesgo
    actualizarFactoresRiesgo(factores_riesgo);
    
    // Actualizar perfil del estudiante
    actualizarPerfil(perfil);
    
    // Mostrar resultados
    mostrarEstado('results');
    
    // Scroll suave a resultados
    document.getElementById('results-card').scrollIntoView({ 
        behavior: 'smooth',
        block: 'nearest'
    });
}

// ============================================================================
// ACTUALIZAR MEDIDOR (GAUGE)
// ============================================================================

function actualizarMedidor(probabilidad) {
    const needle = document.getElementById('gauge-needle');
    const probabilityValue = document.getElementById('probability-value');
    
    // Actualizar valor numérico
    probabilityValue.textContent = `${probabilidad.toFixed(1)}%`;
    
    // Calcular ángulo de la aguja (-90° a 90°)
    // 0% = -90°, 50% = 0°, 100% = 90°
    const angle = -90 + (probabilidad * 1.8);
    
    // Animar la aguja
    needle.style.transform = `rotate(${angle}deg)`;
    
    // Cambiar color según riesgo
    if (probabilidad < 30) {
        probabilityValue.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    } else if (probabilidad < 60) {
        probabilityValue.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    } else {
        probabilityValue.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    }
    probabilityValue.style.webkitBackgroundClip = 'text';
    probabilityValue.style.webkitTextFillColor = 'transparent';
}

// ============================================================================
// ACTUALIZAR BADGE DE RIESGO
// ============================================================================

function actualizarBadgeRiesgo(nivel, color) {
    const riskStatus = document.getElementById('risk-status');
    const badge = riskStatus.querySelector('.risk-badge');
    
    // Determinar icono y clase
    let icono, clase;
    if (nivel === 'BAJO') {
        icono = '🟢';
        clase = 'bajo';
    } else if (nivel === 'MEDIO') {
        icono = '🟡';
        clase = 'medio';
    } else {
        icono = '🔴';
        clase = 'alto';
    }
    
    // Actualizar badge
    badge.className = `risk-badge ${clase}`;
    badge.innerHTML = `
        <span class="risk-icon">${icono}</span>
        <span class="risk-text">RIESGO ${nivel}</span>
    `;
}

// ============================================================================
// ACTUALIZAR FACTORES DE RIESGO
// ============================================================================

function actualizarFactoresRiesgo(factores) {
    const factorsList = document.getElementById('risk-factors-list');
    
    if (factores.length === 0) {
        factorsList.innerHTML = '<p class="no-factors">✓ No se detectaron factores de riesgo críticos</p>';
    } else {
        factorsList.innerHTML = factores.map(factor => `
            <div class="factor-item">
                <div class="factor-name">⚠️ ${factor.factor}</div>
                <div class="factor-value">Valor: ${factor.valor}</div>
                <div class="factor-description">${factor.descripcion}</div>
            </div>
        `).join('');
    }
}

// ============================================================================
// ACTUALIZAR PERFIL DEL ESTUDIANTE
// ============================================================================

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

// ============================================================================
// RESET DEL FORMULARIO
// ============================================================================

function resetForm() {
    document.getElementById('prediction-form').reset();
    mostrarEstado('initial');
}

// ============================================================================
// VERIFICAR CONEXIÓN CON BACKEND
// ============================================================================

async function verificarConexion() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy' && data.modelo_cargado) {
            console.log('✓ Conexión con backend exitosa');
            console.log('✓ Modelo cargado correctamente');
        } else {
            console.warn('⚠️ Backend conectado pero modelo no cargado');
        }
    } catch (error) {
        console.error('❌ Error de conexión con backend:', error);
        console.log('💡 Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:5000');
    }
}

// Verificar conexión al cargar
setTimeout(verificarConexion, 1000);
