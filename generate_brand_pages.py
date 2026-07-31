"""
Generate all brand pages for AirbagCrashReset.nl
Creates: /audi/index.html, /volkswagen/index.html, etc.
"""
import json, os, re
import xml.etree.ElementTree as ET
import zipfile

# ── Load data ──────────────────────────────────────────────────────────────────
PROJECT_DIR = '/Users/sammihamadeh/Desktop/AutomotiveNL-26/AirbagCrash'
raw_json_path = (
    '/Users/sammihamadeh/.gemini/antigravity/brain/cbd86e4c-0d7d-4cb1-91f6-8cb47dd3ca25/modules_raw.json'
)
with open(raw_json_path, 'r', encoding='utf-8') as f:
  data = json.load(f)

BRANDS_DATA = data.get('brands', [])

# ── Brand display names ────────────────────────────────────────────────────────
BRAND_NAMES = {
    'alfa-romeo': 'Alfa Romeo',
    'audi': 'Audi',
    'bmw': 'BMW',
    'byd': 'BYD',
    'chevrolet': 'Chevrolet',
    'citroen': 'Citroën',
    'dacia': 'Dacia',
    'fiat': 'Fiat',
    'ford': 'Ford',
    'honda': 'Honda',
    'hyundai': 'Hyundai',
    'jaguar': 'Jaguar',
    'jeep': 'Jeep',
    'kia': 'Kia',
    'land-rover': 'Land Rover',
    'mazda': 'Mazda',
    'mercedes': 'Mercedes-Benz',
    'mini': 'Mini',
    'mitsubishi': 'Mitsubishi',
    'nissan': 'Nissan',
    'opel': 'Opel',
    'peugeot': 'Peugeot',
    'renault': 'Renault',
    'seat': 'Seat',
    'skoda': 'Škoda',
    'suzuki': 'Suzuki',
    'tesla': 'Tesla',
    'toyota': 'Toyota',
    'volkswagen': 'Volkswagen',
    'volvo': 'Volvo',
}

