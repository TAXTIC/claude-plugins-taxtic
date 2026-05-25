# comun-anonimizacion

Plugin transversal de seguridad para el equipo Taxtic.

## Componentes

- **Skill `/anonimizar`** — anonimiza RUTs, nombres, empresas y montos en cualquier texto.
- **Hook `pre-prompt`** — detecta RUTs chilenos reales en el input y alerta antes de enviar.
- **Hook `post-edit`** — alerta si un archivo guardado contiene RUTs reales.

## Instalación

```
/plugin install comun-anonimizacion@claude-plugins-taxtic
```

## Uso

### Skill

```
/anonimizar
[pegar texto a anonimizar]
```

### Hooks

Los hooks se activan automáticamente al instalar el plugin. No requieren acción explícita.

## Versión

0.1.0
