# Landing Page B2B — Grupo Acrilan S.A.S. (Textiles Acrilán S.A.S.)

Página web y landing page institucional B2B para **Grupo Acrilan S.A.S.**, líder en manufactura de dotaciones empresariales e indumentaria en Cali, Colombia (desde 1983).

Diseño y tipografía alineados con la identidad visual oficial del portal **[www.grupoacrilan.com](https://www.grupoacrilan.com/es)**.

---

## 📁 Estructura del Proyecto

```text
ACRILAN DOTACIONES/
├── index.html                     # Landing page completa, moderna y responsiva
├── README.md                      # Documentación técnica y comercial
└── assets/
    ├── logo.jpg                   # Isotipo / Logotipo oficial de Grupo Acrilan
    ├── hero-banner-acrilan.jpg    # Banner principal 2K full-width (16:9 widescreen)
    └── catalogo_acrilan.pdf       # Catálogo institucional completo (23 páginas)
```

---

## 🎨 Tipografía y Estilo Oficial Grupo Acrilan

Se actualizó la tipografía global del sitio para homologarla con la presencia digital oficial de Grupo Acrilan:
- **Titulares, Botones, Menús y Etiquetas:** **Montserrat** (`weights: 400, 500, 600, 700, 800`) — Tipografía geométrica, moderna, sobria e institucional.
- **Cuerpo de texto, Fichas y Tablas:** **Poppins** (`weights: 300, 400, 500, 600`) — Lectura fluida, limpia y de alta legibilidad en pantallas retina y móviles.
- **Paleta Institucional:**
  - *Verde Azulado Acrilan:* `#1f6f68` (Acrilan Signature Teal) y `#e6f4f2` (Light Teal).
  - *Azul Eléctrico Corporativo:* `#0f62fe` y `#0043ce`.
  - *Bases Neutras:* `#f8fafc`, `#f1f5f9` y blanco puro `#ffffff`.

---

## 🎨 Arquitectura Visual de Secciones y Divisores (Línea Oficial Grupo Acrilan)

Se rediseñó la estructura espacial y cromática de la página para eliminar la apariencia plana y dotarla de un ritmo visual dinámico, con transiciones nítidas y elegantes entre cada capítulo:

- **Contenedores de Ancho Completo (`main-flow` + `section-block`):** Cada sección se expande al 100% del ancho de la pantalla con fondos alternados que definen con precisión las fronteras temáticas.
- **Transición Angular SVG a Sección Industrial Oscura (`#matriz`):**
  - Se implementó un divisor diagonal geométrico en SVG (`polygon points="0,60 1440,0 1440,60"`) que introduce la sección de **Capacidades de Planta e Integración Vertical** con un impactante tema *Industrial Dark Slate* (`#0b1120`), acorde a la tecnología de punta de la fábrica de Acrilan (31 tejedoras circulares, tintorería y PTAR).
  - Un segundo divisor diagonal inverso devuelve la lectura al fondo claro para el protocolo de muestras.
- **Franjas Tricolor Institucionales:** Barras superiores de acento de 4px que combinan los colores del isotipo de Grupo Acrilan (Verde Acrilán `#1f6f68`, Azul Eléctrico `#0f62fe` y Ámbar `#f59e0b`).
- **Insignias Numeradas de Sección (`section-badge-pill`):** Cada sección cuenta con un identificador corporativo con índice (`01 / CATÁLOGO`, `02 / INTEGRACIÓN VERTICAL`, `03 / PROTOCOLO DE AUDITORÍA`, `04 / ESG`, `05 / SIMULADOR`, `06 / CONTACTO`).
- **Fondos Alternados por Contenido:**
  - *Hero:* Blanco pulcro con tarjetas institucionales.
  - *Catálogo:* Gris neutro suave (`#f8fafc`) que realza las tarjetas de producto y sus fotografías.
  - *Planta y Matriz Técnica:* Slate oscuro industrial (`#0b1120` y `#1e293b`) con acentos cian y teal.
  - *Protocolo de Muestras:* Blanco con tarjetas de etapas.
  - *Sostenibilidad ESG:* Suave degradé verde menta/ecológico (`#f0fdf4` a `#f8fafc`).
  - *Configurador de Lote:* Taller técnico en gris pizarra claro (`#f1f5f9`).
  - *Footer:* Azul carbón institucional (`#090e17`).

---

## 🖼️ Banner Principal Superior (2K, +35% Tamaño y Alineado al Extremo Derecho)

- **Aumento de Tamaño del 35%:** La caja contenedora creció de 1.080px a **1.458px** (`max-width: 1458px; width: 100%;`), permitiendo apreciar la prenda polo, las costuras y los detalles técnicos con un impacto visual mucho mayor.
- **Ubicación en el Extremo Derecho:** Alineado mediante `margin: 0 0 0 auto` y `align-items: flex-end`, posicionando la prenda sobre el costado derecho de la pantalla sin ningún tipo de recorte (`object-fit: contain`).
- **Fondo Degradado Continuo:** Se integra suavemente sobre un fondo continuo (`#f8f3f0` a `#f1edea`), asegurando que en pantallas panorámicas y ultrawide la transición visual sea impecable.
- **Hotspots Interactivos Adaptados:** Los 4 puntos interactivos sobre la polo ahora despliegan sus fichas técnicas hacia el interior izquierdo para permanecer 100% legibles sin salirse del borde de la pantalla.
- **Ribbon de Especificaciones y Acciones:** Accesos directos a catálogo, cotizador y descarga de PDF justo debajo de la cabecera.

---

## 🏛️ Clientes Institucionales y Certificaciones de Calidad (Costado Izquierdo Hero)

En la sección inicial del cuerpo de la página (`#hero`), la columna izquierda se diseñó especialmente como un bloque de máxima credibilidad y autoridad B2B:

- **Encabezado Oficial:** `CLIENTES INSTITUCIONALES QUE CONFÍAN EN TEXTILES ACRILÁN S.A.S.:`
- **Subtítulo de Certificaciones:** `CERTIFICACIONES: ISO 9001:2015 · SMETA · DISNEY FAMA`
- **13 Clientes Institucionales (Tarjetas interactivas con efecto hover):**
  - TOTTO
  - ARTURO CALLE
  - PATPRIMO
  - RIFLE JEANS WEAR
  - SPEEDO
  - FALABELLA
  - ÉXITO
  - CENCOSUD
  - PILATOS
  - BIG JOHN
  - TICKET
  - BASEBALLISM
  - AZÚCAR
- **Certificados de Calidad que Manejamos (Bloque de insignias oficiales):**
  - **ISO 9001 (BUREAU VERITAS)**
  - **SMETA AUDITED**
  - **DISNEY FAMA CERTIFIED**
- **Indicadores Rápidos de Planta:** 170 TN/mes Tejeduría y Tintorería, 600.000 prendas/mes Confección, y Mitigación de CO₂ con Energía Solar.
- **Botones de Conversión:** Acceso directo a explorar el catálogo y descargar el catálogo en PDF.

---

## 🏷️ Catálogo Oficial de Prendas con Fotos Reales del Catálogo y Modal de Detalle

Cada una de las 10 referencias del catálogo incluye ahora su **fotografía oficial recortada y optimizada** directamente desde el PDF de 23 páginas (`assets/products/*.jpg`), con visor ampliado (*Lightbox Modal*) interactivo al hacer clic:

1. **Polo Premium Manga Corta Caballero (200 g/m²):** [`assets/products/polo-premium.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/polo-premium.jpg) — 50-50% Polialgodón, tejido Piqué, cuello estructurado, 10 colores oficiales con tabla de medidas (S, M, L, XL).
2. **T-Shirt Cuello Redondo Manga Corta 180g:** [`assets/products/tshirt-180.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/tshirt-180.jpg) — 100% Algodón Peinado de fibra larga, cuello rib doble, 8 colores de catálogo y medidas.
3. **T-Shirt Cuello Redondo Manga Corta 155g:** [`assets/products/tshirt-155.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/tshirt-155.jpg) — 100% Algodón, rib 1x1, 10 colores de catálogo (tallas XS a XL).
4. **T-Shirt Cuello V Manga Corta para Caballero:** [`assets/products/tshirt-vneck.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/tshirt-vneck.jpg) — 100% Algodón Peinado, corte moderno en V, 10 colores.
5. **Polo Premium Caballero y Dama (Full Package):** [`assets/products/full-polo-couple.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-polo-couple.jpg) — Confección en pares corporativos (hombre/mujer), pedido mínimo desde **380 unidades**.
6. **T-Shirt Cuello Redondo Caballero y Dama (Full Package):** [`assets/products/full-tshirt-couple.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-tshirt-couple.jpg) — Silueta masculina y femenina, pedido mínimo desde **550 unidades**.
7. **T-Shirt Manga Larga para Caballero:** [`assets/products/full-tshirt-long.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-tshirt-long.jpg) — Protección en campo (agroindustria y logística).
8. **Tank Top para Dama:** [`assets/products/full-tank-top.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-tank-top.jpg) — Silueta femenina ligera y transpirable.
9. **Camiseta Interior Esqueleto / Cuello V:** [`assets/products/full-underwear-tank.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-underwear-tank.jpg) — Prenda interior 100% algodón peinado.
10. **Mini T-Shirt Infantil:** [`assets/products/full-kids-tshirt.jpg`](file:///c:/Users/USUARIO/Desktop/ACRILAN%20DOTACIONES/assets/products/full-kids-tshirt.jpg) — Para colegios, vacaciones recreativas y cajas de compensación.

- **Calibración Quirúrgica de Máscaras por Prenda (13 Modelos Analizados 1 a 1):**
  Se rediseñó el sistema de segmentación analizando individualmente cada una de las 13 fotografías originales extraídas del catálogo PDF para eliminar cualquier fuga o sangrado sobre pantalones, cuellos o brazos:
  - **Fronteras Verticales Anatómicas Precisas:** Se midió pixel por pixel el inicio de hombros/escote y el dobladillo inferior exacto (ej. Polo Premium en $y=444$ antes del jean en $y=448$, T-Shirt 180g en $y=502$ antes del jean en $y=508$, T-Shirt Hombre en $y=408$ antes de pantalones oscuros en $y=415$).
  - **Discriminación Espectral por Tipo de Tejido:** Reglas específicas para cada color original (verde esmeralda, rojo brillante, negro profundo, azul noche, púrpura, blanco neutro, gris melange y prendas sin mangas).
  - **Protección de Piel y Extremidades:** En las prendas sin mangas (`full-tank-top`, `full-underwear-tank`) los hombros y brazos quedan 100% aislados; en la foto infantil (`full-kids-tshirt`) el brazo cruzado del niño sobre el torso se preserva intacto con su piel natural.
  - **Cierre Morfológico y Suavizado Gaussiano ($r=0.6$):** Relleno de micro-sombras en costuras y transición fotográfica realista sin bordes duros.
  - **Verificación de Sanidad Fotográfica:** Se auditó numéricamente la diferencia cromática entre la base y cada una de las 65 variantes, certificando un **0.00 de alteración en cabeza/rostro y 0.00 en pantalones/jeans** en todas las prendas.
- **Modelos Ampliados al Máximo (+60% de Tamaño en Tarjeta y Modal):** Se eliminaron los márgenes vacíos de las imágenes originales y se aumentó la altura del contenedor multimedia a **330 px** en tarjeta y **520 px** en el modal, permitiendo que las prendas y los modelos ocupen el espacio de forma imponente y con gran nivel de detalle visual.
- **Sincronización en WhatsApp y Cotizador:** Al cambiar el color de una prenda, el enlace de WhatsApp y el mensaje de cotización incluyen automáticamente el tono elegido (ej. *"Quiero cotizar Polo Premium en color 304 Rojo"*).
- **Visor Ampliado (Modal / Lightbox):** Al hacer clic sobre la foto o el botón "Ver foto y ficha", se abre una vista ampliada de 960 px donde también es posible previsualizar todos los colores disponibles en tiempo real.

---

## 🏭 Capacidades Reales de Planta en Cali

- **Tejeduría Circular:** 31 máquinas circulares, **170 toneladas/mes** de tela cruda.
- **Tintorería y Acabados:** **170 toneladas/mes**, termofijado en rama y PTAR propia con 2 reactores UASB.
- **Corte:** 3 mesas de 30 metros, **30.000 prendas/día**.
- **Confección:** **600.000 unidades al mes**.
- **Estampado Industrial:** Pulpo automático 100% eléctrico (10 colores) + pulpo manual (8 colores con registro láser), capacidad **150.000 unidades/mes**.
- **Bordado:** 2 máquinas bordadoras industriales (**20.000 unidades/mes**).
- **Sustentabilidad y Social:** Paneles solares (-38.87 TN CO₂/año = 1.866 árboles), 60% ahorro de agua en tintorería, 82% colaboradores sobre el mínimo.
- **Certificaciones:** ISO 9001:2015 (Bureau Veritas), SMETA y Disney FAMA.

---

## 📞 Datos de Contacto Oficiales

- **Dirección:** Calle 11 # 22-91, Cali, Valle del Cauca, Colombia.
- **Celular y WhatsApp B2B:** `+57 312 8519775`
- **PBX:** `+57 (602) 5577789`
- **Correos:** `info@grupoacrilan.com` · `mercadeo@grupoacrilan.com`
- **Web:** `www.grupoacrilan.com`
