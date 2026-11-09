import sys; sys.path.insert(0,'/home/claude/nivalis')
from common import *
TABS=['Conditions','Systems','Energy','Doors','Cold chain','Activity']
CSS=font_css()+'''
:root{--ink:#11181C;--muted:#55616B;--faint:#66727C;--line:#E3E8EC;--sect:#F1F4F6;--petrol:#0C4A5C;--coral:#FF8A78;--red:#D6432C;--crit-bg:#FFE4DE;--crit-ink:#8A1C0F;--ui:'Onest',system-ui,sans-serif;--disp:'Bricolage Grotesque','Onest',sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:393px;height:852px;overflow:hidden}
body{position:relative;font-family:var(--ui);color:var(--ink);font-size:14px;line-height:20px;-webkit-font-smoothing:antialiased;background:#EDF2F5;background-image:radial-gradient(420px 300px at 100% 0%,#D9EEF4 0%,rgba(217,238,244,0) 100%),radial-gradient(360px 280px at 0% 60%,#E4EEF0 0%,rgba(228,238,240,0) 100%)}
.ic{flex:none;display:block}
.pg{position:absolute;left:0;right:0;top:0;bottom:0;padding:59px 16px 0}
.nav{height:44px;display:flex;align-items:center;justify-content:space-between}
.logo{height:28px;width:auto;mix-blend-mode:multiply}
.nb{display:flex;gap:8px}
.ib{position:relative;width:44px;height:44px;border-radius:14px;background:#fff;border:1px solid #DCE3E8;display:flex;align-items:center;justify-content:center}
.ib i{position:absolute;top:-5px;right:-5px;min-width:17px;height:17px;border-radius:9px;background:#D92D20;color:#fff;font-style:normal;font-size:11px;font-weight:600;line-height:17px;text-align:center;border:2px solid #fff;box-sizing:content-box;padding:0 1px}
h1{font-family:var(--disp);font-weight:600;font-size:21px;line-height:26px;letter-spacing:-.02em;margin-top:12px;white-space:nowrap}
.chips{margin-top:8px;display:flex;align-items:center;gap:8px}
.sel{white-space:nowrap;flex:none;height:32px;display:inline-flex;align-items:center;gap:6px;padding:0 8px 0 10px;border-radius:10px;background:#fff;font-size:13.5px;border:1px solid #DCE3E8}
.sel .ic:last-child{color:var(--faint)}
.sel.dt{margin-left:auto;font-size:12.5px;padding:0 10px 0 8px;gap:5px;color:#3B4750}.sel.dt .ic{color:var(--faint)}
.tabs{margin:10px -16px 0;padding:0 16px;display:flex;gap:22px;border-bottom:1px solid #DCE3E8;height:38px;overflow:hidden}
.tab{height:38px;line-height:36px;font-size:14px;color:var(--muted);white-space:nowrap;border-bottom:2px solid transparent;margin-bottom:-1px}
.tab.on{color:var(--ink);font-weight:500;border-color:var(--ink)}
.hero{position:relative;margin-top:12px;border-radius:24px;background:var(--petrol);color:#fff;padding:18px 20px 0;overflow:hidden}
.hero:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 9px);-webkit-mask-image:linear-gradient(110deg,transparent 15%,#000 85%);mask-image:linear-gradient(110deg,transparent 15%,#000 85%)}
.hero:after{content:'';position:absolute;left:-30px;top:30px;width:300px;height:180px;background:radial-gradient(closest-side,rgba(96,214,232,.30),rgba(96,214,232,0));pointer-events:none}
.hero>*{position:relative;z-index:1}
.hh{display:flex;justify-content:space-between;align-items:flex-start}
.hh b{display:block;font-size:17px;font-weight:600;line-height:22px}
.hh .s{display:block;font-size:12.5px;color:rgba(255,255,255,.74);line-height:17px;margin-top:1px}
.pill{display:inline-flex;align-items:center;gap:5px;height:26px;padding:0 11px;border-radius:999px;font-size:12.5px;font-weight:600;white-space:nowrap;background:var(--crit-bg);color:var(--crit-ink)}
.fig{font-family:var(--disp);font-weight:600;font-size:60px;line-height:64px;letter-spacing:-.035em;white-space:nowrap;margin-top:8px}
.fig .neg{display:inline-block;width:.34em;height:.085em;background:#fff;border-radius:2px;margin-right:.07em;vertical-align:.27em}
.fig .dec{color:rgba(255,255,255,.52)} .fig .u{font-size:22px;letter-spacing:0;position:relative;top:-22px;margin-left:5px;color:rgba(255,255,255,.78);font-weight:500}
.st{display:flex;justify-content:space-between;font-size:13px;line-height:20px;padding:4px 0;border-top:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.74)}
.st b{font-weight:600;color:#fff;font-size:14px} .st b.w{color:var(--coral)}
.sts{margin-top:8px}
.strip{position:relative}
.tk{position:absolute;bottom:0;border-radius:3px;background:rgba(255,255,255,.34)}
.tk.hot{background:var(--coral)}
.sp{position:absolute;left:0;right:0;height:0;border-top:1px dashed rgba(255,255,255,.5)}
.axis{position:relative;height:16px;margin-top:5px}
.al{position:absolute;top:0;font-size:11px;color:rgba(255,255,255,.72);white-space:nowrap}
.sect{position:absolute;left:16px;right:16px;background:var(--sect);border-radius:22px;padding:4px}
.sh{height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 14px}
.sh h2{font-size:16px;font-weight:600}
.sh span{font-size:12.5px;color:var(--faint)}
.inner{background:#fff;border-radius:18px;border:1px solid var(--line);overflow:hidden}
.eng{padding:16px 16px 14px;border-bottom:1px solid #EEF1F3}
.eng .k{font-size:13px;color:var(--muted)}
.eng .v{font-family:var(--disp);font-weight:600;font-size:30px;line-height:34px;letter-spacing:-.02em} .eng .v small{font-family:var(--ui);font-size:14px;color:var(--muted);font-weight:500;margin-left:4px;letter-spacing:0}
.trk{height:8px;border-radius:99px;background:#E4E9ED;margin-top:10px;overflow:hidden} .trk i{display:block;height:100%;border-radius:99px;background:var(--petrol)}
.eng .m{display:flex;justify-content:space-between;font-size:12.5px;color:var(--faint);margin-top:7px}
.kv{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid #EEF1F3;font-size:14px} .kv span{color:var(--muted)} .kv b{font-weight:600}
.fade{position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(180deg,rgba(237,242,245,0),#EDF2F5 62%)}
.dock{position:absolute;left:16px;right:16px;bottom:30px;background:#fff;border-radius:24px;padding:14px;box-shadow:0 12px 32px -8px rgba(12,38,50,.28)}
.dock .tx{font-size:13.5px;line-height:18px;padding:0 4px 12px;color:var(--ink)} .dock .tx span{color:var(--muted)}
.dock .bs{display:flex;gap:8px}
.btn{height:46px;display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:15px;font-size:14.5px;font-weight:500;white-space:nowrap}
.btn.o{border:1px solid #CBD3D9;background:#fff;width:132px}
.btn.p{background:#11181C;color:#fff;flex:1}
/* plan */
.rooms{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:8px 8px 0}
.room{border-radius:10px;background:#F5F7F8;border:1px solid #E6EAED;padding:7px 9px;height:56px}
.room b{display:block;font-weight:500;font-size:12px;line-height:15px} .room em{display:block;font-style:normal;font-size:11.5px;color:var(--faint);line-height:15px;margin-top:2px}
.zb{position:relative;margin:6px 8px 0;border-radius:16px;background:var(--petrol);color:#fff;padding:14px 16px 0;height:206px;overflow:hidden}
.zb:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 9px);-webkit-mask-image:linear-gradient(110deg,transparent 10%,#000 85%);mask-image:linear-gradient(110deg,transparent 10%,#000 85%)}
.zb:after{content:'';position:absolute;left:-30px;top:20px;width:260px;height:160px;background:radial-gradient(closest-side,rgba(96,214,232,.28),rgba(96,214,232,0))}
.zb>*{position:relative;z-index:1}
.zb .fig{font-size:56px;line-height:60px;margin-top:4px}
.tg{display:flex;gap:6px;position:absolute;left:16px;bottom:14px}
.tag{height:22px;padding:0 8px;border-radius:6px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);font-size:12px;line-height:20px;color:#fff}
.zr{position:absolute;right:16px;bottom:14px;text-align:right;font-size:12.5px;color:rgba(255,255,255,.76)} .zr b{display:block;font-size:14px;color:var(--coral);font-weight:600}
.zs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px 8px 8px}
.z{border-radius:14px;padding:10px 10px;height:116px;border:1px solid #D3DAE0;position:relative}
.z.a{background:#EAF3F9}.z.c{background:#EAF5EE}.z.d{background:#F4F6F7}
.z .l{font-size:12.5px;line-height:16px;font-weight:500;color:#34414A}
.z .t{font-family:var(--disp);font-weight:600;font-size:26px;line-height:30px;letter-spacing:-.02em;margin-top:6px} .z .t small{font-family:var(--ui);font-size:12px;color:var(--muted);font-weight:500;margin-left:2px;position:relative;top:-8px;letter-spacing:0}
.z .tag{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.85);border:1px solid #D3DAE0;color:#34414A;height:20px;font-size:11.5px;line-height:18px;padding:0 6px}
/* systems */
.cnt{height:24px;padding:0 10px;border-radius:999px;font-size:12px;line-height:24px;background:#E3E8EC;color:#3A4650;font-weight:500;white-space:nowrap} .cnt.c{background:var(--crit-bg);color:var(--crit-ink);font-weight:600}
.srch{height:44px;border-radius:14px;background:rgba(255,255,255,.85);border:1px solid #DCE3E8;display:flex;align-items:center;gap:8px;padding:0 12px;color:var(--faint);font-size:14px}
.row{height:68px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid #EEF1F3}
.row:last-of-type{border-bottom:0}
.row b{display:block;font-size:14.5px;font-weight:600;line-height:19px} .row em{display:block;font-style:normal;font-size:12.5px;color:var(--faint);line-height:17px;margin-top:1px}
.row .r{text-align:right} .row .r b{font-weight:500}
.hero.hs .fig{font-size:64px;line-height:68px}
.ticks8{display:flex;gap:8px;align-items:flex-end;height:48px;margin-top:16px}
.ticks8 i{flex:1;height:34px;border-radius:4px;background:rgba(255,255,255,.34)} .ticks8 i.hot{height:48px;background:var(--coral)}
'''
def shell(active=0,h1='Baltimore Cold Distribution Center'):
    tabs=''.join(f'<div class="tab {"on" if i==active else ""}">{n}</div>' for i,n in enumerate(TABS))
    return f'''<div class="nav"><img class="logo" src="{LOGO}" alt="Nivalis Building Operations"><div class="nb"><span class="ib">{icon("bell",20)}<i>1</i></span><span class="ib">{icon("menu",20)}</span></div></div>
<h1>{h1}</h1>
<div class="chips"><span class="sel">{icon("building",16)}BCD-01{icon("chevdown",14)}</span><span class="sel">Floor 1{icon("chevdown",14)}</span><span class="sel dt">{icon("clock",14)}{NOW}</span></div>
<div class="tabs">{tabs}</div>'''
def dock():
    return f'''<div class="dock"><div class="tx">EXC-2417 is active. <span>Zone B is {DEV} °C high.</span></div><div class="bs"><span class="btn o">Investigate</span><span class="btn p">Open EXC-2417{icon("arrow",17,1.75)}</span></div></div>'''
