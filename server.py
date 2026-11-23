"""RiskLens MCP: analista de riesgo conversacional sobre datos de transacciones."""
from pathlib import Path
import pandas as pd
from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parent / "data" / "transacciones.csv"
mcp = FastMCP("risklens")


def cargar() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["fecha"])
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    return df


@mcp.tool()
def kpis_generales() -> dict:
    """KPIs generales: ventas totales, transacciones, ticket promedio y clientes únicos."""
    df = cargar()
    return {
        "ventas_totales": round(df["monto"].sum(), 2),
        "transacciones": int(len(df)),
        "ticket_promedio": round(df["monto"].mean(), 2),
        "clientes_unicos": int(df["cliente_id"].nunique()),
        "periodo": f"{df['fecha'].min().date()} a {df['fecha'].max().date()}",
    }


@mcp.tool()
def consumo_por_categoria(categoria: str = "region") -> list[dict]:
    """Ventas agrupadas por 'region', 'forma_pago' o 'canal'."""
    df = cargar()
    if categoria not in {"region", "forma_pago", "canal"}:
        return [{"error": "Usa region, forma_pago o canal"}]
    g = df.groupby(categoria)["monto"].agg(["sum", "count", "mean"]).reset_index()
    g["participacion_%"] = (g["sum"] / g["sum"].sum() * 100).round(1)
    g = g.rename(columns={"sum": "ventas", "count": "transacciones", "mean": "ticket_promedio"})
    return g.round(2).sort_values("ventas", ascending=False).to_dict("records")


@mcp.tool()
def perfil_cliente(cliente_id: str) -> dict:
    """Comportamiento de consumo de un cliente específico."""
    df = cargar()
    c = df[df["cliente_id"] == cliente_id]
    if c.empty:
        return {"error": f"Cliente {cliente_id} no encontrado"}
    mensual = c.groupby("mes")["monto"].sum()
    return {
        "cliente_id": cliente_id,
        "gasto_total": round(c["monto"].sum(), 2),
        "compras": int(len(c)),
        "ticket_promedio": round(c["monto"].mean(), 2),
        "region": c["region"].mode()[0],
        "forma_pago_preferida": c["forma_pago"].mode()[0],
        "ultima_compra": str(c["fecha"].max().date()),
        "gasto_mensual": mensual.round(2).to_dict(),
    }


@mcp.tool()
def senales_de_riesgo() -> dict:
    """Señales de riesgo: concentración de ingresos (HHI), tendencia mensual y recomendaciones."""
    df = cargar()
    part = df.groupby("cliente_id")["monto"].sum() / df["monto"].sum()
    hhi = round(float((part ** 2).sum() * 10000), 1)
    top10 = round(float(part.sort_values(ascending=False).head(10).sum() * 100), 1)
    mensual = df.groupby("mes")["monto"].sum()
    var = round(float(mensual.pct_change().iloc[-1] * 100), 1) if len(mensual) > 1 else 0.0
    rec = []
    if top10 > 40:
        rec.append("Alta dependencia de pocos clientes: diversificar la cartera.")
    if var < -5:
        rec.append("Caída de ventas en el último mes: revisar precios, canales y clientes en riesgo de fuga.")
    if not rec:
        rec.append("Sin alertas críticas: mantener monitoreo mensual.")
    return {"hhi_clientes": hhi, "participacion_top10_%": top10,
            "variacion_ultimo_mes_%": var, "recomendaciones": rec}


GLOSARIO = {
    "hhi": "Índice Herfindahl-Hirschman: suma de participaciones al cuadrado; mide concentración (0-10000).",
    "ticket promedio": "Monto promedio por transacción: ventas totales / número de transacciones.",
    "var": "Value at Risk: pérdida máxima esperada con cierto nivel de confianza en un horizonte dado.",
    "churn": "Tasa de clientes que dejan de comprar en un periodo.",
    "inflacion": "Aumento generalizado y sostenido del nivel de precios.",
    "tipo de cambio": "Precio de una moneda en términos de otra.",
}


@mcp.tool()
def definir_concepto(concepto: str) -> str:
    """Definición de un concepto financiero o económico."""
    return GLOSARIO.get(concepto.lower().strip(),
                        "Concepto no está en el glosario; el agente puede explicarlo con su conocimiento general.")


if __name__ == "__main__":
    mcp.run()
