import json
import urllib.request
import time
import zipfile
import io
import os
import tempfile
import xml.etree.ElementTree as ET
import random

# --- Throttling para evitar bloqueos ---
REQUEST_DELAY_SECONDS = 1.25
REQUEST_JITTER_SECONDS = 0.75
BACKOFF_ON_ERROR_SECONDS = 3.0

def throttle_request():
    # Small randomized delay to spread requests.
    time.sleep(REQUEST_DELAY_SECONDS + random.random() * REQUEST_JITTER_SECONDS)

# Muestra de 10 juegos (5 de Lanzamiento Completo y 5 en Early Access)
# Muestra ajustada con mas Early Access que completos
COMPLETE_APP_IDS = [
    # --- Lanzamientos Completos / Versión Final (25 juegos) ---
    730,       # Counter-Strike 2
    271590,    # Grand Theft Auto V
    292030,    # The Witcher 3: Wild Hunt
    1091500,   # Cyberpunk 2077
    367520,    # Hollow Knight
    1245620,   # Elden Ring
    1174180,   # Red Dead Redemption 2
    105600,    # Terraria
    413150,    # Stardew Valley
    620,       # Portal 2
    553850,    # Helldivers 2
    582010,    # Monster Hunter: World
    814380,    # Sekiro: Shadows Die Twice
    489830,    # The Elder Scrolls V: Skyrim Special Edition
    377160,    # Fallout 4
    782330,    # DOOM Eternal
    1086940,   # Baldur's Gate 3 
    252490,    # Rust 
    264710,    # Subnautica 
    427520,    # Factorio 
    1145360,   # Hades 
    2144740,   # Ghost of Tsushima DIRECTOR'S CUT
    805550,    # Assetto Corsa Competizione
    250900,    # The Binding of Isaac: Rebirth
    289070,    # Sid Meier’s Civilization VI
]

EARLY_ACCESS_APP_IDS = [
    # --- ACTUALMENTE en Early Access (25 juegos) ---
    1623730,   # Palworld (Supervivencia/Multijugador)
    1145350,   # Hades II (Acción/Roguelike)
    1363080,   # Manor Lords (Estrategia/Construcción)
    2363900,   # Lethal Company (Terror/Multijugador cooperativo)
    892970,    # Valheim (Supervivencia/Mundo abierto)
    739630,    # Phasmophobia (Terror psicológico)
    108600,    # Project Zomboid (Supervivencia/RPG táctico)
    1203620,   # Enshrouded (RPG de acción/Supervivencia)
    1282100,   # No Rest for the Wicked (RPG de acción)
    2670630,   # Supermarket Simulator (Simulación/Gestión)
    2474300,   # Gray Zone Warfare (Shooter táctico)
    1326470,   # Abiotic Factor (Supervivencia/Multijugador)
    284160,    # BeamNG.drive (Simulación de físicas y conducción)
    2465620,   # Le Mans Ultimate (Simulador de carreras competitivo)
    1466860,   # Techtonica (Automatización/Construcción de fábricas)
    2060160,   # The Farmer Was Replaced (Lógica/Programación agrícola)
    2427700,   # Backpack Battles (Estrategia/Gestión de inventario)
    1812450,   # Bellwright (Estrategia/Supervivencia)
    1366540,   # Dyson Sphere Program (Automatización espacial)
    2208920,   # Void Crew (Simulación espacial cooperativa)
    1604030,   # V Rising (Supervivencia/Construcción de bases)
    1119730,   # Darkest Dungeon II (RPG/Roguelike por turnos)
    954850,    # Kerbal Space Program 2 (Simulación espacial y física)
    1465460,   # Infection Free Zone (Estrategia de construcción de ciudades)
    2399830,   # ARK: Survival Ascended (Supervivencia/Dinosaurios)
]

# Early Access adicionales obtenidos desde la tienda/SteamSpy + validacion en la tienda
EXTRA_EARLY_ACCESS_COUNT = 40
STORESEARCH_PAGE_SIZE = 50
STORESEARCH_MAX_PAGES = 6

COLUMNS = [
    "AppID", "Nombre", "Precio base (USD)", "Porcentaje de reseñas positivas",
    "Categoría de reseñas", "Pico histórico / CCU", "Jugadores Promedio",
    "Estado de lanzamiento", "Soporte Multiplataforma", "Género principal"
]

def get_json(url):
    throttle_request()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"  [!] Error consultando {url}: {e}")
        time.sleep(BACKOFF_ON_ERROR_SECONDS)
        return None


def get_current_players(appid):
    url = (
        "https://api.steampowered.com/"
        "ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid="
        f"{appid}"
    )
    data = get_json(url)
    if data and "response" in data:
        return data["response"].get("player_count")
    return None