# ── Brand descriptions ─────────────────────────────────────────────────────────
BRAND_DESCRIPTIONS = {
    'alfa-romeo': (
        'Wij resetten airbag modules van alle Alfa Romeo modellen. Neem contact'
        ' op met uw onderdeelnummer.'
    ),
    'audi': (
        'Wij resetten Bosch airbag modules voor alle Audi modellen — van de A1'
        ' tot de Q8. Snel, veilig en plug & play.'
    ),
    'bmw': (
        "Professionele airbag module reset voor BMW. Bosch en Autoliv ECU's"
        ' worden volledig hersteld naar fabriekstoestand.'
    ),
    'byd': (
        'Airbag crash data reset voor BYD elektrische voertuigen. Contacteer ons'
        ' voor recente modellen.'
    ),
    'chevrolet': (
        'Wij resetten airbag modules voor alle Chevrolet modellen — inclusief'
        ' Matiz, Spark, Cruze en Captiva.'
    ),
    'citroen': (
        'Bosch, Continental en TRW airbag modules voor alle Citroën modellen'
        ' gereset. Snel en zonder dealer.'
    ),
    'dacia': (
        'Airbag module reset voor alle Dacia modellen. Logan, Sandero, Duster'
        ' en meer.'
    ),
    'fiat': (
        'Fiat airbag modules gereset voor 500, Panda, Punto, Tipo en alle'
        ' andere modellen.'
    ),
    'ford': (
        'Ford airbag reset specialist — van de Fiesta tot de Mondeo en Focus.'
        ' Bosch, TRW en Autoliv.'
    ),
    'honda': (
        'Honda airbag module reset voor alle modellen — Civic, CR-V, HR-V, Jazz'
        ' en meer. 2.221 modules in database.'
    ),
    'hyundai': (
        'Hyundai airbag crash data reset — i20, i30, i40, Tucson, Santa Fe en'
        ' alle andere modellen.'
    ),
    'jaguar': (
        'Jaguar airbag ECU reset voor XE, XF, XJ, F-Pace, E-Pace en I-Pace.'
    ),
    'jeep': (
        'Jeep airbag module reset voor Renegade, Compass, Cherokee, Grand'
        ' Cherokee en meer.'
    ),
    'kia': (
        'Kia airbag reset voor Picanto, Rio, Ceed, Sportage, Sorento en alle'
        ' andere modellen.'
    ),
    'land-rover': (
        'Land Rover & Range Rover airbag module reset — Discovery, Defender,'
        ' Evoque en Sport.'
    ),
    'mazda': (
        'Mazda airbag crash data reset — Mazda 2, 3, 6, CX-3, CX-5, CX-30 en alle'
        ' andere modellen.'
    ),
    'mercedes': (
        'Mercedes-Benz airbag module reset voor A, B, C, E, S-Klasse en alle'
        ' AMG/SUV modellen.'
    ),
    'mini': (
        'Mini airbag module reset — One, Cooper, Cooper S, Clubman en'
        ' Countryman.'
    ),
    'mitsubishi': (
        'Mitsubishi airbag reset voor Colt, Lancer, ASX, Outlander, Eclipse'
        ' Cross en meer.'
    ),
    'nissan': (
        'Nissan airbag crash data reset — van de Micra tot de Qashqai en'
        ' Navara. 1.091 modules beschikbaar.'
    ),
    'opel': (
        'Opel airbag module reset voor Corsa, Astra, Mokka, Insignia, Zafira en'
        ' meer.'
    ),
    'peugeot': (
        'Peugeot airbag module reset — 108, 208, 308, 408, 508, 2008, 3008 en'
        ' alle andere modellen.'
    ),
    'renault': (
        'Renault airbag crash data reset voor Clio, Megane, Scenic, Kadjar,'
        ' Captur en meer.'
    ),
    'seat': (
        'Seat airbag module reset voor Ibiza, Leon, Ateca, Arona, Tarraco en'
        ' alle andere modellen.'
    ),
    'skoda': (
        'Škoda airbag module reset — Fabia, Octavia, Superb, Kodiaq, Karoq en'
        ' meer.'
    ),
    'suzuki': (
        'Suzuki airbag reset voor Alto, Swift, Vitara, S-Cross, Jimny en alle'
        ' andere modellen.'
    ),
    'tesla': 'Tesla airbag module reset voor Model 3, Model S, Model X en Model Y.',
    'toyota': (
        'Toyota airbag crash data reset — van de Yaris tot de Land Cruiser.'
        ' 1.486 modules in database.'
    ),
    'volkswagen': (
        'Volkswagen airbag module reset — Polo, Golf, Passat, Tiguan, T-Roc en'
        ' meer. 800 modules.'
    ),
    'volvo': (
        'Volvo airbag module reset voor V40, V60, V90, XC40, XC60 en XC90.'
    ),
}


# ── Filter BRANDS_DATA against Excel (airbag.xlsx) ─────────────────────────────
def read_xlsx(filename):
  with zipfile.ZipFile(filename, 'r') as z:
    strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
      s_tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
      for si in s_tree:
        texts = [t.text for t in si.iter() if t.tag.endswith('}t') and t.text]
        strings.append(''.join(texts))
    wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
    sheets = []
    for sh in wb_tree.iter():
      if sh.tag.endswith('}sheet'):
        sheets.append((
            sh.attrib.get('name'),
            sh.attrib.get(
                '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
            ),
        ))
    rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rel_map = {}
    for rel in rels_tree:
      rel_map[rel.attrib.get('Id')] = rel.attrib.get('Target')
    first_sheet_id = sheets[0][1]
    target = rel_map[first_sheet_id]
    if not target.startswith('xl/'):
      target = 'xl/' + target
    sheet_tree = ET.fromstring(z.read(target))
    rows = []
    for row in sheet_tree.iter():
      if row.tag.endswith('}row'):
        row_data = []
        for c in row:
          if c.tag.endswith('}c'):
            t = c.attrib.get('t')
            val = ''
            for v in c:
              if v.tag.endswith('}v') and v.text:
                if t == 's':
                  val = strings[int(v.text)]
                else:
                  val = v.text
            row_data.append(val)
        rows.append(row_data)
    return rows


excel_path = os.path.join(PROJECT_DIR, 'airbag.xlsx')
if not os.path.exists(excel_path):
  excel_path = '/Users/sammihamadeh/Downloads/airbag.xlsx'

excel_rows = read_xlsx(excel_path)[1:]
excel_normalized_strings = set()
excel_tokens = set()


