import json, re, base64
ROOT='/home/claude/nivalis'
FONTS='/home/claude/fonts/node_modules/@fontsource'
ICONS={k:v['svg'] for k,v in json.load(open(f'{ROOT}/icons.json')).items()}
def icon(name,size=18,sw=1.5,cls=''):
    s=ICONS[name]
    s=re.sub(r'width="24"',f'width="{size}"',s,1); s=re.sub(r'height="24"',f'height="{size}"',s,1)
    s=s.replace('stroke-width="1.5"',f'stroke-width="{sw}"')
    if 'stroke-width' not in s: s=s.replace('<svg',f'<svg stroke-width="{sw}"',1)
    return s.replace('<svg',f'<svg class="ic {cls}" aria-hidden="true"',1)
LOGO='data:image/png;base64,'+base64.b64encode(open(f'{ROOT}/logo.png','rb').read()).decode()

MINUS='−'
def t(v,d=1):  # signed temp text
    s=f'{abs(v):.{d}f}'
    return (MINUS if v<0 else '')+s
# ---- shared data (one source of truth)
NOW='Fri, Nov 6, 10:24 EST'
SETPOINT=-18.0
READINGS=[-18.5,-18.6,-18.4,-18.7,-18.9,-18.6,-18.5,-18.4,-18.6,-18.5,-18.7,-18.5,-18.4,   # Thu 11:24 .. Thu 23:24
          -18.3,-18.2,-18.0,-17.8,-17.5,-17.2,-16.8,-16.4,-16.0,-15.8,-16.1]                # Fri 00:24 .. Fri 10:24
assert len(READINGS)==24
CUR=READINGS[-1]; assert CUR==-16.1
DEV=round(CUR-SETPOINT,1); assert DEV==1.9
LO,HI=min(READINGS),max(READINGS); assert (LO,HI)==(-18.9,-15.8)
FIRST_ABOVE=next(i for i,v in enumerate(READINGS) if v>SETPOINT); assert FIRST_ABOVE==16  # Fri 03:24
ENERGY=48.2; CAP=66.8; PCT=round(ENERGY/CAP*100); assert PCT==72
ZONES={'A':-18.4,'B':-16.1,'C':3.2,'D':7.1}
assert ZONES['B']==CUR
SYSTEMS=[
 dict(id='CR-01',sub='Refrigeration, Frozen B',status='Critical',signal=t(CUR)+' °C',owner='Refrigeration',action='Investigate'),
 dict(id='EF-3',sub='Refrigeration, evaporator fan',status='Warning',signal='Airflow restored, 4.5 A',owner='Refrigeration',action='Inspect'),
 dict(id='AHU-02',sub='HVAC, office',status='Normal',signal='Supply 21.6 °C',owner='Facilities',action='None'),
 dict(id='Electrical supply',sub='Utility',status='Normal',signal=f'415 V, {ENERGY} kW',owner='Electrical',action='None'),
 dict(id='GEN-01',sub='Backup generator',status='Normal',signal='Standby, 0 kW',owner='Electrical',action='None'),
]
N_TOTAL=8; N_CRIT,N_WARN,N_NORM=1,1,6; assert N_CRIT+N_WARN+N_NORM==N_TOTAL
import datetime
assert datetime.date(2026,11,6).strftime('%a')=='Fri' and datetime.date(2026,11,5).strftime('%a')=='Thu'
assert datetime.date(2026,11,23).strftime('%a')=='Mon' and datetime.date(2026,10,23).strftime('%a')=='Fri'

def font_css():
    f=lambda fam,pkg,w:f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;src:url('file://{FONTS}/{pkg}/files/{pkg}-latin-{w}-normal.woff2') format('woff2');}}"
    return ''.join(f('Onest','onest',w) for w in (400,500,600))+''.join(f('Bricolage Grotesque','bricolage-grotesque',w) for w in (500,600,700))

def ticks_html(width,tick_w,h_max,h_min,box_h,label_px):
    pitch=width/24
    out=[]
    for i,v in enumerate(READINGS):
        h=h_min+(v+19.0)/3.5*(h_max-h_min)
        cls='tk hot' if v>SETPOINT else 'tk'
        if i==23: cls+=' now'
        out.append(f'<i class="{cls}" style="left:{i*pitch+(pitch-tick_w)/2:.1f}px;width:{tick_w}px;height:{h:.1f}px"></i>')
    sp_h=h_min+(SETPOINT+19.0)/3.5*(h_max-h_min)
    out.append(f'<i class="sp" style="bottom:{sp_h:.1f}px"></i>')
    def lab(i,txt,align):
        x=i*pitch+pitch/2
        st={'l':'left:0','r':'right:0','c':f'left:{x:.1f}px;transform:translateX(-50%)'}[align]
        return f'<span class="al" style="{st}">{txt}</span>'
    axis=lab(0,'Thu 11:24','l')+lab(16,'Fri 03:24','c')+lab(23,'Fri 10:24','r')
    return f'<div class="strip" style="width:{width}px;height:{box_h}px">{"".join(out)}</div><div class="axis" style="width:{width}px">{axis}</div>'

def render(html,out,w,h,scale):
    from playwright.sync_api import sync_playwright
    open(out.replace('.png','.html'),'w').write(html)
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=scale)
        pg.goto('file://'+out.replace('.png','.html')); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(300)
        info=pg.evaluate('''()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{if(e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflow==='visible' && e.clientWidth>0 && e.tagName!=='svg'&&e.tagName!=='path'&&e.tagName!=='I'){bad.push(e.className+':'+e.textContent.slice(0,30))}});
          const f=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+f.weight);
          const txt=document.body.innerText;
          return {bad:bad.slice(0,12),fonts:[...new Set(f)],txt}}''')
        pg.screenshot(path=out,clip={'x':0,'y':0,'width':w,'height':h})
        b.close()
    txt=info['txt']
    for ch in ['·','•','—','–']:
        assert ch not in txt,('banned char',repr(ch))
    print(out.split('/')[-1],'overflow:',info['bad'],'fonts:',info['fonts'])
    return info

# ---------- architectural floor plan (shared by desktop and mobile) ----------
def plan_svg(mode='d'):
    D = mode == 'd'
    ink, mut, wall, red = '#11181C', '#5A6670', '#8A96A0', '#D6432C'
    if D:
        W, H, ls, ts, tb = 600, 246, 12, 26, 34
        R = {'eng':(6,6,124,56),'ele':(130,6,132,56),'ctl':(262,6,128,56),
             'A':(6,62,170,164),'B':(176,62,214,164),'dock':(390,6,204,104),'C':(390,110,204,116)}
        OUT = (6,6,588,220)
        doors = [('v',176,150,176),('v',390,168,194),('h',62,200,226),('h',110,470,500)]
        ext = ('h',6,470,512)
        lab = {'eng':['Engine Room 1'],'ele':['Electrical Room'],'ctl':['Control Room'],'A':['Frozen Zone A'],'B':['Frozen Zone B'],'C':['Chilled Zone C'],'dock':['Dock Buffer 2']}
        rk_w, lx, ly = 58, 14, 22
    else:
        W, H, ls, ts, tb = 320, 244, 11.5, 24, 30
        R = {'eng':(4,4,116,44),'ele':(120,4,100,44),'ctl':(220,4,96,44),
             'A':(4,48,138,112),'B':(142,48,174,112),'C':(4,160,166,80),'dock':(170,160,146,80)}
        OUT = (4,4,312,236)
        doors = [('v',142,98,122),('h',160,196,220),('h',48,60,82)]
        ext = ('h',240,226,262)
        lab = {'eng':['Engine','Room 1'],'ele':['Electrical','Room'],'ctl':['Control','Room'],'A':['Frozen Zone A'],'B':['Frozen Zone B'],'C':['Chilled Zone C'],'dock':['Dock Buffer 2']}
        rk_w, lx, ly = 44, 12, 18
    temps = {'A':ZONES['A'],'B':ZONES['B'],'C':ZONES['C'],'dock':ZONES['D']}
    marks = {'A':['EF-1'],'B':['CR-01','EF-3'],'C':['AHU-02']}
    o = [f'<svg class="plansvg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
         f'<defs><pattern id="hx{mode}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="{red}" stroke-opacity=".24" stroke-width="1"/></pattern></defs>']
    svc = ('eng','ele','ctl')
    for k,(x,y,w,h) in R.items():
        fill = '#F6F8F9' if k in svc else '#FFFFFF'
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{wall}" stroke-width="1.5"/>')
    x,y,w,h = R['B']
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFF8F6"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#hx{mode})"/>')
    ox,oy,ow,oh = OUT
    # red inner outline of zone B, then outer wall
    o.append(f'<rect x="{x+1.5}" y="{y+1.5}" width="{w-3}" height="{h-3}" fill="none" stroke="{red}" stroke-width="1.5"/>')
    o.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="none" stroke="#2F3A43" stroke-width="2.5"/>')
    # doors
    def gap(d, thick=4):
        a,c,p1,p2 = d
        if a == 'v':
            return (f'<rect x="{c-thick/2}" y="{p1}" width="{thick}" height="{p2-p1}" fill="#fff"/>'
                    f'<line x1="{c-3}" y1="{p1}" x2="{c+3}" y2="{p1}" stroke="{wall}" stroke-width="1.2"/><line x1="{c-3}" y1="{p2}" x2="{c+3}" y2="{p2}" stroke="{wall}" stroke-width="1.2"/>')
        return (f'<rect x="{p1}" y="{c-thick/2}" width="{p2-p1}" height="{thick}" fill="#fff"/>'
                f'<line x1="{p1}" y1="{c-3}" x2="{p1}" y2="{c+3}" stroke="{wall}" stroke-width="1.2"/><line x1="{p2}" y1="{c-3}" x2="{p2}" y2="{c+3}" stroke="{wall}" stroke-width="1.2"/>')
    for d in doors: o.append(gap(d))
    o.append(gap(ext, 5))
    # labels, temperatures, markers, racks
    for k,(x,y,w,h) in R.items():
        crit = k == 'B'
        for i,line in enumerate(lab[k]):
            o.append(f'<text x="{x+lx}" y="{y+ly+i*(ls+3)}" font-size="{ls}" font-weight="400" fill="{"#A8301D" if crit else mut}">{line}</text>')
        if k in temps:
            sz = tb if crit else ts
            o.append(f'<text x="{x+lx-1}" y="{y+ly+sz+(8 if D else 6)}" font-family="Bricolage Grotesque, Onest, sans-serif" font-size="{sz}" font-weight="600" letter-spacing="-.02em" fill="{"#B3321F" if crit else ink}">{t(temps[k])}</text>')
        for i,m in enumerate(marks.get(k,[])):
            mx = x+lx+i*(62 if D else 58); my = y+h-(18 if D else 16)
            c = red if (m=='CR-01') else '#4A5762'
            o.append(f'<rect x="{mx}" y="{my-4.5}" width="9" height="9" transform="rotate(45 {mx+4.5} {my})" fill="{"#fff" if m!="CR-01" else red}" stroke="{c}" stroke-width="1.3"/>')
            o.append(f'<text x="{mx+14}" y="{my+3.6}" font-size="{10.5 if D else 10}" font-weight="{600 if m=="CR-01" else 500}" fill="{"#A8301D" if m=="CR-01" else "#34414A"}">{m}</text>')
        if k in ('A','B'):
            n = 3 if D else (3 if k=='B' else 2)
            rx = x+w-rk_w-12; base = y+h-14
            for j in range(n):
                ry = base-(j*(16 if D else 15))-11
                for q in (0,6):
                    o.append(f'<rect x="{rx}" y="{ry+q}" width="{rk_w}" height="5" fill="none" stroke="{"#C4584A" if crit else "#9AA6AE"}" stroke-width="1"/>')
    if D:
        x,y,w,h = R['B']
        o.append(f'<g transform="translate({x+w-92},{y+9})"><path d="M5.5 1 L10.5 10 L0.5 10 Z" fill="none" stroke="#A8301D" stroke-width="1.3" stroke-linejoin="round"/><line x1="5.5" y1="4.2" x2="5.5" y2="6.8" stroke="#A8301D" stroke-width="1.2"/><text x="17" y="10" font-size="11.5" font-weight="600" fill="#A8301D">EXC-2417</text></g>')
        o.append(f'<text x="8" y="{H-3}" font-size="10.5" fill="#66727C">Temperatures in °C</text>')
        o.append(f'<g transform="translate({W-14},{H-14})" stroke="#66727C" fill="none" stroke-width="1.2"><path d="M0 12 L0 1 M-3 4 L0 0 L3 4"/></g><text x="{W-30}" y="{H-3}" font-size="10.5" fill="#66727C">N</text>')
    else:
        x,y,w,h = R['B']
        o.append(f'<g transform="translate({x+12},{y+64})"><path d="M5 1 L9.5 9.5 L0.5 9.5 Z" fill="none" stroke="#A8301D" stroke-width="1.2" stroke-linejoin="round"/><line x1="5" y1="4" x2="5" y2="6.4" stroke="#A8301D" stroke-width="1.1"/><text x="15" y="9.3" font-size="10.5" font-weight="600" fill="#A8301D">EXC-2417</text></g>')
    o.append('</svg>')
    return ''.join(o)

