import sys; sys.path.insert(0,'/home/claude/nivalis')
from common import *

NAV=[('Buildings','building',True),('Incidents','alert',False),('Cold chain','snow',False),('Refrigeration','thermo',False),('Energy','zap',False),('Sensors','wifi',False),('Maintenance','tool',False),('Evidence','evidence',False),('Administration','settings',False)]
PLAN_B64=open('/home/claude/nivalis/plan_b64.txt').read()
TABS=['Conditions','Systems','Energy','Doors','Cold chain','Activity']

def racks(cols=8,rows=3,w=150,h=46):
    cw=w/cols; rh=h/rows; r=[]
    for j in range(rows):
        for i in range(cols):
            r.append(f'<rect x="{i*cw+1:.1f}" y="{j*rh+2:.1f}" width="{cw-2:.1f}" height="{rh-5:.1f}" rx="1.5"/>')
    return f'<svg class="racks" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(r)}</svg>'

def zone(name,temp,tags,cls='',note=''):
    return f'''<div class="zone {cls}"><div class="zl">{name}</div><div class="zt">{t(temp)}<small>°C</small></div>
    <div class="ztags">{"".join(f'<span class="tag">{x}</span>' for x in tags)}</div>{note}{racks() if cls!="dock" else racks(6,3,110,46)}</div>'''