def page(body,extra=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}{extra}</body></html>'

def m1():
    kv=[('Active equipment','2 of 2 running'),('Door state','Closed'),('Zone B access','Closed'),('Next maintenance, PM-3172','Nov 23'),('Last service','Oct 23')]
    kvh=''.join(f'<div class="kv"><span>{a}</span><b>{b}</b></div>' for a,b in kv)
    hero=f'''<section class="hero"><div class="hh"><div><b>Frozen Zone B</b><span class="s">Incident EXC-2417, active</span></div><span class="pill">{icon("alert",14,1.75)}Critical</span></div>
 <div class="fig" aria-label="{t(CUR)} degrees Celsius"><span class="neg"></span>16<span class="dec">.1</span><span class="u">°C</span></div>
 <div class="sts"><div class="st"><span>Setpoint</span><b>{t(SETPOINT)} °C</b></div><div class="st"><span>Deviation</span><b class="w">+{DEV} °C</b></div><div class="st"><span>24 h range</span><b>{t(LO)} to {t(HI)} °C</b></div></div>
 <div style="margin-top:14px;padding-bottom:14px">{ticks_html(321,6,46,10,46,0)}</div></section>'''
    sect=f'''<section class="sect" style="top:600px"><div class="sh"><h2>Energy and equipment</h2></div><div class="inner"><div class="eng"><div class="k">Energy load</div><div class="v">{ENERGY}<small>kW</small></div><div class="trk"><i style="width:{ENERGY/CAP*100:.1f}%"></i></div><div class="m"><span>{PCT}% of capacity</span><span>{CAP} kW</span></div></div>{kvh}</div></section>'''
    return page(f'<div class="pg">{shell(0)}{hero}</div>{sect}<div class="fade"></div>{dock()}')