# ---------- incident zone chart (fine-grained series built from the same hourly readings) ----------
def zone_series():
    import numpy as np
    from scipy.interpolate import PchipInterpolator
    tk=np.arange(0,24)*60.0
    f=PchipInterpolator(tk,np.array(READINGS))
    t=np.arange(0,1381,5.0)
    noise=0.035*np.sin(t*0.21)+0.02*np.sin(t*0.6+1)
    taper=np.clip(np.minimum(t,1380-t)/20,0,1)
    th24=f(t)+noise*taper
    th24[-1]=READINGS[-1]
    ramp=np.clip((t-1140)/240,0,1); ramp=ramp*ramp*(3-2*ramp)
    th23=th24+0.5*ramp+0.03*np.sin(t*0.9)*ramp
    th23[-1]=round(READINGS[-1]+0.5,1)
    return t,th24,th23
def zone_chart(W=784,H=118,axis=22):
    t,a,b=zone_series()
    ymin,ymax=-20.0,-14.0
    X=lambda m:m/1380*W
    Y=lambda v:(ymax-v)/(ymax-ymin)*H
    def path(ts,vs): return 'M'+' L'.join(f'{X(x):.1f} {Y(v):.1f}' for x,v in zip(ts,vs))
    # crossing of the setpoint
    import numpy as np
    idx=next(i for i,v in enumerate(a) if v>SETPOINT and t[i]>=900)
    i0=idx-1
    cx=t[i0]+(SETPOINT-a[i0])/(a[idx]-a[i0])*(t[idx]-t[i0])
    hot_t=[cx]+list(t[idx:]); hot_v=[SETPOINT]+list(a[idx:])
    d0,d1,l1=1286,1286+47,1356   # planned defrost 08:50-09:37, loading ended 10:00
    inc=1020                     # incident opened Fri 04:24
    o=[f'<svg class="zchart" width="{W}" height="{H+axis}" viewBox="0 0 {W} {H+axis}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><pattern id="zh" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#fff" stroke-opacity=".28" stroke-width="1"/></pattern></defs>',
       f'<rect x="0" y="{Y(-18):.1f}" width="{W}" height="{H-Y(-18):.1f}" fill="#fff" fill-opacity=".09"/>',
       f'<rect x="{X(d0):.1f}" y="0" width="{X(l1)-X(d0):.1f}" height="{H}" fill="url(#zh)"/>',
       f'<line x1="0" x2="{W}" y1="{Y(-18):.1f}" y2="{Y(-18):.1f}" stroke="#fff" stroke-opacity=".6" stroke-dasharray="4 4"/>',
       f'<text x="4" y="{Y(-18)-5:.1f}" font-size="11" fill="#fff" fill-opacity=".7">{MINUS}18</text>',
       f'<text x="4" y="{H-6}" font-size="11" fill="#fff" fill-opacity=".6">Operating band, up to {MINUS}18 °C</text>',
       f'<line x1="{X(inc):.1f}" x2="{X(inc):.1f}" y1="0" y2="{H}" stroke="#fff" stroke-opacity=".5" stroke-dasharray="2 4"/>',
       f'<text x="{X(inc)-6:.1f}" y="11" font-size="11" text-anchor="end" fill="#fff" fill-opacity=".78">Incident opened 04:24</text>',
       f'<text x="{X(d0)-6:.1f}" y="11" font-size="11" text-anchor="end" fill="#fff" fill-opacity=".78">Defrost, loading</text>',
       f'<path d="{path(t,b)}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="1.5 3" stroke-linecap="round"/>',
       f'<path d="{path(t,a)}" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>',
       f'<path d="{path(hot_t,hot_v)}" fill="none" stroke="#FF8A78" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>',
       f'<circle cx="{X(1380):.1f}" cy="{Y(a[-1]):.1f}" r="4.5" fill="#fff" stroke="#FF8A78" stroke-width="2.4"/>']
    for m,lab in [(36,'12:00'),(276,'16:00'),(516,'20:00'),(756,'Fri 00:00'),(996,'04:00'),(1236,'08:00')]:
        o.append(f'<text x="{X(m):.1f}" y="{H+16}" font-size="11.5" text-anchor="middle" fill="#fff" fill-opacity=".7">{lab}</text>')
    o.append(f'<text x="{W}" y="{H+16}" font-size="11.5" text-anchor="end" fill="#fff" fill-opacity=".9" font-weight="500">10:24</text>')
    o.append('</svg>')
    return ''.join(o)

