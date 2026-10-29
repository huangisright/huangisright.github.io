#!/usr/bin/env python3
"""build.py — 由 data.json 產生 IsRight 入口的所有頁面。

用法：python3 build.py        （在這個資料夾裡跑；會寫出 index.html 與 c/*.html）

- 首頁只放分類卡片，點了進到 c/<分類>.html，不在首頁展開。
- 「未完成」＝ data.json 的 drafts（多半是 Claude 上做的試作版，檔案在 draft/）。
  確認完成時：把 draft/<slug>.html 搬到 <分類 id>/，再把那一筆從 drafts 移到該分類的 items。
- 「GitHub 專案」＝ data.json 的 repos。
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
esc = lambda s: html.escape(str(s), quote=True)

DOODLES = {
  "hand": '<path d="M8 40 L30 12 L52 38 Z"/><circle cx="30" cy="12" r="3.2"/><path d="M33 15 L41 9"/><path d="M41 9 L39 4 M41 9 L46 7"/><path d="M20 28 C26 25 34 25 40 27"/>',
  "tools": '<path d="M13 40 L36 16"/><circle cx="41" cy="11" r="6.5"/><path d="M19 13 L44 39"/><path d="M44 39 L47 43 L42 42 Z"/>',
  "geo": '<path d="M9 41 L30 7 L52 40 L10 41.5"/><circle cx="30.5" cy="29" r="9"/><circle cx="30.5" cy="29" r="1"/>',
  "iso": '<ellipse cx="30" cy="25" rx="25" ry="17"/><ellipse cx="29" cy="26" rx="16" ry="10.5"/><ellipse cx="29" cy="26" rx="7" ry="4.5"/><circle cx="29" cy="26" r="1.2"/>',
  "door": '<path d="M16 43 L15.5 7 L44 6 L45 43"/><circle cx="38" cy="24" r="3"/><path d="M38 27 L38 32"/><path d="M8 43 L53 43"/>',
  "wind": '<path d="M5 15 C18 10 33 20 46 13 C52 10 54 17 49 18"/><path d="M9 26 C24 21 38 30 54 23"/><path d="M5 37 C19 32 33 41 45 35 C51 32 53 39 48 40"/>',
  "list": '<path d="M9 9 L17 9 L17 17 L9 17 Z"/><path d="M11 13 L13 15.5 L19 7"/><path d="M24 13 L52 12"/><path d="M9 25 L17 25 L17 33 L9 33 Z"/><path d="M11 29 L13 31.5 L19 23"/><path d="M24 29 L46 29.5"/><path d="M9 41 L17 41 L17 47 L9 47"/><path d="M24 44 L50 43"/>',
  "draft": '<path d="M12 40 L40 12 L47 19 L19 47 L10 49 Z"/><path d="M36 16 L43 23"/><path d="M6 8 C14 6 20 10 26 7"/>',
  "repo": '<circle cx="16" cy="10" r="4.5"/><circle cx="16" cy="40" r="4.5"/><circle cx="42" cy="18" r="4.5"/><path d="M16 14.5 L16 35.5"/><path d="M42 22.5 C42 32 26 28 17 36"/>',
}

CSS = """
:root{--paper:#fdfcf8;--ink:#1b1b1b;--pencil:#77756f;--faint:#d9d6cc;--marker:#d4472b;--hl:#fff2a8;
--title:"IsRight Hand","LXGW WenKai TC","Kaiti TC","KaiTi",serif;
--wob:255px 15px 225px 15px/15px 225px 15px 255px;--wob2:15px 255px 15px 225px/225px 15px 255px 15px}
@media (prefers-color-scheme:dark){:root{--paper:#1c1d1f;--ink:#ecebe6;--pencil:#9c9a93;--faint:#3a3b3e;--marker:#ff7a5c;--hl:#4a4320}}
*{box-sizing:border-box}html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.6 "LXGW WenKai TC","Kaiti TC","KaiTi",serif}
.wrap{max-width:900px;margin:0 auto;padding:30px 16px 70px}
a{color:inherit}
.crumb{font-size:15px;color:var(--pencil)}.crumb a{text-decoration:underline dotted}
header{display:flex;align-items:flex-end;gap:14px;flex-wrap:wrap;margin-top:8px}
h1{font-family:var(--title);margin:0;font-size:42px;font-weight:700;line-height:1.1}
.sub{color:var(--pencil);font-size:16px;margin:6px 0 0}
.doodle-me{width:64px;height:64px;flex:none;stroke:var(--ink);fill:none;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
#q{width:100%;font:inherit;font-size:17px;color:var(--ink);background:transparent;border:2px solid var(--ink);border-radius:var(--wob);padding:9px 14px;outline:none;margin:24px 0 4px}
#q:focus{background:var(--hl)}
.shelf{margin-top:30px}
.shelf h2{font-family:var(--title);font-size:26px;margin:0 0 12px;font-weight:700;display:inline-block;padding:0 6px;background:linear-gradient(transparent 55%,var(--hl) 55%)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:18px}
a.card{text-decoration:none;border:2.5px solid var(--ink);border-radius:var(--wob);padding:14px 14px 12px;display:flex;flex-direction:column;gap:4px;transition:transform .12s}
a.card:nth-child(even){border-radius:var(--wob2)}
a.card:hover{transform:rotate(-1deg);background:var(--hl)}
a.card:nth-child(even):hover{transform:rotate(1deg)}
a.card svg{width:60px;height:48px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.card .n{font-family:var(--title);font-size:23px;font-weight:700}
.card .c{font-size:14px;color:var(--pencil)}
.card.dashed{border-style:dashed}
.note{color:var(--pencil);font-size:16px;margin:6px 0 0}
.scribble{height:10px;width:180px;margin:6px 0 10px}.scribble path{stroke:var(--marker);stroke-width:3;fill:none;stroke-linecap:round}
ul.items{list-style:none;margin:0;padding:0}
ul.items li{display:flex;align-items:baseline;gap:10px;padding:9px 2px;border-bottom:1.5px dashed var(--faint);flex-wrap:wrap}
ul.items li::before{content:"→";color:var(--pencil);flex:none}
ul.items li.sub{border:none;padding:18px 0 2px;font-size:15px;color:var(--pencil);letter-spacing:.08em}
ul.items li.sub::before{content:""}
h3.grp{font-family:var(--title);font-size:24px;margin:26px 0 4px}
ul.items a{text-decoration:none;font-size:19px;background-image:linear-gradient(var(--ink),var(--ink));background-size:0 2px;background-repeat:no-repeat;background-position:0 100%;transition:background-size .2s}
ul.items a:hover{background-size:100% 2px}
.d{color:var(--pencil);font-size:15px}
.tag{font-size:13px;color:var(--marker);border:1.5px solid var(--marker);border-radius:var(--wob2);padding:0 7px;line-height:1.6}
.tag.c{color:var(--pencil);border-color:var(--pencil);border-style:dashed}
.copy{margin-left:auto;font:inherit;font-size:14px;color:var(--pencil);background:none;border:none;cursor:pointer;text-decoration:underline dotted}
.copy:hover{color:var(--ink)}
.box{border:2px dashed var(--pencil);border-radius:var(--wob2);padding:12px 16px;color:var(--pencil);font-size:15px;margin-top:18px}
#results{margin-top:10px}
footer{margin-top:50px;color:var(--pencil);font-size:14px;border-top:1.5px dashed var(--faint);padding-top:14px}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&display=swap" rel="stylesheet">'
         '<link href="{root}fonts/isright-hand.css" rel="stylesheet">')

COPY_JS = """document.addEventListener("click",e=>{const b=e.target.closest(".copy");if(!b)return;
const u=new URL(b.dataset.u,location.href).href;navigator.clipboard.writeText(u).then(()=>{b.textContent="複製了";setTimeout(()=>b.textContent="複製連結",1200)}).catch(()=>prompt("複製這個連結：",u));});"""

SCRIBBLE = '<svg class="scribble" viewBox="0 0 180 10" aria-hidden="true"><path d="M2 6 C40 2 70 9 110 5 S160 3 178 6"/></svg>'
TYPE_LABEL = {"Docs": "Claude 文件", "Slides": "Claude 簡報", "Design": "Claude 設計", "Dashboard": "Claude 儀表板"}


def page(title, body, root, desc=""):
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{esc(title)}</title>
{FONTS.format(root=root)}<style>{CSS}</style></head>
<body><div class="wrap">{body}</div><script>{COPY_JS}</script></body></html>
"""


def href(u, root):
    return u if u.startswith(("http://", "https://")) else root + u


def li(it, root):
    if "h" in it:
        return f'<li class="sub">{esc(it["h"])}</li>'
    u = href(it["u"], root)
    tags = ""
    if it.get("stu"):
        tags += '<span class="tag">給學生</span>'
    if it.get("type") and it["type"] != "html":
        tags += f'<span class="tag c">{TYPE_LABEL.get(it["type"], "Claude")}</span>'
    d = f'<span class="d">{esc(it["d"])}</span>' if it.get("d") else ""
    return (f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(it["t"])}</a>{d}{tags}'
            f'<button class="copy" data-u="{esc(u)}">複製連結</button></li>')


def count(items):
    return sum(1 for i in items if "h" not in i)


def card(href_, name, dz, sub, dashed=False):
    return (f'<a class="card{" dashed" if dashed else ""}" href="{esc(href_)}"><svg viewBox="0 0 60 48" aria-hidden="true">{DOODLES[dz]}</svg>'
            f'<span class="n">{esc(name)}</span><span class="c">{esc(sub)}</span></a>')


def crumb(root, here):
    return f'<div class="crumb"><a href="{root}index.html">← IsRight 入口</a>　／　{esc(here)}</div>'


drafts = D["drafts"]
cat_of = D["draft_cats"]
draft_count = {}
for x in drafts:
    k = cat_of.get(x["cat"], "misc")
    draft_count[k] = draft_count.get(k, 0) + 1

os.makedirs(os.path.join(HERE, "c"), exist_ok=True)
search_index = []

# ---- 分類頁 ----
for shelf in D["shelves"]:
    for c in shelf["cats"]:
        root = "../"
        n = count(c["items"])
        body = crumb(root, shelf["name"]) + f'<header><h1>{esc(c["name"])}</h1></header><p class="note">{esc(c["note"])}</p>{SCRIBBLE}'
        if n:
            body += '<ul class="items">' + "".join(li(i, root) for i in c["items"]) + "</ul>"
        nd = draft_count.get(c["id"], 0)
        if nd:
            body += f'<p class="box">另有 {nd} 個試作版在<a href="draft.html#{c["id"]}">「未完成」</a>，確認後會搬過來。</p>'
        open(os.path.join(HERE, "c", c["id"] + ".html"), "w", encoding="utf-8").write(page(c["name"] + "｜IsRight 入口", body, root))
        for i in c["items"]:
            if "h" not in i:
                search_index.append({"t": i["t"], "d": i.get("d", ""), "u": href(i["u"], ""), "c": c["name"], "stu": i.get("stu", 0)})

# ---- 未完成 ----
root = "../"
groups = {}
for x in drafts:
    groups.setdefault(x["cat"], []).append(x)
body = crumb(root, "未完成") + '<header><h1>未完成</h1></header><p class="note">Claude 上做的試作版。確認完成後，搬到該去的分類。</p>' + SCRIBBLE
body += '<p class="box">標「Claude 文件／簡報／設計」的，內容還在 Claude 上，只有你自己打得開；其餘的檔案都已放在網站上。</p>'
for name, items in groups.items():
    body += f'<h3 class="grp" id="{cat_of.get(name, "misc")}">{esc(name)}　<span class="d">{len(items)} 個</span></h3><ul class="items">'
    body += "".join(li(i, root) for i in items) + "</ul>"
    for i in items:
        search_index.append({"t": i["t"], "d": "未完成", "u": href(i["u"], ""), "c": "未完成"})
open(os.path.join(HERE, "c", "draft.html"), "w", encoding="utf-8").write(page("未完成｜IsRight 入口", body, root))

# ---- GitHub 專案 ----
body = crumb(root, "GitHub 專案") + '<header><h1>GitHub 專案</h1></header><p class="note">每個 repo 一行：左邊是網站，右邊是原始碼。</p>' + SCRIBBLE + '<ul class="items">'
for r in D["repos"]:
    repo = f'https://github.com/huangisright/{r["name"]}'
    site = (f'<a href="{esc(r["site"])}" target="_blank" rel="noopener">{esc(r["t"])}</a>' if r.get("site")
            else f'<span>{esc(r["t"])}</span>')
    priv = '<span class="tag c">私人 repo</span>' if r.get("private") else ""
    body += f'<li>{site}<span class="d">{esc(r["name"])}</span>{priv}<a class="copy" style="text-decoration:underline dotted" href="{repo}" target="_blank" rel="noopener">原始碼</a></li>'
    if r.get("site"):
        search_index.append({"t": r["t"], "d": r["name"], "u": r["site"], "c": "GitHub 專案"})
body += "</ul>"
open(os.path.join(HERE, "c", "repos.html"), "w", encoding="utf-8").write(page("GitHub 專案｜IsRight 入口", body, root))

# ---- 首頁 ----
me = ('<svg class="doodle-me" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="13" r="8"/>'
      '<path d="M32 21 L32.5 42"/><path d="M32.5 42 L24 59"/><path d="M32.5 42 L41 58"/>'
      '<path d="M32 28 L20 35"/><path d="M32 28 L47 21"/><path d="M47 21 L58 6 L61 22 Z"/></svg>')
body = (f'<header>{me}<div><h1>IsRight 的入口</h1><p class="sub">教學頁面、課堂工具，還有要丟給學生的連結。</p></div></header>'
        '<input id="q" type="search" placeholder="找東西……" autocomplete="off" aria-label="搜尋全部"><div id="results"></div><div id="shelves">')
for shelf in D["shelves"]:
    body += f'<section class="shelf"><h2>{esc(shelf["name"])}</h2><div class="cards">'
    for c in shelf["cats"]:
        n = count(c["items"]); nd = draft_count.get(c["id"], 0)
        sub = f"{n} 個" + (f"・試作 {nd}" if nd else "") if n else f"試作 {nd} 個，在未完成"
        body += card(f'c/{c["id"]}.html', c["name"], c["dz"], sub, dashed=(n == 0))
    body += "</div></section>"
body += '<section class="shelf"><h2>其他</h2><div class="cards">'
body += card("c/repos.html", "GitHub 專案", "repo", f'{len(D["repos"])} 個 repo')
body += card("c/draft.html", "未完成", "draft", f"{len(drafts)} 個試作版", dashed=True)
body += "</div></section></div>"
body += '<footer>虛線框＝還沒完成的。滑鼠移到卡片上，卡片會歪一下。</footer>'
body += ("<script>const IDX=" + json.dumps(search_index, ensure_ascii=False) + """;
const q=document.getElementById("q"),R=document.getElementById("results"),S=document.getElementById("shelves");
const e=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
q.addEventListener("input",()=>{const t=q.value.trim().toLowerCase();if(!t){R.innerHTML="";S.hidden=false;return;}
S.hidden=true;const h=IDX.filter(i=>(i.t+i.d+i.c+(i.stu?"給學生":"")).toLowerCase().includes(t));
R.innerHTML=h.length?'<ul class="items">'+h.map(i=>`<li><a href="${e(i.u)}" target="_blank" rel="noopener">${e(i.t)}</a><span class="d">${e(i.c)}</span>${i.stu?'<span class="tag">給學生</span>':''}<button class="copy" data-u="${e(i.u)}">複製連結</button></li>`).join("")+"</ul>":'<p class="note">什麼都沒有。也許它還在你的腦袋裡，還沒做出來。</p>';});
</script>""")
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page("IsRight 入口", body, ""))
print(f"index.html＋c/ 共 {len(os.listdir(os.path.join(HERE, 'c')))} 頁；搜尋索引 {len(search_index)} 筆")
