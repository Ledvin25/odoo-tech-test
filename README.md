# Sale Dimension Quantity

Este módulo permite calcular automáticamente la **cantidad de venta** (`product_uom_qty`) a partir de **Largo × Ancho × Alto** en las líneas de pedido de ventas en Odoo 18.  
Además, añade estos campos en la vista y en el **reporte PDF** de cotización/pedido.

> **📂 Nota:** Las capturas de pantalla y PDFs solicitadas están incluidos en la raíz de este repositorio.

---

## 📦 Información General
- **Nombre del módulo:** `sale_dimension_qty`
- **Versión:** Odoo 18
- **Licencia:** LGPL-3
- **Dependencias:** `sale`

---

## ⚙️ Funcionalidad
- Nuevos campos en `sale.order.line`:
  - `x_length` → Largo
  - `x_width` → Ancho
  - `x_height` → Alto
  - `x_dimension_qty` → Diagnóstico del cálculo
- La **cantidad de producto** (`product_uom_qty`) se calcula como:
  ```
  product_uom_qty = x_length * x_width * x_height
  ```
- Se recalcula en **onchange**, **create** y **write** (cubriendo casos manuales y de importación).
- En las vistas:
  - `product_uom_qty` queda en **solo lectura**.
  - Se muestran los tres campos de dimensiones.
- En el **PDF (QWeb)**:
  - Se reemplaza la columna de **Quantity** por **Largo, Ancho, Alto**.
  - Totales permanecen consistentes.
- **UX extra:** si Largo, Ancho y Alto están en 0, se muestra un **aviso** indicando que el subtotal será 0.

> Por defecto, las dimensiones se asumen en **metros**.

---

## 📂 Estructura del módulo
```
sale_dimension_qty/
├─ __init__.py
├─ __manifest__.py
├─ models/
│  └─ sale_order_line.py
├─ views/
│  └─ sale_order_views.xml
├─ report/
│  └─ sale_report.xml
└─ tests/
   ├─ __init__.py
   └─ test_sale_dimension_qty.py
```

---

## 🔧 Instalación

### Opción 1: Con Docker Compose (Recomendado)
Si tienes Docker Compose, simplemente ejecuta:
```bash
docker compose up --build -d
```
Esto montará automáticamente el entorno completo con Odoo 18 + PostgreSQL y el módulo `sale_dimension_qty` ya disponible para activar.

### Opción 2: Instalación manual
1. **Usar el ZIP incluido** en este repositorio (ya viene listo)
2. **Pegar el ZIP** directamente en tu carpeta de addons de Odoo
3. **O cargar desde la interfaz web**:
   - Ir a Apps → Upload
   - Seleccionar el archivo ZIP incluido en el repo
   - Hacer clic en Install

### Verificación
- **Usuario:** `admin` (por defecto)
- **Contraseña:** `admin` (por defecto)
- **URL:** http://localhost:8069

---

## 🚀 Uso
1. Crear una **Cotización**.
2. En las líneas, ingresar **Largo, Ancho y Alto**.
3. La **Cantidad** se calculará automáticamente.
4. Al imprimir el **PDF de cotización**, se mostrarán las columnas de **Largo, Ancho y Alto** en lugar de **Quantity**.

---

## ✅ Pruebas automáticas
Las pruebas se corren en **HTTP con puerto alternativo** y sin workers:

```bash
odoo -c /etc/odoo/odoo.conf -d <DB>   -u sale_dimension_qty   --test-enable   --test-tags="post_install,-at_install"   --workers=0 --stop-after-init   --http-port=8070
```
> **Nota:** La base de datos creada por defecto en el entorno Docker Compose se llama `odoo`.

Pruebas incluidas:
- Verificar que **Cantidad = Largo × Ancho × Alto**.
- Verificar que el **Subtotal** se actualiza con los cambios de dimensiones.
- Validar que las dimensiones no pueden ser negativas.

---

## 📸 Entregables recomendados
- **Vista tree/form** mostrando dimensiones y cantidad en solo lectura.
- **PDF de cotización** con columnas Largo, Ancho y Alto.
- **Aviso** cuando alguna línea tiene dimensiones en 0.

---

## 📌 Notas de diseño
- Se asume **metros** como unidad estándar.
- Compatible con **productos consumibles** y **servicios**.
- El aviso usa `role="status"` para cumplir con las normas de accesibilidad ARIA.

---

## 📝 Licencia
LGPL-3
