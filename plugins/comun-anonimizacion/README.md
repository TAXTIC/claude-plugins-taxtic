# comun-anonimizacion

Plugin transversal de seguridad para el equipo Taxtic.

## Componentes

- **Skill `/anonimizar`** — anonimiza RUTs, nombres, empresas y montos en cualquier texto.
- **Hook `pre-prompt`** — detecta RUTs chilenos reales en el input y alerta antes de enviar.
- **Hook `post-edit`** — alerta si un archivo guardado contiene RUTs reales.

Los hooks usan **PowerShell** (preinstalado en Windows 10/11). No requieren Python.

## Instalación

```
/plugin install comun-anonimizacion@plugins-taxtic
```

## Uso

### Skill

```
/anonimizar
[pegar texto a anonimizar]
```

### Hooks

Los hooks se activan automáticamente al instalar el plugin. No requieren acción explícita.

## Dependencias

- **Sin dependencias para uso básico.** PowerShell 5.1+ está preinstalado en Windows 10/11.
- *Opcional (legacy / fallback):* `detect_rut.py` (versión Python equivalente). No se usa por defecto; útil para entornos no-Windows o para pruebas.

## Versión

0.2.0
