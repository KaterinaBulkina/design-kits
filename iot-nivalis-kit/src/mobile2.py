import sys, math; sys.path.insert(0,'/home/claude/nivalis')
from mobile import *
M=MINUS
CSS2=CSS+'''
.pg{overflow:hidden}
.nav2{height:44px;display:grid;grid-template-columns:44px 1fr 44px;align-items:center}
.nav2 h3{font-size:17px;font-weight:600;text-align:center;line-height:22px;letter-spacing:-.01em}
.bk{width:44px;height:44px;border-radius:14px;background:#fff;border:1px solid #DCE3E8;display:flex;align-items:center;justify-content:center}
.bk .ic{transform:rotate(180deg)}
.lt{position:relative;margin-top:10px;border-radius:20px;color:#0A3B49;padding:16px 18px 14px;overflow:hidden;background:linear-gradient(160deg,#CFE9EC,#EEF8F7);box-shadow:inset 0 0 0 1px #BBDDE2}
.lt:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(12,74,92,.06) 0 1px,transparent 1px 9px);-webkit-mask-image:linear-gradient(110deg,transparent 20%,#000 90%);mask-image:linear-gradient(110deg,transparent 20%,#000 90%)}
.lt>*{position:relative;z-index:1}
.tags{display:flex;gap:6px;align-items:center}
.pill.c{background:var(--crit-bg);color:var(--crit-ink)}
.pill.w{background:#FFEBC9;color:#6B3F00}
.pill.n{background:rgba(255,255,255,.7);color:#0A3B49;box-shadow:inset 0 0 0 1px #BBDDE2;font-weight:500}
.big{height:52px;font-family:var(--disp);font-weight:600;font-size:56px;line-height:56px;letter-spacing:-.035em;margin-top:10px;white-space:nowrap;color:#0A3B49}
.big .dec{color:rgba(10,59,73,.5)} .big .u{font-size:22px;letter-spacing:0;position:relative;top:-20px;margin-left:5px;font-weight:500;color:rgba(10,59,73,.75)}
.big .neg{display:inline-block;width:.34em;height:.085em;background:#0A3B49;border-radius:2px;margin-right:.07em;vertical-align:.27em}
.sub2{font-size:14px;line-height:20px;color:#2F5E6B;margin-top:6px}
.g2{display:grid;grid-template-columns:1fr 1fr;margin-top:12px;border-top:1px solid #BBDDE2}
.g2>div{padding:9px 0 8px;border-bottom:1px solid #BBDDE2;min-height:62px}
.g2>div:nth-child(odd){padding-right:10px;border-right:1px solid #BBDDE2}.g2>div:nth-child(even){padding-left:14px}
.g2>div:nth-last-child(-n+2){border-bottom:0;padding-bottom:0}
.g2 span{display:block;font-size:12.5px;line-height:16px;color:#2F5E6B}
.g2 b{display:block;font-size:17px;line-height:22px;font-weight:600;color:#0A3B49;white-space:nowrap}
.g2 b.r{color:#B3321D}
.g2 em{display:block;font-style:normal;font-size:12.5px;line-height:16px;color:#4B7580;white-space:nowrap}
.card{margin-top:10px;background:#fff;border-radius:18px;border:1px solid var(--line);overflow:hidden}
.ch{display:flex;justify-content:space-between;align-items:baseline;padding:12px 16px 0}
.ch h2{font-size:17px;font-weight:600;line-height:22px}.ch span{font-size:12.5px;color:var(--faint)}
.lrow{min-height:48px;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 16px;border-top:1px solid #EEF1F3}
.lrow:first-child{border-top:0}
.lrow b{display:block;font-size:15px;line-height:20px;font-weight:600}.lrow em{display:block;font-style:normal;font-size:13px;line-height:17px;color:var(--faint)}
.lrow .rr{display:flex;align-items:center;gap:6px;color:var(--muted);font-size:14px;white-space:nowrap}
.tg2{height:24px;border-radius:7px;padding:0 8px;font-size:12.5px;line-height:24px;font-weight:500;background:#E8EDF0;color:#34414A;white-space:nowrap}
.tg2.c{background:#FFE4DE;color:#8A1C0F}.tg2.a{background:#FFEBC9;color:#6B3F00}.tg2.g{background:#E1F2E7;color:#1B6B3A}
.bar2{position:absolute;left:0;right:0;bottom:0;height:98px;padding:12px 16px 0;background:rgba(246,249,250,.88);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);border-top:1px solid #D5DDE2;display:flex;gap:10px;align-items:flex-start}
.b2{height:50px;border-radius:13px;display:inline-flex;align-items:center;justify-content:center;gap:8px;font-size:16px;font-weight:500;white-space:nowrap}
.b2.s{padding:0 14px;color:var(--ink);background:#fff;border:1px solid #CBD3D9}
.b2.p{flex:1;background:#11181C;color:#fff}
.lg{display:flex;gap:14px;padding:4px 16px 12px;font-size:12.5px;color:var(--muted)}.lg i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;background:#9AA7B0}
.chips2{display:flex;gap:6px;flex-wrap:wrap;padding:0 16px 14px}
.chip3{height:32px;padding:0 12px;border-radius:10px;background:#F1F4F6;border:1px solid #E3E8EC;font-size:14px;line-height:30px}
.seg{display:flex;gap:3px;margin-top:14px}.seg i{display:block;height:34px;border-radius:6px;font-style:normal;color:#fff;font-size:13px;font-weight:600;line-height:34px;padding-left:8px}
.sl{display:flex;gap:3px;margin-top:4px;font-size:12px;color:#2F5E6B}.sl span{white-space:nowrap}
.lot{display:flex;align-items:center;justify-content:space-between;padding:0 16px;min-height:60px;border-top:1px solid #EEF1F3}
.lot:first-of-type{border-top:0}
.lot small{display:block;font-size:12.5px;color:var(--faint);line-height:16px}.lot b{display:block;font-size:15px;line-height:20px;font-weight:600}
.lot .r{text-align:right}.lot .r b{font-weight:500}
.lot.sel{background:#FFF3F0;position:relative}.lot.sel:before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--red)}
.ev{padding:10px 16px 12px;background:#FFF3F0;border-top:1px solid #F6D6CF;font-size:14px;line-height:19px;color:#5E1D12}.ev b{font-weight:600}
.dm{display:flex;justify-content:space-between;align-items:center;min-height:56px;padding:0 16px;border-top:1px solid #EEF1F3}
.dm b{font-size:15px;line-height:20px;font-weight:600;display:block}.dm em{font-style:normal;font-size:13px;color:var(--faint);display:block;line-height:17px}.dm .v{font-family:var(--disp);font-weight:600;font-size:18px}
.dm .v.c{color:#B3321D}
'''
def page2(body,extra=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS2}</style></head><body>{body}{extra}</body></html>'
def nav2(title):
    return f'<div class="nav2"><span class="bk">{icon("chevright",20,1.75)}</span><h3>{title}</h3><span class="bk" style="margin-left:auto">{icon("dots",20)}</span></div>'
