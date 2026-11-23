# RiskLens MCP — Analista de riesgo conversacional

**Dojo AI Hackathon 2026 · Track 02: Build for Business**
Autor: Diego Sáenz · Costa Rica

## Problema
Las empresas tienen datos de ventas y clientes dispersos y les cuesta convertirlos en decisiones con
perspectiva de **riesgo**, visión **prospectiva** y contexto **macrofinanciero**. Los dashboards muestran
números, pero no responden preguntas ni recomiendan acciones.

## Solución
Un servidor **MCP (Model Context Protocol)** que permite a cualquier agente de IA (Claude, Cursor, etc.)
conversar con los datos del cliente:
- Preguntar por KPIs: ventas totales, ticket promedio, clientes únicos.
- Ver el comportamiento de consumo por **región, forma de pago o canal**.
- Analizar a un **cliente específico** (frecuencia, gasto, tendencia).
- Obtener **señales de riesgo** (concentración de ingresos, caída de ventas) con recomendaciones.
- Consultar definiciones de conceptos financieros y económicos.

## PRD resumido
| Elemento | Definición |
|---|---|
| Usuario | Gerentes y analistas de pymes y empresas medianas en LATAM |
| Dolor | Datos sin interpretación; decisiones sin enfoque de riesgo |
| MVP | Servidor MCP con 5 herramientas sobre un CSV de transacciones |
| Privacidad | Los datos se procesan localmente; no salen de la máquina del cliente (pensado bajo NDA) |
| Métrica de éxito | Tiempo de pregunta a hallazgo accionable < 1 minuto |
| Próximos pasos | Series de tiempo y pronóstico, noticias y redes sociales, conectores CRM/ERP, datos macro (BCCR, FRED) |

## Herramientas MCP
| Herramienta | Qué hace |
|---|---|
| `kpis_generales` | Ventas, transacciones, ticket promedio, clientes |
| `consumo_por_categoria` | Agrupa ventas por región, forma de pago o canal |
| `perfil_cliente` | Comportamiento de un cliente específico |
| `senales_de_riesgo` | Concentración de ingresos (HHI), tendencia mensual y recomendaciones |
| `definir_concepto` | Glosario de conceptos financieros y económicos |

## Instalación
```bash
pip install "mcp[cli]" pandas
python server.py            # o: mcp dev server.py
```
Configuración para Claude Desktop (`claude_desktop_config.json`):
```json
{ "mcpServers": { "risklens": { "command": "python", "args": ["/ruta/a/risklens-mcp/server.py"] } } }
```
Para usar tus datos, reemplaza `data/transacciones.csv` (columnas: fecha, cliente_id, region, forma_pago, canal, monto).

## Cómo se usó AI coding
- **Claude** (Anthropic): definición del producto y PRD, código del servidor MCP, datos de ejemplo y documentación.
- Todo el proyecto se construyó durante el hackathon (22 de noviembre de 2026); no había trabajo previo.

## Estado
MVP funcional con datos sintéticos. Proyecto iniciado desde cero durante el hackathon.
