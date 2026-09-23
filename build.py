import re, glob, html, subprocess, pathlib
src = glob.glob("/Users/avilevi/Documents/avi-workspace/HRIS/*.md")[0]
s = open(src, encoding="utf-8").read()
fm = re.match(r"^---\n(.*?)\n---\n", s, re.S).group(1)
body = s[re.match(r"^---\n.*?\n---\n", s, re.S).end():]
# drop the H1 (the page header carries it) and the trailing italics line
body = re.sub(r"^# .*?\n", "", body.lstrip(), count=1)
body = body.replace("\n\n> **ההקשר של המסמך.**", "\n\n<!-- -->\n\n> **ההקשר של המסמך.**")
pathlib.Path("body.md").write_text(body, encoding="utf-8")
subprocess.run(["npx","--yes","marked","--gfm","-i","body.md","-o","body.html"], check=True)
h = open("body.html", encoding="utf-8").read()
# mermaid
def mer(m): return '<pre class="mermaid">'+html.unescape(m.group(1))+'</pre>'
h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', mer, h, flags=re.S)
# heading ids + toc
toc=[]; counter=[0]
def hid(m):
    lvl, txt = m.group(1), m.group(2)
    counter[0]+=1; i=f"s{counter[0]}"
    plain=re.sub(r"<.*?>","",txt)
    toc.append((int(lvl), i, plain))
    return f'<h{lvl} id="{i}">{txt}</h{lvl}>'
h = re.sub(r'<h([23])>(.*?)</h\1>', hid, h)
# wrap tables for horizontal scroll
h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
# callouts: first two blockquotes are glossary + context
h = h.replace("<blockquote>", '<blockquote class="callout">')
toc_html = "".join(f'<a class="l{l}" href="#{i}">{t}</a>' for l,i,t in toc if l==2)
import components
h = components.apply(h)
tpl = open("template.html", encoding="utf-8").read()
out = tpl.replace("{{BODY}}", h).replace("{{TOC}}", toc_html)
pathlib.Path("index.html").write_text(out, encoding="utf-8")
print("index.html", len(out), "bytes; toc", len(toc))
