s=open('desktop.py').read()
a=s.index("    body=f'''"); b=s.index("    return f'<!doctype")
new = r'''    nav=''.join(f'<div class="nav {"on" if n=="Incidents" else ""}">{icon(ic,18)}<span>{n}</span></div>' for n,ic,on in NAV)
    TABS2=['Overview','Evidence','Plan','Inventory','Activity']
    tabs=''.join(f'<div class="tab {"on" if i==0 else ""}">{n}</div>' for i,n in enumerate(TABS2))
    css=css.replace('grid-template-columns:560px 1fr;gap:16px;height:318px','grid-template-columns:1fr;gap:16px;height:128px')
    css=css.replace('grid-template-columns:800px 1fr;gap:16px;height:540px','grid-template-columns:640px 1fr;gap:16px;height:420px')
    css+=""".back{width:34px;height:34px;background:#fff;border:1px solid #D8DEE3;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#3B4750;box-shadow:0 1px 2px rgba(12,38,50,.05)} .back .ic{transform:rotate(180deg)}
.top .l{gap:12px} .top .l h1{margin-right:4px}
.pill.act{background:#E8ECEF;color:#3A4650} .top .pill{height:26px;font-size:13px;padding:0 12px}
.kv.s{height:54px}
.foot{height:44px;margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:13px;color:var(--faint);border-top:1px solid #EEF1F3} .foot b{font-weight:500;color:var(--ink)}
.btn.sq{width:40px;padding:0;justify-content:center}
.big{font-family:var(--disp);font-weight:600;font-size:30px;line-height:34px;letter-spacing:-.02em}
.hero2{position:relative;border-radius:22px;background:var(--petrol);color:#fff;overflow:hidden;display:flex;align-items:center;padding:0 32px}
.hero2:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 10%,#000 70%);mask-image:linear-gradient(100deg,transparent 10%,#000 70%)}
.hero2:after{content:'';position:absolute;left:120px;top:-40px;width:520px;height:220px;background:radial-gradient(closest-side,rgba(96,214,232,.30),rgba(96,214,232,0));pointer-events:none}
.hero2>*{position:relative;z-index:1}
.hero2 .tt{width:250px} .hero2 .tt b{display:block;font-size:20px;font-weight:600;line-height:26px;letter-spacing:-.01em} .hero2 .tt span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px;margin-top:2px}
.hero2 .fig{margin-right:auto}
.hero2 .stat{padding:0 34px;border-left:1px solid rgba(255,255,255,.16)} .hero2 .stat:last-child{padding-right:6px}
.hero2 .stat span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px} .hero2 .stat b{display:block;font-family:var(--disp);font-weight:600;font-size:26px;line-height:32px;letter-spacing:-.02em;margin-top:4px;white-space:nowrap} .hero2 .stat b small{font-family:var(--ui);font-size:14px;font-weight:500;letter-spacing:0;margin-left:3px;color:rgba(255,255,255,.72)} .hero2 .stat b.w{color:var(--coral)}
.lanewrap{padding:16px 22px 8px}
"""
    lk=[('Hypothesis','Cooling capacity loss'),('Evidence for','CR-01 down 17%, EF-3 draw low'),('Evidence against','Door closed, no open events'),('Uncertainty','Moderate, about 30%')]
    lkh=''.join(f'<div class="kv s"><span>{a}</span><b>{b}</b></div>' for a,b in lk)
    sm=[('Owner','Felix Whitaker'),('Opened','Fri 04:24'),('Approver','Facility Operations Manager'),('Data freshness','Under 1 min')]
    smh=''.join(f'<div class="kv"><span>{a}</span><b>{b}</b></div>' for a,b in sm)
    DUR='6 h 00 min'
    body=f\'\'\'
<aside class="side"><img class="logo" src="{LOGO}" alt="Nivalis Building Operations">
 <div class="org"><div><b>Harlow Cold Logistics</b><span>Organization</span></div><span class="ud"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 6.5 8 3l3.5 3.5M4.5 9.5 8 13l3.5-3.5"/></svg></span></div>
 <div class="navs">{nav}</div>
 <div class="sync">Data synced<b>{NOW}</b></div></aside>
<main class="sheet">
 <div class="top"><div class="l"><span class="back">{icon("arrow",18)}</span><h1>Incident EXC-2417</h1><span class="pill crit">{icon("alert",14,1.75)}Critical</span><span class="pill act">Active</span></div>
  <div class="r"><span class="sel dtb">{icon("clock",16)}{NOW}</span><span class="bell">{icon("bell",18)}<i>1</i></span><span class="sel">{icon("user",16)}Operations{icon("chevdown",16)}</span></div></div>
 <div class="tabsrow"><div class="tabs">{tabs}</div><span class="sel">{icon("building",16)}BCD-01, Frozen Zone B{icon("chevdown",16)}</span></div>
 <div class="r2">
  <section class="hero2">
   <div class="tt"><b>Frozen Zone B</b><span>Temperature excursion</span></div>
   <div class="fig num" aria-label="{t(CUR)} degrees Celsius"><span class="neg"></span>16<span class="dec">.1</span><span class="u">°C</span></div>
   <div class="stat"><span>Setpoint</span><b>{t(SETPOINT)}<small>°C</small></b></div>
   <div class="stat"><span>Deviation</span><b class="w">+{DEV}<small>°C</small></b></div>
   <div class="stat"><span>Open for</span><b>{DUR}</b></div>
  </section>
 </div>
 <div class="r2" style="height:376px;margin-top:16px">
  <section class="sect"><div class="sh"><h2>Signal correlation</h2><span style="font-size:13px;color:var(--faint)">Last 23 hours, Zone B</span></div>
   <div class="inner"><div class="lanewrap">{lane_chart(1236)}</div></div></section>
 </div>
 <div class="r3" style="height:420px">
  <section class="sect"><div class="sh"><div class="lft"><h2>Likely cause</h2><span class="cnt">Preliminary</span></div></div><div class="inner">{lkh}
   <div class="foot"><span>Other factors not ruled out</span><b>Review analysis</b></div></div></section>
  <section class="sect"><div class="sh"><h2>Summary</h2></div><div class="inner">
   <div class="eng"><div class="k"><span>Inventory exposure</span></div><div class="big num">42<small style="font-family:var(--ui);font-size:14px;color:var(--muted);font-weight:500;margin-left:6px;letter-spacing:0">pallets</small></div><div class="m" style="margin-top:6px"><span>Potentially exposed, QA review pending</span></div></div>
   {smh}</div></section>
 </div>
</main>
<div class="fade"></div>
<div class="bar"><div class="tx">Active, awaiting approval. <span>Next step: dispatch a technician to CR-01 and EF-3.</span></div><div class="bs"><span class="btn o">Assign</span><span class="btn o">Acknowledge</span><span class="btn p">Dispatch technician{icon("arrow",16,1.75)}</span><span class="btn o sq">{icon("dots",18)}</span></div></div>
\'\'\'
'''.replace("\\'\\'\\'","'''")
s=s[:a]+new+s[b:]
s=s.replace("render(build(),f'{ROOT}/out/desktop.png',1600,1000,1.6)","render(build(),f'{ROOT}/out/incident-desktop.png',1600,1000,1.6)")
open('incident.py','w').write(s)