def bar2(sec,pri,arrow=True):
    return f'<div class="bar2"><span class="b2 s">{sec}</span><span class="b2 p">{pri}{icon("arrow",18,1.75) if arrow else ""}</span></div>'

def smooth(pts):
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1,len(pts)):
        x0,y0=pts[i-1];x1,y1=pts[i];cx=(x0+x1)/2
        d+=f' C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}'
    return d
def inc_chart(W=329,H=150):
    L=4;R=W-4;T=22;th=88
    def X(f):return L+(R-L)*f
    def Y(v):return T+(-15-v)/4*th
    n=60;pts=[]
    for i in range(n+1):
        f=i/n
        base=-18.5+0.3*math.sin(f*17)+0.12*math.sin(f*41)
        if f>0.62: base=base+((f-0.62)/0.38)**1.35*2.45
        pts.append((X(f),Y(base)))
    pts[-1]=(X(1),Y(-16.1))
    yl=Y(-18.0);xo=X(0.73)
    cr=next(i for i,p in enumerate(pts) if p[1]<yl and i>30)
    red=pts[cr-1:]
    area=smooth(red)+f' L{red[-1][0]:.1f},{yl:.1f} L{red[0][0]:.1f},{yl:.1f} Z'
    s=f'<line x1="{L}" x2="{R}" y1="{yl:.1f}" y2="{yl:.1f}" stroke="#3B5A68" stroke-dasharray="4 4"/><text x="{L}" y="{yl-8:.1f}" font-size="12" fill="#3B5A68">Upper limit {M}18.0</text>'
    s+=f'<path d="{area}" fill="rgba(255,138,120,.2)"/>'
    s+=f'<path d="{smooth(pts[:cr])}" fill="none" stroke="#0C4A5C" stroke-width="2.4" stroke-linecap="round"/><path d="{smooth(red)}" fill="none" stroke="#E5533D" stroke-width="2.8" stroke-linecap="round"/>'
    s+=f'<circle cx="{X(1):.1f}" cy="{Y(-16.1):.1f}" r="5" fill="#fff" stroke="#E5533D" stroke-width="2.4"/>'
    s+=f'<text x="{xo:.1f}" y="{T-8}" text-anchor="middle" font-size="12" fill="#B3321D">Opened 04:24</text><line x1="{xo:.1f}" x2="{xo:.1f}" y1="{T-2}" y2="{T+th+4}" stroke="#D6432C" stroke-dasharray="3 3"/>'
    for f,lab in ((0,'12:00'),(1,'Now')):
        s+=f'<text x="{X(f):.1f}" y="{H-4}" text-anchor="{"start" if f==0 else "end"}" font-size="12" fill="#66727C">{lab}</text>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{s}</svg>'