def is_early_access_app(appid):
    store_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
    store_data = get_json(store_url)
    if store_data and str(appid) in store_data and store_data[str(appid)].get("success"):
        data = store_data[str(appid)]["data"]
        genres = [g["description"] for g in data.get("genres", [])]
        return "Early Access" in genres
    return False

def get_storesearch_early_access_ids(limit):
    ids = []
    for page in range(STORESEARCH_MAX_PAGES):
        start = page * STORESEARCH_PAGE_SIZE
        url = (
            "https://store.steampowered.com/api/storesearch/?"
            f"term=&start={start}&count={STORESEARCH_PAGE_SIZE}&cc=us&l=en&filter=earlyaccess"
        )
        data = get_json(url)
        items = data.get("items", []) if data else []
        if not items:
            break

        for item in items:
            appid = item.get("id")
            if not isinstance(appid, int):
                continue
            if appid in ids:
                continue
            if is_early_access_app(appid):
                ids.append(appid)
            if len(ids) >= limit:
                return ids
            time.sleep(0.4)
    return ids

def get_steamspy_early_access_ids(limit):
    spy_url = "https://steamspy.com/api.php?request=top100in2weeks"
    spy_data = get_json(spy_url)
    if not spy_data:
        return []

    ids = []
    for appid_str in spy_data.keys():
        try:
            appid = int(appid_str)
        except ValueError:
            continue

        if is_early_access_app(appid):
            ids.append(appid)
        if len(ids) >= limit:
            break
        time.sleep(0.5)
    return ids

def get_extra_early_access_ids(limit):
    ids = get_storesearch_early_access_ids(limit)
    if len(ids) >= limit:
        return ids

    remaining = limit - len(ids)
    ids.extend(get_steamspy_early_access_ids(remaining))
    return ids

# ─── Generador de .xlsx sin librerías externas ────────────────────────────────

def xml_str(tag, text="", **attrs):
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    if attr_str:
        return f'<{tag} {attr_str}>{text}</{tag}>'
    return f'<{tag}>{text}</{tag}>'

