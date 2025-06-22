# 🐜 Hormigah - Control de Gastos Hormiga

Una aplicación web personal para **controlar esos pequeños gastos diarios** que pasan desapercibidos pero que al final del año suman cantidades importantes.

## 🎯 Concepto

**Objetivo:** Crear conciencia financiera mediante visualización impactante del dinero que "se escapa" sin darte cuenta, mostrando proyecciones anuales que generen el momento *"😱 ¡No sabía que gastaba tanto!"*

**Gastos que incluye:** ☕ Café, 🍕 Delivery, 🚗 Taxis innecesarios, 🛍️ Compras por impulso, 📱 Apps no usadas, etc.

## 🔧 Stack Tecnológico

- **Backend:** Django 5.x + SQLite
- **Frontend:** Django Templates + Tailwind CSS + HTMX + Alpine.js + Chart.js
- **Deploy:** Via CDN (fase MVP)

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

#### 📝 **Control de Versiones**
- [x] Repositorio Git inicializado
- [x] Primer commit con modelos

---

### 🚧 **EN PROGRESO**

*Actualmente no hay tareas en progreso*

---

### ❌ **PENDIENTE**

#### 🔧 **Backend**
- [ ] Configurar Django Admin
- [ ] Crear categorías iniciales (fixtures)
- [ ] Crear vistas básicas (dashboard, formularios)
- [ ] Configurar URLs
- [ ] Crear formularios Django

#### 🎨 **Frontend**
- [ ] Estructura de templates (`base.html`)
- [ ] Configurar Tailwind CSS (CDN)
- [ ] Configurar HTMX (CDN)
- [ ] Dashboard principal
- [ ] Formulario para agregar gastos
- [ ] Página de estadísticas

#### 📈 **Funcionalidades**
- [ ] CRUD completo de gastos
- [ ] Filtros por fecha/categoría
- [ ] Gráficos con Chart.js
- [ ] Proyecciones anuales
- [ ] Cálculo de métricas
- [ ] Sistema de usuarios

#### 🚀 **Deploy**
- [ ] Configuración para producción
- [ ] Variables de entorno
- [ ] Configuración de archivos estáticos

## 🗂️ Estructura del Proyecto

```
hormigah/
├── apps/
│   ├── core/           # Utilidades base
│   └── expenses/       # ✅ App principal (modelos listos)
├── config/             # ✅ Configuración Django
├── templates/          # ❌ Por crear
├── static/             # ❌ Por crear
├── requirements.txt    # ❌ Por crear
└── README.md           # ✅ Este archivo
```

## 🏃‍♂️ Instalación y Uso

### Requisitos
- Python 3.8+
- Django 5.x

### Setup Local
```bash
# Clonar repositorio
git clone [URL_REPO]
cd hormigah

# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias (cuando esté requirements.txt)
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Correr servidor
python manage.py runserver
```

## 📊 Progreso General

**Completado:** 15%
- ✅ Setup y modelos base

**Próximo Milestone:** Dashboard básico funcionando (30%)

## 🎯 Próximos Pasos (Prioridad)

1. **Configurar Django Admin** - Para poder gestionar datos
2. **Crear categorías iniciales** - Café, delivery, transporte, etc.
3. **Template base** - Layout principal con Tailwind
4. **Vista dashboard** - Página principal básica
5. **Formulario agregar gasto** - Funcionalidad core

## 📝 Notas de Desarrollo

- **Commits:** Usar conventional commits en español
- **Comentarios:** Solo cuando aporten valor real
- **Estilo:** Código en inglés, comentarios en español

---

**Última actualización:** Enero 2025
**Estado:** 🚧 En desarrollo activo 