def m_incident():
    hero=f'''<section class="lt"><div class="tags"><span class="pill c">{icon("alert",14,1.75)}Critical</span><span class="pill n">Containment in progress</span></div>
<div class="big" aria-label="{t(CUR)} degrees Celsius"><span class="neg"></span>16<span class="dec">.1</span><span class="u">°C</span></div><div class="sub2">Frozen Zone B, temperature excursion</div>
<div class="g2"><div><span>Upper limit</span><b>{t(SETPOINT)} °C</b><em>Configured</em></div><div><span>Deviation</span><b class="r">+{DEV} °C</b><em>Above limit</em></div><div><span>Open for</span><b>6 h 00 min</b><em>Since 04:24 EST</em></div><div><span>Owner</span><b>Felix Whitaker</b><em>Facility Ops Manager</em></div></div></section>'''
    ch=f'''<section class="card"><div class="ch"><h2>Signal correlation</h2><span>Last 23 h</span></div><div style="padding:8px 16px 4px">{inc_chart()}</div>
<div class="lrow"><div><b>EF-3 current</b><em>Normal 4.8 A</em></div><div class="rr"><b style="color:var(--ink)">4.5 A</b></div></div>
<div class="lrow"><div><b>CR-01 cooling</b><em>Normal 32.4 kW</em></div><div class="rr"><b style="color:var(--ink)">26.9 kW</b></div></div></section>'''
    lst='''<section class="card"><div class="lrow"><div><b>Response</b><em>5 steps, 2 active</em></div><div class="rr">Open</div></div></section>'''
    return page2(f'<div class="pg">{nav2("Incident EXC-2417")}{hero}{ch}{lst}</div>{bar2("Assign owner","Dispatch technician")}')

