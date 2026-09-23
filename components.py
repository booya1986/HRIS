import re, html

def h3_text_to_id(h, needle):
    m = re.search(r'<h3 id="(s\d+)">([^<]*' + re.escape(needle) + r'[^<]*)</h3>', h)
    return m.group(1) if m else None

def section_span(h, hid, stop_levels=("h2","h3")):
    """return (start, end) indices for heading with id hid up to the next h2/h3"""
    m = re.search(r'<h[23] id="' + hid + r'">', h)
    start = m.start()
    nxt = re.search(r'<h[23] id="', h[m.end():])
    end = m.end() + nxt.start() if nxt else len(h)
    return start, end

def stepper(h):
    step = '''
<div class="stepper" role="list">
  <button class="step" data-go="opt1" role="listitem"><span class="n">שלב 1</span><b>Core HRIS</b><small>מערכת רשומה אמינה · 3 עד 5 אנשים</small></button>
  <div class="cond">תנאי מעבר, נתונים נקיים, מילון הגדרות, ממשק שכר יציב</div>
  <button class="step" data-go="opt2" role="listitem"><span class="n">שלב 2</span><b>HRIS + People Analytics</b><small>מערכת ועוד צוות אנליטיקה · 6 עד 10 אנשים</small></button>
  <div class="cond">תנאי מעבר, ערך מוכח, ביקוש שעולה על ההיצע, ממשל AI</div>
  <button class="step" data-go="opt3" role="listitem"><span class="n">שלב 3</span><b>Full-stack HR Tech</b><small>כל מחסנית ה-HR Tech כמוצר · 10 ומעלה, Product Owner</small></button>
</div>'''
    return re.sub(r'<pre class="mermaid">.*?</pre>', step, h, count=1, flags=re.S)

def calculator(h):
    hid = h3_text_to_id(h, "כמה אנשים")
    s, e = section_span(h, hid)
    sec = h[s:e]
    calc = '''
<div class="calc">
  <div class="calc-h"><b>מחשבון גודל צוות אנליטיקה</b><span>לפי היחסים של Insight222. גררו את הסליידר לגודל הארגון</span></div>
  <div class="calc-row"><label for="orgsize">עובדים בארגון</label><input id="orgsize" type="range" min="1000" max="100000" step="500" value="10000"><output id="orgout">10,000</output></div>
  <div class="calc-out">
    <div><small>צוות בשנה הראשונה (1 ל-4,800)</small><b id="c1">2</b></div>
    <div><small>צוות ותיק (1 ל-2,700)</small><b id="c2">4</b></div>
    <div><small>ממוצע 2025 (1 ל-2,500)</small><b id="c3">4</b></div>
  </div>
  <p class="calc-note">זה צד האנליטיקה בלבד. את צד המערכות (קונפיגורציה, הרשאות, ממשקים) מוסיפים מעל.</p>
</div>'''
    i = sec.find('<div class="tbl">')
    sec = sec[:i] + calc + sec[i:]
    return h[:s] + sec + h[e:]

def option_tabs(h):
    ids = [h3_text_to_id(h, f"אופציה {n}.") for n in (1,2,3)]
    spans = [section_span(h, i) for i in ids]
    labels = [("שלב 1","Core HRIS","3 עד 5 אנשים"),("שלב 2","HRIS + People Analytics","6 עד 10 אנשים"),("שלב 3","Full-stack HR Tech","10 ומעלה")]
    bar = '<div class="tabbar" role="tablist">' + "".join(
        f'<button role="tab" class="tab{" on" if k==1 else ""}" data-tab="opt{k+1}" aria-selected="{"true" if k==1 else "false"}"><span>{a}</span><b>{b}</b><small>{c}</small></button>'
        for k,(a,b,c) in enumerate(labels)) + '</div>'
    panels = "".join(f'<section class="panel{" on" if k==1 else ""}" id="opt{k+1}" role="tabpanel">{h[s:e]}</section>' for k,(s,e) in enumerate(spans))
    block = f'<div class="opts">{bar}{panels}</div>'
    return h[:spans[0][0]] + block + h[spans[2][1]:]

def weight(h):
    hid = h3_text_to_id(h, "אז כמה משקל")
    s, e = section_span(h, hid)
    sec = h[s:e]
    vis = '''
<figure class="weight">
  <figcaption>משקל פונקציית הדאטה מתוך היחידה, לפי שלב. הערכה שלי על סמך הראיות</figcaption>
  <div class="wrow"><span>שלב 1 · Core HRIS</span><div class="wbar"><i style="--w:25%"></i></div><b>כרבע</b></div>
  <div class="wrow"><span>שלב 2 · HRIS + People Analytics</span><div class="wbar"><i style="--w:55%"></i></div><b>לפחות חצי</b></div>
  <div class="wrow"><span>שלב 3 · Full-stack HR Tech</span><div class="wbar"><i style="--w:100%"></i></div><b>הסיבה שהיחידה קיימת</b></div>
</figure>'''
    i = sec.find('</p>') + 4
    return h[:s] + sec[:i] + vis + sec[i:] + h[e:]

def parse_table(tbl_html):
    rows = re.findall(r'<tr>(.*?)</tr>', tbl_html, flags=re.S)
    out=[]
    for r in rows:
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S)
        out.append([c.strip() for c in cells])
    return out[0], out[1:]