def build():
    rows=''
    for s in SYSTEMS:
        crit=s['status']=='Critical'
        st=f'<span class="pill crit">{icon("alert",14,1.75)}Critical</span>' if crit else '<span class="ok">Normal</span>'
        sig,at=s['signal'],'at 10:24'
        act=f'<span class="act">{s["action"]}</span>' if crit else '<span class="none">None</span>'
        rows+=f'''<tr class="{'hot' if crit else ''}"><td class="id"><b>{s["id"]}</b><em>{s["sub"]}</em></td><td>{st}</td><td class="sig">{sig} <em>{at}</em></td><td>{s["owner"]}</td><td>{act}</td></tr>'''
    kv=[('Active equipment','2 of 2 running'),('Door state','Closed'),('Zone B access','Closed'),('Next maintenance, PM-3172','Nov 23'),('Last service','Oct 23')]
    kvh=''.join(f'<div class="kv"><span>{a}</span><b>{b}</b></div>' for a,b in kv)
    nav=''.join(f'<div class="nav {"on" if on else ""}">{icon(ic,18)}<span>{n}</span></div>' for n,ic,on in NAV)
    tabs=''.join(f'<div class="tab {"on" if i==0 else ""}">{n}</div>' for i,n in enumerate(TABS))
    css=f'''{font_css()}
:root{{--frame:#EEF2F5;--ink:#11181C;--muted:#55616B;--faint:#66727C;--line:#E3E8EC;--sect:#F3F5F7;--petrol:#0C4A5C;--coral:#FF8A78;--red:#D6432C;--crit-bg:#FFE4DE;--crit-ink:#8A1C0F;--ui:'Onest',system-ui,sans-serif;--disp:'Bricolage Grotesque','Onest',sans-serif}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1600px;height:1000px;overflow:hidden}}
body{{background:radial-gradient(1100px 700px at 100% 0%,#C7E6EC 0%,rgba(199,230,236,0) 70%),radial-gradient(900px 700px at 0% 100%,#D3E3F1 0%,rgba(211,227,241,0) 70%),linear-gradient(160deg,#DDEFF2 0%,#E8EFF4 50%,#DCE6F0 100%);font-family:var(--ui);color:var(--ink);font-size:14px;line-height:20px;-webkit-font-smoothing:antialiased;position:relative}}
.num{{font-variant-numeric:tabular-nums}}
.ic{{flex:none;display:block}}
.side{{position:absolute;left:0;top:0;width:232px;height:1000px;padding:26px 16px 24px}}
.logo{{display:block;height:36px;width:auto;mix-blend-mode:multiply;margin-left:4px}}
.org{{margin-top:24px;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 10px 0 12px;background:#fff;border:1px solid #D5DEE4;border-radius:14px;box-shadow:0 1px 2px rgba(12,38,50,.06)}} .org .ud{{flex:none;width:26px;height:26px;margin-left:6px;border-radius:8px;background:#F1F4F6;display:flex;align-items:center;justify-content:center;color:#55616B}}
.org b{{display:block;white-space:nowrap;font-size:13px;font-weight:600;line-height:18px}} .org span{{display:block;font-size:12px;color:var(--faint);line-height:16px}}
.navs{{margin-top:22px}}
.nav{{height:38px;display:flex;align-items:center;gap:12px;padding:0 12px;border-radius:10px;font-size:14px;color:#3B4750;margin-bottom:2px}}
.nav.on{{background:#fff;color:var(--ink);font-weight:600;box-shadow:0 1px 2px rgba(12,38,50,.08),0 4px 12px -4px rgba(12,38,50,.16);border:1px solid #D5DEE4;padding:0 11px}} .nav.on .ic{{color:var(--petrol)}}
.sync{{position:absolute;left:20px;bottom:24px;font-size:12px;line-height:16px;color:var(--faint)}} .sync b{{display:block;font-weight:400;color:var(--ink);margin-top:2px}}
.sheet{{position:absolute;left:232px;top:8px;right:8px;bottom:8px;background:radial-gradient(700px 360px at 100% 0%,rgba(190,228,236,.55),rgba(190,228,236,0) 70%),radial-gradient(600px 400px at 0% 100%,rgba(205,224,240,.45),rgba(205,224,240,0) 70%),#fff;border-radius:22px;padding:26px 28px 0;overflow:hidden}}
.sheet:before{{content:'';position:absolute;inset:0;background-image:radial-gradient(circle,#9FB3C0 1.1px,transparent 1.5px);background-size:16px 16px;-webkit-mask-image:linear-gradient(200deg,#000 0%,rgba(0,0,0,.0) 75%);mask-image:linear-gradient(200deg,#000 0%,rgba(0,0,0,0) 75%);opacity:.7;pointer-events:none}}
.sheet>*{{position:relative}}
.top{{display:flex;align-items:center;justify-content:space-between;height:44px}}
.top .l,.top .r{{display:flex;align-items:center;gap:14px}}
h1{{font-family:var(--disp);font-weight:600;font-size:27px;line-height:32px;letter-spacing:-.025em}}
.sel{{height:34px;display:inline-flex;align-items:center;gap:8px;padding:0 10px 0 12px;border:1px solid #D8DEE3;border-radius:10px;background:#fff;font-size:14px;color:var(--ink)}}
.sel .ic:last-child{{color:var(--faint)}} .sel.dtb{{padding:0 12px 0 10px;color:#3B4750}} .sel.dtb .ic:last-child{{color:var(--faint)}}
.date{{font-size:13px;color:var(--muted)}}
.bell{{position:relative;width:34px;height:34px;background:#fff;border:1px solid #D8DEE3;border-radius:10px;box-shadow:0 1px 2px rgba(12,38,50,.05);display:flex;align-items:center;justify-content:center}}
.bell i{{position:absolute;top:-6px;right:-6px;min-width:17px;height:17px;border-radius:9px;background:#D92D20;color:#fff;font-style:normal;font-size:11px;font-weight:600;line-height:17px;text-align:center;box-shadow:0 0 0 2px #fff}}
.tabsrow{{margin-top:12px;display:flex;align-items:flex-end;justify-content:space-between;border-bottom:1px solid var(--line);height:42px}}
.tabs{{display:flex;gap:26px}}
.tab{{height:42px;line-height:40px;font-size:14px;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-1px}}
.tab.on{{color:var(--ink);font-weight:500;border-color:var(--ink)}}
.tabsrow .sel{{margin-bottom:6px;height:30px;font-size:13px}}
.r2{{margin-top:16px;display:grid;grid-template-columns:560px 1fr;gap:16px;height:318px}}
.r3{{margin-top:16px;display:grid;grid-template-columns:800px 1fr;gap:16px;height:540px}}
/* hero */
.hero{{position:relative;border-radius:22px;background:var(--petrol);color:#fff;padding:24px 28px 0;overflow:hidden}}
.hero:before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 18%,#000 80%);mask-image:linear-gradient(100deg,transparent 18%,#000 80%)}}
.hero:after{{content:'';position:absolute;left:-40px;top:40px;width:420px;height:260px;background:radial-gradient(closest-side,rgba(96,214,232,.30),rgba(96,214,232,0));pointer-events:none}}
.hero>*{{position:relative;z-index:1}}
.hh{{display:flex;justify-content:space-between;align-items:flex-start}}
.hh b{{font-size:20px;font-weight:600;line-height:26px;letter-spacing:-.01em;display:block}}
.hh span.s{{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px;margin-top:2px}}
.pill{{display:inline-flex;align-items:center;gap:5px;height:24px;padding:0 10px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap}}
.pill.crit{{background:var(--crit-bg);color:var(--crit-ink)}}
.hero .pill.crit{{height:26px;font-size:13px;padding:0 12px}}
.fr{{display:flex;align-items:flex-end;justify-content:space-between;margin-top:14px}}
.fig{{font-family:var(--disp);font-weight:600;font-size:64px;line-height:68px;letter-spacing:-.035em;white-space:nowrap}}
.fig .neg{{display:inline-block;width:.34em;height:.085em;background:#fff;border-radius:2px;margin-right:.07em;vertical-align:.27em}} .fig .dec{{color:rgba(255,255,255,.52)}} .fig .u{{font-size:24px;letter-spacing:0;position:relative;top:-24px;margin-left:5px;color:rgba(255,255,255,.78);font-weight:500}}
.sts{{width:236px;padding-bottom:6px}}
.st{{display:flex;justify-content:space-between;font-size:13px;line-height:20px;padding:3px 0;border-top:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.72)}}
.st:first-child{{border-top:0}} .st b{{font-weight:600;color:#fff;font-size:14px}} .st b.w{{color:var(--coral)}}
.stripbox{{position:absolute;left:28px;bottom:42px}}
.strip{{position:relative}}
.tk{{position:absolute;bottom:0;border-radius:4px;background:rgba(255,255,255,.34)}}
.tk.hot{{background:var(--coral)}}
.sp{{position:absolute;left:0;right:0;height:0;border-top:1px dashed rgba(255,255,255,.5)}}
.axis{{position:relative;height:18px;margin-top:6px}}
.al{{position:absolute;top:0;font-size:12px;color:rgba(255,255,255,.7);white-space:nowrap}}
/* sections */
.sect{{background:var(--sect);border-radius:18px;padding:4px;display:flex;flex-direction:column;min-height:0}}
.sh{{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 14px 0 14px}}
.sh h2{{font-size:15px;font-weight:600;line-height:20px}}
.sh .lft{{display:flex;align-items:center;gap:10px}}
.cnt{{height:24px;padding:0 9px;border-radius:999px;font-size:12px;line-height:24px;background:#E8ECEF;color:#3A4650;font-weight:500}} .cnt.c{{background:var(--crit-bg);color:var(--crit-ink);font-weight:600}}
.search{{width:230px;height:32px;border:1px solid #D8DEE3;background:#fff;border-radius:9px;display:flex;align-items:center;gap:8px;padding:0 10px;color:var(--faint);font-size:13px}}
.inner{{flex:1;min-height:0;background:#fff;border-radius:14px;border:1px solid var(--line);overflow:hidden;display:flex;flex-direction:column}}
table{{width:100%;border-collapse:collapse;table-layout:fixed}}
th{{height:38px;text-align:left;font-size:12px;font-weight:400;color:var(--faint);padding:0 0 0 18px;border-bottom:1px solid var(--line)}}
td{{height:76px;padding:0 0 0 18px;font-size:14px;border-bottom:1px solid #EEF1F3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
tr.hot td{{background:#FFF5F3}}
td.id b{{display:block;font-weight:600;font-size:14px;line-height:19px}} td.sig{{padding-right:6px}} td.id em,td.sig em{{font-style:normal;color:var(--faint);font-size:12.5px}} td.id em{{display:block;line-height:17px}}
td.sig em{{margin-left:4px}}
.ok{{color:var(--muted)}} .none{{color:var(--faint)}} .act{{font-weight:600}}
.foot{{height:40px;margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:13px;color:var(--faint);border-top:1px solid #EEF1F3}} .foot b{{font-weight:500;color:var(--ink)}}
/* plan */
.plan{{flex:1;min-height:0;padding:2px 4px 2px;display:flex}} .plansvg{{width:100%;height:100%;display:block}} .planimg{{width:100%;height:100%;object-fit:contain;display:block}}
.rooms{{grid-column:1/3;display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}}
.room{{border-radius:8px;background:#F5F7F8;border:1px solid #E6EAED;padding:5px 10px}} .room b{{display:block;font-weight:500;font-size:12.5px;line-height:17px}} .room em{{display:block;font-style:normal;font-size:12px;color:var(--faint);line-height:16px}}
.zone{{position:relative;border-radius:8px;border:1.5px solid #AEB9C1;padding:8px 12px;overflow:hidden;background:#fff}}
.zone.a{{background:#EAF3F9}} .zone.c{{background:#EAF5EE}} .zone.dock{{background:#F4F6F7}}
.zone.b{{border-color:var(--red);background:#FDEFEC}}
.zone.b:before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(214,67,44,.10) 0 1px,transparent 1px 8px)}}
.zone>*{{position:relative}}
.zl{{font-size:12.5px;color:#34414A;line-height:16px;font-weight:500}}
.zt{{font-family:var(--disp);font-weight:600;font-size:26px;line-height:30px;letter-spacing:-.02em;font-variant-numeric:tabular-nums}} .zt small{{font-family:var(--ui);font-size:13px;font-weight:500;letter-spacing:0;margin-left:3px;color:var(--muted);position:relative;top:-8px}}
.ztags{{position:absolute;left:12px;bottom:7px;display:flex;gap:6px}}
.tag{{height:20px;padding:0 7px;border-radius:5px;background:rgba(255,255,255,.85);border:1px solid #D3DAE0;font-size:11.5px;line-height:18px;color:#34414A}}
.racks{{position:absolute;right:12px;bottom:10px;opacity:.55}} .racks rect{{fill:none;stroke:#7D8B95;stroke-width:1}}
.zone.b .racks rect{{stroke:#B5503E}}
.zone.b .note{{position:absolute;right:12px;top:8px;display:flex;align-items:center;gap:4px;font-size:12px;font-weight:600;color:#A8301D}}
/* facts */
.eng{{padding:16px 18px 14px;border-bottom:1px solid #EEF1F3}}
.eng .k{{font-size:13px;color:var(--muted);display:flex;justify-content:space-between;align-items:flex-end}}
.eng .v{{font-family:var(--disp);font-weight:600;font-size:30px;line-height:34px;letter-spacing:-.02em}} .eng .v small{{font-family:var(--ui);font-size:14px;color:var(--muted);font-weight:500;margin-left:4px;letter-spacing:0}}
.trk{{height:8px;border-radius:99px;background:#E4E9ED;margin-top:12px;overflow:hidden}} .trk i{{display:block;height:100%;border-radius:99px;background:var(--petrol)}}
.eng .m{{display:flex;justify-content:space-between;font-size:12.5px;color:var(--faint);margin-top:8px}}
.kv{{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 18px;border-bottom:1px solid #EEF1F3;font-size:14px}} .kv:last-child{{border-bottom:0}} .kv span{{color:var(--muted)}} .kv b{{font-weight:600}}
/* bar */
.fade{{position:absolute;left:232px;right:8px;bottom:8px;height:150px;border-radius:0 0 22px 22px;background:linear-gradient(180deg,rgba(255,255,255,0),#fff 72%);pointer-events:none}}
.bar{{position:absolute;z-index:2;left:50%;transform:translateX(-50%);bottom:30px;height:64px;padding:0 12px 0 22px;display:flex;align-items:center;gap:36px;background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:0 10px 30px -8px rgba(12,38,50,.22)}}
.bar .tx{{font-size:14px;color:var(--ink);white-space:nowrap}} .bar .tx span{{color:var(--muted)}}
.btn{{height:40px;display:inline-flex;align-items:center;gap:8px;padding:0 16px;border-radius:11px;font-size:14px;font-weight:500;white-space:nowrap}}
.btn.o{{border:1px solid #CBD3D9;background:#fff;color:var(--ink)}} .btn.p{{background:#11181C;color:#fff}}
.bar .bs{{display:flex;gap:8px}}
'''
    nav=''.join(f'<div class="nav {"on" if n=="Incidents" else ""}">{icon(ic,18)}<span>{n}</span></div>' for n,ic,on in NAV)
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
.hero2 .tt{width:auto;margin-left:28px;padding-top:0} .hero2 .tt b{display:block;font-size:20px;font-weight:600;line-height:26px;letter-spacing:-.01em} .hero2 .tt span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px;margin-top:2px}
.hero2 .fig{margin-right:0;position:relative;top:6.5px}.hero2 .tt{margin-right:auto}
.hero2 .stat{padding:0 34px;border-left:1px solid rgba(255,255,255,.16)} .hero2 .stat:last-child{padding-right:6px}
.hero2 .stat span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px} .hero2 .stat b{display:block;font-family:var(--disp);font-weight:600;font-size:26px;line-height:32px;letter-spacing:-.02em;margin-top:4px;white-space:nowrap} .hero2 .stat b small{font-family:var(--ui);font-size:14px;font-weight:500;letter-spacing:0;margin-left:3px;color:rgba(255,255,255,.72)} .hero2 .stat b.w{color:var(--coral)}
/* light accent hero for inner pages */
.lt{background:linear-gradient(120deg,#CFE9EC 0%,#E3F3F2 55%,#EEF8F7 100%)!important;color:#0A3A47!important;box-shadow:inset 0 0 0 1px #BBDDE2}
.lt:before{background:repeating-linear-gradient(135deg,rgba(12,74,92,.07) 0 1px,transparent 1px 10px)!important}
.lt:after{background:radial-gradient(closest-side,rgba(255,255,255,.95),rgba(255,255,255,0))!important}
.lt .fig,.lt .fg{color:#0C4A5C!important}
.lt .fig .neg{background:#0C4A5C!important}
.lt .dec,.lt .fig .dec,.lt .fg .dec{color:rgba(12,74,92,.42)!important}
.lt .u,.lt .fig .u,.lt .fg .u,.lt .stat b small{color:#2F6272!important}
.lt .hd b,.lt .tt b,.lt .stat b,.lt .h3s b{color:#0A3A47!important}
.lt .hd span,.lt .tt span,.lt .stat span,.lt .cv,.lt .sl,.lt .segn,.lt .h3s span,.lt .bt span,.lt .ax span{color:#4A6872!important}
.lt .bn{color:#0A3A47!important} .lt .bn.al2{color:#C23B22!important}
.lt .stat b.w,.lt .h3s b.w{color:#C23B22!important}
.lt .stat,.lt .h3s,.lt .h3s div{border-color:rgba(12,74,92,.15)!important}
.lt .ax i{border-color:rgba(12,74,92,.28)!important}
.lt .trk2{background:rgba(12,74,92,.15)!important} .lt .trk2 .fill{background:#0C4A5C!important} .lt .trk2 .mk{background:#0C4A5C!important} .lt .trk2 .mk.al{background:var(--coral)!important}
.lt .sb2:not(.nd){color:#fff!important;border-right-color:#E3F3F2!important}
.lt .sg:nth-child(1) .sb2{background:#0C4A5C!important} .lt .sg:nth-child(2) .sb2{background:#33707F!important} .lt .sg:nth-child(4) .sb2{background:#6A9EAB!important}
.lt .sb2.nd{border-right-color:#E3F3F2!important}
.hero2 .stat em{display:block;font-style:normal;font-size:12.5px;line-height:16px;color:rgba(255,255,255,.72);margin-top:2px;white-space:nowrap}
.lt .stat em{color:#4A6872!important}
.hero2 .stat{padding:0 26px}
.as{padding:18px 22px 0}
.as .hl{font-family:var(--disp);font-size:21px;line-height:27px;font-weight:600;letter-spacing:-.01em}
.as .el{margin-top:16px;font-size:13px;color:var(--faint);padding-bottom:6px}
.er{padding:11px 0;border-top:1px solid #EEF1F3;font-size:14.5px;line-height:21px;color:var(--ink)}
.rr{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid #EEF1F3}
.rr b{display:block;font-size:15px;line-height:20px;font-weight:600} .rr span{display:block;font-size:13.5px;line-height:19px;color:var(--muted);margin-top:1px}
.rr .rs{text-align:right} .rr .rs b{font-size:14px;font-weight:600} .rr .rs b.w{color:#A24A10} .rr .rs b.m{color:var(--muted);font-weight:500}
.rr .rs a{display:block;font-size:13.5px;line-height:19px;color:var(--petrol);font-weight:600;margin-top:1px}
.rn{padding:14px 20px;font-size:13px;line-height:19px;color:var(--faint)}
.lanewrap{padding:16px 22px 8px}
"""
    css+="""
.top .pill.warn{background:#FFE9DA;color:#8A3B0B}
.e2{margin-top:16px;display:grid;grid-template-columns:560px 1fr;gap:16px;height:622px}.lc{display:flex;flex-direction:column;gap:16px;min-height:0}
.e3{margin-top:16px;display:grid;grid-template-columns:1fr;gap:16px;height:250px}
.hero3{position:relative;border-radius:22px;background:var(--petrol);color:#fff;overflow:hidden;padding:24px 28px 0;display:flex;flex-direction:column}
.hero3:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 18%,#000 80%);mask-image:linear-gradient(100deg,transparent 18%,#000 80%)}
.hero3:after{content:'';position:absolute;left:-40px;top:30px;width:420px;height:260px;background:radial-gradient(closest-side,rgba(96,214,232,.30),rgba(96,214,232,0));pointer-events:none}
.hero3>*{position:relative;z-index:1}
.hero3 .hd b{display:block;font-size:20px;font-weight:600;line-height:26px;letter-spacing:-.01em} .hero3 .hd span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px;margin-top:2px}
.hero3 .fg{font-family:var(--disp);font-weight:600;font-size:88px;line-height:92px;letter-spacing:-.035em;margin-top:14px;white-space:nowrap}
.hero3 .fg .dec{color:rgba(255,255,255,.52)} .hero3 .fg .u{font-size:30px;letter-spacing:0;margin-left:8px;color:rgba(255,255,255,.78);font-weight:500;position:relative;top:-34px}
.bl{position:relative;margin-top:30px;padding-bottom:34px;height:72px}
.trk2{position:relative;height:10px;border-radius:99px;background:rgba(255,255,255,.16)}
.trk2 .fill{position:absolute;left:0;top:0;height:100%;border-radius:99px;background:#fff}
.trk2 .gap{position:absolute;top:0;height:100%;background:repeating-linear-gradient(135deg,rgba(255,138,120,.9) 0 2px,rgba(255,138,120,.25) 2px 5px);border-radius:0 99px 99px 0}
.trk2 .mk{position:absolute;top:-6px;width:2px;height:22px;margin-left:-1px;border-radius:2px;background:#fff}
.trk2 .mk.al{background:var(--coral)}
.bt{position:absolute;left:0;right:0;top:22px;height:16px} .bt span{position:absolute;font-size:12px;color:rgba(255,255,255,.6);transform:translateX(-50%)} .bt span:first-child{transform:none} .bt span:last-child{transform:translateX(-100%)} .bt span{white-space:nowrap}
.bn{position:absolute;top:-26px;font-size:12px;white-space:nowrap;transform:translateX(-50%);color:rgba(255,255,255,.85)} .bn.al2{color:var(--coral)} .bn.bs2{transform:translateX(-12%)}
.h3s{margin-top:auto;display:grid;grid-template-columns:1fr 1fr 1fr;border-top:1px solid rgba(255,255,255,.16);margin-left:-28px;margin-right:-28px}
.h3s div{padding:10px 0 12px 28px;border-left:1px solid rgba(255,255,255,.16)} .h3s div:first-child{border-left:0}
.h3s span{display:block;font-size:12.5px;color:rgba(255,255,255,.7);line-height:17px} .h3s b{display:block;font-family:var(--disp);font-weight:600;font-size:21px;line-height:26px;letter-spacing:-.01em;margin-top:2px;white-space:nowrap} .h3s b.w{color:var(--coral)}
.heatw{padding:18px 20px 0}
td.mut{color:var(--muted)} td.lk{font-weight:500;color:var(--ink)}
.e3 td{height:50px} .e3 th{height:40px}
.e3 td b{font-weight:600}
.pill.bk{background:#DCEBF1;color:#0C4A5C}
.top .pill.bk{height:26px;font-size:13px;padding:0 12px}
.asm{padding:16px 20px 0}
.asm .fd{font-size:15px;line-height:23px;color:var(--ink);padding-bottom:16px;border-bottom:1px solid #EEF1F3}
.asm .cf{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid #EEF1F3}
.asm .cf .k{font-size:13px;color:var(--muted);width:90px} .asm .cf b{font-family:var(--disp);font-size:26px;line-height:30px;font-weight:600;letter-spacing:-.02em}
.asm .cf .trk{flex:1;margin-top:0}
.asm ul{list-style:none;padding:12px 0 0} .asm li{font-size:14px;line-height:20px;color:var(--ink);padding:5px 0 5px 0} .asm li span{color:var(--muted)}
.asm .rh{font-size:13px;color:var(--muted);padding-top:12px}
.chartw{padding:20px 22px 6px}
.mi li{list-style:none}
.foot2{height:52px;margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding:0 22px;border-top:1px solid #EEF1F3;font-size:14px;color:var(--muted)} .foot2 b{color:var(--ink);font-weight:600} .foot2 .lk2{color:var(--ink);font-weight:500}
.asm .hl{font-family:var(--disp);font-size:21px;line-height:26px;font-weight:600;letter-spacing:-.015em;color:var(--ink)}
.asm .sb{font-size:14px;line-height:21px;color:var(--muted);margin-top:6px;padding-bottom:12px;border-bottom:1px solid #EEF1F3}
.asm .chk{display:flex;gap:8px;margin-top:8px} .asm .chk span{height:34px;padding:0 14px;border-radius:11px;background:#F3F5F7;border:1px solid #E3E8EC;display:flex;align-items:center;font-size:14px;font-weight:500}
.asm .cf2{font-size:12.5px;color:var(--faint);margin-top:10px}
.evl{width:350px;border-left:1px solid #EEF1F3;display:flex;flex-direction:column;padding:6px 0}
.ev{flex:1;display:flex;align-items:center;gap:14px;padding:0 22px;border-bottom:1px solid #EEF1F3} .ev:last-child{border-bottom:0}
.ev .pn{flex:none;width:26px;height:26px;border-radius:50%;background:var(--petrol);color:#fff;font-size:12.5px;font-weight:600;display:flex;align-items:center;justify-content:center} .ev .pn.now{background:#fff;border:2px solid var(--petrol);position:relative} .ev .pn.now:after{content:'';width:8px;height:8px;border-radius:50%;background:var(--petrol)}
.ev div{position:relative;flex:1} .ev b{display:block;font-size:14px;font-weight:600;line-height:19px;padding-right:56px} .ev .tm{position:absolute;right:0;top:0;font-size:13px;color:var(--ink);font-weight:500} .ev em{display:block;font-style:normal;font-size:13px;color:var(--muted);line-height:18px;margin-top:2px}
"""

    import os
    ST=os.environ.get('ACT_STATE','pending'); AP=ST!='pending'; PERM=ST!='approved-noperm'; QU=ST=='queued'
    NOWT='Fri, Nov 6, 10:26 EST' if AP else NOW
    DASH='stroke-dasharray="6 5"' if AP else ''
    PT='51.7 kW projected' if AP else '51.7 kW'
    PWH=128 if AP else 72
    TICKS=[(0,'10:11',0),(15,'Now',1),(30,'10:41',0),(60,'11:11',0)] if AP else [(0,'10:09',0),(15,'Now',1),(30,'10:39',0),(45,'10:54',0),(60,'11:09',0)]
    chk=[('Target and limits','Both evaporators are approved for backup mode.','Passed','#DDF1E4','#1B6B3A',True,[('Equipment','EVAP-FZB-02 and EVAP-FZB-03'),('Run time','30 min, within the 30 min limit'),('Active interlocks','None'),('Controller limits','Request matches')]),
         ('Policy','POL-COLD-07 allows backup mode in Frozen Zone B.','Passed','#DDF1E4','#1B6B3A',False,[]),
         ('Rollback','Stop sequence and restore previous controller state.','Passed','#DDF1E4','#1B6B3A',False,[]),
         ('Verification','Acknowledgement is not success. Airflow response within 3 min is checked on site.','After run','#DCEBF1','#0C4A5C',False,[])]
    def acc(a,d,s,bg,fg,op,det):
        chev=icon("chevdown" if op else "chevright",18,1.75)
        body=''.join(f'<div class="kvr"><span>{k}</span><b>{v}</b></div>' for k,v in det)
        return f'<div class="ac {"open" if op else ""}"><div class="ah"><span class="cv2">{chev}</span><div class="at"><b>{a}</b><em>{d}</em></div><span class="cnt" style="background:{bg};color:{fg}">{s}</span></div>{"<div class=ab>"+body+"</div>" if op else ""}</div>'
    chk_h=''.join(acc(*c) for c in chk)
    cnt_t='3 passed, 1 after run'
    if AP:
        cnt_t='3 passed, 1 pending'
        def gh(a,b): return f'<div class="gh"><span>{a}</span><span>{b}</span></div>'
        G='#DDF1E4','#1B6B3A'
        A=[('Target and limits','Both evaporators are approved for backup mode.','Passed',*G,False,[]),
           ('Policy','POL-COLD-07 allows backup mode in Frozen Zone B.','Passed',*G,False,[]),
           ('Rollback','Stop sequence and restore previous controller state.','Passed',*G,False,[]),
           ('Verification','Physical airflow check has not started. It begins after dispatch.','Pending','#DCEBF1','#0C4A5C',False,[])]
        rec='<div class="ar"><div class="ar1"><span class="ck2"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9.5 7.5 13 14 5.5"/></svg></span><div class="at2"><b>Approved by Felix Whitaker</b><span>Facility Operations Manager</span></div><div class="tm"><b>10:25 EST</b><span>Fri, Nov 6</span></div></div><div class="as2"><div><span>Policy</span><b>POL-COLD-07, Passed</b></div><div><span>Approved parameters</span><b><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="#1B6B3A" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px"><rect x="2.5" y="6" width="9" height="6" rx="1.8"/><path d="M4.5 6V4.5a2.5 2.5 0 0 1 5 0V6"/></svg>Locked</b></div><div><span>Next step</span><b>Awaiting dispatch</b></div></div></div>'
        chk_h=rec+gh('Before execution','Completed')+''.join(acc(*a) for a in A[:3])+gh('After dispatch','Pending')+acc(*A[3])
    pills=('<span class="pill ok">Approved</span><span class="pill act">Awaiting dispatch</span>' if AP else '<span class="pill warn">Approval required</span>')+'<span class="cnt">ACT-1184</span>'
    if QU: pills='<span class="pill qu">Queued</span><span class="cnt">ACT-1184</span>'
    AEV='Calculated after dispatch' if AP else '10:54'
    C2=('Controller state','No command sent') if AP else ('Approver','Felix Whitaker, Facility Operations')
    PROJ='Projected' if AP else 'If approved'
    if QU:
        C2=('Controller state','Queued, not sent')
        LH2='Execution'; cnt_t='Queued'
        chk_s='<svg width="14" height="14" viewBox="0 0 18 18" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9.5 7.5 13 14 5.5"/></svg>'
        tl=[('Approved','Felix Whitaker','10:25:00','done'),('Queued','Luis Ortega','10:26:00','cur'),('Sent','','Pending','pend'),('Controller acknowledgement','','Pending','pend'),('Physical verification','','Pending','pend')]
        def mk(s):
            if s=='done': return '<span class="mk d">'+chk_s+'</span>'
            if s=='cur': return '<span class="mk c">'+icon("clock",15,2)+'</span>'
            return '<span class="mk p"></span>'
        tlh=''.join(f'<div class="tr {s}"><span class="mkw">{mk(s)}</span><b>{a}</b><span class="ac2">{w}</span><span class="tt2">{tm}</span></div>' for a,w,tm,s in tl)
        banner='<div class="qb"><div class="qb1"><span class="ck3">'+icon("clock",18,2)+'</span><div class="at2"><b>ACT-1184 has been queued for dispatch.</b><span>The approved command is waiting for the control integration to send it to CTRL-FZB-03. No controller acknowledgement has been received.</span></div></div></div>'
        G2='#DDF1E4','#1B6B3A'
        tl_h=banner+'<div class="tl">'+tlh+'</div>'
        chk_h=acc('Approval record','Felix Whitaker, 10:25 EST. Parameters locked.','Locked',*G2,False,[])+acc('Policy checklist','3 passed, 1 pending after dispatch.','Read only','#E8ECEF','#3A4650',False,[])
    else:
        LH2='Policy checklist'
    NOWKW,ADD,CAPKW=48.2,3.5,66.8
    PK=lambda v:v/CAPKW*100
    em_,ebl_,ea_,ek_,ep_=energy_solve()
    def fchart(W=440,H=262):
        PL_,PR_,TT_,BB_=38,16,30,H-34
        x0,x1=0,60
        X=lambda m:PL_+(m-x0)/(x1-x0)*(W-PL_-PR_)
        Y=lambda v:TT_+(70-v)/30*(BB_-TT_)
        def smooth(pts):
            d=f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
            for k in range(len(pts)-1):
                p0=pts[max(k-1,0)];p1=pts[k];p2=pts[k+1];p3=pts[min(k+2,len(pts)-1)]
                c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
                d+=f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
            return d
        o=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Onest, sans-serif">',
           '<defs><linearGradient id="gh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C4A5C" stop-opacity=".16"/><stop offset="1" stop-color="#0C4A5C" stop-opacity="0"/></linearGradient>'
           '<linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5543B" stop-opacity=".30"/><stop offset="1" stop-color="#E5543B" stop-opacity=".06"/></linearGradient>'
           '<linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B6B3A" stop-opacity=".02"/><stop offset="1" stop-color="#1B6B3A" stop-opacity=".14"/></linearGradient><pattern id="hp" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#E5543B" stroke-opacity=".28" stroke-width="1.4"/></pattern></defs>']
        for v in (40,50,60):
            o.append(f'<line x1="{PL_}" x2="{W-PR_}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#EDF0F2"/>')
        for v in (40,50,60,70):
            o.append(f'<text x="{PL_-10}" y="{Y(v)+4:.1f}" font-size="11.5" text-anchor="end" fill="#8995A0">{v}</text>')
        o.append(f'<line x1="{PL_}" x2="{W-PR_}" y1="{Y(66.8):.1f}" y2="{Y(66.8):.1f}" stroke="#E5543B" stroke-opacity=".7" stroke-width="1.4"/>')
        o.append(f'<text x="{W-PR_-6}" y="{Y(66.8)-7:.1f}" font-size="11.5" font-weight="600" text-anchor="end" fill="#B3321F">Capacity 66.8 kW</text>')
        hist=[float(v) for v in ea_[-8:]]; hx=[15*k/7 for k in range(8)]
        hp=[(X(a),Y(b)) for a,b in zip(hx,hist)]
        o.append(f'<path d="{smooth(hp)} L{X(15):.1f} {BB_} L{X(0):.1f} {BB_} Z" fill="url(#gh)"/>')
        base=Y(48.2); top=Y(51.7)
        fp=[(X(15),base),(X(17),top),(X(43),top),(X(45),base)]
        o.append(f'<path d="M{X(15):.1f} {base:.1f} C{X(16.5):.1f} {base:.1f} {X(15.5):.1f} {top:.1f} {X(18):.1f} {top:.1f} L{X(42):.1f} {top:.1f} C{X(44.5):.1f} {top:.1f} {X(43.5):.1f} {base:.1f} {X(45):.1f} {base:.1f} Z" fill="{'#E5543B' if AP else 'url(#gf)'}" fill-opacity="{'.07' if AP else '1'}"/>')
        o.append(f'<path d="M{X(15):.1f} {base:.1f} L{W-PR_} {base:.1f}" stroke="#8A9AA5" stroke-width="1.5" stroke-dasharray="1.5 4" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M{X(15):.1f} {base:.1f} C{X(16.5):.1f} {base:.1f} {X(15.5):.1f} {top:.1f} {X(18):.1f} {top:.1f} L{X(42):.1f} {top:.1f} C{X(44.5):.1f} {top:.1f} {X(43.5):.1f} {base:.1f} {X(45):.1f} {base:.1f}" stroke="#E5543B" stroke-width="2.4" {DASH} fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<path d="{smooth(hp)}" stroke="#0C4A5C" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<line x1="{X(15):.1f}" x2="{X(15):.1f}" y1="{TT_-6}" y2="{BB_}" stroke="#11181C" stroke-opacity=".22" stroke-dasharray="3 4"/>')
        o.append(f'<circle cx="{X(15):.1f}" cy="{base:.1f}" r="9" fill="#0C4A5C" fill-opacity=".14"/><circle cx="{X(15):.1f}" cy="{base:.1f}" r="4.8" fill="#fff" stroke="#0C4A5C" stroke-width="2.4"/>')
        if not AP: o.append(f'<circle cx="{X(45):.1f}" cy="{base:.1f}" r="4" fill="#fff" stroke="#8A9AA5" stroke-width="2"/>')
        cx=X(30)
        o.append(f'<rect x="{cx-PWH/2:.1f}" y="{top-34:.1f}" width="{PWH}" height="24" rx="12" fill="#FFE9E3"/><text x="{cx:.1f}" y="{top-17.5:.1f}" font-size="12.5" font-weight="600" text-anchor="middle" fill="#B3321F">{PT}</text>')
        for m,l,b in TICKS:
            if b: o.append(f'<rect x="{X(m)-19:.1f}" y="{H-27}" width="38" height="20" rx="10" fill="#11181C"/><text x="{X(m):.1f}" y="{H-12.5}" font-size="11.5" text-anchor="middle" fill="#fff" font-weight="600">{l}</text>')
            else: o.append(f'<text x="{X(m):.1f}" y="{H-12}" font-size="11.5" text-anchor="middle" fill="#8995A0">{l}</text>')
        o.append('</svg>')
        return ''.join(o)
    css+="""
.e6{margin-top:16px;display:grid;grid-template-columns:1.55fr 1fr;gap:16px;height:546px}
.pa{margin-top:16px;height:254px}
.pa .inner{flex-direction:row;align-items:stretch}
.pl{width:520px;padding:26px 30px;border-right:1px solid #EEF1F3;display:flex;flex-direction:column}
.pl .k{font-size:13px;color:var(--faint)} .pl b{display:block;font-family:var(--disp);font-size:28px;line-height:32px;font-weight:600;letter-spacing:-.025em;margin-top:6px} .pl p{font-size:15.5px;line-height:23px;color:var(--muted);margin-top:10px}
.pg{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr}
.pg div{padding:6px 30px;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #EEF1F3;border-left:1px solid #EEF1F3} .pg div:nth-child(odd){border-left:0} .pg div:nth-last-child(-n+2){border-bottom:0}
.pg span{font-size:13px;color:var(--faint)} .pg b{font-size:17px;line-height:23px;font-weight:600;margin-top:5px}
.ac{border-bottom:1px solid #EEF1F3;padding:0 20px} .ac:last-child{border-bottom:0}
.ah{display:flex;align-items:center;gap:14px;min-height:70px} .cv2{width:30px;height:30px;border-radius:9px;background:#F3F5F7;display:flex;align-items:center;justify-content:center;color:#3B4750;flex:none}
.at{flex:1} .at b{display:block;font-size:17px;line-height:23px;font-weight:600} .at em{display:block;font-style:normal;font-size:14px;line-height:20px;color:var(--muted);margin-top:2px}
.ab{margin:0 0 16px 44px;border-radius:12px;background:#F6F8F9;padding:4px 18px}
.kvr{display:flex;justify-content:space-between;align-items:center;height:42px;border-bottom:1px solid #E9EDF0;font-size:14.5px} .kvr:last-child{border-bottom:0} .kvr span{color:var(--muted)} .kvr b{font-weight:600;text-align:right}
.top .pill.warn{background:#FFE9DA;color:#8A3B0B}
.e6 td{height:106px;padding-left:20px} .e6 th{height:42px;font-size:13px;padding-left:20px}
td.id b{display:block;font-size:17px;line-height:23px;font-weight:600} td.id em{display:block;font-style:normal;font-size:14px;line-height:20px;color:var(--muted);margin-top:2px;white-space:normal}
.e6 .cnt{height:28px;line-height:28px;font-size:13px;font-weight:600;padding:0 13px}
.sub0{padding:0 14px 10px;font-size:14px;color:var(--muted)}
.rk{margin:16px;border-radius:14px;position:relative;overflow:hidden;background:linear-gradient(120deg,#CFE9EC 0%,#E3F3F2 55%,#EEF8F7 100%);box-shadow:inset 0 0 0 1px #BBDDE2;padding:16px 20px 16px}
.rk .rt{display:flex;align-items:center;gap:12px;font-size:16px;color:var(--ink)} .rk:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(12,74,92,.07) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 20%,#000 90%);mask-image:linear-gradient(100deg,transparent 20%,#000 90%)} .rk>*{position:relative} .rk .rt .ic{color:#0C4A5C} .rk .rt b{font-weight:600}
.rk .tr3{position:relative;height:18px;border-radius:5px;-webkit-mask:repeating-linear-gradient(90deg,#000 0 7px,transparent 7px 10px);mask:repeating-linear-gradient(90deg,#000 0 7px,transparent 7px 10px);background:rgba(12,74,92,.16);margin-top:20px}
.rk .tr3 i{position:absolute;top:0;height:100%} .rk .tr3 .a{left:0;background:var(--petrol)} .rk .tr3 .b{background:#E5543B}
.rk .lbs{position:relative;height:50px;margin-top:10px;font-size:13px;color:var(--muted)} .rk .lbs span{position:absolute;white-space:nowrap;color:#4A6872} .rk .lbs b{display:block;font-family:var(--disp);font-size:22px;line-height:26px;letter-spacing:-.01em;color:#0A3A47;font-weight:600}
.hero5{position:relative;border-radius:22px;background:var(--petrol);color:#fff;overflow:hidden;padding:24px 28px 0;display:flex;flex-direction:column}
.hero5:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.075) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 18%,#000 80%);mask-image:linear-gradient(100deg,transparent 18%,#000 80%)}
.hero5:after{content:'';position:absolute;left:-40px;top:20px;width:420px;height:260px;background:radial-gradient(closest-side,rgba(96,214,232,.30),rgba(96,214,232,0));pointer-events:none}
.hero5>*{position:relative;z-index:1}
.hero5 .hd b{display:block;font-size:20px;font-weight:600;line-height:26px;letter-spacing:-.01em} .hero5 .hd span{display:block;font-size:13px;color:rgba(255,255,255,.72);line-height:18px;margin-top:2px}
.hero5 .fg{font-family:var(--disp);font-weight:600;font-size:92px;line-height:96px;letter-spacing:-.035em;margin-top:16px} .hero5 .fg .u{font-size:30px;letter-spacing:0;margin-left:10px;color:rgba(255,255,255,.78);font-weight:500;position:relative;top:-34px}
.hero5 .cv{font-size:15.5px;line-height:23px;color:rgba(255,255,255,.88);margin-top:6px}
.h4s{margin-top:auto;margin-left:-28px;margin-right:-28px;border-top:1px solid rgba(255,255,255,.16)}
.h4s div{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:62px;border-top:1px solid rgba(255,255,255,.16)} .h4s div:first-child{border-top:0}
.h4s span{font-size:13.5px;color:rgba(255,255,255,.72)} .h4s b{font-family:var(--disp);font-weight:600;font-size:20px;letter-spacing:-.01em}
.cb{width:22px;height:22px;border:1.5px solid #8A97A1;border-radius:6px;background:#fff;flex:none}
.dsub2{padding:4px 22px 6px;font-size:14px;font-weight:600}
.btn.dis{opacity:.45}
.top .pill.ok{background:#DDF1E4;color:#1B6B3A}
.gh{display:flex;justify-content:space-between;padding:12px 20px 6px;font-size:12.5px;font-weight:600;color:var(--faint);border-bottom:1px solid #EEF1F3}
.ar{margin:14px 14px 4px;border-radius:14px;background:#EAF6EE;padding:16px 20px 14px}
.ar1{display:flex;align-items:center;gap:14px}
.ck2{width:36px;height:36px;border-radius:50%;background:#1B6B3A;display:flex;align-items:center;justify-content:center;flex:none}
.at2{flex:1} .at2 b{display:block;font-family:var(--disp);font-size:20px;line-height:25px;font-weight:600;color:#12351F;letter-spacing:-.01em} .at2 span{display:block;font-size:13.5px;line-height:19px;color:#4C6A57;margin-top:1px}
.tm{text-align:right} .tm b{display:block;font-family:var(--disp);font-size:20px;line-height:25px;font-weight:600;color:#12351F} .tm span{display:block;font-size:13.5px;line-height:19px;color:#4C6A57;margin-top:1px}
.as2{display:flex;margin-top:14px;border-top:1px solid rgba(27,107,58,.18);padding-top:10px} .as2>div{flex:1;border-left:1px solid rgba(27,107,58,.18);padding-left:16px} .as2>div:first-child{border-left:0;padding-left:0}
.as2 span{display:block;font-size:12.5px;color:#4C6A57;line-height:17px} .as2 b{display:block;font-size:15px;line-height:21px;font-weight:600;color:#12351F;margin-top:1px}
.top .pill.qu{background:#DCEBF1;color:#0C4A5C}
.qb{margin:12px 14px 0;border-radius:14px;background:#EAF1F5;padding:12px 18px}
.qb1{display:flex;gap:14px;align-items:flex-start}
.ck3{width:36px;height:36px;border-radius:50%;background:#0C4A5C;color:#fff;display:flex;align-items:center;justify-content:center;flex:none}
.qb .at2 b{color:#0A3A47;font-size:18px;line-height:24px} .qb .at2 span{color:#4A6872;font-size:13.5px;line-height:19px;margin-top:3px}
.tl{margin:6px 14px 4px;padding:0 6px}
.live{position:relative;overflow:hidden;background:linear-gradient(120deg,#CFE9EC 0%,#E3F3F2 55%,#EEF8F7 100%);box-shadow:inset 0 0 0 1px #BBDDE2}
.live:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(12,74,92,.07) 0 1px,transparent 1px 10px);-webkit-mask-image:linear-gradient(100deg,transparent 30%,#000 95%);mask-image:linear-gradient(100deg,transparent 30%,#000 95%);pointer-events:none}
.live>*{position:relative}
.live .sh h2{color:#0A3A47} .live .sh .cnt{background:#0C4A5C;color:#fff}
.lcol .ah{min-height:56px} .lcol{display:flex;flex-direction:column;gap:12px;min-height:0} .lcol>.sect:first-child{flex:none} .lcol>.sect:last-child{flex:1}
.tr{position:relative;display:grid;grid-template-columns:46px 1fr 150px 84px;align-items:center;height:36px;font-size:14.5px}
.tr b{font-weight:600;color:var(--ink)} .tr .ac2{color:var(--muted)} .tr .tt2{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
.tr.pend b{color:var(--muted);font-weight:500} .tr.pend .tt2{color:var(--faint);font-weight:500}
.mkw{position:relative;display:flex;justify-content:center}
.mk{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative;z-index:1;box-sizing:border-box}
.mk.d{background:#1B6B3A} .mk.c{background:#0C4A5C;color:#fff} .mk.p{background:#fff;border:2px solid #C7D0D6}
.tr:not(:last-child) .mkw:after{content:'';position:absolute;left:50%;top:30px;height:26px;border-left:2px solid #C7D0D6;transform:translateX(-1px)}
.tr.done .mkw:after{border-left-color:#1B6B3A}
.tr.cur .mkw:after,.tr.pend .mkw:after{border-left-style:dashed}
.apv .ah{min-height:60px} .apv .at em{font-size:13.5px;line-height:19px}
.foot3{padding:14px 22px;font-size:14px;line-height:21px;color:var(--muted);border-top:1px solid #EEF1F3} .foot3 b{color:var(--ink);font-weight:600}
"""
    if AP:
        perm_btn='<span class="btn p">Send action to controller'+icon("arrow",16,1.75)+'</span>' if PERM else '<span class="btn p dis">Send action to controller</span>'
        exec_line='Authorized executor: Luis Ortega, Control-room Operator.' if PERM else 'Execution permission required. Authorized executor: Luis Ortega, Control-room Operator.'
        bar_html=f'<div class="bar"><div class="tx"><b style="font-weight:600">ACT-1184 is approved and ready for dispatch.</b> <span>Equipment has not been changed.</span><span style="display:block;font-size:13px;margin-top:2px;color:var(--faint)">{exec_line}</span></div><div class="bs"><span class="btn o">Review approval</span>{perm_btn}</div></div>'
    if QU:
        bar_html='<div class="bar" style="height:78px"><div class="tx" style="white-space:normal;width:560px;line-height:19px"><b style="font-weight:600">ACT-1184 is queued.</b> <span>Equipment has not been changed.</span><span style="display:block;font-size:13px;margin-top:2px;color:var(--faint)">Dispatch is cancelled if authorization expires, controller freshness fails or safety policy changes before sending.</span></div><div class="bs"><span class="btn o">Review approval</span><span class="btn p dis">'+icon("clock",16,1.75)+'Dispatch pending</span></div></div>'
    elif not AP:
        bar_html='''<div class="bar"><div class="cb"></div><div class="tx"><b style="font-weight:600">I reviewed the checklist. The backup action is allowed and bounded.</b><span style="display:block;font-size:13px;margin-top:2px">Parameters and policy version are stored with the approval.</span></div><div class="bs"><span class="btn o">Reject proposal</span><span class="btn p dis">Approve ACT-1184{icon("arrow",16,1.75)}</span></div></div>'''
    left_html=f'''<section class="sect"><div class="sh"><div class="lft"><h2>{LH2}</h2><span class="cnt">{cnt_t}</span></div></div>
   <div class="inner {'apv' if AP else ''}" style="overflow:hidden">{chk_h}</div></section>'''
    if QU:
        left_html=f'''<div class="lcol"><section class="sect live"><div class="sh"><div class="lft"><h2>Execution</h2><span class="cnt">Queued</span></div></div><div class="inner">{tl_h}</div></section><section class="sect"><div class="sh"><div class="lft"><h2>Approval and policy</h2><span class="cnt">Read-only</span></div></div><div class="inner">{chk_h}</div></section></div>'''
    body=f'''
<aside class="side"><img class="logo" src="{LOGO}" alt="Nivalis Building Operations">
 <div class="org"><div><b>Harlow Cold Logistics</b><span>Organization</span></div><span class="ud"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 6.5 8 3l3.5 3.5M4.5 9.5 8 13l3.5-3.5"/></svg></span></div>
 <div class="navs">{nav}</div>
 <div class="sync">Data synced<b>{NOWT}</b></div></aside>
<main class="sheet">
 <div class="top"><div class="l"><span class="back">{icon("arrow",18)}</span><h1>EXC-2417 / Remote action</h1>{pills}</div>
  <div class="r"><span class="sel dtb">{icon("clock",16)}{NOWT}</span><span class="bell">{icon("bell",18)}<i>1</i></span></div></div>
 <section class="sect pa"><div class="sh"><div class="lft"><h2>Proposed action</h2></div><span style="font-size:13px;color:var(--faint)">Proposed by System assessment, 10:12</span></div>
  <div class="inner"><div class="pl"><span class="k">Remote action</span><b>Activate backup evaporator mode</b><p>Run backup evaporator sequence for <span style="white-space:nowrap">EVAP-FZB-02</span> and <span style="white-space:nowrap">EVAP-FZB-03</span> for up to 30 minutes while EF-3 is inspected.</p></div>
   <div class="pg"><div><span>Zone</span><b>Frozen Zone B</b></div><div><span>Maximum run time</span><b>30 min</b></div><div><span>Automatic end</span><b>{AEV}</b></div><div><span>{C2[0]}</span><b>{C2[1]}</b></div><div><span>Controller</span><b>CTRL-FZB-03</b></div><div><span>Setpoint and interlocks</span><b>No changes</b></div></div></div></section>
 <div class="e6">
  {left_html}
  <section class="sect"><div class="sh"><div class="lft"><h2>Demand impact</h2></div></div>
   <div class="inner"><div class="rk" style="margin:16px"><div class="rt">{icon("activity",22,1.75)}<span><b>Low risk:</b> +{ADD} kW, {CAPKW-NOWKW-ADD:.1f} kW below capacity.</span></div>
     <div class="tr3"><i class="a" style="width:{PK(NOWKW):.2f}%"></i><i class="b" style="left:{PK(NOWKW):.2f}%;width:{PK(ADD):.2f}%"></i></div>
     <div class="lbs"><span style="left:0"><b>{NOWKW} kW</b>Now</span><span style="right:128px;text-align:right"><b>{NOWKW+ADD:.1f} kW</b>{PROJ}</span><span style="right:0;text-align:right"><b>{CAPKW} kW</b>Capacity</span></div></div>
    <div class="dsub2">Expected demand, kW</div><div style="padding:0 16px">{fchart()}</div>
</div></section>
 </div>
</main>
<div class="fade"></div>
{bar_html}
'''
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
if __name__=='__main__':
    render(build(),f'{ROOT}/out/action-desktop.png',1600,1000,1.6)
    MCSS="""<style>
.scrim{position:absolute;inset:0;z-index:20;background:rgba(14,30,38,.42);display:flex;align-items:center;justify-content:center}
.md{width:660px;background:#fff;border-radius:22px;box-shadow:0 30px 80px -20px rgba(8,28,38,.45),0 0 0 1px rgba(12,38,50,.06);display:flex;flex-direction:column;overflow:hidden}
.md .mh{padding:26px 30px 0;display:flex;justify-content:space-between;align-items:flex-start}
.md .mh .k{font-size:13px;color:var(--faint)} .md .mh h3{font-family:var(--disp);font-size:26px;line-height:31px;font-weight:600;letter-spacing:-.02em;margin-top:4px}
.md .x{width:34px;height:34px;border-radius:10px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:#3B4750;flex:none}
.md .ds{padding:10px 30px 0;font-size:15px;line-height:22px;color:var(--muted)}
.md .pv{margin:18px 30px 0;border-radius:14px;background:#F6F8F9;padding:2px 18px}
.md .pv .kvr{height:39px;font-size:14.5px}
.md .pv .kvr .cnt{height:22px;line-height:22px;font-size:12px;padding:0 10px;margin-left:8px;font-weight:600}
.md .nt{margin:14px 30px 0;font-size:13.5px;line-height:20px;color:var(--muted)} .md .nt b{color:var(--ink);font-weight:600}
.md .ck{margin:16px 30px 0;display:flex;gap:12px;align-items:center;font-size:14.5px;line-height:21px;color:var(--ink);font-weight:500}
.md .ck .cb{width:22px;height:22px}
.md .cb.on{background:var(--petrol);border-color:var(--petrol);display:flex;align-items:center;justify-content:center}
.md .mf{margin-top:22px;padding:16px 30px;border-top:1px solid #EEF1F3;display:flex;align-items:center;justify-content:space-between}
.md .mf .who{font-size:13px;line-height:18px;color:var(--faint)} .md .mf .who b{display:block;font-size:14px;color:var(--ink);font-weight:600}
.md .mf .bs{display:flex;gap:8px}
</style>"""
    def modal(on):
        chk='<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 7.5 5.5 10.5 11.5 3.5"/></svg>' if on else ''
        rows=[('Target equipment','EVAP-FZB-02, EVAP-FZB-03'),('Controller','CTRL-FZB-03'),('Maximum run time','30 minutes'),('Expected additional demand','+3.5 kW'),('Policy','POL-COLD-07<span class="cnt" style="background:#DDF1E4;color:#1B6B3A">Passed</span>'),('Safety lockouts','None active'),('Temperature setpoint','Unchanged'),('Verification','Airflow response within 3 minutes')]
        rh=''.join(f'<div class="kvr"><span>{k}</span><b>{v}</b></div>' for k,v in rows)
        return f'''<div class="scrim"><div class="md"><div class="mh"><div><span class="k">ACT-1184 for EXC-2417, Frozen Zone B</span><h3>Approve backup evaporator mode</h3></div><span class="x">{icon("close",16,1.75)}</span></div>
<div class="ds">Authorize this action for dispatch by an approved control-room operator. Approval does not start the equipment.</div>
<div class="pv">{rh}</div>
<div class="nt"><b>Any change to the approved parameters requires a new approval.</b> The platform records the approver, timestamp, policy version and exact approved parameters.</div>
<div class="ck"><div class="cb {"on" if on else ""}">{chk}</div><span>I reviewed the equipment, operating limits and verification requirements.</span></div>
<div class="mf"><div class="who">Approving as<b>Felix Whitaker, Facility Operations Manager</b></div><div class="bs"><span class="btn o">Cancel</span><span class="btn p {"" if on else "dis"}">Approve ACT-1184{icon("arrow",16,1.75)}</span></div></div></div></div>'''
    import os
    for on,name in ((False,'action-desktop-approve'),(True,'action-desktop-approve-checked')):
        h=build().replace('</style>',MCSS[7:-8]+'</style>',1).replace('</body>',modal(on)+'</body>')
        render(h,f'{ROOT}/out/{name}.png',1600,1000,1.6)
    for stt,name in (('approved','action-desktop-approved'),('approved-noperm','action-desktop-approved-noperm')):
        os.environ['ACT_STATE']=stt
        render(build(),f'{ROOT}/out/{name}.png',1600,1000,1.6)
    os.environ['ACT_STATE']='approved'
    DCSS=""".md.d .pv{margin-top:14px;padding:2px 18px} .md.d .pv .kvr{height:34px;font-size:14px}
.md.d .ds{padding-top:8px}
.md.d .af{margin:14px 30px 0;border-radius:14px;background:#EEF3F6;padding:14px 18px}
.md.d .af b{display:block;font-size:14.5px;line-height:20px;font-weight:600;color:var(--ink)} .md.d .af p{font-size:14px;line-height:21px;color:var(--muted);margin-top:3px}
.md.d .rc{margin:14px 30px 0;font-size:13px;color:var(--faint)}
.md.d .rc .ch{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap} .md.d .rc .ch span{font-size:13.5px;color:var(--ink);border:1px solid #DCE2E7;border-radius:99px;padding:5px 12px;font-weight:500}
.md.d .mf{margin-top:18px}"""
    rows=[('Facility','BCD-01, Baltimore'),('Controller','CTRL-FZB-03'),('Equipment','EVAP-FZB-02 and EVAP-FZB-03'),('Maximum duration','30 minutes'),('Estimated additional demand','+3.5 kW'),('Temperature setpoints','Unchanged'),('Active safety lockouts','None'),('Approval','Felix Whitaker, 10:25 EST'),('Policy','POL-COLD-07<span class="cnt" style="background:#DDF1E4;color:#1B6B3A">Passed</span>')]
    rh=''.join(f'<div class="kvr"><span>{k}</span><b>{v}</b></div>' for k,v in rows)
    m2=f'''<div class="scrim"><div class="md d"><div class="mh"><div><span class="k">ACT-1184 for EXC-2417, Frozen Zone B</span><h3>Send backup mode to controller?</h3></div><span class="x">{icon("close",16,1.75)}</span></div>
<div class="ds">ACT-1184 will request the approved backup evaporator sequence for Frozen Zone B.</div>
<div class="pv">{rh}</div>
<div class="rc">Rechecked immediately before sending<div class="ch"><span>Permission</span><span>Controller data freshness</span><span>Approval validity</span><span>Safety policy</span></div></div>
<div class="af"><b>After dispatch</b><p>The system will wait for controller acknowledgement, then check the physical airflow response. Sending the command does not confirm successful equipment operation.</p></div>
<div class="mf"><div class="who">Sending as<b>Luis Ortega, Control-room Operator</b></div><div class="bs"><span class="btn o">Cancel</span><span class="btn p">Send to controller{icon("arrow",16,1.75)}</span></div></div></div></div>'''
    h=build().replace('</style>',MCSS[7:-8]+DCSS+'</style>',1).replace('</body>',m2+'</body>')
    render(h,f'{ROOT}/out/action-desktop-send.png',1600,1000,1.6)
    os.environ['ACT_STATE']='queued'
    render(build(),f'{ROOT}/out/action-desktop-queued.png',1600,1000,1.6)