def m2():
    hero=f'''<section class="hero" style="padding-bottom:12px"><div class="hh"><div><b>Frozen Zone B</b><span class="s">Incident EXC-2417, active</span></div><span class="pill">{icon("alert",14,1.75)}Critical</span></div>
 <div style="display:flex;align-items:flex-end;justify-content:space-between"><div class="fig" style="font-size:56px;line-height:60px" aria-label="{t(CUR)} degrees Celsius"><span class="neg"></span>16<span class="dec">.1</span><span class="u">°C</span></div>
 <div style="text-align:right;padding-bottom:6px;font-size:12.5px;color:rgba(255,255,255,.74);line-height:17px">Deviation<b style="display:block;font-size:15px;color:var(--coral);font-weight:600">+{DEV} °C</b></div></div></section>'''
    sect=f'<section class="sect" style="top:396px"><div class="sh"><h2>Floor plan</h2><span>Floor 1, temperatures in °C</span></div><div class="inner" style="padding:6px 6px 4px">{plan_svg("m")}</div></section>'
    return page(f'<div class="pg">{shell(0)}{hero}</div>{sect}{dock()}','<style>.plansvg{width:100%;display:block}</style>')
def m3():
    rows=''
    for s in SYSTEMS:
        rows+=f'<div class="row" style="{"background:#FFF3F0" if s["id"]=="CR-01" else ""}"><div><b>{s["id"]}</b><em>{s["sub"]}</em></div><div class="r"><b>{s["signal"]}</b><em>{s["owner"]}</em></div></div>'
    ticks=''.join(f'<i class="{"hot" if i==0 else ""}"></i>' for i in range(N_TOTAL))
    hero=f'''<section class="hero hs" style="padding-bottom:18px"><div class="hh"><div><b>Needs action</b><span class="s">CR-01, Refrigeration, Frozen B</span></div><span class="pill">{icon("alert",14,1.75)}Critical</span></div>
 <div class="fig">{N_CRIT}<span class="u" style="font-size:20px;top:-26px;margin-left:8px">of {N_TOTAL} systems</span></div><div class="ticks8">{ticks}</div></section>'''
    sect=f'''<section class="sect" style="top:488px"><div class="sh"><h2>Building systems</h2><span>Showing {len(SYSTEMS)} of {N_TOTAL}</span></div><div class="inner">{rows}</div></section>'''
    chips=f'<div class="chips" style="margin-top:0"></div>'
    body=f'<div class="pg">{shell(1,"Baltimore Cold Distribution Center")}{hero}</div>{sect}<div class="fade"></div>{dock()}'
    return page(body)
if __name__=='__main__':
    for n,f in [('mobile-1-conditions',m1),('mobile-2-floor-plan',m2),('mobile-3-systems',m3)]:
        render(f(),f'{ROOT}/out/{n}.png',393,852,3)
