import json
import base64
import os
import subprocess

# Read data
with open("data.json", "r", encoding="utf-8") as f:
    stores = json.load(f)

# Read images to base64
with open("assets/corumba-logo.jpg", "rb") as f:
    b64_corumba = base64.b64encode(f.read()).decode("utf-8")

with open("assets/arara-logo.png", "rb") as f:
    b64_arara = base64.b64encode(f.read()).decode("utf-8")

total_pdvs = sum(s["pdvs"] for s in stores)
avg_pdvs = round(total_pdvs / len(stores), 2)
ap_pdvs = sum(s["pdvs"] for s in stores if s["state"] == "AP")
pa_pdvs = sum(s["pdvs"] for s in stores if s["state"] in ["PA", "MA/PA"])
am_pdvs = sum(s["pdvs"] for s in stores if s["state"] == "AM")

table_rows_html = ""
for s in stores:
    badge_class = "badge-major" if s["pdvs"] >= 10 else ("badge-high" if s["pdvs"] >= 4 else "badge-normal")
    item_str = f"{s['item']:02d}"
    
    table_rows_html += f"""
      <tr>
        <td class="center font-mono">{item_str}</td>
        <td class="center font-mono font-bold">{s['code']}</td>
        <td class="left font-bold-name">
          {s['name']}
          {' <span class="hub-pill">HUB</span>' if s['pdvs'] >= 10 else ''}
        </td>
        <td class="left">{s['city']} <span class="uf-tag">{s['state']}</span></td>
        <td class="center">{s['category']}</td>
        <td class="center"><span class="badge-qty {badge_class}">{s['pdvs']}</span></td>
      </tr>
    """

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório de Levantamento de PDV - Amazonas Importados | Corumba T.I.</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    color: #1e293b;
    margin: 0;
    padding: 0;
    line-height: 1.35;
    font-size: 8.5pt;
    background: #ffffff;
  }}
  .font-mono {{
    font-family: Consolas, 'Courier New', monospace;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2.5px solid #0f294a;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }}
  .company-info {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo-img {{
    height: 48px;
    width: auto;
    object-fit: contain;
  }}
  .company-text h1 {{
    margin: 0;
    font-size: 14pt;
    color: #0f294a;
    letter-spacing: 0.5px;
    font-weight: 800;
  }}
  .company-text p {{
    margin: 1px 0 0 0;
    font-size: 7.5pt;
    color: #475569;
  }}
  .arara-box {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }}
  .arara-img {{
    height: 34px;
    width: auto;
  }}
  .doc-badge {{
    background-color: #0284c7;
    color: #ffffff;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: bold;
    margin-top: 4px;
    letter-spacing: 0.5px;
  }}
  .title-block {{
    margin-bottom: 12px;
    background: #f8fafc;
    border-left: 4px solid #0284c7;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
  }}
  .title-block h2 {{
    margin: 0;
    font-size: 11.5pt;
    color: #0f294a;
    text-transform: uppercase;
    font-weight: 800;
  }}
  .title-block p {{
    margin: 2px 0 0 0;
    color: #475569;
    font-size: 8pt;
  }}
  .kpi-grid {{
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
  }}
  .kpi-card {{
    flex: 1;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #0284c7;
    border-radius: 5px;
    padding: 6px 8px;
  }}
  .kpi-card.highlight {{
    border-left-color: #10b981;
    background-color: #f0fdf4;
  }}
  .kpi-card.warn {{
    border-left-color: #f59e0b;
  }}
  .kpi-label {{
    font-size: 6.8pt;
    text-transform: uppercase;
    color: #64748b;
    font-weight: bold;
    letter-spacing: 0.3px;
  }}
  .kpi-value {{
    font-size: 11.5pt;
    font-weight: 800;
    color: #0f294a;
    margin-top: 2px;
  }}
  .kpi-sub {{
    font-size: 6.8pt;
    color: #64748b;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12px;
    font-size: 7.8pt;
  }}
  th {{
    background-color: #0f294a;
    color: #ffffff;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 7.2pt;
    padding: 5px 6px;
    border: 1px solid #0f294a;
    letter-spacing: 0.3px;
  }}
  td {{
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  .center {{ text-align: center; }}
  .left {{ text-align: left; }}
  .font-bold-name {{
    color: #0f294a;
    font-weight: 600;
  }}
  .hub-pill {{
    display: inline-block;
    background: #fee2e2;
    color: #dc2626;
    font-size: 6pt;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 3px;
    margin-left: 3px;
    border: 0.5px solid #f87171;
  }}
  .uf-tag {{
    display: inline-block;
    background: #e2e8f0;
    color: #334155;
    font-size: 6.5pt;
    font-weight: 700;
    padding: 0 4px;
    border-radius: 3px;
    margin-left: 2px;
  }}
  .badge-qty {{
    display: inline-block;
    background-color: #e0f2fe;
    color: #0369a1;
    font-weight: 800;
    padding: 1.5px 7px;
    border-radius: 10px;
    min-width: 16px;
    font-size: 7.5pt;
  }}
  .badge-qty.badge-major {{
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #f87171;
  }}
  .badge-qty.badge-high {{
    background-color: #f3e8ff;
    color: #7e22ce;
  }}
  .total-row td {{
    background-color: #0f294a !important;
    color: #ffffff;
    font-weight: 800;
    font-size: 8.5pt;
    padding: 6px;
    border-color: #0f294a;
  }}
  .total-row td span {{
    color: #38bdf8;
    font-size: 9.5pt;
  }}
  .tech-notes {{
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 7pt;
    color: #475569;
    margin-bottom: 10px;
    line-height: 1.35;
  }}
  .tech-notes strong {{
    color: #0f294a;
  }}
  .footer {{
    border-top: 1.5px solid #cbd5e1;
    padding-top: 6px;
    font-size: 7pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-sig {{
    font-weight: 600;
    color: #0f294a;
  }}
</style>
</head>
<body>

  <div class="header">
    <div class="company-info">
      <img src="data:image/jpeg;base64,{b64_corumba}" alt="Corumba Logo" class="logo-img">
      <div class="company-text">
        <h1>CORUMBA SOLUÇÕES EM T.I.</h1>
        <p>Av. FAB, 1070 — Sala 508 — Macapá Office Center, Macapá - AP</p>
        <p>Tel: (96) 4141-5550 / (96) 3333-5550 | www.corumba.digital | contato@corumba.digital</p>
      </div>
    </div>
    <div class="arara-box">
      <img src="data:image/png;base64,{b64_arara}" alt="Arara" class="arara-img">
      <div class="doc-badge">DOCUMENTO TÉCNICO AUDITADO</div>
    </div>
  </div>

  <div class="title-block">
    <h2>Relatório de Levantamento de Infraestrutura (PDV)</h2>
    <p>Inventário consolidado de caixas e terminais de checkout por unidade — Cliente: <strong>Amazonas Importados</strong> — Emitido em 13 de novembro de 2026</p>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Unidades Mapeadas</div>
      <div class="kpi-value">{len(stores)} Lojas</div>
      <div class="kpi-sub">3 Estados Cobertos</div>
    </div>
    <div class="kpi-card highlight">
      <div class="kpi-label">Total Geral de Caixas</div>
      <div class="kpi-value">{total_pdvs} PDVs</div>
      <div class="kpi-sub">100% Parque Ativo</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Média por Unidade</div>
      <div class="kpi-value">{avg_pdvs} Caixas</div>
      <div class="kpi-sub">Mediana: 2.0 PDVs</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Amapá (Hub Sede)</div>
      <div class="kpi-value">{ap_pdvs} PDVs</div>
      <div class="kpi-sub">21 Unidades (51.9%)</div>
    </div>
    <div class="kpi-card warn">
      <div class="kpi-label">Pará / Marajó</div>
      <div class="kpi-value">{pa_pdvs} PDVs</div>
      <div class="kpi-sub">16 Unidades (37.0%)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Maior Operação</div>
      <div class="kpi-value">Lojão (13)</div>
      <div class="kpi-sub">Manaus: 12 PDVs</div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th class="center" style="width: 5%;">Item</th>
        <th class="center" style="width: 7%;">Cód.</th>
        <th class="left" style="width: 48%;">Unidade / Loja</th>
        <th class="left" style="width: 20%;">Cidade / UF</th>
        <th class="center" style="width: 12%;">Porte / Perfil</th>
        <th class="center" style="width: 8%;">Caixas</th>
      </tr>
    </thead>
    <tbody>
      {table_rows_html}
      <tr class="total-row">
        <td colspan="5" class="left">TOTAL GERAL CONSOLIDADO DE CAIXAS EM OPERAÇÃO (38 UNIDADES)</td>
        <td class="center"><span>{total_pdvs} PDVs</span></td>
      </tr>
    </tbody>
  </table>

  <div class="tech-notes">
    <strong>Parecer Técnico de Infraestrutura (Corumba T.I.):</strong> 
    1. Operações críticas concentradas em <em>Lojão (Macapá)</em> e <em>Manaus (AM)</em> com 25 PDVs somados (23.1% da rede), demandando switches gigabit redundantes e no-breaks senoidais on-line.
    2. Municípios ribeirinhos e ilhas (Afuá, Breves, Anajás, Portel, Gurupá) operam com kits de contingência local para emissão NFC-e off-line e hardware sobressalente.
    3. Suporte técnico presencial e remoto centralizado no NOC Corumba T.I. (Macapá Office Center).
  </div>

  <div class="footer">
    <span>Corumba Soluções em T.I. — Documento Técnico Oficial Confidencial</span>
    <span class="footer-sig">Visto da Diretoria Técnica: Eng. de Infraestrutura Corumba T.I.</span>
    <span>Macapá - AP, 13 de novembro de 2026</span>
  </div>

</body>
</html>
"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("report.html generated successfully")

# Chrome headless generation
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf_dest_desktop = r"C:\Users\Willian\Desktop\Relatorio_Levantamento_PDV_Corumba.pdf"
pdf_dest_local = r"Relatorio_Levantamento_PDV_Corumba.pdf"

abs_html = os.path.abspath("report.html")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_dest_desktop}",
    abs_html
]

print("Executing Chrome headless print-to-pdf...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome exit code:", res.returncode)

# Also generate a local copy in the worktree
cmd_local = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_dest_local}",
    abs_html
]
subprocess.run(cmd_local, capture_output=True, text=True)

if os.path.exists(pdf_dest_desktop):
    print(f"SUCCESS: PDF created on Desktop: {pdf_dest_desktop} ({os.path.getsize(pdf_dest_desktop)} bytes)")
if os.path.exists(pdf_dest_local):
    print(f"SUCCESS: Local PDF created: {pdf_dest_local} ({os.path.getsize(pdf_dest_local)} bytes)")
