# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Plugin `contabilidad-rendiciones`: skill `/extractor-rendiciones` (PDFs de caja chica → CSV + Excel, con columna `Pagina`, hojas resumen usadas como control, filas `NO_PROCESADO` para PDFs ilegibles) y agente `auditor-rendiciones` (resumen global + CRÍTICO/ADVERTENCIA/INFO sobre el CSV).

## [0.1.0] - 2026-05-25

### Added
- Marketplace `plugins-taxtic` con 5 plugins.
- Plugin `comun-anonimizacion`: skill `/anonimizar` (RUTs/nombres/montos) + hook UserPromptSubmit y PostToolUse para detección de RUTs reales (módulo 11) en prompts y archivos editados.
- Plugin `contabilidad-facturas`: skills `/extractor-facturas` (PDFs → CSV con campos estándar) y `/clasificar-cuentas` (PUC chileno mínimo); agente `auditor-facturas` (CRÍTICO/ADVERTENCIA/INFO sobre CSV extraído).
- Plugin `contabilidad-conciliacion` (MVP): skill `/conciliacion-bancaria` (cartola vs libro) y agente `detector-anomalias` (outliers estadísticos, descripciones genéricas).
- Plugin `rrhh-planilla` (MVP): skills `/validar-planilla` (estructura, aritmética, descuentos legales) y `/comparar-planillas` (mes vs mes con umbral).
- Plugin `asesoria-normativa` (MVP): skills `/resumen-circular-sii` (PDF/URL → resumen estructurado) y `/checklist-f29` (checklist pre-envío por giro y régimen); agente `consultor-tributario` (Q&A normativa chilena).
- 10 PDFs sintéticos de facturas en `assets/samples/facturas-octubre/` + script generador (`generador_facturas.py` con `reportlab`).

### Fixed
- Marketplace renombrado de `claude-plugins-taxtic` a `plugins-taxtic` (Claude Code rechaza prefijo "claude" por conflicto con namespace oficial Anthropic).
- Hook `comun-anonimizacion` ahora citea path `${CLAUDE_PLUGIN_ROOT}/hooks/detect_rut.py` para soportar usuarios Windows con espacios en el nombre.