def ef_chart(W=329,H=205):
    L=4;R=W-4
    def X(f):return L+(R-L)*f
    ys=lambda v:42+(5.2-v)/3.2*(H-100)
    pts=[]
    for i in range(61):
        f=i/60
        if f<0.18:v=4.8
        elif f<0.30:v=4.8-(f-0.18)/0.12*2.5
        elif f<0.46:v=2.3+0.05*math.sin(i)
        else:v=2.3+(min(1,(f-0.46)/0.2))*2.2
        pts.append((X(f),ys(v)))
    s=f'<rect x="{X(0.3):.1f}" y="26" width="{X(0.46)-X(0.3):.1f}" height="{H-54}" rx="6" fill="#DCEBF2"/><text x="{(X(0.3)+X(0.46))/2+14:.1f}" y="16" text-anchor="middle" font-size="12" fill="#2F5E6B">Backup fan on</text>'
    s+=f'<line x1="{L}" x2="{R}" y1="{ys(4.8):.1f}" y2="{ys(4.8):.1f}" stroke="#3B5A68" stroke-dasharray="4 4"/><text x="{L}" y="{ys(4.8)-7:.1f}" font-size="12" fill="#3B5A68">Normal 4.8 A</text>'
    s+=f'<path d="{smooth(pts)}" fill="none" stroke="#0C4A5C" stroke-width="2.8" stroke-linecap="round"/><circle cx="{X(1):.1f}" cy="{ys(4.5):.1f}" r="5" fill="#fff" stroke="#0C4A5C" stroke-width="2.4"/>'
    for f,lab in ((0,'09:38'),(0.38,'10:00'),(1,'10:24')):
        a='start' if f==0 else ('end' if f==1 else 'middle')
        s+=f'<text x="{X(f):.1f}" y="{H-6}" text-anchor="{a}" font-size="12" fill="#66727C">{lab}</text>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{s}</svg>'
def m_ef3():
    pct=4.5/6*100;nb=4.8/6*100
    hero=f'''<section class="lt" style="margin-top:6px"><div style="font-size:14px;color:#2F5E6B;line-height:20px">Fan power draw, updated 12 sec ago</div>
<div class="big" style="margin-top:2px">4<span class="dec">.5</span><span class="u">A</span></div>
<div style="position:relative;height:34px;margin-top:6px"><div style="position:absolute;left:{nb}%;top:0;transform:translateX(-50%);font-size:12.5px;color:#2F5E6B;white-space:nowrap">Normal 4.8 A</div>
<div style="position:absolute;left:0;right:0;top:22px;height:10px;border-radius:99px;background:rgba(10,59,73,.14);overflow:hidden"><i style="display:block;width:{pct}%;height:100%;background:#0C4A5C;border-radius:99px"></i></div>
<i style="position:absolute;left:{nb}%;top:18px;width:2px;height:18px;background:#0A3B49"></i></div>
<div style="display:flex;justify-content:space-between;font-size:12px;color:#4B7580;margin-top:3px"><span>0</span><span>2</span><span>4</span><span>6 A</span></div>
</section>'''
    g=hero.replace('.g2','.g2')
    say=f'''<section class="card" style="margin-top:10px"><div style="padding:14px 16px 0"><div style="font-family:var(--disp);font-weight:600;font-size:22px;line-height:27px;letter-spacing:-.015em">The fan works again, but it needs a check.</div></div>
<div style="padding:10px 16px 4px;font-size:13px;color:var(--faint)">Check on site</div><div class="chips2" style="padding-top:0"><span class="chip3">Belt</span><span class="chip3">Motor</span><span class="chip3">Fan blades</span></div></section>'''
    ch=f'''<section class="card"><div class="ch"><h2>What happened</h2><span>Today, 09:38 to 10:24</span></div><div style="padding:6px 16px 4px">{ef_chart()}</div></section>'''
    head=f'''<div style="margin-top:8px;display:flex;gap:6px;align-items:center"><span class="pill w">{icon("alert",14,1.75)}Warning</span><span class="pill n" style="background:#fff">Airflow restored</span></div>'''
    return page2(f'<div class="pg">{nav2("Evaporator fan EF-3")}{head}{hero}{say}{ch}</div>{bar2("Incident","Create maintenance work",False)}')

