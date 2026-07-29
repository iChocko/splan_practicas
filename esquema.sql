-- =====================================================================
--  esquema.sql — Estructura de la base de datos compartida
--  Práctica 04 · SPLAN
--
--  ESTE ARCHIVO ES EL CONTRATO. Las dos tablas de datos las llena una
--  persona distinta, pero ambas viven aquí y deben poder unirse.
--
--  Si necesitan cambiar algo de este archivo: abran un issue, discútanlo
--  y háganlo en un PR aparte. Un cambio aquí rompe el trabajo de la otra.
-- =====================================================================


-- ---------------------------------------------------------------------
-- CATÁLOGOS (vienen precargados; nadie los llena desde la API)
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_municipio (
    cve_mun     TEXT PRIMARY KEY,   -- clave INEGI de 3 dígitos: '001'..'013'
    municipio   TEXT NOT NULL
);

INSERT OR IGNORE INTO dim_municipio (cve_mun, municipio) VALUES
    ('001', 'Calkiní'),
    ('002', 'Campeche'),
    ('003', 'Carmen'),
    ('004', 'Champotón'),
    ('005', 'Hecelchakán'),
    ('006', 'Hopelchén'),
    ('007', 'Palizada'),
    ('008', 'Tenabo'),
    ('009', 'Escárcega'),
    ('010', 'Calakmul'),
    ('011', 'Candelaria'),
    ('012', 'Seybaplaya'),
    ('013', 'Dzitbalché');


-- Puente entre el mundo micro (SCIAN) y el mundo macro (ITAEE).
-- Esta tabla es la razón por la que las dos mitades del proyecto se
-- pueden unir. Sin ella, cada quien tendría datos incomparables.
CREATE TABLE IF NOT EXISTS dim_sector_actividad (
    sector_id       TEXT PRIMARY KEY,   -- código SCIAN de 2 dígitos
    sector_nombre   TEXT NOT NULL,
    gran_division   TEXT NOT NULL       -- 'Primarias' | 'Secundarias' | 'Terciarias'
);

INSERT OR IGNORE INTO dim_sector_actividad (sector_id, sector_nombre, gran_division) VALUES
    ('11', 'Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza', 'Primarias'),
    ('21', 'Minería', 'Secundarias'),
    ('22', 'Generación, transmisión y distribución de energía eléctrica, agua y gas', 'Secundarias'),
    ('23', 'Construcción', 'Secundarias'),
    ('31', 'Industrias manufactureras (31)', 'Secundarias'),
    ('32', 'Industrias manufactureras (32)', 'Secundarias'),
    ('33', 'Industrias manufactureras (33)', 'Secundarias'),
    ('43', 'Comercio al por mayor', 'Terciarias'),
    ('46', 'Comercio al por menor', 'Terciarias'),
    ('48', 'Transportes, correos y almacenamiento (48)', 'Terciarias'),
    ('49', 'Transportes, correos y almacenamiento (49)', 'Terciarias'),
    ('51', 'Información en medios masivos', 'Terciarias'),
    ('52', 'Servicios financieros y de seguros', 'Terciarias'),
    ('53', 'Servicios inmobiliarios y de alquiler de bienes muebles e intangibles', 'Terciarias'),
    ('54', 'Servicios profesionales, científicos y técnicos', 'Terciarias'),
    ('55', 'Corporativos', 'Terciarias'),
    ('56', 'Servicios de apoyo a los negocios y manejo de residuos', 'Terciarias'),
    ('61', 'Servicios educativos', 'Terciarias'),
    ('62', 'Servicios de salud y de asistencia social', 'Terciarias'),
    ('71', 'Servicios de esparcimiento culturales y deportivos', 'Terciarias'),
    ('72', 'Servicios de alojamiento temporal y de preparación de alimentos y bebidas', 'Terciarias'),
    ('81', 'Otros servicios excepto actividades gubernamentales', 'Terciarias'),
    ('93', 'Actividades legislativas, gubernamentales y de impartición de justicia', 'Terciarias');


-- ---------------------------------------------------------------------
-- CAPA MICRO — la llena Abgail desde la API del DENUE
-- Granularidad: un renglón = un establecimiento
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS denue_establecimiento (
    id_establecimiento  TEXT PRIMARY KEY,   -- campo "Id" del DENUE
    clee                TEXT,
    nombre              TEXT,
    razon_social        TEXT,
    cve_ent             TEXT NOT NULL,      -- '04' para Campeche
    cve_mun             TEXT NOT NULL,      -- '001'..'013'
    sector_id           TEXT NOT NULL,      -- SCIAN 2 dígitos
    clase_actividad_id  TEXT,
    clase_actividad     TEXT,
    estrato_texto       TEXT,               -- como lo entrega el INEGI
    estrato_min         INTEGER,            -- derivado por Abgail
    estrato_max         INTEGER,            -- derivado por Abgail
    latitud             REAL,
    longitud            REAL,
    fecha_alta          TEXT,
    fecha_extraccion    TEXT NOT NULL,
    FOREIGN KEY (cve_mun)   REFERENCES dim_municipio (cve_mun),
    FOREIGN KEY (sector_id) REFERENCES dim_sector_actividad (sector_id)
);

CREATE INDEX IF NOT EXISTS ix_denue_mun    ON denue_establecimiento (cve_mun);
CREATE INDEX IF NOT EXISTS ix_denue_sector ON denue_establecimiento (sector_id);


-- ---------------------------------------------------------------------
-- CAPA MACRO — la llena Aremy desde la API de Indicadores (BIE)
-- Granularidad: un renglón = un dato de una serie en un periodo
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bie_observacion (
    indicador_id      TEXT NOT NULL,   -- clave del indicador en el BIE
    area_geografica   TEXT NOT NULL,   -- '00' nacional, '04' Campeche
    periodo           TEXT NOT NULL,   -- tal como lo entrega el INEGI
    anio              INTEGER,         -- derivado por Aremy
    trimestre         INTEGER,         -- derivado por Aremy (NULL si no aplica)
    valor             REAL,
    fecha_extraccion  TEXT NOT NULL,
    PRIMARY KEY (indicador_id, area_geografica, periodo),
    FOREIGN KEY (indicador_id) REFERENCES bie_indicador (indicador_id)
);

-- Metadatos de cada serie descargada: qué mide y a qué gran división
-- corresponde. La columna `gran_division` es la que permite el JOIN
-- con la capa micro a través de dim_sector_actividad.
CREATE TABLE IF NOT EXISTS bie_indicador (
    indicador_id     TEXT PRIMARY KEY,
    indicador_nombre TEXT NOT NULL,
    gran_division    TEXT,             -- 'Primarias'|'Secundarias'|'Terciarias'|'Total'|NULL
    unidad           TEXT,
    frecuencia       TEXT,             -- 'Trimestral' | 'Mensual' | 'Anual'
    fuente           TEXT
);

CREATE INDEX IF NOT EXISTS ix_bie_periodo ON bie_observacion (anio, trimestre);
