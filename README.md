# 🐜 Hormigah - Control de Gastos Hormiga

Una aplicación web personal para **controlar esos pequeños gastos diarios** que pasan desapercibidos pero que al final del año suman cantidades importantes.

## 🎯 Concepto

**Objetivo:** Crear conciencia financiera mediante visualización impactante del dinero que "se escapa" sin darte cuenta, mostrando proyecciones anuales que generen el momento *"😱 ¡No sabía que gastaba tanto!"*

**Gastos que incluye:** ☕ Café, 🍕 Delivery, 🚗 Taxis innecesarios, 🛍️ Compras por impulso, 📱 Apps no usadas, etc.

## 🔧 Stack Tecnológico

- **Backend:** Django 5.2.3 + SQLite
- **Frontend:** Django Templates + Tailwind CSS + Chart.js
- **Gráficas:** Chart.js (gráficos de dona y líneas)
- **Responsive:** Diseño móvil-first con navegación hamburguesa

## 📊 Estado del Proyecto

### ✅ **COMPLETADO**

#### 🏗️ **Setup Inicial**
- [x] Proyecto Django configurado
- [x] Estructura de apps (`core`, `expenses`)
- [x] Entorno virtual configurado
- [x] `.gitignore` completo para Django
- [x] Configuración de archivos corregida

#### 🗃️ **Modelos de Datos**
- [x] Modelo `Category` (categorías de gastos)
- [x] Modelo `Expense` (gastos individuales)
- [x] Relaciones ForeignKey configuradas
- [x] Migraciones creadas y aplicadas
- [x] Base de datos SQLite funcionando

#### 🔧 **Backend Completo**
- [x] Django Admin configurado
- [x] Categorías iniciales creadas (Café, Delivery, Transporte, etc.)
- [x] Vistas funcionales (dashboard, formularios, listas)
- [x] URLs configuradas
- [x] Formularios Django con validación
- [x] Sistema de autenticación (login/logout)

#### 🎨 **Frontend Completo**
- [x] Estructura de templates (`base.html`)
- [x] Tailwind CSS configurado (CDN)
- [x] Chart.js integrado (CDN)
- [x] Dashboard principal con gráficas interactivas
- [x] Formulario para agregar gastos
- [x] Lista completa de gastos
- [x] Navegación móvil responsive

#### 📈 **Funcionalidades Avanzadas**
- [x] CRUD completo de gastos
- [x] Gráfico de dona - gastos por categoría
- [x] Gráfico de líneas - tendencia temporal
- [x] Métricas en tiempo real (totales, promedios)
- [x] Estados vacíos con mensajes informativos
- [x] Navegación hamburguesa para móviles
- [x] Menú de usuario con dropdown

#### 📱 **Responsive Design**
- [x] Dashboard adaptable a móviles
- [x] Navegación hamburguesa funcional
- [x] Gráficas responsive
- [x] Tablas con scroll horizontal
- [x] Formularios optimizados para touch

#### 📝 **Control de Versiones**
- [x] Repositorio Git con commits organizados
- [x] Rama `feature/web-interface` completada
- [x] Commits con conventional commits

---

### 🚧 **EN PROGRESO**

*Actualmente no hay tareas en progreso*

---

### ❌ **PENDIENTE**

#### 📈 **Funcionalidades Avanzadas**
- [ ] Filtros por fecha/categoría
- [ ] Proyecciones anuales automáticas
- [ ] Alertas de gastos excesivos
- [ ] Exportación de datos (CSV/PDF)
- [ ] Comparativas mensuales

#### 🎨 **Mejoras de UX**
- [ ] Modo oscuro
- [ ] Animaciones de transición
- [ ] Notificaciones push
- [ ] Shortcuts de teclado

#### 🚀 **Deploy y Producción**
- [ ] Configuración para producción
- [ ] Variables de entorno
- [ ] Configuración de archivos estáticos
- [ ] Base de datos PostgreSQL
- [ ] Deploy en servidor

## 🗂️ Estructura del Proyecto

