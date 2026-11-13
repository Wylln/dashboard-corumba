import json
import re

with open("referencia/Relatório de Lavantamento de PDV - Amazonas Importados.html", "r", encoding="utf-8") as f:
    html = f.read()

# Pattern to capture each row:
pattern = re.compile(r'<tr><td class="center">(\d+)</td><td class="center">(\d+)</td><td class="left">(.*?)</td><td class="center"><span class="[^"]*">(\d+)</span></td></tr>')
matches = pattern.findall(html)

items = []
total = 0
for m in matches:
    item_num = int(m[0])
    code = m[1]
    name = re.sub(r'<[^>]+>', '', m[2]).strip()
    pdv = int(m[3])
    total += pdv
    
    # Infer city and state
    state = "AP"
    city = "Macapá"
    if "Santana" in name:
        city = "Santana"
        state = "AP"
    elif "Altamira" in name:
        city = "Altamira"
        state = "PA"
    elif "Oiapoque" in name:
        city = "Oiapoque"
        state = "AP"
    elif "Belém" in name:
        city = "Belém"
        state = "PA"
    elif "Breves" in name:
        city = "Breves"
        state = "PA"
    elif "Jari" in name:
        city = "Laranjal do Jari"
        state = "AP"
    elif "Afuá" in name:
        city = "Afuá"
        state = "PA"
    elif "Portel" in name:
        city = "Portel"
        state = "PA"
    elif "Cândido Mendes" in name:
        city = "Cândido Mendes"
        state = "MA/PA"
    elif "Pedra Branca" in name:
        city = "Pedra Branca"
        state = "AP"
    elif "Porto Grande" in name:
        city = "Porto Grande"
        state = "AP"
    elif "Porto de Moz" in name:
        city = "Porto de Moz"
        state = "PA"
    elif "Calçoene" in name:
        city = "Calçoene"
        state = "AP"
    elif "Amapá" in name:
        city = "Amapá"
        state = "AP"
    elif "Mazagão" in name:
        city = "Mazagão"
        state = "AP"
    elif "Oriximiná" in name:
        city = "Oriximiná"
        state = "PA"
    elif "Lourenço" in name:
        city = "Lourenço"
        state = "AP"
    elif "Anajás" in name:
        city = "Anajás"
        state = "PA"
    elif "Almeirim" in name:
        city = "Almeirim"
        state = "PA"
    elif "Barcarena" in name:
        city = "Barcarena"
        state = "PA"
    elif "Abaetetuba" in name:
        city = "Abaetetuba"
        state = "PA"
    elif "Manaus" in name:
        city = "Manaus"
        state = "AM"
    elif "Santarém" in name:
        city = "Santarém"
        state = "PA"
    elif "Gurupá" in name:
        city = "Gurupá"
        state = "PA"
    
    # Store category
    if pdv >= 10:
        cat = "Mega Hub"
        badge_color = "red"
    elif pdv >= 4:
        cat = "Polo Regional"
        badge_color = "purple"
    elif pdv == 3:
        cat = "Loja Tradicional"
        badge_color = "blue"
    elif pdv == 2:
        cat = "Loja Padrão"
        badge_color = "green"
    else:
        cat = "Loja Compacta"
        badge_color = "gray"

    items.append({
        "item": item_num,
        "code": code,
        "name": name,
        "city": city,
        "state": state,
        "pdvs": pdv,
        "category": cat,
        "badge_color": badge_color
    })

print(f"Total Rows: {len(items)}, Sum of PDVs: {total}")
with open("data.json", "w", encoding="utf-8") as out:
    json.dump(items, out, indent=2, ensure_ascii=False)