# ---------- incident correlation lanes (shared time axis, same synthetic story) ----------
def lane_chart(W=1272):
    import numpy as np
    fmt=globals()['t']
    t,a,b=zone_series()
    L,R=210,104
    PW=W-L-R
    X=lambda m:L+m/1380*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#EEF1F3'
    o=[f'<svg class="lanes" width="{W}" height="300" viewBox="0 0 {W} 300" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><pattern id="lh" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#9DB0BC" stroke-opacity=".7" stroke-width="1"/></pattern></defs>']
    ticks=[(36,'12:00'),(276,'16:00'),(516,'20:00'),(756,'Fri 00:00'),(996,'04:00'),(1236,'08:00')]
    for m,_ in ticks: o.append(f'<line x1="{X(m):.1f}" x2="{X(m):.1f}" y1="22" y2="268" stroke="{grid}"/>')
    # lane geometry: (top,height)
    LT=(24,86); LE=(118,36); LC=(162,36); LD=(206,26); LF=(240,26)
    def label(top,h,name,src,val,hot=False):
        o.append(f'<text x="0" y="{top+h/2-2}" font-size="13" font-weight="600" fill="{ink}">{name}</text>')
        o.append(f'<text x="0" y="{top+h/2+14}" font-size="11.5" fill="{mut}">{src}</text>')
        o.append(f'<text x="{W}" y="{top+h/2+5}" font-size="14" font-weight="600" text-anchor="end" fill="{coral if hot else ink}">{val}</text>')
    # lane separators
    for y in (114,158,202,236): o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{grid}"/>')
    # --- zone temperature
    ymin,ymax=-20.0,-14.0; top,h=LT
    Yt=lambda v: top+(ymax-v)/(ymax-ymin)*h
    o.append(f'<rect x="{L}" y="{Yt(-18):.1f}" width="{PW}" height="{top+h-Yt(-18):.1f}" fill="#E7F0F4"/>')
    o.append(f'<line x1="{L}" x2="{L+PW}" y1="{Yt(-18):.1f}" y2="{Yt(-18):.1f}" stroke="#7E919D" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{L-8}" y="{Yt(-18)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">{MINUS}18</text>')
    path=lambda ts,vs,Y:'M'+' L'.join(f'{X(x):.1f} {Y(v):.1f}' for x,v in zip(ts,vs))
    idx=next(i for i,v in enumerate(a) if v>SETPOINT and t[i]>=900); i0=idx-1
    cx=t[i0]+(SETPOINT-a[i0])/(a[idx]-a[i0])*(t[idx]-t[i0])
    o.append(f'<path d="{path(t,b,Yt)}" fill="none" stroke="#8A9AA5" stroke-width="1.4" stroke-dasharray="1.5 3" stroke-linecap="round"/>')
    o.append(f'<path d="{path(t,a,Yt)}" fill="none" stroke="{teal}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(f'<path d="{path([cx]+list(t[idx:]),[SETPOINT]+list(a[idx:]),Yt)}" fill="none" stroke="{coral}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(1380):.1f}" cy="{Yt(a[-1]):.1f}" r="4.5" fill="#fff" stroke="{coral}" stroke-width="2.4"/>')
    label(top,h,'Zone temperature','TH-24, TH-23 dotted',f'{fmt(CUR)} °C',True)
    # --- EF-3 current draw
    top,h=LE; Ye=lambda v: top+(6.0-v)/(6.0-3.0)*h
    rng=np.random.RandomState(7)
    cur=5.2+0.05*np.sin(t*0.5)+0.03*np.sin(t*1.7)
    drop=np.clip((t-936)/(1380-936),0,1); drop=drop**0.8
    cur=cur-1.3*drop; cur[-1]=3.9
    o.append(f'<line x1="{L}" x2="{L+PW}" y1="{Ye(5.2):.1f}" y2="{Ye(5.2):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>')
    o.append(f'<text x="{L-8}" y="{Ye(5.2)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">5.2 A</text>')
    o.append(f'<path d="{path(t,cur,Ye)}" fill="none" stroke="{teal}" stroke-width="1.8" stroke-linejoin="round"/>')
    label(top,h,'EF-3 current draw','Baseline 5.2 A','3.9 A')
    # --- CR-01 capacity (steps)
    top,h=LC; Yc=lambda v: top+(34.0-v)/(34.0-24.0)*h
    steps=[(0,32.4),(936,30.6),(1006,28.4),(1146,26.9),(1380,26.9)]
    d=f'M{X(steps[0][0]):.1f} {Yc(steps[0][1]):.1f}'
    for (m0,v0),(m1,v1) in zip(steps,steps[1:]): d+=f' L{X(m1):.1f} {Yc(v0):.1f} L{X(m1):.1f} {Yc(v1):.1f}'
    o.append(f'<line x1="{L}" x2="{L+PW}" y1="{Yc(32.4):.1f}" y2="{Yc(32.4):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>')
    o.append(f'<text x="{L-8}" y="{Yc(32.4)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">32.4 kW</text>')
    o.append(f'<path d="{d}" fill="none" stroke="{teal}" stroke-width="1.8" stroke-linejoin="round"/>')
    label(top,h,'CR-01 cooling capacity','Baseline 32.4 kW','26.9 kW')
    # --- door blocks
    top,h=LD
    for m0,m1 in [(166,196),(396,431),(606,641),(836,866),(1332,1356)]:
        o.append(f'<rect x="{X(m0):.1f}" y="{top+5}" width="{max(X(m1)-X(m0),4):.1f}" height="{h-10}" rx="3" fill="#B7C5CE"/>')
    label(top,h,'Door','DS-08, open blocks','Closed')
    # --- defrost blocks
    top,h=LF
    for m0,m1 in [(206,253),(566,613),(926,973),(1286,1333)]:
        o.append(f'<rect x="{X(m0):.1f}" y="{top+5}" width="{X(m1)-X(m0):.1f}" height="{h-10}" rx="3" fill="url(#lh)" stroke="#9DB0BC"/>')
    label(top,h,'Defrost','Planned, every 6 h','Idle')
    # --- incident marker
    inc=1020
    o.append(f'<line x1="{X(inc):.1f}" x2="{X(inc):.1f}" y1="18" y2="268" stroke="{coral}" stroke-dasharray="3 4"/>')
    o.append(f'<text x="{X(inc)-8:.1f}" y="14" font-size="11.5" font-weight="600" text-anchor="end" fill="#B3321F">Incident opened 04:24</text>')
    o.append(f'<line x1="{X(1380):.1f}" x2="{X(1380):.1f}" y1="18" y2="268" stroke="{ink}" stroke-opacity=".35"/>')
    o.append(f'<text x="{X(1380):.1f}" y="14" font-size="11.5" font-weight="600" text-anchor="end" fill="{ink}">Now</text>')
    for m,lab in ticks: o.append(f'<text x="{X(m):.1f}" y="288" font-size="11.5" text-anchor="middle" fill="{mut}">{lab}</text>')
    o.append(f'<text x="{X(1380):.1f}" y="288" font-size="11.5" font-weight="500" text-anchor="middle" fill="{ink}">10:24</text>')
    o.append('</svg>')
    return ''.join(o)

def lane_chart2(W=1236):
    import numpy as np
    fmt=globals()['t']
    t,a,b=zone_series()
    PL,PR=44,110
    PW=W-PL-PR
    X=lambda m:PL+m/1380*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#E9EDF0'
    H=424
    o=[f'<svg class="lanes" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><pattern id="lh2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#8FA4B1" stroke-opacity=".35" stroke-width="1"/></pattern>'
       '<linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".12"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient>'
       '<linearGradient id="gc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5543B" stop-opacity=".22"/><stop offset="1" stop-color="#E5543B" stop-opacity=".06"/></linearGradient></defs>']
    TT,TH=34,158            # temperature plot
    EF=(222,52); CR=(304,52) # small plots (top,h)
    BOT=CR[0]+CR[1]
    # event bands through all plots
    DEF=[(206,253),(566,613),(926,973),(1286,1333)]
    DOOR=[(166,196),(396,431),(606,641),(836,866),(1332,1356)]
    for m0,m1 in DEF:
        o.append(f'<rect x="{X(m0):.1f}" y="{TT}" width="{X(m1)-X(m0):.1f}" height="{BOT-TT}" fill="#EEF3F6"/><rect x="{X(m0):.1f}" y="{TT}" width="{X(m1)-X(m0):.1f}" height="{BOT-TT}" fill="url(#lh2)"/>')
    # temperature grid
    ymin,ymax=-19.6,-15.0
    Yt=lambda v: TT+(ymax-v)/(ymax-ymin)*TH
    for v in (-19,-18,-17,-16,-15):
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Yt(v):.1f}" y2="{Yt(v):.1f}" stroke="{grid}"/>')
        o.append(f'<text x="{PL-10}" y="{Yt(v)+4:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">{MINUS if v<0 else ""}{abs(v)}</text>')
    ticks=[(36,'12:00'),(276,'16:00'),(516,'20:00'),(756,'Fri 00:00'),(996,'04:00'),(1236,'08:00')]
    for m,_ in ticks: o.append(f'<line x1="{X(m):.1f}" x2="{X(m):.1f}" y1="{TT}" y2="{BOT}" stroke="{grid}" stroke-dasharray="2 4"/>')
    # setpoint
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Yt(-18):.1f}" y2="{Yt(-18):.1f}" stroke="#5E7380" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<text x="{PL+8}" y="{Yt(-18)-7:.1f}" font-size="11.5" fill="#5E7380">Upper limit {MINUS}18.0</text>')
    path=lambda ts,vs,Y:'M'+' L'.join(f'{X(x):.1f} {Y(v):.1f}' for x,v in zip(ts,vs))
    idx=next(i for i,v in enumerate(a) if v>SETPOINT and t[i]>=900); i0=idx-1
    cx=t[i0]+(SETPOINT-a[i0])/(a[idx]-a[i0])*(t[idx]-t[i0])
    # area under line
    hx=[cx]+list(t[idx:]); hv=[SETPOINT]+list(a[idx:])
    o.append(f'<path d="{path(hx,hv,Yt)} L{X(1380):.1f} {Yt(SETPOINT):.1f} Z" fill="url(#gc)"/>')
    o.append(f'<path d="{path(t,b,Yt)}" fill="none" stroke="#8A9AA5" stroke-width="1.6" stroke-dasharray="1.5 3" stroke-linecap="round"/>')
    o.append(f'<path d="{path(t[:idx],a[:idx],Yt)} L{X(cx):.1f} {Yt(SETPOINT):.1f}" fill="none" stroke="{teal}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<path d="{path(hx,hv,Yt)}" fill="none" stroke="{coral}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    # door ticks on baseline of temp plot
    for m0,m1 in DOOR:
        o.append(f'<rect x="{X(m0):.1f}" y="{TT+TH-12}" width="{max(X(m1)-X(m0),3):.1f}" height="8" rx="2" fill="#7E919D" fill-opacity=".75"/>')
    ye=Yt(a[-1])
    o.append(f'<circle cx="{X(1380):.1f}" cy="{ye:.1f}" r="5" fill="#fff" stroke="{coral}" stroke-width="2.6"/>')
    o.append(f'<text x="{W}" y="{ye+1:.1f}" font-size="19" font-weight="600" text-anchor="end" fill="{coral}" font-family="Bricolage Grotesque, Onest, sans-serif">{fmt(CUR)} °C</text>')
    o.append(f'<text x="{W}" y="{ye+19:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">TH-23 {fmt(-15.6)}</text>')
    o.append(f'<text x="{W}" y="{TT+8}" font-size="12.5" font-weight="600" text-anchor="end" fill="{ink}" opacity="0">.</text>')
    o.append(f'<text x="{PL+8}" y="{TT+18}" font-size="13" font-weight="600" fill="{ink}">Zone temperature</text><text x="{PL+138}" y="{TT+18}" font-size="12" fill="{mut}">TH-24</text>')
    # small panels
    rng=np.random.RandomState(11)
    def smallpanel(top,h,title,base_txt,series,y0,y1,base,endtxt,unit_dash=True,tt=None):
        tt=t if tt is None else tt
        Y=lambda v: top+(y1-v)/(y1-y0)*h
        o.append(f'<text x="{PL}" y="{top-9}" font-size="13" font-weight="600" fill="{ink}">{title}</text><text x="{PL+len(title)*7.4+10:.0f}" y="{top-9}" font-size="12" fill="{mut}">{base_txt}</text>')
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{top+h}" y2="{top+h}" stroke="{grid}"/>')
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(base):.1f}" y2="{Y(base):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>')
        o.append(f'<path d="{path(tt,series,Y)} L{X(1380):.1f} {top+h} L{X(0):.1f} {top+h} Z" fill="url(#ga)"/>')
        o.append(f'<path d="{path(tt,series,Y)}" fill="none" stroke="{teal}" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round"/>')
        o.append(f'<circle cx="{X(1380):.1f}" cy="{Y(series[-1]):.1f}" r="3.6" fill="#fff" stroke="{teal}" stroke-width="2"/>')
        o.append(f'<text x="{W}" y="{Y(series[-1])+5:.1f}" font-size="15" font-weight="600" text-anchor="end" fill="{ink}">{endtxt}</text>')
    sm=lambda x:x*x*(3-2*x)
    n=len(t)
    tf=np.concatenate([np.arange(0,1330,5.0),np.arange(1330,1381,1.0)])
    cur=ef3_current(tf)
    smallpanel(*EF,'EF-3 current draw','Baseline 4.8 A',cur,2.0,5.6,4.8,'4.5 A',tt=tf)
    wob2=np.cumsum(rng.randn(n))*0.05; wob2-=np.linspace(wob2[0],wob2[-1],n)
    cap=32.4+0.12*np.sin(t*0.2)+0.5*wob2*np.clip(1-t/1380,0.3,1)
    cap=cap-5.5*sm(np.clip((t-930)/450,0,1)); cap[-1]=26.9
    smallpanel(*CR,'CR-01 cooling capacity','Baseline 32.4 kW',cap,26.2,33.0,32.4,'26.9 kW')
    # markers
    inc=1020
    o.append(f'<line x1="{X(inc):.1f}" x2="{X(inc):.1f}" y1="{TT-4}" y2="{BOT}" stroke="{coral}" stroke-dasharray="3 4"/>')
    o.append(f'<circle cx="{X(inc):.1f}" cy="{TT-4}" r="3" fill="{coral}"/>')
    o.append(f'<text x="{X(inc)-8:.1f}" y="{TT-1}" font-size="11.5" font-weight="600" text-anchor="end" fill="#B3321F">Incident opened 04:24</text>')
    o.append(f'<line x1="{X(1380):.1f}" x2="{X(1380):.1f}" y1="{TT-4}" y2="{BOT}" stroke="{ink}" stroke-opacity=".3"/>')
    o.append(f'<text x="{X(1380)-8:.1f}" y="{TT-1}" font-size="11.5" font-weight="600" text-anchor="end" fill="{ink}">Now</text>')
    for m,lab in ticks: o.append(f'<text x="{X(m):.1f}" y="{BOT+22}" font-size="11.5" text-anchor="middle" fill="{mut}">{lab}</text>')
    o.append(f'<text x="{X(1380):.1f}" y="{BOT+22}" font-size="11.5" font-weight="600" text-anchor="middle" fill="{ink}">10:24</text>')
    items=[('#9DB0BC','Defrost'),('#5E7380','Door open'),(coral,'Above limit'),('#8A9AA5','TH-23, primary air')]
    cx0=PL+4; ly=BOT+56
    for c,l in items:
        o.append(f'<circle cx="{cx0+9}" cy="{ly}" r="9" fill="{c}" fill-opacity=".22"/><circle cx="{cx0+9}" cy="{ly}" r="4.5" fill="{c}"/>')
        o.append(f'<text x="{cx0+26}" y="{ly+4.5}" font-size="13.5" fill="#4A5560">{l}</text>')
        cx0+=26+len(l)*7.3+34
    o.append('</svg>')
    return ''.join(o)


# ---- EF-3 episode (one source of truth). minutes since Thu 11:24; Fri 09:38 = 1334, now 10:24 = 1380
EF_BASE=4.8
def ef3_current(tm):
    import numpy as np
    tm=np.asarray(tm,float); r=tm-1334.0
    rng=np.random.RandomState(3)
    cur=EF_BASE+0.03*np.sin(tm*0.33)+0.02*np.sin(tm*1.3)
    ramp=lambda a,b,x: np.clip((x-a)/(b-a),0,1)
    sm=lambda x:x*x*(3-2*x)
    cur=np.where(r>=12, EF_BASE-2.45*sm(ramp(12,14.5,r))+0.05*np.sin(r*1.7), cur)
    cur=np.where(r>=22, 2.35+1.25*sm(ramp(22,24.5,r))+0.05*np.sin(r*1.7), cur)
    cur=np.where(r>=24.5, 3.6+0.9*sm(ramp(24.5,36,r))+0.03*np.sin(r*1.7), cur)
    cur=np.where(tm>=1380, 4.5, cur)
    return cur
def ef3_airflow(tm):
    import numpy as np
    r=np.asarray(tm,float)-1334.0
    ramp=lambda a,b,x: np.clip((x-a)/(b-a),0,1)
    sm=lambda x:x*x*(3-2*x)
    dip=sm(ramp(12,15,r))*(1-sm(ramp(22,29,r)))
    out=100-40*dip+0.6*np.sin(r*1.1)
    return np.where(np.asarray(tm,float)>=1380,100.0,out)
def zone_fine(tm):
    import numpy as np
    t5,a,b=zone_series()
    tm=np.asarray(tm,float)
    return np.interp(tm,t5,a)+0.025*np.sin(tm*0.9)*(tm<1380)

def equip_chart(W=1236):
    """EF-3 telemetry and zone response, Fri 09:38 to 10:24, shared time axis."""
    import numpy as np
    fmt=globals()['t']
    PL,PR=56,100
    PW=W-PL-PR
    T0,T1=1334.0,1380.0
    X=lambda tm:PL+(tm-T0)/(T1-T0)*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#E9EDF0'
    tm=np.arange(T0,T1+0.01,0.5)
    ev=[(1346,'09:50','Current drop','detected','#5E7380'),(1349,'09:53','Backup mode','sent',teal),(1350,'09:54','Controller','acknowledged',teal),(1356,'10:00','Airflow','restored','#1F8A70')]
    CW,CHH=112,46
    cent=[PL+60,PL+178,PL+296,PL+414]
    LA=(122,54); LB=(214,46); LC=(300,38); LD=(386,84)   # (top,height)
    BOT=LD[0]+LD[1]
    H=BOT+22+50
    o=[f'<svg class="lanes" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><linearGradient id="ea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".13"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient></defs>']
    # time grid
    for mm in range(2,47,10):
        x=PL+mm/46*PW
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{LA[0]-6}" y2="{BOT}" stroke="{grid}" stroke-dasharray="2 4"/>')
    labs=[]
    lab=lambda top,h,title,sub: labs.append(f'<text x="{PL}" y="{top-9}" font-size="13" font-weight="600" fill="{ink}" stroke="#fff" stroke-width="4" paint-order="stroke">{title}</text><text x="{PL+len(title)*7.4+10:.0f}" y="{top-9}" font-size="12" fill="{mut}" stroke="#fff" stroke-width="4" paint-order="stroke">{sub}</text>')
    path=lambda xs,ys,Y:'M'+' L'.join(f'{X(a):.1f} {Y(b):.1f}' for a,b in zip(xs,ys))
    # lane separators
    for y in (LA[0]+LA[1]+14,LB[0]+LB[1]+14,LC[0]+LC[1]+14): o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{grid}"/>')
    # A: fan current
    top,h=LA; Y=lambda v: top+(6.0-v)/6.0*h
    for v in (0,3,6): o.append(f'<text x="{PL-10}" y="{Y(v)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">{v}</text>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(4.8):.1f}" y2="{Y(4.8):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>')
    cur=ef3_current(tm)
    o.append(f'<path d="{path(tm,cur,Y)} L{X(T1):.1f} {top+h} L{X(T0):.1f} {top+h} Z" fill="url(#ea)"/>')
    o.append(f'<path d="{path(tm,cur,Y)}" fill="none" stroke="{teal}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(4.5):.1f}" r="4" fill="#fff" stroke="{teal}" stroke-width="2.2"/>')
    o.append(f'<text x="{W}" y="{Y(4.5)+5:.1f}" font-size="16" font-weight="600" text-anchor="end" fill="{ink}">4.5 A</text>')
    lab(top,h,'Fan current','A, baseline 4.8')
    # B: airflow proxy
    top,h=LB; Y=lambda v: top+(110-v)/90*h
    for v in (60,100): o.append(f'<text x="{PL-10}" y="{Y(v)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">{v}%</text>')
    af=ef3_airflow(tm)
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(100):.1f}" y2="{Y(100):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>')
    o.append(f'<path d="{path(tm,af,Y)}" fill="none" stroke="#3E91AE" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(100):.1f}" r="4" fill="#fff" stroke="#3E91AE" stroke-width="2.2"/>')
    o.append(f'<text x="{W}" y="{Y(100)+5:.1f}" font-size="16" font-weight="600" text-anchor="end" fill="{ink}">100%</text>')
    lab(top,h,'Airflow proxy','% of baseline')
    # C: controller command (Off / Running / Backup)
    top,h=LC; lv={'Backup':top+4,'Running':top+h/2,'Off':top+h-4}
    for k,y in lv.items(): o.append(f'<text x="{PL-10}" y="{y+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">{k}</text>')
    xs=[T0,1349,1349,1356,1356,T1]; ys=[lv['Running'],lv['Running'],lv['Backup'],lv['Backup'],lv['Running'],lv['Running']]
    o.append(f'<path d="{path(xs,ys,lambda v:v)}" fill="none" stroke="{teal}" stroke-width="2.4" stroke-linejoin="round"/>')
    for xx,yy in ((1349,lv['Backup']),(1356,lv['Running'])): o.append(f'<circle cx="{X(xx):.1f}" cy="{yy:.1f}" r="4" fill="#fff" stroke="{teal}" stroke-width="2.2"/>')
    o.append(f'<text x="{W}" y="{lv["Running"]+5:.1f}" font-size="16" font-weight="600" text-anchor="end" fill="{ink}">Running</text>')
    lab(top,h,'Controller command','state')
    # D: zone temperature with safe band
    top,h=LD; Y=lambda v: top+(-14-v)/8*h
    o.append(f'<rect x="{PL}" y="{Y(-18):.1f}" width="{PW}" height="{Y(-22)-Y(-18):.1f}" fill="#E7F0F4"/>')
    for v in (-22,-20,-18,-16,-14): o.append(f'<text x="{PL-10}" y="{Y(v)+4:.1f}" font-size="11" text-anchor="end" fill="{mut}">{MINUS}{abs(v)}</text>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(-18):.1f}" y2="{Y(-18):.1f}" stroke="#5E7380" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<text x="{PL+8}" y="{Y(-18)+16:.1f}" font-size="11.5" fill="#5E7380">Safe band {MINUS}22 to {MINUS}18 °C</text>')
    zt=zone_fine(tm)
    o.append(f'<path d="{path(tm,zt,Y)} L{X(T1):.1f} {Y(-18):.1f} L{X(T0):.1f} {Y(-18):.1f} Z" fill="#E5543B" fill-opacity=".10"/>')
    o.append(f'<path d="{path(tm,zt,Y)}" fill="none" stroke="{coral}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(zt[-1]):.1f}" r="5" fill="#fff" stroke="{coral}" stroke-width="2.6"/>')
    o.append(f'<text x="{W}" y="{Y(zt[-1])-2:.1f}" font-size="17" font-weight="600" text-anchor="end" fill="{coral}" font-family="Bricolage Grotesque, Onest, sans-serif">{fmt(CUR)} °C</text>')
    o.append(f'<text x="{W}" y="{Y(zt[-1])+15:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">10:24</text>')
    lab(top,h,'Frozen Zone B','temperature, °C')
    # event leaders + cards
    for (em,tt,l1,l2,c),cx in zip(ev,cent):
        ex=X(em)
        o.append(f'<path d="M{cx} {CHH+2} L{cx} {CHH+10} L{ex:.1f} {CHH+22} L{ex:.1f} {LA[0]-6}" fill="none" stroke="{c}" stroke-width="1.4"/>')
        o.append(f'<line x1="{ex:.1f}" x2="{ex:.1f}" y1="{LA[0]-6}" y2="{BOT}" stroke="{c}" stroke-width="1.4" stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{ex:.1f}" cy="{LA[0]-6}" r="3" fill="{c}"/>')
        o.append(f'<rect x="{cx-CW/2}" y="0.5" width="{CW}" height="{CHH}" rx="10" fill="#fff" stroke="#D5DCE1"/><rect x="{cx-CW/2+10}" y="10" width="3" height="26" rx="1.5" fill="{c}" opacity="0"/>')
        o.append(f'<text x="{cx}" y="17" font-size="12.5" font-weight="600" text-anchor="middle" fill="{ink}">{tt}</text>')
        o.append(f'<text x="{cx}" y="31" font-size="11.5" text-anchor="middle" fill="{mut}">{l1}</text><text x="{cx}" y="43" font-size="11.5" text-anchor="middle" fill="{mut}">{l2}</text>')
    o.extend(labs)
    o.append(f'<line x1="{X(T1):.1f}" x2="{X(T1):.1f}" y1="{LA[0]-6}" y2="{BOT}" stroke="{ink}" stroke-opacity=".28"/>')
    # x axis
    for mm,lb in [(2,'09:40'),(12,'09:50'),(22,'10:00'),(32,'10:10'),(42,'10:20')]:
        o.append(f'<text x="{PL+mm/46*PW:.1f}" y="{BOT+22}" font-size="11.5" text-anchor="middle" fill="{mut}">{lb}</text>')
    o.append(f'<text x="{X(T1):.1f}" y="{BOT+22}" font-size="11.5" font-weight="600" text-anchor="middle" fill="{ink}">10:24</text>')
    # legend, plain text with halo dots
    items=[('#0C4A5C','Fan current'),('#3E91AE','Airflow proxy'),('#0C4A5C','Controller command'),('#E5543B','Zone temperature')]
    cx0=PL; ly=BOT+50
    for c,l in items:
        o.append(f'<circle cx="{cx0+9}" cy="{ly}" r="9" fill="{c}" fill-opacity=".22"/><circle cx="{cx0+9}" cy="{ly}" r="4.5" fill="{c}"/><text x="{cx0+26}" y="{ly+4.5}" font-size="13" fill="#4A5560">{l}</text>')
        cx0+=26+len(l)*6.8+22
    o.append('</svg>')
    return ''.join(o)

def equip_chart2(W=1236):
    import numpy as np
    fmt=globals()['t']
    PL,PR=176,104
    PW=W-PL-PR
    T0,T1=1334.0,1380.0
    X=lambda tm:PL+(tm-T0)/(T1-T0)*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#E9EDF0'
    tm=np.arange(T0,T1+0.01,0.5)
    ev=[(1346,'09:50','Current drop','detected'),(1349,'09:53','Backup mode','sent'),(1350,'09:54','Controller','acknowledged'),(1356,'10:00','Airflow','restored')]
    CW,CHH=112,46
    cent=[PL+170,PL+292,PL+414,PL+536]
    LA=(84,54); LB=(152,46); LC=(212,38); LD=(268,70)
    BOT=LD[0]+LD[1]
    H=BOT+34
    o=[f'<svg class="lanes" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><linearGradient id="ea2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".14"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient></defs>']
    # backup band + grid
    o.append(f'<rect x="{X(1349):.1f}" y="{LA[0]-8}" width="{X(1356)-X(1349):.1f}" height="{BOT-LA[0]+8}" fill="#EAF2F6"/>')
    for mm in range(2,47,5):
        x=PL+mm/46*PW
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{LA[0]-8}" y2="{BOT}" stroke="{grid}" stroke-dasharray="2 4"/>')
    for y in (LA[0]+LA[1]+9,LB[0]+LB[1]+9,LC[0]+LC[1]+9): o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{grid}"/>')
    path=lambda xs,ys,Y:'M'+' L'.join(f'{X(a):.1f} {Y(b):.1f}' for a,b in zip(xs,ys))
    def label(top,h,title,sub,val,col=ink):
        o.append(f'<text x="0" y="{top+h/2-1}" font-size="13" font-weight="600" fill="{ink}">{title}</text><text x="0" y="{top+h/2+15}" font-size="11.5" fill="{mut}">{sub}</text>')
        return val
    note=lambda x,y,txt: o.append(f'<text x="{x}" y="{y}" font-size="11" fill="#8794A0">{txt}</text>')
    # A fan current
    top,h=LA; Y=lambda v: top+(6.0-v)/6.0*h
    cur=ef3_current(tm)
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(4.8):.1f}" y2="{Y(4.8):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>'); note(PL+6,Y(4.8)-6,'Baseline 4.8 A')
    o.append(f'<path d="{path(tm,cur,Y)} L{X(T1):.1f} {top+h} L{X(T0):.1f} {top+h} Z" fill="url(#ea2)"/>')
    o.append(f'<path d="{path(tm,cur,Y)}" fill="none" stroke="{teal}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(4.5):.1f}" r="4.5" fill="#fff" stroke="{teal}" stroke-width="2.4"/>')
    o.append(f'<text x="{W}" y="{Y(4.5)+6:.1f}" font-size="17" font-weight="600" text-anchor="end" fill="{ink}">4.5 A</text>')
    label(top,h,'Fan current','EF-3, amperes','')
    # B airflow
    top,h=LB; Y=lambda v: top+(108-v)/60*h
    af=ef3_airflow(tm)
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(100):.1f}" y2="{Y(100):.1f}" stroke="#9DB0BC" stroke-dasharray="3 4"/>'); note(PL+6,Y(100)-6,'Baseline 100%')
    o.append(f'<path d="{path(tm,af,Y)}" fill="none" stroke="#3E91AE" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(100):.1f}" r="4.5" fill="#fff" stroke="#3E91AE" stroke-width="2.4"/>')
    o.append(f'<text x="{W}" y="{Y(100)+6:.1f}" font-size="17" font-weight="600" text-anchor="end" fill="{ink}">100%</text>')
    label(top,h,'Airflow proxy','% of baseline','')
    # C command
    top,h=LC; yb,yr=top+6,top+h-8
    note(PL+6,yb+4,'Backup')
    xs=[T0,1349,1349,1356,1356,T1]; ys=[yr,yr,yb,yb,yr,yr]
    o.append(f'<path d="{path(xs,ys,lambda v:v)}" fill="none" stroke="{teal}" stroke-width="2.6" stroke-linejoin="round"/>')
    for xx,yy in ((1349,yb),(1356,yr)): o.append(f'<circle cx="{X(xx):.1f}" cy="{yy:.1f}" r="4.5" fill="#fff" stroke="{teal}" stroke-width="2.4"/>')
    o.append(f'<text x="{W}" y="{yr+6:.1f}" font-size="17" font-weight="600" text-anchor="end" fill="{ink}">Running</text>')
    label(top,h,'Controller command','state','')
    # D zone temp
    top,h=LD; Y=lambda v: top+(-15-v)/5*h
    o.append(f'<rect x="{PL}" y="{Y(-18):.1f}" width="{PW}" height="{Y(-20)-Y(-18):.1f}" fill="#E7F0F4"/>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(-18):.1f}" y2="{Y(-18):.1f}" stroke="#5E7380" stroke-width="1.2" stroke-dasharray="5 4"/>')
    note(PL+6,Y(-18)+15,'Safe band, '+MINUS+'22 to '+MINUS+'18 °C')
    zt=zone_fine(tm)
    o.append(f'<path d="{path(tm,zt,Y)} L{X(T1):.1f} {Y(-18):.1f} L{X(T0):.1f} {Y(-18):.1f} Z" fill="{coral}" fill-opacity=".10"/>')
    o.append(f'<path d="{path(tm,zt,Y)}" fill="none" stroke="{coral}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(zt[-1]):.1f}" r="5" fill="#fff" stroke="{coral}" stroke-width="2.6"/>')
    o.append(f'<text x="{W}" y="{Y(zt[-1])+6:.1f}" font-size="17" font-weight="600" text-anchor="end" fill="{coral}" font-family="Bricolage Grotesque, Onest, sans-serif">{fmt(CUR)} °C</text>')
    label(top,h,'Frozen Zone B','temperature, °C','')
    # event hairlines + cards
    for (em,tt,l1,l2),cx in zip(ev,cent):
        ex=X(em)
        o.append(f'<path d="M{cx} {CHH+1} L{cx} {CHH+10} L{ex:.1f} {CHH+22} L{ex:.1f} {LA[0]-8}" fill="none" stroke="#9DB0BC" stroke-width="1.2"/>')
        o.append(f'<line x1="{ex:.1f}" x2="{ex:.1f}" y1="{LA[0]-8}" y2="{BOT}" stroke="#9DB0BC" stroke-width="1.2" stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{ex:.1f}" cy="{LA[0]-8}" r="3.2" fill="{teal}"/>')
        o.append(f'<rect x="{cx-CW/2}" y="0.5" width="{CW}" height="{CHH}" rx="10" fill="#fff" stroke="#D5DCE1"/>')
        o.append(f'<text x="{cx}" y="17" font-size="12.5" font-weight="600" text-anchor="middle" fill="{ink}">{tt}</text><text x="{cx}" y="31" font-size="11.5" text-anchor="middle" fill="{mut}">{l1}</text><text x="{cx}" y="43" font-size="11.5" text-anchor="middle" fill="{mut}">{l2}</text>')
    o.append(f'<line x1="{X(T1):.1f}" x2="{X(T1):.1f}" y1="{LA[0]-8}" y2="{BOT}" stroke="{ink}" stroke-opacity=".28"/>')
    for mm,lb in [(2,'09:40'),(7,'09:45'),(12,'09:50'),(17,'09:55'),(22,'10:00'),(27,'10:05'),(32,'10:10'),(37,'10:15'),(42,'10:20')]:
        o.append(f'<text x="{PL+mm/46*PW:.1f}" y="{BOT+22}" font-size="11.5" text-anchor="middle" fill="{mut}">{lb}</text>')
    o.append(f'<text x="{X(T1):.1f}" y="{BOT+22}" font-size="11.5" font-weight="600" text-anchor="middle" fill="{ink}">10:24</text>')
    o.append('</svg>')
    return ''.join(o)

