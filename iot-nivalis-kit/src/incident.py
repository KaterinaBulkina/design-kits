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
    lk=[('Hypothesis','Cooling capacity loss'),('Evidence for','CR-01 down 17%, EF-3 dip at 09:50'),('Evidence against','Door closed, no open events'),('Uncertainty','Moderate, about 30%')]
    lkh=''.join(f'<div class="kv s"><span>{a}</span><b>{b}</b></div>' for a,b in lk)
    sm=[('Owner','Felix Whitaker'),('Opened','Fri 04:24'),('Approver','Facility Operations Manager'),('Data freshness','Under 1 min')]
    smh=''.join(f'<div class="kv"><span>{a}</span><b>{b}</b></div>' for a,b in sm)
    DUR='6 h 00 min'
    body=f'''
<aside class="side"><img class="logo" src="{LOGO}" alt="Nivalis Building Operations">
 <div class="org"><div><b>Harlow Cold Logistics</b><span>Organization</span></div><span class="ud"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 6.5 8 3l3.5 3.5M4.5 9.5 8 13l3.5-3.5"/></svg></span></div>
 <div class="navs">{nav}</div>
 <div class="sync">Data synced<b>{NOW}</b></div></aside>
<main class="sheet">
 <div class="top"><div class="l"><span class="back">{icon("arrow",18)}</span><h1>Incident EXC-2417</h1><span class="pill crit">{icon("alert",14,1.75)}Critical</span><span class="pill act">Containment in progress</span></div>
  <div class="r"><span class="sel dtb">{icon("clock",16)}{NOW}</span><span class="bell">{icon("bell",18)}<i>1</i></span><span class="sel">{icon("user",16)}Operations{icon("chevdown",16)}</span></div></div>
 <div class="tabsrow"><div class="tabs">{tabs}</div><span class="sel">{icon("building",16)}BCD-01, Frozen Zone B{icon("chevdown",16)}</span></div>
 <div class="r2">
  <section class="hero2 lt">
   <div class="fig num" aria-label="{t(CUR)} degrees Celsius"><span class="neg"></span>16<span class="dec">.1</span><span class="u">°C</span></div>
   <div class="tt"><b>Frozen Zone B</b><span>Temperature excursion</span></div>
   <div class="stat"><span>Upper limit</span><b>{t(SETPOINT)}<small>°C</small></b><em>Configured</em></div>
   <div class="stat"><span>Deviation</span><b class="w">+{DEV}<small>°C</small></b><em>Above limit</em></div>
   <div class="stat"><span>Open for</span><b>{DUR}</b><em>Since 04:24 EST</em></div>
   <div class="stat"><span>Owner</span><b>Felix Whitaker</b><em>Facility Operations Manager</em></div>
  </section>
 </div>
 <div class="r2" style="height:524px;margin-top:16px">
  <section class="sect"><div class="sh"><h2>Signal correlation</h2><span style="font-size:13px;color:var(--faint)">Last 23 hours, Zone B</span></div>
   <div class="inner"><div class="lanewrap">{lane_chart2(1236)}</div></div></section>
 </div>
 <div class="r3" style="height:440px;grid-template-columns:1fr 1.05fr">
  <section class="sect"><div class="sh"><div class="lft"><h2>Assessment</h2><span class="cnt">Preliminary</span></div></div><div class="inner"><div class="as">
   <div class="hl">Cooling performance reduced, cause under investigation</div>
   <div class="el">Supporting evidence</div>
   <div class="er">CR-01 cooling capacity is 26.9 kW, below its recent baseline of 32.4 kW.</div>
   <div class="er">Zone temperature is {t(CUR)} °C, above the upper limit of {t(SETPOINT)} °C.</div>
   <div class="er">EF-3 had a temporary current drop around 09:50.</div>
   <div class="er">EF-3 airflow recovered around 10:00, but inspection is still required.</div>
   <div class="er">The timing and contribution of each equipment anomaly remain under investigation.</div>
  </div></div></section>
  <section class="sect"><div class="sh"><h2>Response</h2></div><div class="inner">
   <div class="rr"><div><b>Inventory hold</b><span>HOLD-2417, 42 pallets</span></div><div class="rs"><b>Active</b><a>Open inventory hold</a></div></div>
   <div class="rr"><div><b>Refrigeration investigation</b><span>CR-01 and EF-3</span></div><div class="rs"><b>Open</b><a>Open EF-3</a></div></div>
   <div class="rr"><div><b>Technician dispatch</b><span>No technician assigned</span></div><div class="rs"><b class="w">Required</b></div></div>
   <div class="rr"><div><b>Remote action</b><span>ACT-1184, backup evaporator mode</span></div><div class="rs"><b class="w">Approval required</b><a>Review remote action</a></div></div>
   <div class="rr" style="border-bottom:0"><div><b>Temperature recovery</b><span>Zone B is above the upper limit</span></div><div class="rs"><b class="m">Not verified</b></div></div>
   <div class="rn" style="margin-top:auto;border-top:1px solid #EEF1F3">The inventory hold is precautionary. Product condition has not been assessed.</div>
  </div></section>
 </div>
</main>
<div class="fade"></div>
<div class="bar"><div class="tx" style="white-space:normal;width:470px;line-height:20px"><b style="font-weight:600">Critical excursion remains active.</b> <span>Cooling capacity is reduced and technical investigation is required.</span></div><div class="bs"><span class="btn o">Assign owner</span><span class="btn o">Review inventory hold</span><span class="btn p">Dispatch technician{icon("arrow",16,1.75)}</span><span class="btn o sq">{icon("dots",18)}</span></div></div>
'''
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
if __name__=='__main__':
    render(build(),f'{ROOT}/out/incident-desktop.png',1600,1000,1.6)
    h=build().replace('</style>','.sheet>.tabsrow,.sheet>.r2{display:none}</style>')
    render(h,f'{ROOT}/out/incident-desktop-response.png',1600,1000,1.6)