def clean_token(s):
  return re.sub(r'[^A-Z0-9]', '', s.upper())


for r in excel_rows:
  for cell in r:
    if cell:
      raw_pn = cell.upper()
      raw_pn = re.sub(r'\([^\)]*\)', '', raw_pn)
      raw_pn = re.sub(r'\b(VIRGIN|DUMP|OBD|BENCH|DIAG)\b', '', raw_pn)
      raw_pn = raw_pn.strip()
      if not raw_pn:
        continue
      excel_normalized_strings.add(clean_token(raw_pn))
      for token in re.split(r'[\s/,-]+', raw_pn):
        cleaned = clean_token(token)
        if len(cleaned) >= 4 and any(c.isdigit() for c in cleaned):
          excel_tokens.add(cleaned)


def item_in_excel(pn, sn):
  tokens_to_check = set()
  for s in [pn, sn]:
    if s:
      s_clean = re.sub(
          r'\b(BOSCH|CONTINENTAL|DENSO|TRW|TEMIC|AUTOLIV|MOBIS|VEONEER|SIEMENS|DELPHI|MARELLI)\b',
          '',
          s,
          flags=re.I,
      )
      norm = clean_token(s_clean)
      if len(norm) >= 4:
        tokens_to_check.add(norm)
      for part in re.split(r'[\s/,-]+', s_clean):
        cleaned = clean_token(part)
        if len(cleaned) >= 4 and any(c.isdigit() for c in cleaned):
          tokens_to_check.add(cleaned)
  return any(
      t in excel_tokens or t in excel_normalized_strings for t in tokens_to_check
  )


filtered_brands_data = []
total_modules_after = 0
brand_counts = {}

for b in BRANDS_DATA:
  slug = b['url'].split('/')[-1]
  new_models = []
  b_after = 0
  for mod in b.get('models', []):
    new_mods = [
        m
        for m in mod.get('modules', [])
        if item_in_excel(m.get('part_number', ''), m.get('supplier_number', ''))
    ]
    if new_mods:
      mod_copy = dict(mod)
      mod_copy['modules'] = new_mods
      new_models.append(mod_copy)
      b_after += len(new_mods)
  b_copy = dict(b)
  b_copy['models'] = new_models
  b_copy['total_modules'] = b_after
  filtered_brands_data.append(b_copy)
  brand_counts[slug] = b_after
  total_modules_after += b_after

BRANDS_DATA = filtered_brands_data

with open(
    os.path.join(PROJECT_DIR, 'modules_filtered.json'), 'w', encoding='utf-8'
) as f:
  json.dump(
      {'brands': BRANDS_DATA, 'total_modules': total_modules_after},
      f,
      ensure_ascii=False,
      indent=2,
  )


# ── Synchronize modules-data.js, index.html, and main.js ───────────────────────
def sync_site_data():
  db_items = []
  for b in BRANDS_DATA:
    b_slug = b['url'].split('/')[-1]
    for mod in b.get('models', []):
      mod_name = mod.get('model', '')
      for m in mod.get('modules', []):
        pn = m.get('part_number', '').strip()
        sn = m.get('supplier_number', '').strip()
        raw_str = f'{pn} - {sn}'.strip(' -')
        db_items.append({
            'brand': b_slug,
            'model': mod_name,
            'part_number': pn,
            'supplier_number': sn,
            'raw': raw_str,
        })
  out_js = os.path.join(PROJECT_DIR, 'modules-data.js')
  with open(out_js, 'w', encoding='utf-8') as f:
    f.write(
        'const MODULE_DB='
        + json.dumps(db_items, separators=(',', ':'))
        + ';\n'
    )
  print(
      f'✓ Synchronized modules-data.js with {len(db_items):,} Excel-matched'
      ' items'
  )

  index_path = os.path.join(PROJECT_DIR, 'index.html')
  with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

  total_str = f'{total_modules_after:,}'.replace(',', '.')
  html = re.sub(r'16\.878', total_str, html)

  for slug, count in brand_counts.items():
    count_str = (
        f"{f'{count:,}'.replace(',', '.')} modules" if count else 'Op aanvraag'
    )
    html = re.sub(
        rf'(<a href="/{slug}/" class="brand-card" data-brand="{slug}">\s*<span>.*?</span>\s*<span class="brand-card__count">).*?(</span>\s*</a>)',
        rf'\g<1>{count_str}\2',
        html,
    )
    opt_str = f'{count:,}'.replace(',', '.') if count else 'Op aanvraag'
    html = re.sub(
        rf'(<option value="{slug}">).*?(</option>)',
        rf'\g<1>{BRAND_NAMES.get(slug, slug.title())} ({opt_str})\2',
        html,
    )

  with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
  print(
      f'✓ Synchronized index.html total ({total_str}) and brand counts'
  )

  main_path = os.path.join(PROJECT_DIR, 'main.js')
  with open(main_path, 'r', encoding='utf-8') as f:
    js = f.read()
  js = re.sub(
      r'Typ om te zoeken in \d+[\.,]?\d* modules\.\.\.',
      f'Typ om te zoeken in {total_str} modules...',
      js,
  )
  with open(main_path, 'w', encoding='utf-8') as f:
    f.write(js)
  print(f'✓ Synchronized main.js placeholder ({total_str})')