def en_chart(W=361,H=132):
    L=30;R=W-78
    ys=lambda v:10+(52-v)/24*(H-44)
    n=140;act=[];bas=[]
    for i in range(n+1):
        f=i/n;day=f*7
        ph=day%1
        b=36+9*math.sin((ph-0.3)*2*math.pi)+2*math.sin(day*9)
        a=b+1.0+0.8*math.sin(day*13)
        if f>0.93:a=b+(f-0.93)/0.07*6.5
        act.append((L+(R-L)*f,ys(a)));bas.append((L+(R-L)*f,ys(b)))
    act[-1]=(R,ys(48.2));bas[-1]=(R,ys(41.7))
    s=''
    for v in (30,40,50):
        s+=f'<line x1="{L}" x2="{R}" y1="{ys(v):.1f}" y2="{ys(v):.1f}" stroke="#DDE3E7"/><text x="{L-8}" y="{ys(v)+4:.1f}" text-anchor="end" font-size="12" fill="#66727C">{v}</text>'
    s+=f'<path d="{smooth(bas)}" fill="none" stroke="#9AA7B0" stroke-width="1.4" stroke-dasharray="2 3"/><path d="{smooth(act)}" fill="none" stroke="#0C4A5C" stroke-width="2.2" stroke-linejoin="round"/>'
    s+=f'<circle cx="{R}" cy="{ys(48.2):.1f}" r="5" fill="#fff" stroke="#0C4A5C" stroke-width="2.4"/><text x="{R+10}" y="{ys(48.2)+5:.1f}" font-size="16" font-weight="600" fill="#11181C" font-family="Bricolage Grotesque">48.2 kW</text><text x="{R+10}" y="{ys(48.2)+21:.1f}" font-size="12" fill="#66727C">Base 41.7</text>'
    for f,lab in ((0,'Fri 30'),(0.5,'Mon 2')):
        s+=f'<text x="{L+(R-L)*f:.1f}" y="{H-6}" text-anchor="{"start" if f==0 else "middle"}" font-size="12" fill="#66727C">{lab}</text>'
    s+=f'<text x="{R}" y="{H-6}" text-anchor="end" font-size="12" font-weight="600" fill="#11181C">Now</text>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{s}</svg>'
def m_energy():
    hero=f'''<section class="hero" style="margin-top:12px;padding:18px 20px 16px"><div class="hh"><div><b>Refrigeration energy</b><span class="s">Last 7 days, baseline 6.1 MWh</span></div><span class="pill" style="background:rgba(255,255,255,.14);color:#fff;font-weight:500">Matched baseline</span></div>
<div class="fig" style="font-size:56px;line-height:60px;margin-top:12px">6<span class="dec">.4</span><span class="u" style="top:-20px">MWh</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;margin-top:14px;border-top:1px solid rgba(255,255,255,.14);padding-top:10px"><div><span style="font-size:12.5px;color:rgba(255,255,255,.74);display:block;line-height:16px">Variance</span><b style="font-size:17px;color:var(--coral);font-weight:600">+3.7%</b></div><div style="padding-left:14px;border-left:1px solid rgba(255,255,255,.14)"><span style="font-size:12.5px;color:rgba(255,255,255,.74);display:block;line-height:16px">Temperature integrity</span><b style="font-size:17px;font-weight:600">97.3%</b></div></div></section>'''
    ch=f'''<section style="margin-top:22px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 style="font-size:20px;font-weight:600">Refrigeration demand</h2><span style="font-size:13px;color:var(--faint)">kW</span></div><div style="margin-top:10px">{en_chart()}</div></section>'''
    def row(a,b,tag,cls,v):
        return f'<div class="lrow" style="min-height:68px;border-top:1px solid #D5DDE2;padding:0"><div><b>{a}</b><em>{b}</em></div><div class="rr"><span class="tg2 {cls}">{tag}</span><b style="color:var(--ink);font-weight:600;width:62px;text-align:right">{v}</b></div></div>'
    rows=f'''<section style="margin-top:22px"><h2 style="font-size:20px;font-weight:600;padding-bottom:8px">What adds demand</h2>{row("EXC-2417 recovery","Compressors run longer","Explained","","+3.5 kW")}{row("CR-02 short cycling","Frequent restarts","Unexplained","a","+2.9 kW")}{row("Normal variation","Weather and load","In range","","+0.2 kW")}</section>'''
    return page2(f'<div class="pg">{shell(2,"Energy and thermal performance")}{hero}{ch}{rows}</div>{bar2("Open incident","Send for review",False)}')