```
hormigah/
├── apps/
│   ├── core/                    # ✅ Utilidades base y templates compartidos
│   │   ├── templates/
│   │   │   ├── base.html       # ✅ Template base con Tailwind + Chart.js
│   │   │   ├── core/includes/  # ✅ Header y footer compartidos
│   │   │   └── registration/   # ✅ Templates de autenticación
│   │   └── ...
│   └── expenses/               # ✅ App principal completa
│       ├── models.py          # ✅ Category y Expense
│       ├── views.py           # ✅ Dashboard, formularios, listas
│       ├── forms.py           # ✅ ExpenseForm con validación
│       ├── urls.py            # ✅ URLs configuradas
│       ├── admin.py           # ✅ Admin interface
│       ├── templates/expenses/ # ✅ Templates específicos
│       └── migrations/        # ✅ Migraciones aplicadas
├── config/                    # ✅ Configuración Django
├── manage.py                  # ✅ Script de gestión
├── requirements.txt           # ❌ Por crear
└── README.md                  # ✅ Este archivo actualizado
```

## 🏃‍♂️ Instalación y Uso

### Requisitos
- Python 3.8+
- Django 5.2.3

### Setup Local
```bash
# Clonar repositorio
git clone [URL_REPO]
cd hormigah

# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install django

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Correr servidor
python manage.py runserver
```

### Acceso
- **Aplicación:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

## 🎨 Características de la Interfaz

### 📊 **Dashboard Principal**
- **Métricas coloridas:** Total mensual, total de gastos, promedio diario
- **Gráfico de dona:** Distribución por categorías con colores personalizados
- **Gráfico de líneas:** Tendencia de gastos en los últimos 30 días
- **Gastos recientes:** Tabla con los últimos 10 gastos

### 📱 **Navegación Móvil**
- **Menú hamburguesa:** Acceso completo en dispositivos móviles
- **Responsive design:** Se adapta a cualquier tamaño de pantalla
- **Touch-friendly:** Botones y enlaces optimizados para tocar

### 🎯 **Formularios**
- **Validación en tiempo real:** Feedback inmediato al usuario
- **Campos inteligentes:** Fecha por defecto, categorías dinámicas
- **Diseño limpio:** Interfaz moderna con Tailwind CSS

## 📊 Progreso General

**Completado:** 85%
- ✅ Backend completo
- ✅ Frontend con gráficas
- ✅ Responsive design
- ✅ Funcionalidades core

**Próximo Milestone:** Deploy en producción (100%)

## 🎯 Próximos Pasos (Prioridad)

1. **Crear requirements.txt** - Para dependencias
2. **Filtros avanzados** - Por fecha y categoría
3. **Proyecciones anuales** - Cálculos automáticos
4. **Deploy en producción** - Servidor real
5. **Optimizaciones de rendimiento** - Caché y queries

## 📝 Notas de Desarrollo

- **Commits:** Conventional commits en español
- **Comentarios:** Solo cuando aporten valor real
- **Estilo:** Código en inglés, comentarios en español
- **Autenticación:** Solo login/logout - usuarios creados vía admin
- **Responsive:** Mobile-first approach con Tailwind CSS
- **Gráficas:** Chart.js con configuración responsive

## 🏆 Funcionalidades Destacadas

### 🍩 **Gráficas Interactivas**
- Gráfico de dona con porcentajes y tooltips
- Gráfico de líneas con animaciones suaves
- Colores dinámicos basados en categorías
- Responsive y touch-friendly

### 📱 **Experiencia Móvil**
- Navegación hamburguesa intuitiva
- Gráficas adaptables a pantallas pequeñas
- Tablas con scroll horizontal
- Menús desplegables optimizados

### 🎨 **Diseño Moderno**
- Tailwind CSS para estilos consistentes
- Gradientes coloridos en métricas
- Iconos emoji para mejor UX
- Estados vacíos informativos

---

**Última actualización:** Junio 2025
**Estado:** 🚀 Interfaz web completa - Lista para uso diario 