sync_site_data()

# ── All brand slugs list (for "other brands" section) ─────────────────────────
ALL_SLUGS = [b['url'].split('/')[-1] for b in BRANDS_DATA]


def render_model_section(model_name, modules):
    """Render one model accordion card with all its module numbers."""
    count = len(modules)
    rows = ''
    for m in modules:
        pn = m.get('part_number', '').strip()
        sn = m.get('supplier_number', '').strip()
        rows += f'''
          <tr>
            <td class="bp__pn">{pn}</td>
            <td class="bp__sn">{sn}</td>
            <td>
              <a href="#contact" class="btn btn--blue" style="padding:6px 14px; font-size:0.78rem; white-space:nowrap;">
                Aanmelden
              </a>
            </td>
          </tr>'''

    return f'''
    <div class="bp__model-card">
      <button class="bp__model-btn" aria-expanded="false">
        <span class="bp__model-name">{model_name}</span>
        <span class="bp__model-count">{count} modules</span>
        <svg class="bp__model-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </button>
      <div class="bp__model-content">
        <div class="bp__model-inner">
          <table class="bp__table">
            <thead>
              <tr>
                <th>OEM Onderdeelnummer</th>
                <th>Leverancier / ECU Code</th>
                <th></th>
              </tr>
            </thead>
            <tbody>{rows}
            </tbody>
          </table>
        </div>
      </div>
    </div>'''


def other_brands_html(current_slug):
    links = ''
    for b in BRANDS_DATA:
        slug = b['url'].split('/')[-1]
        if slug == current_slug:
            continue
        name = BRAND_NAMES.get(slug, slug.title())
        total = b.get('total_modules', 0)
        count_str = f'{total:,}'.replace(',', '.') if total else 'Op aanvraag'
        links += f'''
        <a href="/{slug}/" class="bp__other-card">
          <span class="bp__other-name">{name}</span>
          <span class="bp__other-count">{count_str}</span>
        </a>'''
    return links


def generate_page(brand_obj):
    slug = brand_obj['url'].split('/')[-1]
    name = BRAND_NAMES.get(slug, slug.title())
    desc = BRAND_DESCRIPTIONS.get(slug, f'Professionele airbag crash data reset voor alle {name} modellen.')
    models = brand_obj.get('models', [])
    total_modules = brand_obj.get('total_modules', 0)

    # Build model sections
    if models:
        model_sections = '\n'.join(render_model_section(m['model'], m['modules']) for m in models)
        db_block = f'''
      <div class="bp__models" id="bp-models">
        {model_sections}
      </div>'''
        no_data_note = ''
    else:
        # Alfa Romeo etc. — no numbered list
        db_block = ''
        no_data_note = '''
      <div class="bp__no-list">
        <div class="bp__no-list-inner">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          <h3>Stuur uw onderdeelnummer op</h3>
          <p>Voor dit merk controleren wij uw module handmatig. Stuur het onderdeelnummer via WhatsApp of het contactformulier — u ontvangt binnen 2 uur reactie.</p>
          <a href="https://wa.me/31652619000" target="_blank" rel="noopener" class="btn btn--wa btn--lg">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
            Stuur module nummer via WhatsApp
          </a>
        </div>
      </div>'''

    module_count_str = f'{total_modules:,}'.replace(',', '.') if total_modules else ''
    module_badge = f'<span class="section-header__badge">{module_count_str} modules</span>' if total_modules else ''
    other_brands = other_brands_html(slug)

    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} Airbag Crash Data Reset | Vanaf €99,- | AirbagCrashReset.nl</title>
  <meta name="description" content="{name} airbag module reset service. {desc} Binnen 24 uur, 100% veilig, plug & play. Vanaf €99,-.">
  <link rel="canonical" href="https://www.airbagcrashreset.nl/{slug}/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <link rel="stylesheet" href="../brand-page.css">