def escape_xml(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_xlsx(rows, columns, output_path):
    """
    Genera un archivo .xlsx válido usando solo zipfile y xml (sin dependencias externas).
    Un .xlsx es simplemente un archivo ZIP con XMLs en su interior.
    """

    # Shared strings (para texto en celdas)
    shared_strings = []
    shared_index = {}

    def get_shared_idx(value):
        key = str(value)
        if key not in shared_index:
            shared_index[key] = len(shared_strings)
            shared_strings.append(key)
        return shared_index[key]

    # Construir filas de la hoja
    sheet_rows = []

    # Fila de encabezados (negrita via estilo 1)
    header_cells = []
    for col_i, col_name in enumerate(columns):
        col_letter = chr(ord('A') + col_i)
        idx = get_shared_idx(col_name)
        header_cells.append(f'<c r="{col_letter}1" t="s" s="1"><v>{idx}</v></c>')
    sheet_rows.append(f'<row r="1">{"".join(header_cells)}</row>')

    # Filas de datos
    for row_i, row in enumerate(rows, start=2):
        cells = []
        for col_i, col_name in enumerate(columns):
            col_letter = chr(ord('A') + col_i)
            value = row.get(col_name, "")
            cell_ref = f"{col_letter}{row_i}"
            try:
                # Si es número, guardarlo como número
                num = float(str(value).replace("%", ""))
                if "%" not in str(value):
                    cells.append(f'<c r="{cell_ref}"><v>{num}</v></c>')
                else:
                    idx = get_shared_idx(value)
                    cells.append(f'<c r="{cell_ref}" t="s"><v>{idx}</v></c>')
            except (ValueError, TypeError):
                idx = get_shared_idx(escape_xml(value))
                cells.append(f'<c r="{cell_ref}" t="s"><v>{idx}</v></c>')
        sheet_rows.append(f'<row r="{row_i}">{"".join(cells)}</row>')

    # ── Contenidos de cada archivo dentro del ZIP ──────────────────────────────

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '</Types>'
    )

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Datos" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>'
    )

    # Estilos: estilo 0 = normal, estilo 1 = negrita para encabezados
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="Calibri"/></font>'
        '<font><b/><sz val="11"/><name val="Calibri"/></font>'
        '</fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0"/>'
        '</cellXfs>'
        '</styleSheet>'
    )

    sheet_data = "\n".join(sheet_rows)
    sheet1 = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{sheet_data}</sheetData>'
        '</worksheet>'
    )

    ss_items = "".join(f'<si><t xml:space="preserve">{s}</t></si>' for s in shared_strings)
    shared_strings_xml = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared_strings)}" uniqueCount="{len(shared_strings)}">'
        f'{ss_items}</sst>'
    )

    # Escribir el ZIP. Intentar la ruta solicitada, si falla por permisos
    # guardar en el directorio temporal y notificar al llamador.
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", rels)
            zf.writestr("xl/workbook.xml", workbook)
            zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
            zf.writestr("xl/worksheets/sheet1.xml", sheet1)
            zf.writestr("xl/sharedStrings.xml", shared_strings_xml)
            zf.writestr("xl/styles.xml", styles)
        return output_path
    except PermissionError:
        fallback = os.path.join(tempfile.gettempdir(), os.path.basename(output_path))
        with zipfile.ZipFile(fallback, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", rels)
            zf.writestr("xl/workbook.xml", workbook)
            zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
            zf.writestr("xl/worksheets/sheet1.xml", sheet1)
            zf.writestr("xl/sharedStrings.xml", shared_strings_xml)
            zf.writestr("xl/styles.xml", styles)
        print(f"   [!] Permission denied writing '{output_path}'. Guardado en: {fallback}")
        return fallback

# ─── Recolección de datos ─────────────────────────────────────────────────────

def main():
    rows = []

    early_access_ids = list(EARLY_ACCESS_APP_IDS)
    extra_early_access = get_extra_early_access_ids(EXTRA_EARLY_ACCESS_COUNT)
    if extra_early_access:
        print(f"Agregando {len(extra_early_access)} Early Access extra...")
        early_access_ids.extend(extra_early_access)
    else:
        print("[!] No se pudieron obtener Early Access extra desde la tienda/SteamSpy.")

    expected_early_access = set(early_access_ids)
    app_ids = []
    seen_ids = set()
    for appid in COMPLETE_APP_IDS + early_access_ids:
        if appid not in seen_ids:
            seen_ids.add(appid)
            app_ids.append(appid)

    print("Recolectando datos para la muestra de Etapa I...")
    for appid in app_ids:
        print(f"\n-> Procesando App ID: {appid}")
        row = {"AppID": appid}

        # 1. API Tienda Steam (Precio, plataformas, genero)
        store_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
        store_data = get_json(store_url)

        if store_data and str(appid) in store_data and store_data[str(appid)].get("success"):
            data = store_data[str(appid)]["data"]
            row["Nombre"] = data.get("name", "N/A")

            if "price_overview" in data:
                row["Precio base (USD)"] = data["price_overview"].get("initial", 0) / 100.0
            elif data.get("is_free"):
                row["Precio base (USD)"] = 0.0
            else:
                row["Precio base (USD)"] = "N/A"

            genres = [g["description"] for g in data.get("genres", [])]
            is_early_access = "Early Access" in genres
            if appid in expected_early_access and not is_early_access:
                print("   [!] No figura como Early Access en la tienda. Omitiendo.")
                time.sleep(1.5)
                continue
            row["Género principal"] = genres[0] if genres else "N/A"
            row["Estado de lanzamiento"] = "Early Access" if is_early_access else "Completo Directo"

            plats = data.get("platforms", {})
            supported = [k.capitalize() for k, v in plats.items() if v]
            row["Soporte Multiplataforma"] = ", ".join(supported)
        else:
            print(f"   [!] No se encontró información en la Tienda para {appid}. Omitiendo.")
            time.sleep(1.5)
            continue

        # 2. SteamSpy API (Picos y reseñas) + Current Players
        spy_url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
        spy_data = get_json(spy_url)
        if spy_data:
            row["Pico histórico / CCU"] = spy_data.get("ccu", "N/A")

            pos = spy_data.get("positive", 0)
            neg = spy_data.get("negative", 0)
            total = pos + neg
            if total > 0:
                row["Porcentaje de reseñas positivas"] = f"{round((pos / total) * 100, 1)}%"
            else:
                row["Porcentaje de reseñas positivas"] = "N/A"

        current_players = get_current_players(appid)
        row["Jugadores Promedio"] = current_players if current_players is not None else "N/A"

        # 3. API Reseñas de Steam (Categoría textual)
        reviews_url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&num_per_page=0"
        reviews_data = get_json(reviews_url)
        if reviews_data and "query_summary" in reviews_data:
            row["Categoría de reseñas"] = reviews_data["query_summary"].get("review_score_desc", "N/A")

        time.sleep(1.5)
        rows.append(row)

    print("\n--------------------------------------------------------------")

    output_file = "muestra_etapa1.xlsx"
    if rows:
        saved_path = build_xlsx(rows, COLUMNS, output_file)
        print(f"¡Listo! Se guardaron {len(rows)} juegos en: {saved_path}")
        print("Abrí el archivo con Excel o LibreOffice Calc.")
    else:
        print("No se pudieron recolectar datos.")

if __name__ == "__main__":
    main()