def m_hold():
    tot=18+12+8+4;assert tot==42
    W=361
    segs=[(18,'#0C4A5C','18'),(12,'#3E7F90','12'),(8,'#E5533D','8'),(4,'#6FA3B1','4')]
    seg=''.join(f'<i style="width:{(W-9)*v/42:.1f}px;background:{c if c!="#E5533D" else "repeating-linear-gradient(135deg,#E5533D 0 4px,#F08E7E 4px 8px)"}">{l if v>=8 else ""}</i>' for v,c,l in segs)
    top=f'''<section style="margin-top:22px"><div style="font-size:15px;color:var(--muted)">Inventory on hold, Frozen Zone B</div>
<div class="big" style="margin-top:6px;height:60px;line-height:60px">42<span style="font-size:22px;font-weight:500;letter-spacing:0;margin-left:8px;color:var(--muted)">pallets in 4 lots</span></div>
<div class="seg" style="margin-top:18px">{seg}</div>
<div style="display:flex;gap:36px;margin-top:26px"><div><span style="font-size:13px;color:var(--muted);display:block">Exposure window</span><b style="font-size:19px;line-height:26px;font-weight:600">05:54 to now</b></div><div><span style="font-size:13px;color:var(--muted);display:block">Evidence gaps</span><b style="font-size:19px;line-height:26px;font-weight:600;color:#B3321D">1 of 4 lots</b></div></div></section>'''
    def lot(n,i,p,tag):
        return f'<div class="lot"><div><b>{i}</b><small>{n}</small></div><div class="r"><b>{p} pallets</b><small>{tag}</small></div></div>'
    cp=f'''<div class="lot sel"><div><b>LOT-CP-4403</b><small>Chicken portions</small></div><div class="r"><b>8 pallets</b><span class="tg2 c">Needs evidence</span></div></div>'''
    lots=f'''<section style="margin-top:34px"><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:8px"><h2 style="font-size:20px;font-weight:600">Lot review</h2><span style="font-size:13px;color:var(--faint)">Hold opened 06:12</span></div>
<div class="lots">{cp}{lot("Frozen peas","LOT-NF-8841",18,"On hold")}{lot("Berry mix","LOT-RM-2217",12,"On hold")}{lot("Dessert trays","LOT-DS-1908",4,"On hold")}</div></section>'''
    return page2(f'<div class="pg">{nav2("Hold HOLD-2417")}{top}{lots}</div>{bar2("Record disposition","Request evidence",False)}','<style>.lots .lot{padding:0 0;min-height:68px;border-top:1px solid #D5DDE2}.lots .lot.sel{padding:0 14px;margin:0 -16px;padding-left:16px;padding-right:16px}.lots .lot:first-child{border-top:1px solid #D5DDE2}</style>')

if __name__=='__main__':
    for n,f in [('mobile-incident',m_incident),('mobile-ef3',m_ef3),('mobile-energy',m_energy),('mobile-hold',m_hold)]:
        render(f(),f'{ROOT}/out/{n}.png',393,852,3)