</head>
<body>

  <!-- ── TOP INFO BAR ── -->
  <div class="topbar">
    <div class="wrap topbar__inner">
      <ul class="topbar__list">
        <li>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          <span>100% Veilige Crash Data Verwijdering</span>
        </li>
        <li>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Binnen 24 uur klaar</span>
        </li>
      </ul>
      <div class="topbar__contact">
        <a href="tel:0652619000">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
          06-52619000
        </a>
      </div>
    </div>
  </div>

  <!-- ── NAVBAR ── -->
  <header class="header" id="header">
    <div class="wrap header__inner">
      <a href="/" class="logo" aria-label="AirbagCrashReset.nl Home">
        <span class="logo__airbag">AIRBAG</span><span class="logo__crash">CRASH</span><span class="logo__reset">RESET</span>
        <span class="logo__badge">PRO</span>
      </a>
      <nav class="nav" aria-label="Hoofdmenu">
        <ul>
          <li><a href="/#werkwijze">Werkwijze</a></li>
          <li><a href="/#merken">Merken</a></li>
          <li><a href="/#prijzen">Tarieven</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/#contact">Contact</a></li>
        </ul>
      </nav>
      <div class="header__actions">
        <a href="https://wa.me/31652619000" target="_blank" rel="noopener" class="btn btn--wa">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          WhatsApp
        </a>
        <a href="/#contact" class="btn btn--primary">Module Resetten</a>
      </div>
      <button class="burger" id="burger-btn" aria-label="Menu openen" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <!-- ── BREADCRUMB ── -->
  <div class="bp__breadcrumb">
    <div class="wrap">
      <nav aria-label="Breadcrumb">
        <ol class="bp__breadcrumb-list">
          <li><a href="/">Home</a></li>
          <li><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></li>
          <li><a href="/#merken">Merken</a></li>
          <li><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></li>
          <li aria-current="page">{name}</li>
        </ol>
      </nav>
    </div>
  </div>

  <!-- ── BRAND HERO ── -->
  <section class="bp__hero">
    <div class="wrap bp__hero-inner">
      <div class="bp__hero-content">
        <div class="hero__tag">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          <span>Airbag Crash Data Reset</span>
        </div>
        <h1 class="bp__hero-title">{name} <span class="hero__title-accent">Airbag Reset</span></h1>
        <p class="bp__hero-sub">{desc}</p>

        <div class="bp__hero-pills">
          <span class="bp__pill bp__pill--green">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Binnen 24 uur
          </span>
          <span class="bp__pill bp__pill--blue">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Plug & play
          </span>
          <span class="bp__pill bp__pill--yellow">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Vanaf €99,-
          </span>
          <span class="bp__pill bp__pill--blue">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            99% Slagingspercentage
          </span>
        </div>

        <div class="bp__hero-btns">
          <a href="/#contact" class="btn btn--primary btn--lg">
            <span>Module Aanmelden</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </a>
          <a href="https://wa.me/31652619000" target="_blank" rel="noopener" class="btn btn--wa btn--lg">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
            WhatsApp
          </a>
        </div>
      </div>

      <!-- Info card -->
      <div class="bp__hero-card">
        <div class="hero__card-top">
          <span class="hero__card-badge">{name.upper()} DATABASE</span>
          <div class="hero__card-price">
            <div class="hero__card-price-val">€99,-</div>
            <div class="hero__card-price-sub">incl. garantie & test</div>
          </div>
        </div>
        <h3>{name} Airbag Modules</h3>
        <p>Wij ondersteunen {f'{total_modules:,}'.replace(',', '.') if total_modules else 'diverse'} {name} airbag modules. Zoek uw part number in de lijst hieronder of neem direct contact op.</p>
        <div class="hero__db-lookup">
          <span class="hero__db-label">Uw module wordt getest na reset:</span>
          <div class="hero__db-code">
            <span>Bosch / TRW / Continental</span>
            <span style="color: #10B981;">✓ SUPPORTED</span>
          </div>
        </div>
        <div class="hero__card-footer">
          <span style="font-size:0.82rem; color: rgba(255,255,255,0.7);">Heerlen • Per post of op afspraak</span>
          <a href="/#contact" class="hero__card-link">
            <span>Aanmelden</span>
            <span>→</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- ── MODULE DATABASE ── -->
  <section class="bp__db" id="onderdeelnummers">
    <div class="wrap">
      <div class="section-header">
        <h2>Ondersteunde {name} Modules</h2>
        {module_badge}
      </div>
      <p class="section-sub">
        Zoek uw OEM-onderdeelnummer of leverancierscode in de lijst hieronder. Staat uw module erbij? Dan kunt u hem direct aanmelden voor reset.
      </p>

      <!-- Inline search for this brand page -->
      <div class="bp__search-wrap">
        <div class="mdb__search-main" style="max-width:560px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="bp-search" placeholder="Zoek op onderdeelnummer of model (bijv. A4, 8K0 959 655)..." autocomplete="off" spellcheck="false">
        </div>
      </div>

      <div id="bp-search-status" class="mdb__status" style="margin-bottom:20px; display:none;">
        <span class="mdb__count-badge" id="bp-search-count"></span>
      </div>

      {no_data_note}
      {db_block}
    </div>
  </section>

  <!-- ── WHY US (reuse main style) ── -->
  <section class="why" style="padding:70px 0;">
    <div class="wrap">
      <div class="section-header">
        <h2>Waarom Kiezen voor Ons?</h2>
        <span class="section-header__badge">Voordelen</span>
      </div>
      <div class="why__grid">
        <div class="why-card why-card--blue">
          <div>
            <div class="why-card__tag">VEILIGHEID</div>
            <h3>99% Slagingspercentage</h3>
            <p>Uitsluitend crash data verwijderd op chip-niveau. Originele codering behouden. Getest voor montage.</p>
          </div>
          <a href="/#contact" class="why-card__btn"><span>Aanmelden</span><span>→</span></a>
        </div>
        <div class="why-card why-card--emerald">
          <div>
            <div class="why-card__tag">SNELHEID</div>
            <h3>Binnen 24 Uur Klaar</h3>
            <p>Geen weken wachten. Module vandaag opgestuurd = morgen gereset en retour.</p>
          </div>
          <a href="https://wa.me/31652619000" target="_blank" rel="noopener" class="why-card__btn"><span>WhatsApp</span><span>→</span></a>
        </div>
        <div class="why-card why-card--white">
          <div>
            <div class="why-card__tag" style="color:var(--clr-blue);">BESPARING</div>
            <h3>Tot 80% Goedkoper</h3>
            <p>Dealer module kost €500-€1.200. Onze reset kost slechts €99 of €149. U behoudt uw originele module.</p>
          </div>
          <a href="/#prijzen" class="why-card__btn"><span>Tarieven bekijken</span><span>→</span></a>
        </div>
      </div>
    </div>
  </section>

  <!-- ── OTHER BRANDS ── -->
  <section class="bp__other-brands">
    <div class="wrap">
      <div class="section-header">
        <h2>Andere Automerken</h2>
        <a href="/#merken" class="section-header__badge" style="text-decoration:none;">Alle 29 merken →</a>
      </div>
      <div class="bp__other-grid">
        {other_brands}
      </div>
    </div>
  </section>

  <!-- ── CONTACT ── -->
  <section class="contact" id="contact">
    <div class="wrap">
      <div class="section-header">
        <h2>Module Aanmelden</h2>
        <span class="section-header__badge">Direct Reset</span>
      </div>
      <div class="contact__grid">
        <div>
          <h3 style="font-family: var(--font-heading); font-size: 1.4rem; font-weight:800; margin-bottom: 12px;">{name} Airbag Reset — Heerlen</h3>
          <p style="font-size: 0.95rem; color:var(--clr-text-sub); line-height: 1.7;">
            Meld uw {name} airbag module direct aan. Vermeld het onderdeelnummer uit de lijst hierboven in het bericht voor de snelste service.
          </p>
          <div class="contact__info-cards">
            <div class="contact__info-item">
              <div class="contact__info-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
              </div>
              <div>
                <div class="contact__info-label">Telefoon / WhatsApp</div>
                <div class="contact__info-val"><a href="tel:0652619000">06 - 52 61 90 00</a></div>
              </div>
            </div>
            <div class="contact__info-item">
              <div class="contact__info-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              </div>
              <div>
                <div class="contact__info-label">E-mail</div>
                <div class="contact__info-val"><a href="mailto:info@airbagcrashreset.nl">info@airbagcrashreset.nl</a></div>
              </div>
            </div>
          </div>
        </div>

        <div class="contact-form-wrap">
          <form id="contact-form" class="contact-form" novalidate>
            <div class="form-row">
              <div class="form-group">
                <label for="name">Uw Naam *</label>
                <input type="text" id="name" name="name" placeholder="bijv. Jan Jansen" required>
              </div>
              <div class="form-group">
                <label for="phone">Telefoonnummer *</label>
                <input type="tel" id="phone" name="phone" placeholder="06-12345678" required>
              </div>
            </div>
            <div class="form-group">
              <label for="email">E-mailadres *</label>
              <input type="email" id="email" name="email" placeholder="uw@email.nl" required>
            </div>
            <div class="form-group">
              <label for="partnr">Onderdeelnummer {name}</label>
              <input type="text" id="partnr" name="partnr" placeholder="Selecteer uit de lijst hierboven...">
            </div>
            <div class="form-group">
              <label for="message">Opmerking</label>
              <textarea id="message" name="message" rows="3" placeholder="Beschrijf kort het probleem..."></textarea>
            </div>
            <button type="submit" class="btn btn--primary btn--lg btn--block">
              <span class="btn__text">Aanvraag Versturen</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
            <div id="form-success" class="form-success" aria-live="polite"></div>
          </form>
        </div>
      </div>
    </div>
  </section>

  <!-- ── FOOTER ── -->
  <footer class="footer">
    <div class="wrap">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="/" class="logo" style="color:#FFFFFF;">
            <span>AIRBAG</span><span style="color:#007FFF;">CRASH</span><span>RESET</span>
            <span class="logo__badge">PRO</span>
          </a>
          <p>Specialist in airbag crash data reset. Alle {name} modellen ondersteund.</p>
        </div>
        <div class="footer__links">
          <div class="footer__col">
            <h3>Navigatie</h3>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/#werkwijze">Werkwijze</a></li>
              <li><a href="/#merken">Merken</a></li>
              <li><a href="/#prijzen">Tarieven</a></li>
            </ul>
          </div>
          <div class="footer__col">
            <h3>Contact</h3>
            <ul>
              <li><a href="tel:0652619000">06-52619000</a></li>
              <li><a href="https://wa.me/31652619000">WhatsApp</a></li>
              <li><a href="mailto:info@airbagcrashreset.nl">info@airbagcrashreset.nl</a></li>
            </ul>
          </div>
          <div class="footer__col">
            <h3>Adres</h3>
            <ul>
              <li>In de Cramer 29c</li>
              <li>6411 RS Heerlen</li>
              <li><a href="https://www.autodiagnose.nl" target="_blank" style="color:var(--clr-yellow);">AutoDiagnose.nl →</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <div class="footer__bottom-inner">
          <div>© 2026 AirbagCrashReset.nl</div>
          <div class="footer__bottom-links">
            <a href="/#contact">Contact</a>
          </div>
        </div>
      </div>
    </div>
  </footer>

  <a href="https://wa.me/31652619000" target="_blank" rel="noopener" class="fab-wa" aria-label="WhatsApp">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
  </a>

  <script src="../brand-page.js"></script>
</body>
</html>'''
    return html


# ── Generate all brand pages ───────────────────────────────────────────────────
generated = []
for brand_obj in BRANDS_DATA:
    slug = brand_obj['url'].split('/')[-1]
    out_dir = os.path.join(PROJECT_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    html = generate_page(brand_obj)
    out_path = os.path.join(out_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    total = brand_obj.get('total_modules', 0)
    generated.append(slug)
    print(f'  ✓ /{slug}/  ({total} modules)')

print(f'\nGenerated {len(generated)} brand pages!')