def equip_chart3(W=850):
    import numpy as np
    fmt=globals()['t']
    PL,PR=34,84
    PW=W-PL-PR
    T0,T1=1334.0,1380.0
    X=lambda tm:PL+(tm-T0)/(T1-T0)*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#E9EDF0'
    tm=np.arange(T0,T1+0.01,0.5)
    EV=[(1346,'1'),(1349,'2'),(1350,'3'),(1356,'4')]
    M=(14,128); S1=(180,34); S2=(238,28); S3=(290,42)
    BOT=S3[0]+S3[1]
    H=BOT+32
    o=[f'<svg class="lanes" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><linearGradient id="e3a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".20"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient></defs>']
    # backup band
    o.append(f'<rect x="{X(1349):.1f}" y="{M[0]}" width="{X(1356)-X(1349):.1f}" height="{BOT-M[0]}" rx="6" fill="#EAF2F6"/>')
    o.append(f'<text x="{(X(1349)+X(1356))/2:.1f}" y="{M[0]+M[1]-8}" font-size="11" text-anchor="middle" fill="#6E8796">Backup fan on</text>')
    path=lambda xs,ys,Y:'M'+' L'.join(f'{X(a):.1f} {Y(b):.1f}' for a,b in zip(xs,ys))
    # main: fan current
    top,h=M; Y=lambda v: top+(6.0-v)/6.0*h
    for v in (0,2,4,6):
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{grid}"/><text x="{PL-10}" y="{Y(v)+4:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">{v}</text>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(4.8):.1f}" y2="{Y(4.8):.1f}" stroke="#7E919D" stroke-dasharray="4 4"/><text x="{PL+8}" y="{Y(4.8)-7:.1f}" font-size="11.5" fill="#66727C">Normal 4.8 A</text>')
    cur=ef3_current(tm)
    o.append(f'<path d="{path(tm,cur,Y)} L{X(T1):.1f} {Y(0):.1f} L{X(T0):.1f} {Y(0):.1f} Z" fill="url(#e3a)"/>')
    o.append(f'<path d="{path(tm,cur,Y)}" fill="none" stroke="{teal}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(4.5):.1f}" r="5" fill="#fff" stroke="{teal}" stroke-width="2.6"/>')
    o.append(f'<text x="{W}" y="{Y(4.5)-2:.1f}" font-size="22" font-weight="600" text-anchor="end" fill="{ink}" font-family="Bricolage Grotesque, Onest, sans-serif">4.5 A</text><text x="{W}" y="{Y(4.5)+15:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">Power draw</text>')
    # hairlines through strips
    for em,_ in EV:
        o.append(f'<line x1="{X(em):.1f}" x2="{X(em):.1f}" y1="{M[0]+M[1]}" y2="{BOT}" stroke="#B8C6CF" stroke-width="1" stroke-dasharray="2 3"/>')
    # strips
    def title(top,t1,t2): o.append(f'<text x="{PL}" y="{top-8}" font-size="12.5" font-weight="600" fill="{ink}">{t1}</text><text x="{PL+len(t1)*7.2+8:.0f}" y="{top-8}" font-size="12" fill="{mut}">{t2}</text>')
    top,h=S1; Y=lambda v: top+(106-v)/56*h
    title(top,'Airflow','% of normal')
    af=ef3_airflow(tm)
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{top+h}" y2="{top+h}" stroke="{grid}"/>')
    o.append(f'<path d="{path(tm,af,Y)}" fill="none" stroke="#3E91AE" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(100):.1f}" r="4" fill="#fff" stroke="#3E91AE" stroke-width="2.2"/><text x="{W}" y="{Y(100)+5:.1f}" font-size="15" font-weight="600" text-anchor="end" fill="{ink}">100%</text>')
    top,h=S2; yb,yr=top+5,top+h-5
    title(top,'Backup fan','on during the dip')
    xs=[T0,1349,1349,1356,1356,T1]; ys=[yr,yr,yb,yb,yr,yr]
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{top+h}" y2="{top+h}" stroke="{grid}"/>')
    o.append(f'<path d="{path(xs,ys,lambda v:v)}" fill="none" stroke="{teal}" stroke-width="2.6" stroke-linejoin="round"/>')
    for xx,yy in ((1349,yb),(1356,yr)): o.append(f'<circle cx="{X(xx):.1f}" cy="{yy:.1f}" r="4" fill="#fff" stroke="{teal}" stroke-width="2.2"/>')
    o.append(f'<text x="{W}" y="{yr+5:.1f}" font-size="15" font-weight="600" text-anchor="end" fill="{ink}">Off</text>')
    top,h=S3; Y=lambda v: top+(-15-v)/5*h
    title(top,'Frozen Zone B','temperature, °C')
    o.append(f'<rect x="{PL}" y="{Y(-18):.1f}" width="{PW}" height="{Y(-20)-Y(-18):.1f}" fill="#E7F0F4"/><line x1="{PL}" x2="{PL+PW}" y1="{Y(-18):.1f}" y2="{Y(-18):.1f}" stroke="#5E7380" stroke-dasharray="5 4"/><text x="{PL+8}" y="{Y(-18)+14:.1f}" font-size="11" fill="#7C8B97">Safe band up to {MINUS}18</text>')
    zt=zone_fine(tm)
    o.append(f'<path d="{path(tm,zt,Y)} L{X(T1):.1f} {Y(-18):.1f} L{X(T0):.1f} {Y(-18):.1f} Z" fill="{coral}" fill-opacity=".10"/>')
    o.append(f'<path d="{path(tm,zt,Y)}" fill="none" stroke="{coral}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(zt[-1]):.1f}" r="4.5" fill="#fff" stroke="{coral}" stroke-width="2.4"/><text x="{W}" y="{Y(zt[-1])+6:.1f}" font-size="15" font-weight="600" text-anchor="end" fill="{coral}">{fmt(CUR)} °C</text>')
    # pins on main curve
    for em,n in EV:
        c=ef3_current(np.array([em]))[0]
        Ym=M[0]+(6.0-c)/6.0*M[1]
        if n=='3':
            o.append(f'<line x1="{X(em):.1f}" x2="{X(em):.1f}" y1="{Ym:.1f}" y2="{Ym-24:.1f}" stroke="{teal}" stroke-width="1.6"/>'); Ym-=26
        o.append(f'<circle cx="{X(em):.1f}" cy="{Ym:.1f}" r="10.5" fill="{teal}" stroke="#fff" stroke-width="2.5"/><text x="{X(em):.1f}" y="{Ym+4:.1f}" font-size="11.5" font-weight="600" text-anchor="middle" fill="#fff">{n}</text>')
    o.append(f'<line x1="{X(T1):.1f}" x2="{X(T1):.1f}" y1="{M[0]}" y2="{BOT}" stroke="{ink}" stroke-opacity=".25"/>')
    for mm,lb in [(2,'09:40'),(12,'09:50'),(22,'10:00'),(32,'10:10'),(42,'10:20')]:
        o.append(f'<text x="{PL+mm/46*PW:.1f}" y="{BOT+22}" font-size="11.5" text-anchor="middle" fill="{mut}">{lb}</text>')
    o.append(f'<text x="{X(T1):.1f}" y="{BOT+22}" font-size="11.5" font-weight="600" text-anchor="middle" fill="{ink}">10:24</text>')
    o.append('</svg>')
    return ''.join(o)

def equip_chart4(W=1236,hover=None):
    """Plain story: one line (fan power draw), three labelled moments."""
    import numpy as np
    PL,PR=20,120
    PW=W-PL-PR
    T0,T1=1334.0,1380.0
    X=lambda tm:PL+(tm-T0)/(T1-T0)*PW
    ink,teal,mut='#11181C','#0C4A5C','#66727C'
    TOP,H0=70,150
    Y=lambda v: TOP+(6.0-v)/6.0*H0
    BOT=TOP+H0
    H=BOT+56
    tm=np.arange(T0,T1+0.01,0.5)
    cur=ef3_current(tm)
    o=[f'<svg class="lanes" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><linearGradient id="e4a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".18"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient>'
       '<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0C2632" flood-opacity=".10"/></filter></defs>']
    # backup band
    bx0,bx1=X(1349),X(1356)
    o.append(f'<rect x="{bx0:.1f}" y="{TOP-6}" width="{bx1-bx0:.1f}" height="{H0+6}" rx="8" fill="#E6F0F4"/>')
    o.append(f'<text x="{(bx0+bx1)/2:.1f}" y="{BOT-30}" font-size="13" font-weight="600" text-anchor="middle" fill="#3E6A7C">Backup fan on</text><text x="{(bx0+bx1)/2:.1f}" y="{BOT-12}" font-size="12" text-anchor="middle" fill="#6E8796">09:53 to 10:00</text>')
    # baseline
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(4.8):.1f}" y2="{Y(4.8):.1f}" stroke="#7E919D" stroke-width="1.2" stroke-dasharray="5 5"/>')
    o.append(f'<text x="{PL}" y="{Y(4.8)-8:.1f}" font-size="12.5" fill="{mut}">Normal, 4.8 A</text>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{BOT}" y2="{BOT}" stroke="#E3E8EC"/>')
    path='M'+' L'.join(f'{X(a):.1f} {Y(b):.1f}' for a,b in zip(tm,cur))
    o.append(f'<path d="{path} L{X(T1):.1f} {BOT} L{X(T0):.1f} {BOT} Z" fill="url(#e4a)"/>')
    o.append(f'<path d="{path}" fill="none" stroke="{teal}" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"/>')
    # end
    o.append(f'<circle cx="{X(T1):.1f}" cy="{Y(4.5):.1f}" r="6" fill="#fff" stroke="{teal}" stroke-width="3"/>')
    o.append(f'<text x="{W}" y="{Y(4.5)+2:.1f}" font-size="28" font-weight="600" text-anchor="end" fill="{ink}" font-family="Bricolage Grotesque, Onest, sans-serif">4.5 A</text>')
    o.append(f'<text x="{W}" y="{Y(4.5)+22:.1f}" font-size="12.5" text-anchor="end" fill="{mut}">Now, still a bit low</text>')
    # hover points + serious tooltips
    style='<style>.pt .tip,.pt .cur{opacity:0;pointer-events:none;transition:opacity .15s}.pt:hover .tip,.pt:hover .cur,.pt.on .tip,.pt.on .cur{opacity:1}.pt .hit{cursor:pointer}.pt .dot{transition:r .12s}.pt:hover .dot,.pt.on .dot{r:7.5}</style>'
    o.append(style)
    ZF=globals()['zone_fine']
    def point(key,em,side,tag,tagbg,tagfg,foot,backup):
        c=float(ef3_current(np.array([em]))[0]); af=float(ef3_airflow(np.array([em]))[0])
        px,py=X(em),Y(c)
        cls='pt on' if hover==key else 'pt'
        g=[f'<g class="{cls}">']
        g.append(f'<line class="cur" x1="{px:.1f}" x2="{px:.1f}" y1="{TOP-6}" y2="{BOT}" stroke="#7E919D" stroke-width="1.2" stroke-dasharray="3 3"/>')
        g.append(f'<circle class="dot" cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#fff" stroke="{teal}" stroke-width="3"/>')
        g.append(f'<circle class="hit" cx="{px:.1f}" cy="{py:.1f}" r="20" fill="transparent"/>')
        # tooltip card
        w,hh=270,254; y0=(H-hh)/2
        x0=px+18 if side=='r' else px-18-w
        g.append(f'<g class="tip" filter="url(#sh)">')
        g.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w}" height="{hh}" rx="14" fill="#fff" stroke="#CBD4DA"/>')
        ay=min(max(py,y0+24),y0+hh-24)
        if side=='r': g.append(f'<path d="M{x0:.1f} {ay-8:.1f} L{x0-9:.1f} {ay:.1f} L{x0:.1f} {ay+8:.1f}" fill="#fff" stroke="#CBD4DA"/><line x1="{x0:.1f}" x2="{x0:.1f}" y1="{ay-7.2:.1f}" y2="{ay+7.2:.1f}" stroke="#fff" stroke-width="2.4"/>')
        else: g.append(f'<path d="M{x0+w:.1f} {ay-8:.1f} L{x0+w+9:.1f} {ay:.1f} L{x0+w:.1f} {ay+8:.1f}" fill="#fff" stroke="#CBD4DA"/><line x1="{x0+w:.1f}" x2="{x0+w:.1f}" y1="{ay-7.2:.1f}" y2="{ay+7.2:.1f}" stroke="#fff" stroke-width="2.4"/>')
        L=x0+20; R=x0+w-20
        hm=int(em-1334)+9*60+38; tmstr=f'{hm//60:02d}:{hm%60:02d}'
        g.append(f'<text x="{L:.1f}" y="{y0+30:.1f}" font-size="15" font-weight="600" fill="{ink}">Fri, Nov 6, {tmstr}</text>')
        tw=len(tag)*7.2+22
        g.append(f'<rect x="{R-tw:.1f}" y="{y0+14:.1f}" width="{tw:.1f}" height="24" rx="8" fill="{tagbg}"/><text x="{R-tw/2:.1f}" y="{y0+30.5:.1f}" font-size="11" font-weight="600" letter-spacing=".08em" text-anchor="middle" fill="{tagfg}">{tag}</text>')
        g.append(f'<line x1="{L-4:.1f}" x2="{R+4:.1f}" y1="{y0+48:.1f}" y2="{y0+48:.1f}" stroke="#E3E8EC"/>')
        rows=[('s',teal,'Power draw',f'{c:.1f} A'),('s','#3E91AE','Airflow',f'{af:.0f}% of normal'),('o','#8794A0','Backup fan',backup)]
        for k,(kind,col,lab,val) in enumerate(rows):
            ry=y0+48+28+k*30
            if kind=='s': g.append(f'<circle cx="{L+6:.1f}" cy="{ry-5:.1f}" r="5.5" fill="{col}"/>')
            else: g.append(f'<circle cx="{L+6:.1f}" cy="{ry-5:.1f}" r="4.6" fill="#fff" stroke="{col}" stroke-width="2"/>')
            g.append(f'<text x="{L+22:.1f}" y="{ry:.1f}" font-size="14" fill="{ink}">{lab}</text><text x="{R:.1f}" y="{ry:.1f}" font-size="14" font-weight="600" text-anchor="end" fill="#3B4750">{val}</text>')
        dy=y0+48+28+3*30-8
        g.append(f'<line x1="{L-4:.1f}" x2="{R+4:.1f}" y1="{dy:.1f}" y2="{dy:.1f}" stroke="#E3E8EC"/>')
        frac=min(max(c/4.8,0),1)
        g.append(f'<rect x="{L:.1f}" y="{dy+16:.1f}" width="{R-L:.1f}" height="8" rx="4" fill="#E4E9ED"/><rect x="{L:.1f}" y="{dy+16:.1f}" width="{(R-L)*frac:.1f}" height="8" rx="4" fill="{teal}"/>')
        g.append(f'<text x="{L:.1f}" y="{dy+44:.1f}" font-size="12.5" fill="{mut}">{frac*100:.0f}% of normal draw</text><text x="{R:.1f}" y="{dy+44:.1f}" font-size="12.5" text-anchor="end" fill="{mut}">Normal 4.8 A</text>')
        fy=dy+58
        g.append(f'<line x1="{L-4:.1f}" x2="{R+4:.1f}" y1="{fy:.1f}" y2="{fy:.1f}" stroke="#D5DCE1" stroke-dasharray="3 3"/>')
        g.append(f'<text x="{L:.1f}" y="{fy+22:.1f}" font-size="13" fill="{mut}">{foot}</text>')
        g.append('</g></g>')
        o.append(''.join(g))
    for mm,lb in [(2,'09:40'),(12,'09:50'),(22,'10:00'),(32,'10:10'),(42,'10:20')]:
        o.append(f'<text x="{PL+mm/46*PW:.1f}" y="{BOT+26}" font-size="12" text-anchor="middle" fill="{mut}">{lb}</text>')
    o.append(f'<text x="{X(T1):.1f}" y="{BOT+26}" font-size="12" font-weight="600" text-anchor="middle" fill="{ink}">10:24</text>')
    point('a',1346,'l','FAN SLOWED','#FFE9DA','#8A3B0B','Power draw starts to fall','Off')
    point('b',1356,'r','RECOVERING','#DCEBF1','#0C4A5C','Airflow starts to come back','Just switched off')
    o.append('</svg>')
    return ''.join(o)