def value_map(h):
    hid = h3_text_to_id(h, "מפת ערך")
    s, e = section_span(h, hid)
    sec = h[s:e]
    m = re.search(r'<div class="tbl"><table>.*?</table></div>', sec, flags=re.S)
    head, rows = parse_table(m.group(0))
    cols = {}; order=[]; cur=None
    for r in rows:
        if r[0].strip():
            cur = re.sub(r'<.*?>','',r[0]); order.append(cur); cols[cur]=[]
        cols[cur].append(r[1:])
    out = '<div class="vmap">'
    for c in order:
        out += f'<div class="vcol"><h4>{c}</h4>'
        for what, why, cond in cols[c]:
            out += f'<div class="vcard"><b>{what}</b><p>{why}</p><p class="vcond"><span>תנאי</span> {cond}</p></div>'
        out += '</div>'
    out += '</div>'
    sec = sec[:m.start()] + out + sec[m.end():]
    return h[:s] + sec + h[e:]

def kpi_tabs(h):
    hid = h3_text_to_id(h, "מסגרת המדידה")
    s, e = section_span(h, hid)
    sec = h[s:e]
    # goal blocks
    pat = re.compile(r'<p><strong>יעד (\d)\. (.*?)</strong>(.*?)</p>\s*<div class="tbl"><table>.*?</table></div>', re.S)
    blocks = list(pat.finditer(sec))
    assert len(blocks)==5, len(blocks)
    bar = '<div class="tabbar kpi" role="tablist">' + "".join(
        f'<button role="tab" class="tab{" on" if k==0 else ""}" data-tab="goal{b.group(1)}" aria-selected="{"true" if k==0 else "false"}"><span>יעד {b.group(1)}</span><b>{b.group(2).rstrip(".")}</b></button>'
        for k,b in enumerate(blocks)) + '</div>'
    filt = '<div class="stagefilter"><span>הצג לפי שלב</span><button class="on" data-stage="all">הכל</button><button data-stage="1">שלב 1</button><button data-stage="2">שלב 2</button><button data-stage="3">שלב 3</button></div>'
    panels = "".join(f'<section class="panel{" on" if k==0 else ""}" id="goal{b.group(1)}" role="tabpanel">{b.group(0)}</section>' for k,b in enumerate(blocks))
    block = f'<div class="opts kpiwrap">{filt}{bar}{panels}</div>'
    sec = sec[:blocks[0].start()] + block + sec[blocks[-1].end():]
    # timeline: the table after "איך יודעים שהצלחנו, לפי שנים"
    m = re.search(r'(<p><strong>איך יודעים שהצלחנו, לפי שנים\.</strong></p>\s*)<div class="tbl"><table>.*?</table></div>', sec, flags=re.S)
    head, rows = parse_table(m.group(0))
    tl = '<div class="timeline">' + "".join(f'<div class="tcard"><span class="dot"></span><b>{r[0]}</b><p>{r[1]}</p></div>' for r in rows) + '</div>'
    sec = sec[:m.start()] + m.group(1) + tl + sec[m.end():]
    return h[:s] + sec + h[e:]

def premortem(h):
    hid = h3_text_to_id(h, "פרה מורטם")
    s, e = section_span(h, hid)
    sec = h[s:e]
    pat = re.compile(r'<p><strong>סיפור (\d)\. (.*?)</strong>(.*?)</p>', re.S)
    ms = list(pat.finditer(sec)); assert len(ms)==3
    cards = '<div class="pm">' + "".join(f'<div class="pmcard"><span class="n">0{m.group(1)}</span><b>{m.group(2)}</b><p>{m.group(3).strip()}</p></div>' for m in ms) + '</div>'
    sec = sec[:ms[0].start()] + cards + sec[ms[-1].end():]
    return h[:s] + sec + h[e:]

def apply(h):
    for f in (stepper, calculator, option_tabs, weight, value_map, kpi_tabs, premortem):
        h = f(h)
    return h

ILL = [
 # (needle in h2/h3 text, file, hebrew caption, place: 'after-heading' | 'before-tbl' )
 ("שלוש אופציות מבנה, מתפתחות", "stages.png", "שלושת השלבים. כל שלב מכיל את הקודם, והמעבר מותנה בנתונים נקיים ובערך מוכח."),
 ("השכר הוא העוגן", "payroll-anchor.png", "הארכיטקטורה הישראלית הרווחת. ליבת HR גלובלית, ממשק, ומנוע שכר מקומי. הממשק הוא החוליה השבירה."),
 ("נקודות עיוורות למי שמגיע מעולם הלמידה", "treadmill.png", "אין השקה. הספק משחרר גרסאות חובה פעמיים בשנה, וכל שחרור דורש רגרסיה."),
 ("הכשל השקט, התאמת מצבה", "headcount.png", "HR וכספים סופרים אחרת ושניהם צודקים. מילון הגדרות משותף הוא הדבר הראשון שהיחידה כותבת."),
 ("מי מרוויח, מי מפסיד", "queue.png", "תור הבקשות בולע צוותים קטנים. intake, SLA ובעלים מהיום הראשון."),
]
def illustrations(h):
    import os
    for needle, fn, cap in ILL:
        if not os.path.exists(os.path.join("assets", fn)): continue
        m = re.search(r'(<h[23] id="s\d+">[^<]*' + re.escape(needle) + r'[^<]*</h[23]>)', h)
        if not m: continue
        fig = f'<figure class="ill"><img src="assets/{fn}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
        h = h[:m.end()] + fig + h[m.end():]
    return h
_apply = apply
def apply(h):
    return illustrations(_apply(h))
