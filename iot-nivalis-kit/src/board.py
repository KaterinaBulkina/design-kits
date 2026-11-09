import sys; sys.path.insert(0,'/home/claude/nivalis-kit/src')
from mobile3 import *
sw=[('petrol','#0C4A5C','#fff'),('aqua','#CFE9EC','#0A3B49'),('ink','#11181C','#fff'),('muted','#55616B','#fff'),('line','#E3E8EC','#11181C'),('coral','#FF8A78','#11181C'),('critical','#D6432C','#fff'),('crit bg','#FFE4DE','#8A1C0F'),('warn bg','#FFEBC9','#6B3F00'),('ok','#1B6B3A','#fff'),('ok bg','#EAF6EE','#12452A')]
swh=''.join(f'<div style="background:{c};color:{t_};height:84px;border-radius:14px;padding:10px 12px;font-size:12.5px;line-height:17px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)"><b style="font-weight:600;display:block">{n}</b>{c}</div>' for n,c,t_ in sw)
def col(title,inner,w):
    return f'<div style="width:{w}px"><div style="font-size:13px;color:#66727C;margin-bottom:10px;text-transform:none">{title}</div>{inner}</div>'
dark='''<section class="hero" style="margin-top:0;padding:16px 18px 14px"><div class="hh"><div><b>Refrigeration energy</b><span class="s">Last 7 days</span></div></div><div class="fig" style="font-size:48px;line-height:52px">6<span class="dec">.4</span><span class="u" style="top:-16px;font-size:18px">MWh</span></div></section>'''
aqua='<section class="lt" style="margin-top:0"><div class="tags"><span class="pill c">Critical</span><span class="pill n">Containment</span></div><div class="big" style="font-size:48px;height:46px;line-height:48px"><span class="neg"></span>16<span class="dec">.1</span><span class="u" style="font-size:18px;top:-16px">°C</span></div><div class="sub2">Frozen Zone B</div></section>'
ar='<section class="ar" style="margin-top:0"><div class="t"><span class="ck">'+check(20)+'</span><div><b>Approved by Felix Whitaker</b><em>Facility Operations Manager, 10:25 EST</em></div></div></section>'
live='<section class="live" style="margin-top:0"><div class="qb"><span class="ci">'+icon("clock",20,1.75)+'</span><div><b>Queued for dispatch</b><p>Waiting for the control integration.</p></div></div></section>'
rows='<div style="background:none">'+prow("Policy","POL-COLD-07","Passed")+prow("Verification","After dispatch","Pending","")+'</div>'
btns='<div style="display:flex;gap:10px"><span class="b2 s">Secondary</span><span class="b2 p">Primary action</span></div>'
tags='<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="tg2 g">Passed</span><span class="tg2 a">Unexplained</span><span class="tg2 c">Needs evidence</span><span class="tg2">On hold</span></div>'
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS3}
html,body{{width:1600px;height:880px;overflow:hidden}}body{{padding:48px 56px}}
.bt{{font-family:var(--disp);font-weight:600;font-size:40px;letter-spacing:-.02em}}
.sec{{margin-top:34px}}.sec>.l{{font-size:13px;color:#66727C;margin-bottom:12px}}
</style></head><body>
<div style="display:flex;align-items:flex-end;justify-content:space-between"><div><div class="bt">Nivalis design kit</div><div style="font-size:15px;color:#55616B;margin-top:12px">Cold-storage building operations. Petrol, aqua, coral. Bricolage Grotesque and Onest.</div></div><img src="{LOGO}" style="height:44px;mix-blend-mode:multiply"></div>
<div class="sec"><div class="l">Color</div><div style="display:grid;grid-template-columns:repeat(11,1fr);gap:10px">{swh}</div></div>
<div class="sec" style="display:flex;gap:56px"><div style="flex:1"><div class="l">Type, display: Bricolage Grotesque 600</div><div style="font-family:var(--disp);font-weight:600;font-size:56px;line-height:60px;letter-spacing:-.035em">-16.1<span style="font-size:22px;font-weight:500;color:#55616B"> °C</span></div><div style="font-family:var(--disp);font-weight:600;font-size:26px;margin-top:10px">Activate backup evaporator mode</div></div>
<div style="flex:1"><div class="l">Type, UI: Onest 400, 500, 600</div><div style="font-size:17px;font-weight:600">Headline 17 semibold</div><div style="font-size:15px;margin-top:6px">Row title 15 semibold, body 15 regular</div><div style="font-size:13px;color:#55616B;margin-top:6px">Footnote 13, captions 12.5 minimum on mobile</div></div>
<div style="flex:1"><div class="l">Radii and buttons</div><div style="font-size:14px;line-height:22px;color:#55616B">Page hero 24, hero card 20, card 18, button 13, tag 7<br>Flat fills, 1px hairlines, no gradient buttons, no glow</div><div style="margin-top:12px">{btns}</div></div></div>
<div class="sec"><div class="l">Components</div><div style="display:flex;gap:28px;align-items:flex-start">
{col("Hero, main pages (dark petrol)",dark,360)}{col("Hero, secondary pages (aqua)",aqua,360)}{col("Approval record (functional, green)",ar,360)}{col("Active process (aqua container)",live,360)}</div>
<div style="display:flex;gap:28px;margin-top:26px;align-items:flex-start">{col("Plain rows on the page, hairlines only",rows,360)}{col("Status tags: only for exceptions",tags,360)}<div style="width:360px"><div style="font-size:13px;color:#66727C;margin-bottom:10px">Rules</div><div style="font-size:14px;line-height:21px;color:#34414A">No middle dots or long dashes in text.<br>One hero per page, never a dark hero on every page.<br>Charts: one line, a dashed limit, one red zone, end label.<br>New first and last name on every design.</div></div></div></div>
</body></html>'''
render(html,'/home/claude/nivalis-kit/preview/nivalis-kit-overview.png',1600,880,1.6)