# ---- Energy week (one source of truth). minutes since Fri Oct 30 10:24; now = Fri Nov 6 10:24 = 10080
def energy_week():
    import numpy as np
    m=np.arange(0,10081,15.0)
    clock=(10*60+24+m)%1440            # minutes of day
    day=((10*60+24+m)//1440).astype(int)  # 0=Fri Oct30 .. 7=Fri Nov 6
    wd=(day+4)%7                         # Mon=0 ... Fri=4, Sat=5, Sun=6  (day0 is Fri)
    wk=(wd<5).astype(float)
    h=clock/60
    g=lambda x,c,w:np.exp(-((x-c)/w)**2)
    base=33.0+7.2*g(h,9.0,3.0)*wk+11.5*g(h,16.6,2.7)*wk+4.5*g(h,15.5,3.5)*(1-wk)+3.0*g(h,11,2.5)-2.6*g(h,3.5,3.0)
    dfs=[2*60+50,8*60+50,14*60+50,20*60+50]
    dcur=np.zeros_like(m)
    for d0 in dfs:
        x=(clock-d0)
        dcur+=3.0*np.clip(np.minimum(x,47-x)/6,0,1)*((x>=0)&(x<=47))
    base=base+dcur
    noise=0.45*np.sin(m/37)+0.18*np.sin(m/13+1.3)
    return m,clock,day,wd,base,noise
def energy_actual(k):
    import numpy as np
    m,clock,day,wd,base,noise=energy_week()
    sm=lambda x:x*x*(3-2*x)
    cr2=k*sm(np.clip((m-(3*1440-10*60-24+6*60))/(1440),0,1))*(1+0.18*np.sin(m/53))   # CR-02 short cycling from Mon Nov 2 06:00
    inc=np.clip((m-(10080-7*60))/(7*60),0,1)**1.4   # incident ramp from Fri 03:24
    a=base+noise*0.8+cr2
    return a,inc
def energy_solve():
    import numpy as np
    m,clock,day,wd,base,noise=energy_week()
    bl=base+noise*0.0
    # matched baseline: smooth version of the same pattern (no noise)
    inc_end=0.0
    def stats(k,inc_peak):
        a,inc=energy_actual(k)
        a=a+inc_peak*inc
        return a
    # fix incident excess so that now = 48.2 kW
    lo,hi=0.0,8.0
    for _ in range(60):
        k=(lo+hi)/2
        a0,inc=energy_actual(k)
        peak=48.2-a0[-1]
        a=a0+peak*inc
        v=(a.sum()-bl.sum())/bl.sum()*100
        if v<3.7: lo=k
        else: hi=k
    return m,bl,a,k,peak


def energy_chart(W=1236,compact=False,th=188):
    import numpy as np
    m,bl,a,k,peak=energy_solve()
    clock=(10*60+24+m)%1440; day=((10*60+24+m)//1440).astype(int)
    PL,PR=(124,96) if compact else (150,96)
    PW=W-PL-PR
    X=lambda mm:PL+mm/10080*PW
    ink,teal,coral,mut,grid='#11181C','#0C4A5C','#E5543B','#66727C','#E9EDF0'
    TT,TH=26,th
    y0,y1=26.0,56.0
    Y=lambda v:TT+(y1-v)/(y1-y0)*TH
    LANE0=TT+TH+24; LH=27
    lanes=['Zones outside band','Active incidents','Defrost cycles','Loading windows']
    BOT=LANE0+LH*4
    H=BOT+66
    o=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
       '<defs><linearGradient id="ge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5543B" stop-opacity=".34"/><stop offset="1" stop-color="#E5543B" stop-opacity=".14"/></linearGradient>'
       '<linearGradient id="gp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".10"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient></defs>']
    # day columns
    mids=[816+1440*i for i in range(7)]   # midnights Sat 31 .. Fri 6
    names=['Sat 31 Oct','Sun 1 Nov','Mon 2 Nov','Tue 3 Nov','Wed 4 Nov','Thu 5 Nov','Fri 6 Nov']
    if compact: names=['Sat 31','Sun 1','Mon 2','Tue 3','Wed 4','Thu 5','Fri 6']
    for i,mm in enumerate(mids):
        if i%2==0: o.append(f'<rect x="{X(mm):.1f}" y="{TT}" width="{X(min(mm+1440,10080))-X(mm):.1f}" height="{BOT-TT}" fill="#F7F9FA"/>')
    o.append(f'<rect x="{PL}" y="{TT}" width="{X(816)-PL:.1f}" height="{BOT-TT}" fill="#F7F9FA" opacity="0"/>')
    for v in (30,40,50):
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{grid}"/>')
        o.append(f'<text x="{PL-12}" y="{Y(v)+4:.1f}" font-size="12" text-anchor="end" fill="{mut}">{v}</text>')
    o.append(f'<text x="0" y="{TT+12}" font-size="13" font-weight="600" fill="{ink}">Refrigeration</text><text x="0" y="{TT+30}" font-size="13" font-weight="600" fill="{ink}">demand</text><text x="0" y="{TT+48}" font-size="12" fill="{mut}">kW</text>')
    # overlap bands
    ov=[]
    for i in range(0,8):
        d0=i*1440-624+14*60+50   # 14:50 on day i
        wdi=(i+4)%7
        if wdi<5 and 0<=d0<10080: ov.append(d0)
    assert len(ov)==5,len(ov)
    for d0 in ov:
        o.append(f'<rect x="{X(d0):.1f}" y="{LANE0+2*LH}" width="{X(d0+47)-X(d0):.1f}" height="{LH*2}" fill="#FFE9E3"/>')
    # lanes
    for i,l in enumerate(lanes):
        yy=LANE0+i*LH
        o.append(f'<text x="0" y="{yy+LH/2+4:.1f}" font-size="13" fill="#34414A">{l}</text>')
        o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{yy+LH:.1f}" y2="{yy+LH:.1f}" stroke="{grid}"/>')
    o.append(f'<line x1="{PL}" x2="{PL+PW}" y1="{LANE0}" y2="{LANE0}" stroke="{grid}"/>')
    for i,mm in enumerate(mids):
        o.append(f'<line x1="{X(mm):.1f}" x2="{X(mm):.1f}" y1="{TT}" y2="{BOT}" stroke="#E3E8EC" stroke-dasharray="2 4"/>')
        o.append(f'<text x="{X(mm)+8:.1f}" y="{BOT+22}" font-size="12" fill="{mut}">{names[i]}</text>')
    o.append(f'<text x="{PL+8}" y="{BOT+22}" font-size="12" fill="{mut}">{"Fri 30" if compact else "Fri 30 Oct"}</text>')
    bar=lambda x0,x1,row,c,h=12:f'<rect x="{X(x0):.1f}" y="{LANE0+row*LH+(LH-h)/2:.1f}" width="{max(X(x1)-X(x0),3):.1f}" height="{h}" rx="3" fill="{c}"/>'
    o.append(bar(10080-270,10080,0,'#E5543B'))
    o.append(bar(10080-360,10080,1,'#F2A093'))
    for i in range(0,8):
        for d0 in (2*60+50,8*60+50,14*60+50,20*60+50):
            s0=i*1440-624+d0
            if 0<=s0<10080: o.append(bar(s0,min(s0+47,10080),2,'#8FB8CE'))
        wdi=(i+4)%7
        wins=[(6*60,8*60+30),(15*60,17*60+30)] if wdi<5 else [(9*60,11*60)]
        for w0,w1 in wins:
            s0=i*1440-624+w0; s1=i*1440-624+w1
            if s1>0 and s0<10080: o.append(bar(max(s0,0),min(s1,10080),3,'#B4BFC7'))
    # demand
    path=lambda xs,ys:'M'+' L'.join(f'{X(x):.1f} {Y(v):.1f}' for x,v in zip(xs,ys))
    segs=[];cur=[]
    for i in range(len(m)):
        if a[i]>bl[i]+0.05: cur.append(i)
        else:
            if len(cur)>1: segs.append(cur)
            cur=[]
    if len(cur)>1: segs.append(cur)
    for sg in segs:
        top=' L'.join(f'{X(m[i]):.1f} {Y(a[i]):.1f}' for i in sg)
        bot=' L'.join(f'{X(m[i]):.1f} {Y(bl[i]):.1f}' for i in reversed(sg))
        o.append(f'<path d="M{top} L{bot} Z" fill="url(#ge)"/>')
    o.append(f'<path d="{path(m,bl)}" fill="none" stroke="#8A9AA5" stroke-width="1.5" stroke-dasharray="1.5 3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="{path(m,a)}" fill="none" stroke="{teal}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    # incident + now
    inc=10080-360
    o.append(f'<line x1="{X(inc):.1f}" x2="{X(inc):.1f}" y1="{TT-4}" y2="{BOT}" stroke="{coral}" stroke-dasharray="3 4"/><circle cx="{X(inc):.1f}" cy="{TT-4}" r="3" fill="{coral}"/>')
    o.append(f'<text x="{X(inc)-8:.1f}" y="{TT-1}" font-size="11.5" font-weight="600" text-anchor="end" fill="#B3321F">{"Opened 04:24" if compact else "Incident opened 04:24"}</text>')
    o.append(f'<line x1="{X(10080):.1f}" x2="{X(10080):.1f}" y1="{TT-4}" y2="{BOT}" stroke="{ink}" stroke-opacity=".3"/>')
    o.append(f'<text x="{X(10080)+(6 if compact else -8):.1f}" y="{TT-1}" font-size="11.5" font-weight="600" text-anchor="{'start' if compact else 'end'}" fill="{ink}">Now</text>')
    ye=Y(a[-1])
    o.append(f'<circle cx="{X(10080):.1f}" cy="{ye:.1f}" r="5" fill="#fff" stroke="{teal}" stroke-width="2.4"/>')
    o.append(f'<text x="{W}" y="{ye+1:.1f}" font-size="19" font-weight="600" text-anchor="end" fill="{ink}" font-family="Bricolage Grotesque, Onest, sans-serif">{a[-1]:.1f} kW</text>')
    o.append(f'<text x="{W}" y="{ye+19:.1f}" font-size="11.5" text-anchor="end" fill="{mut}">Baseline {bl[-1]:.1f}</text>')
    items=[(teal,'Actual demand'),('#8A9AA5','Matched baseline'),(coral,'Above baseline'),('#8FB8CE','Defrost cycle'),('#B4BFC7','Loading window'),('#F2A093','Defrost overlaps loading')]
    if compact: items=[(teal,'Actual'),('#8A9AA5','Baseline'),(coral,'Above baseline'),('#8FB8CE','Defrost'),('#B4BFC7','Loading'),('#F2A093','Overlap')]
    cx0=PL+4; ly=BOT+46
    for c,l in items:
        if l=='Defrost overlaps loading': c='#F2A093'
        o.append(f'<circle cx="{cx0+9}" cy="{ly}" r="9" fill="{c}" fill-opacity=".25"/><circle cx="{cx0+9}" cy="{ly}" r="4.5" fill="{c}"/>')
        o.append(f'<text x="{cx0+26}" y="{ly+4.5}" font-size="13.5" fill="#4A5560">{l}</text>')
        cx0+=26+len(l)*7.3+30
    o.append('</svg>')
    return ''.join(o)
