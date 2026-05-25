# contabilidad-conciliacion

Plugin de conciliación bancaria y detección de anomalías para el equipo Taxtic.

## Componentes

- **Skill `/conciliacion-bancaria`** — matchea cartola CSV vs libro CSV.
- **Agent `detector-anomalias`** — analiza cartola en busca de patrones anómalos.

## Instalación

```
/plugin install contabilidad-conciliacion@plugins-taxtic
```

## Uso

```
/conciliacion-bancaria
[indicar paths cartola.csv y libro.csv]
```

## Versión

0.1.0 (MVP — pendiente: soporte multi-cuenta, integración bancos vía API)
