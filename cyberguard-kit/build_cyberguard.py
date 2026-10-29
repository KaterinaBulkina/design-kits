import re,base64,pathlib
S=pathlib.Path(__file__).resolve().parent; V=S; D=S/'out'; A=S/'assets'; D.mkdir(exist_ok=True)
def ico(n,c='i'):
    s=(V/f'node_modules/lucide-static/icons/{n}.svg').read_text()
    s=re.sub(r'<!--.*?-->','',s,flags=re.S); s=re.sub(r'\swidth="\d+"','',s,count=1); s=re.sub(r'\sheight="\d+"','',s,count=1)
    return re.sub(r'class="[^"]*"',f'class="{c}"',s,count=1)
F=(V/'node_modules/@fontsource-variable').as_uri()
b64=lambda p:base64.b64encode(p.read_bytes()).decode()
MAYA='data:image/jpeg;base64,'+b64(A/'maya.jpg'); ME='data:image/jpeg;base64,'+b64(A/'me.jpg')
# ---- data + asserts
SIG=[('id',14*60+5),('id',14*60+40),('id',15*60+10),('id',16*60+30),('da',17*60+20),('da',18*60+5),('da',19*60+15),('da',20*60+30),('nw',21*60+40),('nw',22*60+10),('ag',23*60),('ag',24*60),('ag',25*60),('ag',26*60)]
assert len(SIG)==14 and len({k for k,_ in SIG})==4
EV=[('02:14','Unusual identity session','Maya Chen signed in from Singapore on a device not seen before.','id','Microsoft Entra ID','Sign-in log','','Identity risk|New device'),
 ('02:18','Restricted file opened','customer_data_2026.csv (Restricted, 48 MB) read from the S3 bucket.','da','AWS CloudTrail','Object access event','','Restricted data|S3 access'),
 ('02:22','Outbound transfer blocked','Upload to <span class=ip>45.133.194.17</span> stopped. File quarantined.','nw','Data Protection Agent','Enforcement log','blk','High-risk IP'),
 ('02:23','Identity and asset analysis','First Singapore sign-in for this user. Device not enrolled in MDM.','ag','Identity and Asset Agent','Analysis','','MDM gap'),
 ('02:24','Evidence correlation','Sign-in, file read and upload attempt link to one identity within 8 minutes.','ag','Threat and Exposure Agent','Correlation','','One identity'),
 ('02:25','Severity assessment','Restricted data, unknown destination, unmanaged device.','ag','Threat and Exposure Agent','Assessment','sev','Restricted data'),
 ('02:27','Remediation plan edited','Jordan Diaz changed the plan to version 2: 6 actions, 2 run automatically.','ag','Remediation Agent','Plan, version 2','now','')]
UP=[('Approval','Security on-call approves the plan'),('Execution','Approved actions run and are logged'),('Verification','Agents confirm egress has stopped'),('Closure','Owner closes with a summary')]
TOTAL=len(EV)+len(UP); DONE=len(EV); assert (TOTAL,DONE)==(11,7)
mins=lambda t:int(t[:2])*60+int(t[3:]); assert all(mins(EV[i][0])<mins(EV[i+1][0]) for i in range(6)) and mins('02:22')-mins('02:14')==8
CONF=86; TK=40; FILL=round(CONF*TK/100); assert FILL==34
GL={'id':('<path d="M6 1 11 6 6 11 1 6Z"/>','#6B1D4A'),'da':('<rect x="1.8" y="1.8" width="8.4" height="8.4" rx="1.6"/>','#B7791F'),'nw':('<circle cx="6" cy="6" r="4.2"/>','#D9480F'),'ag':('<path d="M6 1 10.3 3.5V8.5L6 11 1.7 8.5V3.5Z"/>','#3C3A36')}
def glyph(k,s=12): p,c=GL[k]; return f'<svg width="{s}" height="{s}" viewBox="0 0 12 12" fill="none" stroke="{c}" stroke-width="1.6">{p}</svg>'
def ribbon(W):
    LX=214;t0=12*60;t1=28*60;X=lambda s:LX+(s-t0)/(t1-t0)*(W-LX-12);P=29;T=8
    LANES=[('id','Microsoft Entra ID'),('da','AWS CloudTrail'),('nw','Data Protection Agent'),('ag','Analysis agents')]
    H=T+P*4+34
    o=f'<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" font-family="SG" font-size="12.5">'
    ly=lambda k:T+[l[0] for l in LANES].index(k)*P+P/2
    xa,xb=X(14*60+5)-14,X(22*60+10)+14
    o+=f'<rect x="{xa}" y="{T-2}" width="{xb-xa}" height="{P*4+4}" rx="10" fill="#F8F1F5"/>'
    for i,(k,n) in enumerate(LANES):
        y=T+i*P+P/2; c=GL[k][1]; cnt=sum(1 for kk,_ in SIG if kk==k)
        o+=f'<line x1="0" x2="{W}" y1="{T+(i+1)*P}" y2="{T+(i+1)*P}" stroke="#F0EEE9"/>' if i<3 else ''
        o+=f'<line x1="{LX-8}" x2="{W-4}" y1="{y}" y2="{y}" stroke="#ECE9E3" stroke-dasharray="1 5" stroke-linecap="round"/>'
        o+=f'<g transform="translate(0 {y-6.5}) scale(1.08)" fill="none" stroke="{c}" stroke-width="1.5">{GL[k][0]}</g><text x="20" y="{y+4.3}" fill="#3C3A36">{n}</text><text x="{LX-22}" y="{y+4.3}" fill="#A5A199" text-anchor="end">{cnt}</text>'
    pts=[(X(s),ly(k)) for k,s in SIG]
    o+='<path d="M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'" fill="none" stroke="#C9C4BA" stroke-width="1.2" stroke-linejoin="round"/>'
    for k,s in SIG:
        x=X(s);y=ly(k);c=GL[k][1]
        if k=='nw' and s==22*60+10: o+=f'<circle cx="{x}" cy="{y}" r="11" fill="rgba(217,72,15,.16)"/><circle cx="{x}" cy="{y}" r="6" fill="#D9480F"/>'; continue
        sh={'id':f'<path d="M{x} {y-6.5}l6.5 6.5-6.5 6.5-6.5-6.5Z"/>','da':f'<rect x="{x-5.5}" y="{y-5.5}" width="11" height="11" rx="2"/>','nw':f'<circle cx="{x}" cy="{y}" r="6"/>','ag':f'<path d="M{x} {y-6.8}l5.9 3.4v6.8l-5.9 3.4-5.9-3.4v-6.8Z"/>'}[k]
        o+=f'<g fill="#fff" stroke="{c}" stroke-width="1.8">{sh}</g>'
    ya=T+P*4+22
    for m in range(12,29,4):
        x=X(m*60);an='start' if m==12 else ('end' if m==28 else 'middle');o+=f'<text x="{x}" y="{ya}" fill="#A5A199" text-anchor="{an}" font-size="11.5">02:{m:02d}</text>'
    return o+'</svg>'

CSS='''
@font-face{font-family:SG;src:url(__F__/hanken-grotesk/files/hanken-grotesk-latin-wght-normal.woff2);font-weight:100 900}
:root{--ink:#1C1B19;--tx:#3C3A36;--mut:#7A776F;--mut2:#A5A199;--line:#E7E4DD;--side:#F4F3EF;--side2:#E9E7E1;--pr:#6B1D4A;--prt:#F8F1F5;--prt2:#EAD6E1;--hi:#D9480F;--hit:#FCEDE5;--ok:#2E7D4F;--amb:#B7791F}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:__CW__px;height:__CH__px;overflow:hidden}
body{font-family:SG,sans-serif;color:var(--ink);font-size:14.5px;-webkit-font-smoothing:antialiased;position:relative;background:__BODYBG__;font-variant-numeric:tabular-nums}
.i{width:19px;height:19px;stroke-width:1.5;flex:none}.i14{width:14px;height:14px;stroke-width:1.7;flex:none}
__WINCSS__
.sb{width:236px;flex:none;background:var(--side);border-right:1px solid var(--line);display:flex;flex-direction:column;padding:22px 10px 14px}
.lg{display:flex;align-items:center;justify-content:space-between;padding:0 12px 0 14px;height:34px;margin-bottom:34px}
.lg div{display:flex;align-items:center;gap:10px}.lg .i{width:24px;height:24px;color:var(--pr);stroke-width:1.8}.lg b{font-size:17.5px;font-weight:600;letter-spacing:-.02em}.lg .c{color:var(--mut);width:16px;height:16px}
.nv{display:flex;flex-direction:column;gap:2px}
.it{height:42px;display:flex;align-items:center;gap:13px;padding:0 14px;color:var(--tx);font-size:14.5px;border:1.5px solid transparent;border-radius:3px}
.it .i{color:var(--tx)}
.it.par{border-color:var(--ink)}
.grp{background:var(--side2);padding:8px 8px 8px;margin:0 0 6px;border-radius:3px}
.grp .sub{height:42px;display:flex;align-items:center;padding:0 16px;color:var(--mut);font-size:14.5px;border-radius:2px}
.grp .sub.on{background:#fff;color:var(--ink)}
.it em{margin-left:auto;font-style:normal;font-size:11.5px;font-weight:600;color:var(--pr);background:var(--prt2);border-radius:999px;min-width:20px;height:20px;display:flex;align-items:center;justify-content:center;padding:0 6px}
.sp{flex:1}
.hl{height:1px;background:var(--line);margin:8px 0}
.me{display:flex;align-items:center;gap:11px;padding:14px 14px 0;border-top:1px solid var(--line);margin-top:8px}.me .av{width:34px;height:34px;border-radius:50%;background-size:cover;background-position:center}
.me b{display:block;font-size:13.5px;font-weight:550}.me span{font-size:12px;color:var(--mut)}
.main{flex:1;display:flex;flex-direction:column;min-width:0;background:#fff}
.top{height:60px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 40px 0 56px;border-bottom:1px solid var(--line)}
.bc{display:flex;align-items:center;gap:9px;font-size:14.5px;color:var(--mut)}.bc .lk{color:var(--mut)}.bc b{font-weight:520;color:var(--ink)}.bc .i14{color:var(--mut2)}
.tr{display:flex;align-items:center;gap:22px}.tr .fld{width:290px;gap:10px;justify-content:flex-start;height:34px}.tr .fld .i14{order:-1}
.tr .bell{color:var(--tx);display:flex}.tr .bell .i{width:20px;height:20px}
.tr .av{width:32px;height:32px;border-radius:50%;background-size:cover;background-position:center}.tr .me2{display:flex;align-items:center;gap:8px;color:var(--mut)}
.hd{padding:26px 56px 0;flex:none;border-bottom:1px solid var(--line)}
.t1{display:flex;justify-content:space-between;align-items:flex-start;gap:30px}
h1{font-size:44px;font-weight:420;letter-spacing:-.04em;line-height:1.1;white-space:nowrap}
.meta{font-size:14.5px;color:var(--mut);margin-top:8px;white-space:nowrap}.meta b{font-weight:450;color:var(--tx)}
.acts{display:flex;gap:10px;margin-top:4px}
.ch{height:42px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:10px;padding:0 14px 0 14px;font-size:14.5px;color:var(--ink);white-space:nowrap}.ch .c{color:var(--mut);width:15px;height:15px;margin-left:2px}
.ch .ok{color:var(--ok)}.ch .pr{color:var(--pr)}
.btn2{width:42px;height:42px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--tx)}
.sev{display:flex;gap:2px;align-items:flex-end;height:15px}.sev i{width:4px;background:#DEDAD2}.sev i.f{background:var(--hi)}
.sev i:nth-child(1){height:6px}.sev i:nth-child(2){height:9px}.sev i:nth-child(3){height:12px}.sev i:nth-child(4){height:15px}
.tabs{display:flex;gap:34px;margin-top:22px;height:48px;align-items:flex-end}
.tab{height:48px;display:flex;align-items:center;gap:7px;font-size:15px;color:var(--mut);position:relative;white-space:nowrap}.tab small{font-size:12.5px;color:var(--mut2)}
.tab.on{color:var(--ink);font-weight:520}.tab.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--pr)}
.body{flex:1;display:grid;grid-template-columns:1fr __RW__px;min-height:0}
.tl{display:flex;flex-direction:column;min-height:0;padding:0 32px 0 56px}
.rb{padding:12px 0 6px;border-bottom:1px solid var(--line);border-top:1px solid var(--line)}
.rbh{display:flex;justify-content:space-between;font-size:13.5px;color:var(--mut)}.rbh b{color:var(--pr);font-weight:520}
.sh2{display:flex;align-items:flex-end;justify-content:space-between;height:__TOOLH__px;padding-bottom:12px}
.sh2 h2{font-size:21px;font-weight:450;letter-spacing:-.02em;line-height:1.1}.sh2 p{font-size:13.5px;color:var(--mut);margin-top:5px}
.sh2 .cs{display:flex;gap:22px;align-items:flex-end}.sh2 .cs .dl{height:32px;display:flex;align-items:center;color:var(--mut)}
.fld{width:290px;gap:10px;justify-content:flex-start;height:34px}.tr .fld .i14{order:-1}
.tr .bell{color:var(--tx);display:flex}.tr .bell .i{width:20px;height:20px}
.tr .av{width:32px;height:32px;border-radius:50%;background-size:cover;background-position:center}.tr .me2{display:flex;align-items:center;gap:8px;color:var(--mut)}
.hd{padding:26px 56px 0;flex:none;border-bottom:1px solid var(--line)}
.t1{display:flex;justify-content:space-between;align-items:flex-start;gap:30px}
h1{font-size:44px;font-weight:420;letter-spacing:-.04em;line-height:1.1;white-space:nowrap}
.meta{font-size:14.5px;color:var(--mut);margin-top:8px;white-space:nowrap}.meta b{font-weight:450;color:var(--tx)}
.acts{display:flex;gap:10px;margin-top:4px}
.ch{height:42px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:10px;padding:0 14px 0 14px;font-size:14.5px;color:var(--ink);white-space:nowrap}.ch .c{color:var(--mut);width:15px;height:15px;margin-left:2px}
.ch .ok{color:var(--ok)}.ch .pr{color:var(--pr)}
.btn2{width:42px;height:42px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--tx)}
.sev{display:flex;gap:2px;align-items:flex-end;height:15px}.sev i{width:4px;background:#DEDAD2}.sev i.f{background:var(--hi)}
.sev i:nth-child(1){height:6px}.sev i:nth-child(2){height:9px}.sev i:nth-child(3){height:12px}.sev i:nth-child(4){height:15px}
.tabs{display:flex;gap:34px;margin-top:22px;height:48px;align-items:flex-end}
.tab{height:48px;display:flex;align-items:center;gap:7px;font-size:15px;color:var(--mut);position:relative;white-space:nowrap}.tab small{font-size:12.5px;color:var(--mut2)}
.tab.on{color:var(--ink);font-weight:520}.tab.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--pr)}
.body{flex:1;display:grid;grid-template-columns:1fr __RW__px;min-height:0}
.tl{display:flex;flex-direction:column;min-height:0;padding:0 32px 0 56px}
.rb{padding:12px 0 6px;border-bottom:1px solid var(--line);border-top:1px solid var(--line)}
.rbh{display:flex;justify-content:space-between;font-size:13.5px;color:var(--mut)}.rbh b{color:var(--pr);font-weight:520}
.tool{display:flex;align-items:flex-end;gap:28px;height:__TOOLH__px;border-bottom:1px solid var(--line);padding-bottom:12px}
.fld{border-bottom:1px solid #CFCBC2;height:32px;display:flex;align-items:center;justify-content:space-between;color:var(--mut);font-size:14.5px;padding-bottom:2px}
.fld .i14{color:var(--mut)}
.th{display:grid;grid-template-columns:64px 28px 1fr 200px 40px;height:38px;align-items:center;font-size:13px;color:var(--mut);border-bottom:1px solid var(--line)}
.rows{position:relative;flex:1;min-height:0}
.rows::before{content:"";position:absolute;left:77px;top:__T1__px;height:__H1__px;border-left:1.5px solid #CFCBC2}
.rows::after{content:"";position:absolute;left:77px;top:__T2__px;height:__H2__px;border-left:1.5px dashed #CFCBC2}
.r{display:grid;grid-template-columns:64px 28px 1fr 200px 40px;align-items:center;height:__RH__px;border-bottom:1px solid var(--line);position:relative}
.r .tm{font-size:13.5px;color:var(--mut)}
.r .nd{position:relative;align-self:stretch}
.r .nd s{position:absolute;left:5px;top:50%;margin-top:-8px;width:12px;height:12px;border-radius:50%;background:#A5A199;border:2px solid #fff;box-sizing:content-box;z-index:1}
.r.blk .nd s{background:var(--hi);box-shadow:0 0 0 4px var(--hit)}
.r.cur .nd s{background:var(--pr);box-shadow:0 0 0 4px var(--prt2)}
.r .bd{padding:0 16px 0 8px}.r .ti{font-size:17px;font-weight:450;letter-spacing:-.015em;display:flex;gap:12px;align-items:center}
.r .ds{font-size:14px;color:var(--mut);margin-top:4px;white-space:nowrap}.r .ds .ip{color:var(--ink)}
.r .src{font-size:14px;color:var(--tx);white-space:nowrap}.r .src div{display:flex;align-items:center;gap:9px}.r .src small{display:block;font-size:12.5px;color:var(--mut);margin:2px 0 0 22px}
.r .go{width:32px;height:32px;border:1px solid var(--line);border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--mut);background:#fff}
.tc{font-size:12.5px;color:var(--tx);border:1px solid var(--line);border-radius:3px;padding:2px 8px;font-weight:400;letter-spacing:0;background:#fff}
.cr{position:absolute;inset:0 -32px 0 -56px;background:var(--prt);border-left:2px solid var(--pr)}
.r>*:not(.cr){position:relative;z-index:1}
.tg{font-size:13.5px;font-weight:500}
.tg.ok{color:var(--ok)}.tg.hi{color:var(--hi)}.tg.amb{color:var(--amb)}
.r.up{height:__UH__px;border-bottom:0}.r.up:first-of-type,.rows>.r.cur+.r.up{margin-top:__GAP__px}
.r.up .nd s{background:#fff;border:1.5px dashed #A5A199;width:11px;height:11px;margin-top:-7px;left:5px}
.r.up .bd{grid-column:3/6}.r.up .ti{font-size:15px;font-weight:420;color:var(--mut);gap:16px}.ud{font-size:14px;font-weight:400;color:var(--mut2)}
.rail{display:flex;flex-direction:column;border-left:1px solid var(--line);overflow:hidden}
.sec{padding:__SP__px 32px;border-bottom:1px solid var(--line)}
.sh{display:flex;justify-content:space-between;align-items:center;font-size:13.5px;color:var(--mut);margin-bottom:12px}.sh a{color:var(--pr);font-weight:480;display:flex;align-items:center;gap:3px;font-size:13px}.sh a .i14{width:13px;height:13px}
.id{display:flex;gap:14px;align-items:center}.id .av{width:48px;height:48px;border-radius:50%;background-size:cover;background-position:center;flex:none}
.id b{font-size:17.5px;font-weight:450;display:block;letter-spacing:-.015em}.id span{display:block;font-size:13px;color:var(--mut);margin-top:2px}
.id .rk{margin-left:auto;text-align:right}.id .rk b{font-size:32px;font-weight:420;letter-spacing:-.03em;color:var(--hi);line-height:1}.id .rk span{font-size:12.5px;margin-top:3px}
.rkb{height:3px;background:var(--line);margin-top:12px;position:relative}.rkb i{position:absolute;left:0;top:0;bottom:0;width:78%;background:var(--hi)}
.rs{display:flex;flex-wrap:wrap;gap:6px 6px;margin-top:12px}.rs span{font-size:12.5px;color:var(--tx);border:1px solid var(--line);border-radius:3px;padding:3px 9px}
.as{display:flex;align-items:center;gap:13px;height:50px}.as+.as{border-top:1px solid var(--line)}.as .g{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none}
.as b{display:block;font-size:14.5px;font-weight:450}.as span{font-size:12.5px;color:var(--mut)}.as .i14{margin-left:auto;color:var(--mut2)}
.gr{display:flex;align-items:center;gap:16px;margin-bottom:6px}.gg{position:relative;width:124px;height:70px;flex:none}.gg svg{width:124px;height:70px}.gg .v{position:absolute;left:0;right:0;bottom:0;text-align:center}.gg .v b{font-size:25px;font-weight:420;letter-spacing:-.04em;line-height:1}
.gr p{font-size:14px;color:var(--tx);line-height:1.35}
.fd div{display:flex;justify-content:space-between;gap:12px;font-size:13.5px;padding:6px 0;color:var(--tx);border-top:1px solid var(--line)}.fd span{white-space:nowrap}.fd .a{color:var(--amb)}.fd .g{color:var(--ok)}.fd .n{color:var(--mut)}
.ms{display:flex;flex-direction:column;gap:10px;font-size:13.5px;color:var(--tx)}.ms div{display:flex;gap:11px;align-items:center}.ms .i14{color:var(--mut2)}
.cta{margin-top:auto;padding:16px 32px 20px;border-top:1px solid var(--line)}.cta .btn{height:48px;width:100%;justify-content:center;border-radius:3px;background:var(--pr);color:#fff;display:flex;align-items:center;gap:10px;font-weight:520;font-size:15px}.cta .btn .i{width:17px;height:17px;stroke-width:1.9}

.gh{display:flex;align-items:center;gap:12px;height:58px;padding-top:2px}.gh .i{width:18px;height:18px;color:var(--mut)}.gh h3{font-size:17px;font-weight:480;letter-spacing:-.015em}.gh h3 small{font-size:14px;color:var(--mut);font-weight:400;margin-left:6px}.gh p{font-size:13.5px;color:var(--mut);margin-left:auto}
.gt{display:grid;grid-template-columns:1fr 136px 66px 94px 66px 118px;align-items:center;column-gap:10px}
.gth{height:34px;font-size:13px;color:var(--mut);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.gr1{height:__GRH__px;border-bottom:1px solid var(--line)}.gr1:last-child{border-bottom:0}
.ac{display:flex;gap:13px;align-items:center;min-width:0}.ac .g{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none}.ac .g .i{width:17px;height:17px}
.ac b{display:flex;align-items:center;gap:8px;font-size:15.5px;font-weight:450;letter-spacing:-.01em;white-space:nowrap}.ac span{display:block;font-size:13px;color:var(--mut);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ac>div{min-width:0}
.tgt b{display:block;font-size:14px;font-weight:420;white-space:nowrap}.tgt span{display:block;font-size:12.5px;color:var(--mut);margin-top:2px}
.cell{font-size:14px;color:var(--tx);white-space:nowrap}.cell.m{color:var(--mut)}
.rk2{font-size:13px;font-weight:480}.rk2.h{color:var(--hi)}.rk2.md{color:var(--amb)}.rk2.l{color:var(--mut)}
.edt{font-size:12px;color:var(--pr);background:var(--prt);border-radius:3px;padding:1px 7px;font-weight:500}
.chg{margin:0 0 12px 47px;background:#F8F7F4;border:1px solid var(--line);border-radius:3px;padding:12px 18px}.chg .t{display:flex;justify-content:space-between;font-size:13.5px}.chg .t b{font-weight:520}.chg .t span{color:var(--mut)}
.chg .c{display:grid;grid-template-columns:1fr 28px 1.2fr;align-items:center;margin-top:10px;font-size:13.5px;color:var(--tx);column-gap:14px}.chg .c .v b{display:flex;align-items:center;gap:8px;font-weight:480;font-size:13.5px}.chg .c .v span{display:block;color:var(--mut);margin:2px 0 0 24px;font-size:13px}.chg .c .i14{color:var(--mut)}
.s2{display:flex;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:6px}
.s2>div{flex:1;padding:12px 0 12px 0}.s2>div+div{padding-left:22px;border-left:1px solid var(--line)}
.s2 small{display:block;font-size:13px;color:var(--mut);margin-bottom:5px}.s2 b{font-size:21px;font-weight:420;letter-spacing:-.02em;display:flex;align-items:center;gap:10px;white-space:nowrap}
.sel{width:150px}
.wch{height:34px;display:flex;align-items:center;gap:9px;padding:0 13px;border:1px solid #EBD6A8;background:#FBF4E3;border-radius:3px;font-size:14px;color:#8A5A12;white-space:nowrap}
.kv div{display:flex;align-items:center;gap:11px;font-size:13.5px;color:var(--tx);padding:3px 0}.kv .i14{color:var(--ok);width:16px;height:16px}.kv span{margin-left:auto;color:var(--mut)}.kv .i14.n{color:var(--mut2)}
.ap{display:flex;gap:13px;align-items:center}.ap .av{width:42px;height:42px;border-radius:50%;background-size:cover;background-position:center}.ap b{display:block;font-size:15px;font-weight:450}.ap span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px}
.dc p{font-size:13.5px;color:var(--tx);line-height:1.4;margin-bottom:12px}
.dc .b1,.dc .b2,.dc .b3{height:37px;border-radius:3px;display:flex;align-items:center;justify-content:center;gap:9px;font-size:14.5px;margin-top:6px}
.dc .b1{border:1px solid #CFCBC2;color:var(--ink)}.dc .b2{background:var(--pr);color:#fff;font-weight:520}.dc .b3{background:#EFEDE8;color:#A5A199}
.dc small{display:block;text-align:center;font-size:12.5px;color:var(--mut);margin-top:8px}
.dc .i14{width:16px;height:16px}
.rl{position:relative}

.gt2{display:grid;grid-template-columns:1fr 122px 104px 108px 60px 102px;align-items:center;column-gap:10px}
.sx{height:__EH__px}
.xr{height:__XRH__px;border-bottom:1px solid var(--line);position:relative}
.xr.att{background:var(--hit);border-bottom:0}.xr.att::before{content:"";position:absolute;left:-56px;top:0;bottom:0;width:2px;background:var(--hi)}.xr.att{box-shadow:-56px 0 0 var(--hit)}
.ac .ch2{color:var(--mut2);width:15px;height:15px;margin-right:-4px;flex:none}
.st2{font-size:14px;color:var(--tx);white-space:nowrap}.st2 b{display:flex;align-items:center;gap:7px;font-weight:420}.st2 .i14{width:16px;height:16px}.st2 .ok{color:var(--ok)}.st2 .bad{color:var(--hi)}.st2 .run{color:var(--amb)}.st2 small{display:block;font-size:12.5px;color:var(--mut);margin:2px 0 0 23px}
.st2.bd b{color:var(--hi)}.own{color:var(--hi);font-size:14px}
.pn{background:#FAF9F7;border:1px solid var(--line);border-top:0;padding:16px 22px 14px;margin-bottom:0}
.pn .cols{display:grid;grid-template-columns:1fr 1fr;column-gap:26px}.pn .cols>div+div{border-left:1px solid var(--line);padding-left:26px}
.pi{display:flex;gap:12px;margin-bottom:12px}.pi:last-child{margin-bottom:0}.pi .i{width:18px;height:18px;color:var(--mut);margin-top:1px}
.pi b{display:block;font-size:14.5px;font-weight:520;margin-bottom:2px}.pi p{font-size:13.5px;color:var(--mut);line-height:1.38}.pi p em{font-style:normal;color:var(--ink)}
.pi .vb{display:inline-flex;align-items:center;gap:6px;margin-top:7px;height:30px;border:1px solid #CFCBC2;border-radius:3px;padding:0 11px;font-size:13.5px;color:var(--ink);background:#fff}
.nx{display:flex;align-items:center;gap:10px;margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}.nx>span{font-size:13.5px;color:var(--mut);margin-right:6px}
.nb{height:34px;border:1px solid #CFCBC2;border-radius:3px;display:flex;align-items:center;gap:8px;padding:0 14px;font-size:14px;color:var(--ink);background:#fff}.nb .i14{width:15px;height:15px}
.mb{display:flex;gap:3px;height:4px;margin-top:9px}.mb i{display:block;height:4px;border-radius:2px}
.apv{font-size:12px;color:var(--ok);background:#EAF3EE;border-radius:3px;padding:1px 7px;font-weight:500}
.s2 small.sb2{font-size:12px;color:var(--mut2);margin:3px 0 0}
.ctn{display:flex;gap:12px;align-items:flex-start;padding:8px 0}.ctn+.ctn{border-top:1px solid var(--line)}.ctn .i14{width:18px;height:18px;margin-top:2px;color:var(--mut2)}
.ctn b{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:14.5px;font-weight:450}.ctn>div>span{display:block;font-size:12.5px;color:var(--mut);margin-top:2px}
.ap b .pill{display:inline-block;margin:0 0 0 6px;vertical-align:1px}.pill{font-size:12px;border:1px solid var(--line);border-radius:3px;padding:1px 8px;color:var(--tx);font-weight:400;white-space:nowrap}.pill.w{border-color:#EBD6A8;background:#FBF4E3;color:#8A5A12}.pill.rd{border-color:#F3C9B5;background:var(--hit);color:var(--hi)}
.rsk p{font-size:13.5px;color:var(--tx);line-height:1.42;margin-bottom:10px}
.rsk .nb{width:max-content;height:32px}

.gt3{display:grid;grid-template-columns:1fr 176px 98px 82px 74px 84px;align-items:center;column-gap:10px}
.ag{height:__ARH__px;border-bottom:1px solid var(--line)}
.ag .ac .g{width:auto;height:auto;border:0;border-radius:0;color:var(--tx)}.ag .ac .g .i{width:20px;height:20px}
.fnd b{display:block;font-size:14px;font-weight:450;white-space:nowrap}.fnd span{display:block;font-size:12.5px;color:var(--mut);margin-top:2px;white-space:nowrap}
.cf .pill{font-size:12.5px;padding:2px 9px}.cf small{display:block;font-size:12px;color:var(--amb);margin-top:4px}
.ow{font-size:13.5px;color:var(--tx);line-height:1.25}.upd b{display:block;font-size:14px;font-weight:420}.upd span{display:block;font-size:12.5px;color:var(--mut);margin-top:2px}
.dp{background:#FAF9F7;border:1px solid var(--line);border-top:0;padding:14px 20px 16px}
.dph{display:flex;align-items:center;gap:13px;padding-bottom:12px}.dph .i{width:20px;height:20px;color:var(--mut)}.dph b{display:block;font-size:15px;font-weight:520}.dph span.s{display:block;font-size:13px;color:var(--mut);margin-top:1px}.dph .nb{margin-left:auto}
.cols2{display:grid;grid-template-columns:1fr 1fr;column-gap:22px}.cols2>div+div{border-left:1px solid var(--line);padding-left:22px}
.fh{display:flex;justify-content:space-between;align-items:center;font-size:13.5px;color:var(--mut)}.fh b{font-weight:450;color:var(--tx)}
.fl{font-size:16px;font-weight:480;letter-spacing:-.01em;margin-top:8px}.cols2 p{font-size:13.5px;color:var(--mut);line-height:1.4;margin-top:4px}
.evh{display:flex;justify-content:space-between;align-items:center;margin-top:12px;font-size:13.5px;color:var(--tx);font-weight:480;padding-bottom:4px}.evh a{color:var(--pr);font-weight:480;font-size:13px;display:flex;align-items:center;gap:3px}.evh a .i14{width:13px;height:13px}
.er{display:flex;align-items:center;gap:12px;height:40px;border-top:1px solid var(--line)}.er .i{width:17px;height:17px;color:var(--mut)}.er b{display:block;font-size:14px;font-weight:420}.er span{display:block;font-size:12.5px;color:var(--mut)}.er .i14{margin-left:auto;color:var(--mut2)}
.qs div{display:flex;gap:11px;align-items:center;font-size:13.5px;color:var(--tx);padding:4px 0}.qs .i14{color:var(--mut2)}
.mt div{display:flex;gap:11px;align-items:center;font-size:13.5px;color:var(--tx);padding:4px 0}.mt .i14{color:var(--mut2)}.mt em{margin-left:auto;font-style:normal;font-size:12px;color:var(--mut);border:1px solid var(--line);border-radius:3px;padding:1px 8px;white-space:nowrap}
.hy p{font-size:13.5px;color:var(--tx);line-height:1.42;margin-bottom:10px}
.sc{display:flex;align-items:center;gap:12px;padding:3px 0}.sc .av{width:40px;height:40px;border-radius:50%;background-size:cover;flex:none}.sc b{display:block;font-size:15px;font-weight:450}.sc span{display:block;font-size:12.5px;color:var(--mut)}.sc .i14{margin-left:auto;color:var(--mut2)}
.sc .g{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none}
.sm{font-size:13.5px;color:var(--tx);line-height:1.42;margin-top:6px}

.dc2{border:1px solid var(--line);border-radius:3px;margin:4px 0 22px}
.dc2h{display:flex;align-items:center;gap:13px;padding:13px 20px;border-bottom:1px solid var(--line)}.dc2h .i{width:20px;height:20px;color:var(--mut)}.dc2h b{display:block;font-size:17px;font-weight:480;letter-spacing:-.015em}.dc2h span.s{display:block;font-size:13.5px;color:var(--amb);margin-top:1px}.dc2h .nb{margin-left:auto}
.fo{display:grid;grid-template-columns:1fr 1fr}.fo>div{padding:15px 22px 10px}.fo>div+div{border-left:1px solid var(--line)}
.fo .a1{font-size:13.5px;color:var(--mut)}.fo .vd{font-size:27px;font-weight:420;letter-spacing:-.035em;margin-top:3px;line-height:1.1}
.cb{display:flex;align-items:center;gap:12px;margin-top:10px;font-size:13px;color:var(--mut)}.cb i{display:block;height:3px;width:150px;background:var(--line);position:relative}.cb i u{position:absolute;left:0;top:0;bottom:0;background:#6B6862}.cb.hi i u{background:var(--hi)}.cb b{color:var(--ink);font-weight:500}
.why{margin-top:12px}.why div{display:flex;align-items:center;gap:11px;height:43px;border-top:1px solid var(--line);font-size:14px;color:var(--tx);white-space:nowrap}.why .i14{width:16px;height:16px}.why .ok{color:var(--ok)}.why .fl2{color:var(--hi)}.why .cav{color:#8A5A12}.why .cav .i14{color:var(--amb)}.why .go2{margin-left:auto;color:var(--mut2);width:14px;height:14px}
.fo .vl{display:flex;align-items:center;gap:3px;font-size:13px;color:var(--pr);font-weight:480;height:30px;border-top:1px solid var(--line)}.fo .vl .i14{width:13px;height:13px}
.at{display:grid;grid-template-columns:1fr 116px 186px 76px 58px 58px 52px;align-items:center;column-gap:10px}
.ath{height:34px;font-size:13px;color:var(--mut);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.atr{height:__ATH__px;border-bottom:1px solid var(--line);font-size:14px;color:var(--tx)}
.atr .an{display:flex;align-items:center;gap:11px;color:var(--ink);font-size:15px}.atr .an .i{width:19px;height:19px;color:var(--tx)}.atr .an .ch2{margin-right:0}
.stt{display:flex;align-items:center;gap:7px;font-size:13.5px;white-space:nowrap}.stt .i14{width:15px;height:15px}.stt.n{color:#8A5A12}.stt.n .i14{color:var(--amb)}.stt.p{color:var(--mut)}.stt.d{color:var(--ok)}
.atr .m{color:var(--mut)}
.ath2{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}.ath2 h3{font-size:17px;font-weight:480;letter-spacing:-.015em}.ath2 h3 small{font-size:14px;color:var(--mut);font-weight:400;margin-left:6px}.ath2 p{font-size:13.5px;color:var(--mut)}
.qi{padding:8px 0;border-top:1px solid var(--line)}.qi:first-of-type{border-top:0}.qi b{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:450}.qi b .i14{color:var(--mut2)}.qi span{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut);margin:3px 0 0 24px}.qi em{white-space:nowrap;font-style:normal;font-size:11.5px;border:1px solid var(--line);border-radius:3px;padding:0 7px;color:var(--tx)}.qi em.pr{border-color:#EBD6A8;background:#FBF4E3;color:#8A5A12}
'''
import math
def gauge():
    cx,cy,r=100,100,84; th=math.pi*CONF/100
    ex=cx-r*math.cos(th); ey=cy-r*math.sin(th)
    return f'<svg viewBox="0 0 200 112"><path d="M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="#E7E4DD" stroke-width="7" stroke-linecap="round"/><path d="M{cx-r} {cy} A{r} {r} 0 0 1 {ex:.2f} {ey:.2f}" fill="none" stroke="#6B1D4A" stroke-width="7" stroke-linecap="round"/></svg>'

JD='data:image/jpeg;base64,'+b64(A/'jordan.jpg')
ACT_A=[('log-in','Revoke active session','Ends the unusual session','Maya Chen','AWS session','High','None','No','Identity Agent',''),
 ('shield','Isolate AWS workload','Blocks external traffic','prod-ml-workload','EC2 instance','High','None','Yes','Response Agent','')]
ACT_R=[('user','Suspend user account','Stops further access','Maya Chen','mchen@brightwell.io','High','None','Yes','Identity Agent',''),
 ('key-round','Rotate production secret','Invalidates exposed keys','S3: prod-data','Access key','High','3 services','Yes','Automation Agent','edt'),
 ('wrench','Disable misused agent tool','Removes the misused tool','prod-ml-workload','EC2 instance','Medium','None','Yes','Security Agent',''),
 ('ticket','Create Linear tickets','Tracks follow-up work','Project: Security','Linear','Low','None','N/A','Integration Agent','')]
assert len(ACT_A)==2 and len(ACT_R)==4
ROLL=sum(1 for a in ACT_A+ACT_R if a[7]=='Yes'); NOROLL=6-ROLL; assert (ROLL,NOROLL)==(4,2)
QCSS='''
.tl.rmx{overflow:hidden;position:relative}.tl.rmx>*{flex:none}
.tl.rmx::after{content:"";position:absolute;left:0;right:0;bottom:0;height:56px;background:linear-gradient(rgba(255,255,255,0),#fff);pointer-events:none}
.qtm{margin:26px 0 8px}
.qth{display:flex;align-items:baseline;justify-content:space-between}
.qth b{font-size:17px;font-weight:480;letter-spacing:-.015em;color:var(--ink)}.qth span.s{font-size:13.5px;color:var(--mut);margin-left:12px}
.qtl{display:flex;gap:18px;font-size:12.5px;color:var(--mut)}.qtl span{display:flex;align-items:center;gap:7px}.qtl i{display:block;width:16px;height:6px;border-radius:3px}
.qtc{position:relative;height:160px;margin-top:18px}
.qtp{position:absolute;left:206px;right:0;top:0;height:136px}
.qtg{position:absolute;top:-6px;bottom:-4px;width:1px;background:var(--line)}
.qtx{position:absolute;top:144px;white-space:nowrap;font-size:12px;color:var(--mut2);transform:translateX(-50%)}
.qtn{position:absolute;left:-206px;width:196px;font-size:13.5px;color:var(--tx);height:20px;line-height:20px;white-space:nowrap}
.qtb{position:absolute;height:8px;margin-top:6px}
.qtb.e{border-radius:4px 0 0 4px}.qtb.v{border-radius:0 4px 4px 0;opacity:.38}
.qtd{position:absolute;background:#fff;padding:0 6px;margin:0 -6px;font-size:12.5px;color:var(--mut);line-height:20px;white-space:nowrap}
.qts{position:absolute;left:0;right:0;height:1px;background:var(--line)}
'''
def REM(mode,AW,RW,DONE,TOTAL):
    win=mode=='win'
    def tr(a):
        ic,n,eff,t1,t2,rk,dp,rb,ex,ed=a
        k={'High':'h','Medium':'md','Low':'l'}[rk]
        tag='<span class="edt">Edited</span>' if ed else ''
        row=f'<div class="gt gr1"><div class="ac"><div class="g">{ico(ic)}</div><div><b>{n}{tag}</b><span>{eff}</span></div></div><div class="tgt"><b>{t1}</b><span>{t2}</span></div><div class="rk2 {k}">{rk}</div><div class="cell{" m" if dp=="None" else ""}">{dp}</div><div class="cell{" m" if rb in ("N/A",) else ""}">{rb}</div><div class="cell">{ex}</div></div>'
        if ed:
            row+=f'<div class="chg"><div class="t"><b>Change from version 1</b><span>Edited by Jordan Diaz, Oct 26, 02:27 UTC</span></div><div class="c"><div class="v"><b>{ico("minus","i14")}Version 1</b><span>Rotate access key only, no restart</span></div>{ico("arrow-right","i14")}<div class="v"><b>{ico("plus","i14")}Version 2, current</b><span>Rotate access key and restart 3 dependent services</span></div></div></div>'
        return row
    th='<div class="gt gth"><span>Action</span><span>Target</span><span>Risk</span><span>Dependencies</span><span>Rollback</span><span>Executor</span></div>'
    g1=f'<div class="gh">{ico("chevron-down")}<h3>Allowed automatically<small>2</small></h3><p>Match policy and run once execution is confirmed</p></div>{th}'+''.join(tr(a) for a in ACT_A)
    g2=f'<div class="gh" style="margin-top:10px">{ico("chevron-down")}<h3>Requires approval<small>4</small></h3><p>Need human approval before they can run</p></div>{th}'+''.join(tr(a) for a in ACT_R)
    SCH=[('Revoke active session','H',0,.5,1.0,'30 sec',0),('Isolate AWS workload','H',0,1.5,2.0,'90 sec',0),
         ('Suspend user account','H',1.0,2.0,2.5,'1 min',1),('Rotate production secret','H',2.0,5.0,6.5,'3 min',1),('Disable misused agent tool','M',2.0,3.5,4.5,'90 sec',1),('Create Linear tickets','L',6.5,7.5,8.0,'1 min',1)]
    RC={'H':'#E8743B','M':'#E2B24F','L':'#B8B3A8'}
    px=lambda m:m/8*100
    qg=''.join(f'<div class="qtg" style="left:{px(m)}%"></div><div class="qtx" style="left:{px(m)}%;'+('transform:none' if m==0 else 'transform:translateX(-100%)' if m==8 else '')+f'">{m} min</div>' for m in (0,2,4,6,8))
    qb=''
    for i,(n,r,s0,e0,v0,d,g) in enumerate(SCH):
        y=i*22+(10 if g else 0)
        qb+=f'<div class="qtn" style="top:{y}px">{n}</div><div class="qtb e" style="top:{y}px;left:{px(s0)}%;width:{px(e0-s0)}%;background:{RC[r]}"></div><div class="qtb v" style="top:{y}px;left:{px(e0)}%;width:{px(v0-e0)}%;background:{RC[r]}"></div><div class="qtd" style="top:{y}px;{("right:calc("+str(100-px(s0))+"% + 12px);text-align:right") if v0>7 else ("left:calc("+str(px(v0))+"% + 12px)")}">{d}</div>'
    qb=qb.replace('class="qtn"','class="qtn" ')
    qtm=f'<div class="qtm"><div class="qth"><div><b>Execution timeline</b><span class="s">Estimated 8 min after approval, by action</span></div><div class="qtl"><span><i style="background:{RC["H"]}"></i>High</span><span><i style="background:{RC["M"]}"></i>Medium</span><span><i style="background:{RC["L"]}"></i>Low</span><span><i style="background:#6B6860;opacity:.38"></i>Verification</span></div></div><div class="qtc"><div class="qtp">{qg}<div class="qts" style="top:{2*22+5}px"></div>{qb}</div></div></div>'
    main=f'''<section class="tl rmx"><div class="sh2"><div><h2>Remediation plan</h2><p>Proposed actions to contain the incident and prevent recurrence</p></div><div class="cs"><div class="fld sel"><span>Plan version 2</span>{ico("chevron-down","i14")}</div><div class="wch">{ico("triangle-alert","i14")}Revalidation required</div></div></div>
<div class="s2"><div><small>Plan version</small><b>2<span class="edt">Edited</span></b></div><div><small>Automated actions</small><b>2</b></div><div><small>Requires approval</small><b>4</b></div><div><small>Total actions</small><b>6</b></div><div><small>Estimated duration</small><b>8 min</b></div></div>
{qtm}{g1}{g2}</section>'''
    rail=f'''<aside class="rail"><div class="sec"><div class="sh">Affected systems<a>View all{ico("chevron-right","i14")}</a></div><div class="as"><div class="av" style="width:34px;height:34px;border-radius:50%;background-size:cover;background-image:url({MAYA});flex:none"></div><div><b>Maya Chen</b><span>mchen@brightwell.io</span></div>{ico("chevron-right","i14")}</div><div class="as"><div class="g">{ico("server")}</div><div><b>prod-ml-workload</b><span>EC2 instance, Production</span></div>{ico("chevron-right","i14")}</div><div class="as"><div class="g">{ico("database")}</div><div><b>brightwell-customer-data</b><span>S3 bucket, Production</span></div>{ico("chevron-right","i14")}</div></div>
<div class="sec"><div class="sh">Policy checks, plan version 2</div><div class="kv"><div>{ico("circle-check","i14")}All actions valid<span>6 / 6</span></div><div>{ico("circle-check","i14")}No policy violations<span>Passed</span></div><div>{ico("circle-check","i14")}Execution order valid<span>Passed</span></div><div>{ico("info","i14 n")}Estimated risk after execution<span>Low</span></div></div></div>
<div class="sec"><div class="sh">Approver</div><div class="ap"><div class="av" style="background-image:url({JD})"></div><div><b>Jordan Diaz</b><span>Security Administrator, jordan.diaz@brightwell.io</span></div></div></div>
<div class="sec"><div class="sh">Rollback coverage</div><div class="kv"><div>Actions with rollback<span>{ROLL} / 6</span></div><div>Actions without rollback{ico("info","i14 n")}<span>{NOROLL} / 6</span></div></div></div>
<div class="sec dc" style="margin-top:auto;border-bottom:0;border-top:1px solid var(--line)"><div class="sh" style="margin-bottom:6px">Decision</div><p>Revalidate the plan after your changes, then approve execution to run the actions.</p><div class="b1">Reject plan</div><div class="b2">{ico("refresh-cw","i14")}Run policy revalidation</div><div class="b3">{ico("play","i14")}Confirm execution</div><small>Disabled until revalidation succeeds</small></div></aside>'''
    return f'<div class="body">{main}{rail}</div>'

DN='data:image/jpeg;base64,'+b64(A/'daniel.jpg')
def EX(mode,AW,RW,DONE,TOTAL):
    win=mode=='win'
    th='<div class="gt2 gth"><span>Action</span><span>Target</span><span>Execution</span><span>Verification</span><span>Rollback</span><span>Owner</span></div>'
    def row(ic,n,ex,t1,t2,e,v,rb,ow,cls,vs,chev):
        vi={'bad':ico("circle-x","i14 bad"),'run':ico("loader","i14 run"),'ok':ico("circle-check","i14 ok")}[vs]
        vt={'bad':'Failed','run':'Verifying','ok':'Verified'}[vs]
        owc='own' if ow=='Unassigned' else 'cell'
        return f'<div class="gt2 xr {cls}"><div class="ac">{ico(chev,"i14 ch2")}<div class="g">{ico(ic)}</div><div><b>{n}</b><span>by {ex}</span></div></div><div class="tgt"><b>{t1}</b><span>{t2}</span></div><div class="st2"><b>{ico("circle-check","i14 ok")}Succeeded</b><small>{e}</small></div><div class="st2 {"bd" if vs=="bad" else ""}"><b>{vi}{vt}</b><small>{v}</small></div><div class="cell{" m" if rb=="N/A" else ""}">{rb}</div><div class="{owc}">{ow}</div></div>'
    r1=row('key-round','Rotate production secret','Automation Agent','S3: prod-data','Access key','02:35','02:41','Yes','Unassigned','att','bad','chevron-down')
    r2=row('wrench','Disable misused agent tool','Security Agent','prod-ml-workload','EC2 instance','02:36','Started 02:40','Yes','Security Agent','','run','chevron-right')
    panel=f'''<div class="pn"><div class="cols"><div><div class="pi">{ico("clipboard-check")}<div><b>Expected state</b><p>S3 access key rotated and all dependent services updated to the new secret. No component uses the previous secret.</p></div></div><div class="pi">{ico("file-search")}<div><b>Observed state</b><p>New key created and applied to the primary configuration, but one dependent service still uses the previous secret.</p></div></div></div>
<div><div class="pi">{ico("database")}<div><b>Verification evidence</b><p>Scan of dependent services found 1 service still using the previous secret.</p><div class="vb">View verification evidence{ico("chevron-right","i14")}</div></div></div><div class="pi">{ico("link")}<div><b>Failed dependency</b><p><em>prod-ml-workload</em> (EC2 instance), configuration still references the previous S3 access key.</p></div></div><div class="pi">{ico("clock")}<div><b>Last check</b><p>Oct 26, 2026, 02:41 UTC</p></div></div></div></div>
<div class="nx"><span>Next steps</span><div class="nb">{ico("refresh-cw","i14")}Retry verification</div><div class="nb">{ico("undo-2","i14")}Rollback action</div><div class="nb">{ico("user-plus","i14")}Assign owner</div></div></div>'''
    def vm_panel():
        X0,X1,T0,H=26,296,16,92; base=T0+H; PWd=360
        xt=lambda m:X0+(m-20)/24*(X1-X0)
        axis=''.join(f'<text x="{xt(m):.1f}" y="{base+22}" font-size="11.5" fill="#A5A199" text-anchor="middle">02:{m:02d}</text><line x1="{xt(m):.1f}" x2="{xt(m):.1f}" y1="{base}" y2="{base+5}" stroke="#D8D4CB"/>' for m in (20,25,30,35,40))
        def grid(vals,ymax):
            return ''.join(f'<line x1="{X0}" x2="{X1}" y1="{T0+H-v/ymax*H:.1f}" y2="{T0+H-v/ymax*H:.1f}" stroke="#E7E4DD"/><text x="0" y="{T0+H-v/ymax*H+4:.1f}" font-size="11.5" fill="#A5A199">{v}</text>' for v in vals)+f'<line x1="{X0}" x2="{X1}" y1="{base}" y2="{base}" stroke="#D8D4CB"/>'
        # A: egress bars
        EG=[6,18,9,5,3,2,0,0,0,0,0,0]; ym=24; slot=(X1-X0)/12
        a=f'<svg width="{PWd}" height="{base+30}" viewBox="0 0 {PWd} {base+30}">'+grid((8,16),ym)+axis
        for i,v in enumerate(EG):
            cx=X0+slot*(i+.5); h=max(v/ym*H,2 if v==0 else 0); col='#E8743B' if i==1 else ('#D9D4CA' if v else '#BFD9C9')
            a+=f'<rect x="{cx-6.5:.1f}" y="{base-h:.1f}" width="13" height="{h:.1f}" rx="2" fill="{col}"/>'
        xi=xt(31)
        a+=f'<line x1="{xi:.1f}" x2="{xi:.1f}" y1="{T0-6}" y2="{base}" stroke="#2E7D4F" stroke-dasharray="3 4"/><text x="{xi+8:.1f}" y="{T0+6}" font-size="12.5" fill="#2E7D4F">Workload isolated 02:31</text>'
        a+=f'<text x="{X0+4}" y="{base-18/ym*H-9:.1f}" font-size="12.5" fill="#B03A08">Upload blocked</text>'
        a+=f'<text x="{X1+16}" y="{base-14}" font-size="14" font-weight="500" fill="#2E7D4F">0 MB/min</text><text x="{X1+16}" y="{base+2}" font-size="12.5" fill="#7A776F">Since 02:32</text></svg>'
        # B: old key requests line
        RQ=[40,42,39,41,43,40,41,42,11,7,6,6]; yb=50
        px=lambda i:X0+slot*(i+.5); py=lambda v:T0+H-v/yb*H
        pts=[(px(i),py(v)) for i,v in enumerate(RQ)]
        d='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
        b=f'<svg width="{PWd}" height="{base+30}" viewBox="0 0 {PWd} {base+30}"><defs><linearGradient id="gk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9480F" stop-opacity=".16"/><stop offset="1" stop-color="#D9480F" stop-opacity="0"/></linearGradient></defs>'+grid((25,50),yb)+axis
        b+=f'<path d="{d} L{pts[-1][0]:.1f} {base} L{pts[0][0]:.1f} {base} Z" fill="url(#gk)"/><path d="{d}" fill="none" stroke="#D9480F" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
        xr=xt(35.3)
        b+=f'<line x1="{xr:.1f}" x2="{xr:.1f}" y1="{T0-6}" y2="{base}" stroke="#A5A199" stroke-dasharray="3 4"/><text x="{xr+8:.1f}" y="{T0+6}" font-size="12.5" fill="#4A4741">Key rotated 02:35</text>'
        b+=f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="#D9480F"/><circle cx="{pts[8][0]:.1f}" cy="{pts[8][1]:.1f}" r="4.5" fill="#fff" stroke="#D9480F" stroke-width="2"/>'
        b+=f'<text x="{X1+16}" y="{pts[-1][1]-6:.1f}" font-size="14" font-weight="500" fill="#B03A08">6 / min</text><text x="{X1+16}" y="{pts[-1][1]+10:.1f}" font-size="12.5" fill="#7A776F">Expected 0</text></svg>'
        hd=lambda ti,su,st,c:f'<div class="vmh"><div><b>{ti}</b><span class="s">{su}</span></div><span class="vst {c}">{st}</span></div>'
        return f'<div class="vmw"><div class="vmp">{hd("Egress to external IPs","prod-ml-workload, MB per minute","Verified","vgd")}{a}</div><div class="vmp">{hd("Requests using the previous key","Dependent services, requests per minute","Failed","vbd")}{b}</div></div>'
    vm=vm_panel()
    gh=lambda icn,t,c,d,st='':f'<div class="gh" {st}>{icn}<h3>{t}<small>{c}</small></h3><p>{d}</p></div>'
    main=f'''<section class="tl afx"><div class="sh2"><div><h2>Execution and verification</h2><p>Monitor the approved plan, verify results and act on failures</p></div><div class="cs"><div class="fld sel"><span>Plan version 2</span>{ico("chevron-down","i14")}</div><div class="wch">{ico("triangle-alert","i14")}Incident remains open</div></div></div>
<div class="s2"><div style="flex:1.5"><small>Plan version</small><b>2<span class="apv">Approved</span></b><small class="sb2">By Jordan Diaz, 02:29 UTC</small></div><div style="padding-right:24px"><small>Started</small><b>6 / 6</b><div class="mb"><i style="flex:4;background:var(--ok)"></i><i style="flex:1;background:#E3B15A"></i><i style="flex:1;background:var(--hi)"></i></div></div><div><small>Verified</small><b>4</b></div><div><small>In progress</small><b>1</b></div><div><small>Needs attention</small><b style="color:var(--hi)">1</b></div><div><small>Not started</small><b>0</b></div></div>
{vm}{gh(ico("triangle-alert","i").replace('class="i"','class="i" style="color:var(--hi)"'),"Needs attention","1","Fix before the incident can close")}{th}{r1}{panel}
{gh(ico("loader"),"In progress","1","Waiting for verification checks",'style="margin-top:6px"')}{r2}
{gh(ico("circle-check").replace('class="i"','class="i" style="color:var(--ok)"'),"Verified","4","4 of 4 verified, last at 02:38",'style="margin-top:6px"').replace(ico("chevron-down"),"")}</section>'''
    rail=f'''<aside class="rail"><div class="sec"><div class="sh">Incident containment</div><div class="ctn">{ico("shield-check","i14")}<div style="flex:1"><b>Immediate containment<span class="pill w">Partial</span></b><span>Account suspended and workload isolated</span></div></div><div class="ctn">{ico("shield","i14")}<div style="flex:1"><b>Full containment<span class="pill rd">Not achieved</span></b><span>Verification pending for 2 actions</span></div></div></div>
<div class="sec rsk"><div class="sh">Unresolved risk</div><p>One dependent service still uses the previous S3 access key, which may allow continued data access.</p><div class="nb">View affected systems{ico("chevron-right","i14")}</div></div>
<div class="sec"><div class="sh">Responsible owner</div><div class="ap"><div class="av" style="background-image:url({DN})"></div><div><b>Daniel Okafor<span class="pill">Human</span></b><span>Platform Engineer, Engineering</span><span>daniel.okafor@brightwell.io</span></div></div></div>
<div class="sec dc" style="margin-top:auto;border-bottom:0;border-top:1px solid var(--line)"><div class="sh" style="margin-bottom:6px">Execution decision</div><p>Address the failed verification to complete containment, or roll the action back if needed.</p><div class="b2">{ico("refresh-cw","i14")}Retry verification</div><div class="b1">{ico("undo-2","i14")}Rollback action</div><div class="b1">Escalate to incident commander{ico("external-link","i14")}</div></div></aside>'''
    return f'<div class="body">{main}{rail}</div>'

KCSS='''
.vmw{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:22px 0 4px}
.vmp{border:1px solid var(--line);border-radius:3px;padding:16px 18px 6px}
.vmh{display:flex;justify-content:space-between;align-items:flex-start}.vmh b{display:block;font-size:15px;font-weight:520;color:var(--ink);letter-spacing:-.005em}.vmh span.s{display:block;font-size:12.5px;color:var(--mut);margin-top:3px}
.vst{font-size:12.5px;font-weight:500;border-radius:3px;padding:3px 9px;white-space:nowrap}.vst.vgd{background:#EAF3EE;color:var(--ok)}.vst.vbd{background:var(--hit);color:#B03A08}
.vmp svg{display:block;margin-top:10px;font-family:inherit;overflow:visible}

.tl.afx{overflow:hidden;position:relative}.tl.afx>*{flex:none}
.tl.afx::after{content:"";position:absolute;left:0;right:0;bottom:0;height:56px;background:linear-gradient(rgba(255,255,255,0),#fff);pointer-events:none}
.kcw{margin:24px 0 10px}
.kch{display:flex;align-items:baseline}.kch b{font-size:17px;font-weight:480;letter-spacing:-.015em;color:var(--ink)}.kch span{font-size:13.5px;color:var(--mut);margin-left:12px}
.kcw svg{display:block;margin-top:10px;font-family:inherit;overflow:visible}
'''
def AF(mode,AW,RW,DONE,TOTAL):
    def why(items):
        o=''
        for k,t in items:
            ic={'ok':ico("circle-check","i14 ok"),'fl':ico("flag","i14 fl2"),'cav':ico("triangle-alert","i14")}[k]
            o+=f'<div class="{"cav" if k=="cav" else ""}">{ic}{t}{ico("chevron-right","i14 go2")}</div>'
        return o
    card=f'''<div class="dc2"><div class="dc2h">{ico("scale")}<div><b>Agents disagree on the session</b><span class="s">Analyst decision required</span></div><div class="nb">{ico("arrow-left-right","i14")}Compare findings</div></div>
<div class="fo"><div><div class="a1">Identity and Asset Agent</div><div class="vd">Likely legitimate</div><div class="cb"><i><u style="width:58%"></u></i><span><b>58%</b> confidence, Medium</span></div><div class="why">{why([("ok","Matches travel record, Singapore, Oct 24 to Oct 30"),("ok","MFA satisfied at sign-in"),("cav","Caveat: device not enrolled in MDM")])}</div><div class="vl">View all 4 evidence items{ico("chevron-right","i14")}</div></div>
<div><div class="a1">Threat and Exposure Agent</div><div class="vd">Compromised</div><div class="cb hi"><i><u style="width:86%"></u></i><span><b>86%</b> confidence, High</span></div><div class="why">{why([("fl","User seen in the US 2 hours earlier"),("fl","Unseen device in the organization"),("fl","Upload to high-risk IP 45.133.194.17")])}</div><div class="vl">View all 5 evidence items{ico("chevron-right","i14")}</div></div></div></div>'''
    W_,X0,X1,T0,H_=884,40,780,18,150
    xx=lambda m:X0+(m-14)/(28-14)*(X1-X0)
    yy=lambda v:T0+(100-v)/80*H_
    def path(pts):
        P=[(xx(a),yy(b)) for a,b in pts]; d=f'M{P[0][0]:.1f} {P[0][1]:.1f}'; r=6
        for i in range(1,len(P)):
            x,y=P[i]; py=P[i-1][1]; s=1 if y>py else -1; rr=min(r,abs(y-py)/2)
            d+=f' H{x-rr:.1f} Q{x:.1f} {py:.1f} {x:.1f} {py+s*rr:.1f} V{y-s*rr:.1f} Q{x:.1f} {y:.1f} {x+rr:.1f} {y:.1f}'
        # end at last x
        d=d.rsplit(' Q',1)[0]+f' Q{P[-1][0]:.1f} {P[-1][1]:.1f} {P[-1][0]:.1f} {P[-1][1]:.1f}'
        return d,P
    IDp=[(14,70),(18,66),(20,63),(23,58)]
    THp=[(18,34),(20,42),(22,71),(24,86)]
    dI,PI=path(IDp);dT,PT=path(THp)
    base=T0+H_
    areaI=dI+f' L{PI[-1][0]:.1f} {base} L{PI[0][0]:.1f} {base} Z';areaT=dT+f' L{PT[-1][0]:.1f} {base} L{PT[0][0]:.1f} {base} Z'
    NOW=xx(26)
    g=''.join(f'<line x1="{X0}" x2="{X1}" y1="{yy(v):.1f}" y2="{yy(v):.1f}" stroke="#E7E4DD"/><text x="0" y="{yy(v)+4:.1f}" font-size="11.5" fill="#A5A199">{v}%</text>' for v in (40,60,80))
    g+=f'<line x1="{X0}" x2="{X1}" y1="{base}" y2="{base}" stroke="#D8D4CB"/>'
    ax=''.join(f'<text x="{xx(m):.1f}" y="{base+22}" font-size="12" fill="#A5A199" text-anchor="middle">02:{m:02d}</text><line x1="{xx(m):.1f}" x2="{xx(m):.1f}" y1="{base}" y2="{base+5}" stroke="#D8D4CB"/>' for m in (14,16,18,20,22,24,26,28))
    CI,CT='#6B6860','#D9480F'
    s=f'<svg width="{W_}" height="{base+32}" viewBox="0 0 {W_} {base+32}"><defs><linearGradient id="gi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CI}" stop-opacity=".12"/><stop offset="1" stop-color="{CI}" stop-opacity="0"/></linearGradient><linearGradient id="gt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CT}" stop-opacity=".16"/><stop offset="1" stop-color="{CT}" stop-opacity="0"/></linearGradient></defs>{g}{ax}'
    s+=f'<line x1="{NOW:.1f}" x2="{NOW:.1f}" y1="{T0-6}" y2="{base}" stroke="#D8D4CB" stroke-dasharray="3 4"/>'
    s+=f'<path d="{areaI}" fill="url(#gi)"/><path d="{areaT}" fill="url(#gt)"/>'
    s+=f'<path d="{dI}" fill="none" stroke="{CI}" stroke-width="2" stroke-linecap="round"/><path d="{dT}" fill="none" stroke="{CT}" stroke-width="2" stroke-linecap="round"/>'
    s+=f'<line x1="{PI[-1][0]:.1f}" x2="{NOW:.1f}" y1="{PI[-1][1]:.1f}" y2="{PI[-1][1]:.1f}" stroke="{CI}" stroke-width="2" stroke-dasharray="2 5" stroke-linecap="round"/><line x1="{PT[-1][0]:.1f}" x2="{NOW:.1f}" y1="{PT[-1][1]:.1f}" y2="{PT[-1][1]:.1f}" stroke="{CT}" stroke-width="2" stroke-dasharray="2 5" stroke-linecap="round"/>'
    # markers
    mk=lambda p,c,fill:f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4.5" fill="{fill}" stroke="{c}" stroke-width="2"/>'
    s+=''.join(mk(p,CI,'#fff') for p in PI[1:-1])+''.join(mk(p,CT,'#fff') for p in PT[:-1] if p!=PT[2])+mk(PT[2],CT,'#fff')+mk(PI[-1],CI,CI)+mk(PT[-1],CT,CT)
    s+=f'<text x="{PI[1][0]:.1f}" y="{PI[1][1]+26:.1f}" font-size="12.5" fill="#4A4741" text-anchor="middle">Device not in MDM</text>'
    s+=f'<text x="{PT[2][0]-12:.1f}" y="{PT[2][1]-12:.1f}" font-size="12.5" fill="#B03A08" text-anchor="end">Upload to 45.133.194.17</text>'
    # gap bracket
    bx=NOW-14
    s+=f'<path d="M{bx-4} {PT[-1][1]:.1f} H{bx} V{PI[-1][1]:.1f} H{bx-4}" fill="none" stroke="#A5A199" stroke-width="1.3"/><text x="{bx-12}" y="{(PT[-1][1]+PI[-1][1])/2+4:.1f}" font-size="12.5" fill="#4A4741" text-anchor="end" font-weight="500">28 pts apart</text>'
    # end labels
    s+=f'<text x="{NOW+16:.1f}" y="{PT[-1][1]+1:.1f}" font-size="13.5" fill="#B03A08" font-weight="500">86%</text><text x="{NOW+16:.1f}" y="{PT[-1][1]+18:.1f}" font-size="12.5" fill="#7A776F">Compromised</text>'
    s+=f'<text x="{NOW+16:.1f}" y="{PI[-1][1]+1:.1f}" font-size="13.5" fill="#3C3A36" font-weight="500">58%</text><text x="{NOW+16:.1f}" y="{PI[-1][1]+18:.1f}" font-size="12.5" fill="#7A776F">Likely legitimate</text></svg>'
    conf=f'<div class="kcw"><div class="kch"><b>How confidence moved</b><span>Each agent in its own verdict, Oct 26, 02:14 to 02:26 UTC</span></div>{s}</div>'
    AG=[('user-round','Identity and Asset Agent','n','Needs review','Session may be legitimate','Medium','4','4','02:23'),
        ('radar','Threat and Exposure Agent','n','Needs review','Session is compromised','High','5','6','02:24'),
        ('files','Evidence Collection Agent','p','In progress','Retrieving CloudTrail logs','—','0','2','02:26'),
        ('shield','Data Protection Agent','d','Completed','Transfer blocked','High','6','4','02:22'),
        ('wrench','Remediation Agent','d','Completed','Plan proposed, 6 actions','High','4','3','02:26')]
    st={'n':ico("triangle-alert","i14"),'p':ico("loader","i14"),'d':ico("circle-check","i14")}
    rows=''.join(f'<div class="at atr"><div class="an">{ico("chevron-right","i14 ch2")}{ico(ic)}{n}</div><div class="stt {k}">{st[k]}{s_}</div><div>{f}</div><div class="{"m" if c=="—" else ""}">{c}</div><div>{ev}</div><div>{so}</div><div class="m">{u}</div></div>' for ic,n,k,s_,f,c,ev,so,u in AG)
    main=f'''<section class="tl afx"><div class="sh2"><div><h2>Agent findings</h2><p>Specialist agents investigate in parallel, you decide when they disagree</p></div><div class="cs"><div class="fld sel"><span>All agents</span>{ico("chevron-down","i14")}</div></div></div>
{card}{conf}<div class="ath2"><h3>Agents<small>5</small></h3><p>2 need review, 1 in progress, 2 completed</p></div>
<div class="at ath"><span>Agent</span><span>Status</span><span>Finding</span><span>Confidence</span><span>Evidence</span><span>Sources</span><span>Updated</span></div>{rows}</section>'''
    qi=lambda q,need,src,extra='':f'<div class="qi"><b>{ico("square","i14")}{q}</b><span>Needs {need}<em>{src}</em>{extra}</span></div>'
    rail=f'''<aside class="rail"><div class="sec"><div class="sh">Shared incident context<a>View all{ico("chevron-right","i14")}</a></div><div class="sc"><div class="av" style="background-image:url({MAYA})"></div><div><b>Maya Chen</b><span>Data Scientist, Engineering</span></div>{ico("chevron-right","i14")}</div><div class="sc"><div class="g">{ico("server")}</div><div><b>prod-ml-workload</b><span>EC2 instance, Production</span></div>{ico("chevron-right","i14")}</div><div class="sc"><div class="g">{ico("database")}</div><div><b>brightwell-customer-data</b><span>S3 bucket, Production</span></div>{ico("chevron-right","i14")}</div><div class="sm">AWS sign-in from an unusual location on a new device, Restricted file opened, outbound transfer blocked.</div></div>
<div class="sec"><div class="sh">What would settle it</div>{qi("Did the user approve the sign-in?","MFA approval log","Identity provider")}{qi("Was the device managed?","EDR process logs","Endpoint")}{qi("Travel or credential theft?","device location history","MDM")}{qi("Was data exfiltrated before the block?","CloudTrail logs","AWS",'<em class="pr">In progress</em>')}</div>
<div class="sec hy dc" style="margin-top:auto;border-bottom:0;border-top:1px solid var(--line)"><div class="sh" style="margin-bottom:6px">Current hypothesis</div><p>Conflicting assessments. One agent finds the session may be legitimate, the other finds likely credential compromise.</p><div class="b2">Record analyst verdict{ico("arrow-right","i14")}</div><small>Record your assessment to complete the investigation</small></div></aside>'''
    return f'<div class="body">{main}{rail}</div>'

def POL(css,CW,CH):
    extra='''
.pl{display:flex;flex:1;min-height:0}
.lc{width:336px;flex:none;border-right:1px solid var(--line);display:flex;flex-direction:column}
.lch{padding:22px 24px 14px}.lch h3{font-size:18px;font-weight:480;letter-spacing:-.015em}.lch h3 small{font-size:14px;color:var(--mut);font-weight:400;margin-left:6px}
.lch .fld{margin-top:14px;width:100%;height:32px}.lch .fld+.fld{margin-top:10px}
.al{display:flex;align-items:center;gap:13px;padding:0 20px 0 24px;min-height:78px;padding-top:12px;padding-bottom:12px;border-top:1px solid var(--line);position:relative}
.al.on{background:var(--prt)}.al.on::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--pr)}
.al .ag2{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;flex:none;background:#fff;color:var(--tx)}.al .ag2 .i{width:17px;height:17px}
.al b{display:block;font-size:14.5px;font-weight:450;letter-spacing:-.01em;white-space:nowrap}.al span{display:block;font-size:12.5px;color:var(--mut);margin-top:3px;white-space:nowrap}
.al .hc{margin-left:auto;align-self:flex-start;margin-top:4px}
.hc{font-size:12px;border-radius:3px;padding:2px 8px;border:1px solid var(--line);color:var(--ok);background:#F3F8F5;white-space:nowrap}.hc.w{color:#8A5A12;border-color:#EBD6A8;background:#FBF4E3}
.cc{flex:1;min-width:0;display:flex;flex-direction:column;padding:0 24px 0 24px}
.ah{display:flex;align-items:center;gap:16px;padding:22px 0 18px}
.ah .big{width:50px;height:50px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx)}.ah .big .i{width:24px;height:24px}
.ah h2{font-size:24px;font-weight:450;letter-spacing:-.025em;display:flex;align-items:center;gap:12px}.ah h2 .st{font-size:13px;font-weight:450;letter-spacing:0;color:var(--ok);border:1px solid var(--line);border-radius:3px;padding:2px 8px;background:#F3F8F5}
.ah .mt2{display:flex;gap:26px;margin-top:6px;font-size:13.5px;color:var(--mut)}.ah .mt2 b{font-weight:450;color:var(--ink);margin-left:6px}
.ah .btns{margin-left:auto;display:flex;gap:10px}.ah .btns .nb{height:38px;padding:0 18px}.ah .btns .k{width:38px;height:38px;border:1px solid #CFCBC2;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--tx)}
.ps{border-top:1px solid var(--line)}
.ph{display:flex;align-items:center;gap:13px;height:52px}.ph .ch2{width:16px;height:16px;color:var(--mut2)}.ph .gi{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none}.ph .gi .i{width:17px;height:17px}
.ph b{display:block;font-size:15.5px;font-weight:480;letter-spacing:-.01em}.ph span.d{display:block;font-size:13px;color:var(--mut);margin-top:1px;white-space:nowrap}
.ph .sm2{margin-left:auto;font-size:13px;color:var(--mut);white-space:nowrap}.ph .eb{height:32px;border:1px solid #CFCBC2;border-radius:3px;display:flex;align-items:center;padding:0 16px;font-size:14px;color:var(--ink);margin-left:16px}
.pr1{display:grid;grid-template-columns:196px 132px 1fr 18px;align-items:center;column-gap:14px;height:40px;margin-left:47px;border-top:1px solid var(--line);font-size:14.5px;color:var(--ink)}
.pr1 .d2{font-size:13.5px;color:var(--mut);white-space:nowrap}.pr1 .i14{color:var(--mut2)}
.pill2{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;border-radius:3px;padding:2px 9px;white-space:nowrap;width:max-content}.pill2 .i14{width:13px;height:13px}
.pill2.a{color:var(--ok);background:#EAF3EE}.pill2.b{color:#6B6862;background:#EFEDE8}.pill2.ap{color:#8A5A12;background:#FBF1D9}
.rl2{width:328px;flex:none;border-left:1px solid var(--line);display:flex;flex-direction:column}
.rl2 .sec{padding:18px 26px}
.ea div{display:grid;grid-template-columns:124px 1fr;padding:6px 0;font-size:13.5px}.ea div span{color:var(--mut)}.ea div b{font-weight:450;color:var(--ink)}.ea div small{display:block;font-size:12.5px;color:var(--mut);margin-top:1px;font-weight:400}
.pc{display:flex;gap:11px;align-items:center;font-size:13.5px;color:var(--tx)}.pc .i14{color:var(--ok);width:18px;height:18px}.pc small{display:block;font-size:12.5px;color:var(--mut);margin-top:2px}
.rc{position:relative;padding-left:22px}.rc+.rc{margin-top:12px}.rc::before{content:"";position:absolute;left:4px;top:7px;width:9px;height:9px;border-radius:50%;background:#A5A199}.rc::after{content:"";position:absolute;left:8px;top:18px;bottom:-14px;border-left:1.5px solid #CFCBC2}.rc:last-child::after{display:none}
.rc b{display:block;font-size:14px;font-weight:450}.rc span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px}
.rl2 .ctab{margin-top:auto;padding:16px 26px 22px;border-top:1px solid var(--line)}
.ctab .b2,.ctab .b1{height:42px;border-radius:3px;display:flex;align-items:center;justify-content:center;gap:9px;font-size:14.5px}.ctab .b2{background:var(--pr);color:#fff;font-weight:520}.ctab .b1{border:1px solid #E6C3B3;color:var(--hi);margin-top:9px}.ctab .i14{width:16px;height:16px}

.sg{display:flex;gap:4px;height:22px;flex:none;align-items:center;width:44px;justify-content:flex-start}.sg i{display:block;width:8px;height:22px;border-radius:4px}.logo{height:31px;display:block}.sgl{margin-left:auto;font-size:13px;color:var(--mut);width:118px;text-align:right;white-space:nowrap}.ph .sgl b{display:inline;color:var(--ink);font-weight:480;font-size:13px}
.ph .sg{margin-left:16px}.ph .sgl{margin-left:auto}.ea2 .sg{height:16px;width:auto}.ea2 .sg i{width:8px;height:16px;border-radius:4px}.ph .eb,.ph .eb0{margin-left:20px;width:64px;height:32px}.ph .eb{justify-content:center;padding:0}
.edt{font-size:11.5px;color:var(--pr);background:var(--prt);border-radius:3px;padding:1px 7px;font-weight:500;margin-left:9px;letter-spacing:0}
.mt2 span,.nb{white-space:nowrap}.mt2{gap:12px!important}.ah .btns{gap:8px!important}.ah .nb{padding:0 14px!important}.mt2 span{font-size:13px}.lgd{display:flex;justify-content:space-between;align-items:center;height:30px;font-size:12.5px;color:var(--mut);border-top:1px solid var(--line)}.lgd div{display:flex;align-items:center;gap:7px}.lgd u{display:inline-block;width:9px;height:9px;border-radius:2px;margin-left:12px}
.al .wn{color:#8A5A12!important}
.hc2{display:inline-flex;align-items:center;gap:6px;margin-left:6px;font-size:12px!important;border-radius:3px;padding:2px 8px;border:1px solid var(--line);color:var(--ok)!important;background:#F3F8F5;font-weight:450!important}.hc2 .i14{width:13px;height:13px}
.ea2>div{display:grid;grid-template-columns:92px 1fr 112px;align-items:center;column-gap:12px;padding:7px 0;font-size:13.5px}.ea2>div>span{color:var(--mut)}.ea2 b{font-weight:450;color:var(--tx);font-size:13px;text-align:right;white-space:nowrap}
.cl{margin-top:8px;border-top:1px solid var(--line);padding-top:10px}.cl div{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--mut);padding:3px 0}.cl .i14{width:16px;height:16px;margin-top:2px}.cl div:first-child .i14{color:var(--amb)}.cl div+div .i14{color:#6B6862}.cl span{line-height:1.3}.cl b{display:block;font-weight:450;color:var(--ink);font-size:13.5px}
.sh .ut{font-size:12px;color:var(--pr);background:var(--prt);border-radius:3px;padding:1px 8px}
.rc.act::before{background:var(--pr);box-shadow:0 0 0 3px var(--prt2)}.rc em{font-style:normal;font-size:11.5px;color:var(--pr);display:block;margin-bottom:1px}.lk2{color:var(--pr)!important}
.uc{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-size:13.5px}.uc b{font-weight:480}.uc a{color:var(--mut)}
.dz{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--line);margin-top:10px;padding:14px 0 0 0}.dz b{display:block;font-size:15px;font-weight:480}.dz span{display:block;font-size:13px;color:var(--mut);margin-top:2px}
.dzb{height:36px;display:flex;align-items:center;gap:8px;padding:0 16px;border:1px solid #E6C3B3;border-radius:3px;color:var(--hi);font-size:14px;white-space:nowrap}.dzb .i14{width:15px;height:15px}
.hdp{padding:22px 40px 22px 56px;flex:none;border-bottom:1px solid var(--line)}.hdp h1{font-size:44px}.hdp p{font-size:15px;color:var(--mut);margin-top:8px}
'''
    A=[('shield','Data Protection Agent','Active, v2.1.0, Jordan Diaz','Healthy',True,''),('search','Investigation Agent','Active, v2.0.3, Jordan Diaz','Healthy',False,''),('radar','Threat and Exposure Agent','Active, v1.4.2, Priya Shah','Healthy',False,''),('wrench','Remediation Agent','Active, v2.3.1, Jordan Diaz','Warning',False,'Verification failed on 1 action'),('files','Evidence Collection Agent','Active, v1.8.0, Alex Kim','Healthy',False,''),('user-round','Identity and Asset Agent','Active, v2.0.1, Jordan Diaz','Healthy',False,'')]
    lst=''.join(f'<div class="al{" on" if on else ""}"><div class="ag2">{ico(ic)}</div><div><b>{n}</b><span>{m}</span>{("<span class=wn>"+wn+"</span>") if wn else ""}</div><span class="hc{" w" if h=="Warning" else ""}">{h}</span></div>' for ic,n,m,h,on,wn in A)
    pill=lambda k:{'a':f'<span class="pill2 a">{ico("circle-check","i14")}Allowed</span>','b':f'<span class="pill2 b">{ico("ban","i14")}Blocked</span>','r':f'<span class="pill2 ap">{ico("shield-alert","i14")}Approval required</span>'}[k]
    def bar(c):
        a_,p_,b_=c
        return '<div class="sg">'+'<i style="background:#3E8A5F"></i>'*a_+'<i style="background:#E3B15A"></i>'*p_+'<i style="background:#B3AEA5"></i>'*b_+'</div>'
    def cnt(rows): return (sum(1 for r in rows if r[1]=='a'),sum(1 for r in rows if r[1]=='r'),sum(1 for r in rows if r[1]=='b'))
    DEST=[('Internal destinations','a','AWS and Azure services in scope',''),('Authorized partners','r','SIEM, ticketing systems','ed'),('Unauthorized destinations','b','All external destinations blocked','')]
    ACT=[('Quarantine transfer','a','Under existing policy',''),('Isolate production workload','r','Requires human approval',''),('Delete protected data','b','Not permitted',''),('Create security findings','a','Create findings and evidence','')]
    assert cnt(DEST)==(1,1,1) and cnt(ACT)==(2,1,1)
    SEC=[('server','Environment scope','Where the agent is active and can act',(2,0,1),None,''),
         ('database','Data access','Data categories it can read and analyze',(2,0,2),None,''),
         ('wrench','Allowed tools','Tools and services it can use',(3,0,1),None,''),
         ('arrow-up-right','Destination controls','Where it can send data or connect',cnt(DEST),DEST,''),
         ('settings','Action permissions','Actions it can take for the organization',cnt(ACT),ACT,''),
         ('user-round','Approval thresholds','When human approval is required',(1,2,0),None,'ed'),
         ('shield','Fail closed','What happens outside policy or on error',(0,0,2),None,'')]
    def sec(ic,t,d,c,rows,ed):
        tag='<span class="edt">Edited</span>' if ed else ''
        o=f'<div class="ps"><div class="ph">{ico("chevron-down" if rows else "chevron-right","i14 ch2")}<div class="gi">{ico(ic)}</div><div><b>{t}{tag}</b><span class="d">{d}</span></div><span class="sgl" style="margin-left:auto"><b>{c[0]}</b> of {sum(c)} allowed</span>{bar(c)}'+(f'<div class="eb">Edit</div>' if t=='Destination controls' else '<div class="eb0"></div>')+'</div>'
        if rows: o+=''.join(f'<div class="pr1"><span>{n}{"<span class=edt>Edited</span>" if e else ""}</span>{pill(k)}<span class="d2">{dd}</span>{ico("chevron-right","i14")}</div>' for n,k,dd,e in rows)
        return o+'</div>'
    S=[sec(*x) for x in SEC]
    eff=lambda lbl,i:f'<div><span>{lbl}</span>{bar(SEC[i][3])}<b>{SEC[i][3][0]} of {sum(SEC[i][3])} allowed</b></div>'
    center=f'''<div class="cc"><div class="ah"><div class="big">{ico("shield")}</div><div><h2>Data Protection Agent<span class="st">Active</span></h2><div class="mt2"><span>Owner<b>Jordan Diaz</b></span><span>Version<b>v2.1.0</b></span><span>Health<b class="hc2">Healthy</b></span><span>Conflicts<b class="hc2">{ico("circle-check","i14")}None</b></span></div></div><div class="btns"><div class="nb">Edit policy</div><div class="k">{ico("ellipsis")}</div></div></div>
<div class="lgd"><span>7 policy sections</span><div><u style="background:#3E8A5F"></u>Allowed<u style="background:#E3B15A"></u>Approval required<u style="background:#8C8880"></u>Blocked</div></div>{''.join(S)}
<div class="dz"><div><b>Emergency disable</b><span>Stops this agent immediately and revokes its access</span></div><div class="dzb">{ico("ban","i14")}Disable agent</div></div></div>'''
    rail=f'''<aside class="rl2"><div class="sec"><div class="sh">Effective access<span class="ut">Includes 2 unsaved changes</span></div><div class="ea2">{eff("Environments",0)}{eff("Data access",1)}{eff("Tools",2)}{eff("Destinations",3)}{eff("Actions",4)}</div><div class="cl"><div>{ico("shield-alert","i14")}<span>Needs approval<b>Isolate production workload</b></span></div><div>{ico("ban","i14")}<span>Prohibited<b>Delete protected data</b></span></div></div></div>
<div class="sec" style="border-top:1px solid var(--line)"><div class="sh">Policy history<a>View all{ico("chevron-right","i14")}</a></div><div class="rc act"><em>Applied in incident</em><b>Blocked outbound transfer</b><span class="lk2">INC-2026-0837, Oct 26, 02:22 UTC</span></div><div class="rc"><b>Environment scope updated</b><span>Oct 22, 10:22 UTC, Jordan Diaz</span></div><div class="rc"><b>External destinations blocked</b><span>Oct 20, 09:18 UTC, Jordan Diaz</span></div><div class="rc"><b>Approval rule updated</b><span>Oct 19, 08:41 UTC, Jordan Diaz</span></div></div>
<div class="ctab"><div class="uc"><b>2 unsaved changes</b><a>Discard</a></div><div class="b2">Save policy changes</div></div></aside>'''
    sb=f'''<aside class="sb"><div class="lg"><div><img class="logo" style="height:31px;display:block" src="{LOGO}"></div>{ico("chevrons-left","i c")}</div>
<div class="nv"><div class="it">{ico("inbox")}Inbox</div><div class="it">{ico("shield-alert")}Security</div><div class="it par">{ico("bot")}Agents</div><div class="grp"><div class="sub">All agents</div><div class="sub on">Policies and permissions</div></div><div class="it">{ico("scroll-text")}Policies</div><div class="it">{ico("square-check")}Approvals<em>3</em></div><div class="it">{ico("clipboard-list")}Audit log</div><div class="it">{ico("plug")}Integrations</div></div>
<div class="sp"></div><div class="nv"><div class="it">{ico("settings")}Settings</div><div class="it">{ico("circle-help")}Help</div></div><div class="me"><div class="av" style="background-image:url({ME})"></div><div><b>Katerina B.</b><span>Brightwell, Security</span></div></div></aside>'''
    top=f'''<div class="top"><div class="bc"><span class="lk">Agents</span>{ico("chevron-right","i14")}<b>Policies and permissions</b></div><div class="tr"><div class="fld"><span>Search incidents, identities, assets</span>{ico("search","i14")}</div><span class="bell">{ico("bell")}</span><div class="me2"><div class="av" style="background-image:url({ME})"></div>{ico("chevron-down","i14")}</div></div></div>'''
    main=f'''<div class="main">{top}<div class="hdp"><h1>Agent policies and permissions</h1><p>Control what each specialist agent can access, what actions it can take, and when approval is required</p></div><div class="pl"><div class="lc"><div class="lch"><h3>Agents<small>6</small></h3><div class="fld"><span>Search agents</span>{ico("search","i14")}</div><div class="fld"><span>Owned by me</span>{ico("chevron-down","i14")}</div></div>{lst}</div>{center}{rail}</div></div>'''
    return f'<!doctype html><meta charset=utf-8><style>{css}{extra}</style><body><div class="app">{sb}{main}</div></body>'
import base64
LOGO='data:image/png;base64,'+base64.b64encode(open(S/'logo'/'logo_full_ink.png','rb').read()).decode()
JORDAN='data:image/jpeg;base64,'+b64(A/'jordan.jpg')
def AUD(css,CW,CH):
    extra='''
.main{background:#fff}
.it.on{background:var(--side2);color:var(--ink)}
.zat{height:60px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 40px 0 56px;border-bottom:1px solid var(--line)}
.zinc{display:flex;align-items:center;gap:12px;font-size:14px;color:var(--mut);height:34px;padding:0 6px 0 0}
.zinc .i14{color:var(--hi);width:17px;height:17px}.zinc b{color:var(--ink);font-weight:520}.zinc .ztt{color:var(--tx)}
.zsv{font-size:12.5px;border-radius:3px;padding:2px 9px;background:var(--hit);color:var(--hi);font-weight:500}
.zahd{padding:24px 32px 0 56px;display:flex;justify-content:space-between;align-items:flex-start}
.zahd h1{font-size:44px}.zahd p{font-size:15px;color:var(--mut);margin-top:6px;white-space:nowrap}
.zahd .zbs{display:flex;gap:10px;margin-top:4px}
.zbo,.zbp{height:40px;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 16px;font-size:14.5px;white-space:nowrap}.zbo{border:1px solid #D8D4CB;color:var(--ink)}.zbp{background:var(--pr);color:#fff;font-weight:520}.zbo .i14,.zbp .i14{width:16px;height:16px}
.zfl{display:flex;gap:6px;align-items:center;padding:20px 32px 16px 56px}
.zsf{width:164px;white-space:nowrap;height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 12px;font-size:14px;color:var(--mut)}.zsf .i14{color:var(--mut)}
.zfc{height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:7px;padding:0 10px 0 12px;font-size:13.5px;color:var(--tx);white-space:nowrap}.zfc .i14{color:var(--mut);width:14px;height:14px}.zfc.zdt{color:var(--ink)}.zfc.zdt .i14:first-child{width:15px;height:15px}
.ztbl{flex:1;min-height:0;display:flex;flex-direction:column;padding:0 32px 0 56px}
.zgh,.zar{display:grid;grid-template-columns:84px 236px 1fr 118px 98px;column-gap:14px;align-items:center}
.zgh{height:36px;font-size:12.5px;color:var(--mut);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.zdr{height:34px;display:flex;align-items:center;justify-content:space-between;font-size:13px;color:var(--mut);background:#FAF9F7;border-bottom:1px solid var(--line);padding:0 0}.zdr b{font-weight:520;color:var(--ink);font-size:13.5px}
.zar{height:54px;border-bottom:1px solid var(--line);position:relative;font-size:14.5px}
.zar.on{background:var(--prt)}.zar.on{margin:0 -32px 0 -56px;padding:0 32px 0 56px}.zar.on::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--pr)}
.zar .ztm{color:var(--tx);font-size:14px}
.zac{display:flex;align-items:center;gap:11px;min-width:0}.zac .zgv{width:32px;height:32px;border-radius:50%;border:1px solid var(--line);background:#fff;display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none;background-size:cover;background-position:center}.zac .zgv .i{width:16px;height:16px}
.zac b,.zev b{display:block;font-weight:450;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.zac span,.zev span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zev{min-width:0}
.zpd{font-size:14px;color:var(--tx);white-space:nowrap}.zpd.zna{color:var(--mut2)}.zpd i{font-style:normal;color:var(--mut)}
.zoc{font-size:12.5px;border-radius:3px;padding:2px 9px;width:max-content;white-space:nowrap}
.zoc.n{background:#EFEDE8;color:#5E5B55}.zoc.g{background:#EAF3EE;color:var(--ok)}.zoc.a{background:#FBF1D9;color:#8A5A12}.zoc.rd{background:var(--hit);color:#B03A08}
.ztf{height:46px;margin-top:auto;display:flex;align-items:center;justify-content:space-between;font-size:13.5px;color:var(--mut)}.ztf .zpg{display:flex;gap:8px;align-items:center}.ztf .zpb{width:30px;height:30px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--tx)}.ztf .zpb.d{color:var(--mut2)}
.zdt2{width:400px;flex:none;border-left:1px solid var(--line);display:flex;flex-direction:column;padding:22px 28px 22px}
.zdh{display:flex;justify-content:space-between;align-items:center}.zdh h3{font-size:20px;font-weight:480;letter-spacing:-.02em}.zdh .zx{width:32px;height:32px;display:flex;align-items:center;justify-content:center;color:var(--tx);border:1px solid var(--line);border-radius:3px}
.zst2{margin-top:14px;padding-bottom:14px;border-bottom:1px solid var(--line)}.zst2 .zr1{display:flex;align-items:center;gap:12px;font-size:14px;color:var(--tx)}.zst2 .zr2{display:flex;align-items:center;gap:8px;margin-top:9px;font-size:13px;color:var(--mut)}
.zcp{width:15px;height:15px;color:var(--mut2);flex:none}
.zg2{display:grid;grid-template-columns:1fr 1fr;column-gap:20px;row-gap:14px;padding:14px 0;border-bottom:1px solid var(--line)}
.zfv label{display:block;font-size:12.5px;color:var(--mut);margin-bottom:4px}.zfv b{display:block;font-weight:450;font-size:14px;line-height:1.3;color:var(--ink)}.zfv span{white-space:nowrap;display:flex;align-items:center;gap:6px;font-size:12.5px;color:var(--mut);margin-top:2px}
.zfv.zw>span{white-space:normal;display:block}.zfv.zw{grid-column:1/3}
.zfv .zln{color:var(--pr);border-bottom:1px solid var(--prt2);font-size:14px;font-weight:480;display:inline}
.zfv .zac b{font-size:14px}
.zsx{display:flex;flex-direction:column;border-bottom:1px solid var(--line)}
.zsr{display:flex;align-items:center;gap:12px;height:40px;font-size:13.5px}.zsr+.zsr{border-top:1px solid var(--line)}.zsr label{width:96px;color:var(--mut);font-size:12.5px;flex:none}.zsr span{flex:1;color:var(--ink);white-space:nowrap}.zsr .i14{color:var(--mut2)}
.zev2{padding:12px 0 6px;border-bottom:1px solid var(--line)}.zev2 h4{font-size:12.5px;font-weight:450;color:var(--mut);margin-bottom:6px}
.zer{display:flex;align-items:center;gap:10px;height:30px;font-size:13.5px;color:var(--tx)}.zer .i14{color:var(--mut)}.zer span{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.zer small{color:var(--mut);font-size:12.5px}
.zig{display:flex;align-items:flex-start;gap:11px;padding:12px 0 0}.zig .i{width:20px;height:20px;color:var(--ok);margin-top:1px}.zig b{display:block;font-weight:450;font-size:14px}.zig span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px}
.zcr{display:flex;align-items:center;gap:10px;padding:12px 0 0;font-size:13px;color:var(--mut)}.zcr b{font-weight:450;color:var(--tx);margin-left:2px}.zcr .zcp{margin-left:auto}
.zvb{margin-top:auto;height:42px;border:1px solid #CFCBC2;border-radius:3px;display:flex;align-items:center;justify-content:center;gap:9px;font-size:14.5px}
.zvb .i14{width:16px;height:16px}

.zsr2{width:420px;height:36px;justify-content:flex-start!important;gap:10px}
.zbn{height:46px;flex:none;display:flex;align-items:center;gap:14px;padding:0 40px 0 56px;background:var(--hit);border-bottom:1px solid #F3D3C2;color:var(--hi)}
.zbn>.i{width:20px;height:20px}.zbt{display:flex;align-items:center;gap:12px;font-size:14px;color:var(--tx);white-space:nowrap}.zbt b{font-weight:520;color:#8F3305}.zbi{font-weight:520;color:var(--ink)}.zsv{font-size:12.5px;background:#fff;color:var(--hi);border:1px solid #F0C3AC;border-radius:3px;padding:1px 9px;font-weight:500}.zst{color:#8A5A42}
.zbb{margin-left:auto;height:30px;border-radius:3px;background:#fff;border:1px solid #EDB9A0;color:#8F3305;display:flex;align-items:center;gap:8px;padding:0 13px;font-size:13.5px;font-weight:480;white-space:nowrap}.zbb .i14{width:15px;height:15px}
.zdt2{padding:24px 28px 22px}.zsx{flex:1;min-height:0;overflow:hidden;position:relative;margin:0 -28px;padding:0 28px;display:block}.zsx::after{content:"";position:absolute;left:0;right:0;bottom:0;height:56px;background:linear-gradient(rgba(255,255,255,0),#fff)}.zsb{position:absolute;right:8px;top:10px;width:4px;height:250px;border-radius:2px;background:#D8D4CB}.zsx .zig{padding:24px 0 80px}
.zvd{margin-top:20px;border:1px solid var(--line);border-radius:3px;padding:18px 18px 18px;display:grid;grid-template-columns:40px 1fr;column-gap:12px;row-gap:14px;align-items:center;background:#FAF9F7}
.zvg{width:40px;height:40px;border-radius:50%;background:#EFEDE8;display:flex;align-items:center;justify-content:center;color:#4F4C47}.zvg .i{width:20px;height:20px}
.zvd b{display:block;font-size:19px;font-weight:480;letter-spacing:-.02em}.zvd span{display:block;font-size:13px;color:var(--mut);margin-top:1px}
.zvd p{grid-column:1/3;font-size:14px;line-height:1.45;color:var(--tx)}.zvd u{text-decoration:none;color:var(--ink);font-weight:480}
.zsc{padding:24px 0 0}.zinl label{display:inline;margin-right:8px}.zinl b{display:inline}.zsc h4{font-size:12px;font-weight:520;color:var(--mut);letter-spacing:.01em;margin-bottom:12px;display:flex;align-items:center;gap:10px}.zsc h4::after{content:"";flex:1;height:1px;background:var(--line)}
.zg2{padding:0;border:0;display:grid;grid-template-columns:1fr 1fr;column-gap:20px;row-gap:18px}
.zba{display:flex;align-items:stretch;gap:10px}.zba>div{flex:1;border:1px solid var(--line);border-radius:3px;padding:12px 14px}.zba .i14{align-self:center;color:var(--mut2)}.zba label{display:block;font-size:12px;color:var(--mut)}.zba b{display:block;font-weight:450;font-size:13.5px;margin-top:1px}.zba .ok{background:#F3F8F5;border-color:#D5E7DC}.zba .ok b{color:#25623F}
.zer{height:34px}
.zids{display:grid;grid-template-columns:1fr 1fr;gap:10px 10px}.zid{display:flex;align-items:center;gap:7px;height:36px;border:1px solid var(--line);border-radius:3px;padding:0 9px;font-size:12.5px;color:var(--mut);min-width:0}.zid b{font-weight:450;color:var(--tx);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.zid .zcp{margin-left:auto}
.zfo{margin-top:0;padding-top:16px;border-top:1px solid var(--line)}.zfo .zig{padding:0 0 10px}
.zvb{margin-top:0}
'''
    CSS2='''
.zdn{flex:none;padding:6px 32px 30px 56px}
.zdh2{display:flex;align-items:baseline;justify-content:space-between}
.zdh2 b{font-size:15px;font-weight:540;color:var(--ink)}.zdh2 span.s{font-size:13px;color:var(--mut);margin-left:10px}
.zdl{display:flex;gap:16px;font-size:12.5px;color:var(--mut)}.zdl span{display:flex;align-items:center;gap:7px}.zdl i{display:block;width:14px;height:6px;border-radius:3px}
.zdc{position:relative;height:108px;margin-top:18px}
.zdp{position:absolute;left:0;right:0;top:0;height:96px;display:flex;align-items:flex-end}
.zdg{position:absolute;left:0;right:0;height:1px;background:var(--line)}
.zdg span{position:absolute;left:0;top:-15px;font-size:11.5px;color:var(--mut2)}
.zdb{position:absolute;top:0;bottom:0;background:var(--hit);opacity:.6;border-radius:2px}
.zdk{flex:1;display:flex;flex-direction:column-reverse;align-items:stretch;margin:0 2px;position:relative}
.zdk i{display:block;border-top:1px solid #fff}.zdk i:first-child{border-top:0}.zdk i:last-child{border-radius:2px 2px 0 0}
.zdm{position:absolute;top:0;bottom:0;width:0;border-left:1.5px dashed var(--pr)}
.zdt3{position:absolute;font-size:12px;white-space:nowrap}
.zdx{position:absolute;top:106px;font-size:11.5px;color:var(--mut2);transform:translateX(-50%)}
.zrs{flex:1;min-height:0;overflow:hidden;position:relative}
.zrs::after{content:"";position:absolute;left:0;right:0;bottom:0;height:50px;background:linear-gradient(rgba(255,255,255,0),#fff);pointer-events:none}
'''
    G=lambda i:f'<div class="zgv">{ico(i)}</div>'
    def actor(g,n,t,photo=None):
        gv=f'<div class="zgv" style="background-image:url({photo})"></div>' if photo else G(g)
        return f'<div class="zac">{gv}<div><b>{n}</b><span>{t}</span></div></div>'
    R=[('02:41:07','shield','Remediation Agent','AI agent','Rotation verification failed','prod/ml-pipeline-key','Allow','v2.3','Failed','rd',None,'wrench'),
       ('02:38:20','wrench','Remediation Agent','AI agent','Created Linear tickets','Linear, project Security','Allow','v2.3','Executed','g',None,'wrench'),
       ('02:34:45','wrench','Remediation Agent','AI agent','Suspended user account','maya.chen@brightwell.io','Approval','v2.3','Executed','g',None,'wrench'),
       ('02:31:09','wrench','Remediation Agent','AI agent','Isolated AWS workload','prod-ml-workload','Allow','v2.3','Executed','g',None,'wrench'),
       ('02:29:30','','Jordan Diaz','Security admin','Approved remediation plan','Version 2, 6 actions','Approval','v2.3','Approved','g',JORDAN,''),
       ('02:27:14','','Jordan Diaz','Security admin','Edited remediation plan','Version 2, rotation plus restarts','Allow','v1.8','Updated','n',JORDAN,''),
       ('02:24:30','radar','Threat and Exposure Agent','AI agent','Correlated evidence','14 signals, one identity','','','Completed','n',None,'radar'),
       ('02:23:05','user-round','Identity and Asset Agent','AI agent','Flagged device not in MDM','Maya Chen, new device','Alert','v2.0','Detected','a',None,'user-round'),
       ('02:22:41','shield','Data Protection Agent','AI agent','Quarantined file','customer_data_2026.csv','Allow','v2.1','Executed','g',None,'shield'),
       ('02:22:36','shield','Data Protection Agent','AI agent','Blocked outbound transfer','45.133.194.17','Deny','v2.1','Blocked','n',None,'shield'),
       ('02:18:12','cloud','AWS CloudTrail','External system','Restricted file opened','customer_data_2026.csv, S3','Alert','v2.1','Detected','a',None,'cloud'),
       ('02:14:03','key-round','Microsoft Entra ID','External system','Unusual sign-in from Singapore','maya.chen','Alert','v2.0','Detected','a',None,'key-round')]
    assert len(R)==12 and all(R[i][0]>R[i+1][0] for i in range(11))
    rows=''
    for t,_,n,ty,ev,tg,dec,ver,oc,ok,ph,gi in R:
        sel=' on' if t=='02:22:36' else ''
        pd=f'<div class="zpd">{dec}, <i>{ver}</i></div>' if dec else '<div class="zpd zna">N/A</div>'
        rows+=f'<div class="zar{sel}"><div class="ztm">{t}</div>{actor(gi,n,ty,ph)}<div class="zev"><b>{ev}</b><span>{tg}</span></div>{pd}<div><span class="zoc {ok}">{oc}</span></div></div>'
    base=[]
    for i in range(26):
        base.append([2+(1 if i%3==0 else 0),1 if i%4==1 else 0,1 if i%5==2 else 0,0,0])
    tot=sum(sum(x) for x in base); k=0
    while tot<91: base[k%26][0]+=1; tot+=1; k+=1
    while tot>91: base[k%26][0]-=1; tot-=1; k+=1
    # order in tuple: executed, other, detected, blocked, failed
    burst=[(4,2,2,0,0),(5,3,5,1,0),(8,7,9,7,0),(8,6,5,4,1),(8,5,3,3,0),(7,4,2,2,1),(4,2,1,2,2)]
    B=[tuple(x) for x in base]+burst
    assert sum(sum(x) for x in B)==214
    COL=['#A9CDB8','#D5D1C8','#E5B65C','#6B1D4A','#D9480F']
    SC=2.35
    cols=''
    for x in B:
        cols+='<div class="zdk">'+''.join(f'<i style="height:{n*SC:.1f}px;background:{COL[j]}"></i>' for j,n in enumerate(x) if n)+'</div>'
    cols+='<div class="zdk"></div>'*3
    pct=lambda m:m/180*100
    ticks=''.join(f'<div class="zdx" style="left:{pct(m)}%;'+('transform:none' if m==0 else 'transform:translateX(-100%)' if m==180 else '')+f'">{m//60:02d}:{m%60:02d}</div>' for m in range(0,181,30))
    grid=''.join(f'<div class="zdg" style="bottom:{n*SC}px"><span>{n}</span></div>' for n in (10,20,30))
    mk=pct(142.6)
    dens=f'<div class="zdn"><div class="zdh2"><div><b>Event activity</b><span class="s">Oct 26, 00:00 to 02:42 UTC, 5 minute intervals</span></div><div class="zdl"><span><i style="background:{COL[0]}"></i>Executed</span><span><i style="background:{COL[2]}"></i>Detected</span><span><i style="background:{COL[3]}"></i>Blocked</span><span><i style="background:{COL[4]}"></i>Failed</span><span><i style="background:{COL[1]}"></i>Other</span></div></div><div class="zdc"><div class="zdp" style="z-index:0"><div class="zdb" style="left:{pct(130)}%;width:{pct(162)-pct(130)}%"></div>{grid}</div><div class="zdp" style="z-index:1">{cols}</div><div class="zdm" style="left:{mk}%;z-index:2"></div><div class="zdt3" style="right:calc({100-mk}% + 14px);top:-4px;color:var(--pr);font-weight:520">Blocked outbound transfer, 02:22</div><div class="zdt3" style="right:calc({100-pct(162)}%);top:-4px;color:#A93B08">INC-2026-0837</div>{ticks}<div class="zdx" style="left:{pct(162)}%;color:var(--ink);font-weight:520;top:100px;background:#fff;padding:0 3px"></div></div></div>'
    top=f'<div class="zat"><div class="fld zsr2">{ico("search","i14")}<span>Search incidents, assets, identities</span></div><div class="tr"><span class="bell">{ico("bell")}</span><div class="me2"><div class="av" style="background-image:url({ME})"></div>{ico("chevron-down","i14")}</div></div></div>'
    banner=f'<div class="zbn">{ico("shield-alert")}<div class="zbt"><b>Active incident</b><span class="zbi">INC-2026-0837</span><span>Sensitive data exfiltration attempt</span><span class="zsv">High</span><span class="zst">Investigating, last updated 3 min ago</span></div><div class="zbb">Open incident{ico("arrow-right","i14")}</div></div>'
    chips=''.join(f'<div class="zfc">{x}{ico("chevron-down","i14")}</div>' for x in ('Actor','Event type','Risk','Outcome','Environment'))
    center=f'''<div class="zctr"><div class="zahd"><div><h1>Audit log</h1><p>Immutable record of activity across agents, users and systems</p></div><div class="zbs"><div class="zbo">{ico("bookmark","i14")}Save view</div><div class="zbp">{ico("download","i14")}Export evidence</div></div></div>
<div class="zfl"><div class="zsf">{ico("search","i14")}Search audit log</div><div class="zfc zdt">{ico("calendar","i14")}Oct 26, 2026{ico("chevron-down","i14")}</div>{chips}</div>
{dens}<div class="ztbl"><div class="zgh"><span>Time (UTC)</span><span>Actor</span><span>Event</span><span>Policy decision</span><span>Outcome</span></div><div class="zdr"><b>Monday, Oct 26, 2026</b><span>214 events</span></div><div class="zrs">{rows}</div>
<div class="ztf"><span>Showing 12 of 214 events</span><div class="zpg"><span>Page 1 of 18</span><div class="zpb d">{ico("chevron-left","i14")}</div><div class="zpb">{ico("chevron-right","i14")}</div></div></div></div></div>'''
    cpi=ico("copy","zcp")
    def idc(k,v): return f'<div class="zid"><span>{k}</span><b>{v}</b>{cpi}</div>'
    rail=f'''<aside class="zdt2"><div class="zdh"><h3>Event details</h3><div class="zx">{ico("x","i14")}</div></div>
<div class="zsx"><div class="zvd"><div class="zvg">{ico("shield-ban")}</div><div><b>Blocked</b><span>Oct 26, 2026, 02:22:36 UTC</span></div><p><u>Data Protection Agent</u> blocked the upload of <u>customer_data_2026.csv</u> to <u>45.133.194.17</u>.</p></div>
<div class="zsc"><h4>What happened</h4><div class="zg2"><div class="zfv"><label>Actor</label>{actor("shield","Data Protection Agent","AI agent, v2.1.0")}</div><div class="zfv"><label>Requested action</label><b>Upload object to external destination</b></div>
<div class="zfv zw"><label>Target</label><b>45.133.194.17</b><span>customer_data_2026.csv, 48 MB, Restricted (customer data)</span></div></div></div>
<div class="zsc"><h4>Decision</h4><div class="zg2"><div class="zfv"><label>Policy snapshot</label><b>Destinations v2.1</b><span><a class="zln" style="font-size:13px">View policy rules</a></span></div><div class="zfv"><label>Final decision</label><b>Deny, v2.1</b><span>Blocked by policy</span></div>
<div class="zfv zw zinl"><label>Approval record</label><b>Not required, automatic</b></div></div></div>
<div class="zsc"><h4>State change</h4><div class="zba"><div><label>Before</label><b>Staged for upload</b></div>{ico("arrow-right","i14")}<div class="ok"><label>After</label><b>Denied, no data left</b></div></div></div>
<div class="zsc"><h4>Context</h4><div class="zg2"><div class="zfv zw"><b><span class="zln">INC-2026-0837</span>&nbsp;&nbsp;Sensitive data exfiltration attempt</b><span>Risk High, Status Investigating</span></div></div></div>
<div class="zsc"><h4>Evidence references</h4><div class="zer">{ico("cloud","i14")}<span>CloudTrail event 9c1b2d3e-4f5a</span>{cpi}</div><div class="zer">{ico("file-text","i14")}<span>S3 access log, athena://logs/2026/10/26</span>{cpi}</div><div class="zer">{ico("shield","i14")}<span>Agent analysis, s3://audit/agents/dp/evt-7f3e</span>{cpi}</div></div>
<div class="zsc"><h4>Identifiers</h4><div class="zids">{idc("Event","evt-7f3e2c9a")}{idc("Source","9c1b2d3e")}{idc("Policy","pol-3e6f2a9b")}{idc("Corr. ID","2d8a1f4e")}</div></div>
<div class="zig">{ico("shield-check")}<div><b>Integrity verified, tamper-evident</b><span>Audit ledger, block #4829173</span></div></div><div class="zsb"></div></div><div class="zfo"><div class="zvb">View related events{ico("arrow-right","i14")}</div></div></aside>'''
    sb=f'''<aside class="sb"><div class="lg"><div><img class="logo" style="height:31px;display:block" src="{LOGO}"></div>{ico("chevrons-left","i c")}</div>
<div class="nv"><div class="it">{ico("inbox")}Inbox</div><div class="it">{ico("shield-alert")}Security</div><div class="it">{ico("bot")}Agents</div><div class="it">{ico("scroll-text")}Policies</div><div class="it">{ico("square-check")}Approvals<em>3</em></div><div class="it on">{ico("clipboard-list")}Audit log</div><div class="it">{ico("plug")}Integrations</div></div>
<div class="sp"></div><div class="nv"><div class="it">{ico("settings")}Settings</div><div class="it">{ico("circle-help")}Help</div></div><div class="me"><div class="av" style="background-image:url({ME})"></div><div><b>Katerina B.</b><span>Brightwell, Security</span></div></div></aside>'''
    return f'<!doctype html><meta charset=utf-8><style>{css}{extra}{CSS2}.zctr{{flex:1;min-width:0;display:flex;flex-direction:column}}</style><body><div class="app">{sb}<div class="main">{top}{banner}<div style="display:flex;flex:1;min-height:0">{center}{rail}</div></div></div></body>'

import random,math
def _chart(W,H):
    rnd=random.Random(11); N=96
    ev=[(418,34),(808,29),(1248,39),(1420,63)]
    det=[]
    for i in range(N+1):
        m=i*15
        base=10+4*math.sin(m/190)+3*math.sin(m/53)+rnd.uniform(-2.2,2.2)
        for em,h in ev:
            base+=(h-10)*math.exp(-((m-em)/26)**2)
        det.append(max(3,base))
    blk=[max(1.5,d*0.42+rnd.uniform(-1,1)) for d in det]
    L,Rr,T,B=34,6,18,H-34; iw=W-L-Rr; ih=B-T
    X=lambda m:L+iw*m/1440; Y=lambda v:B-ih*v/80
    def path(vals):
        pts=[(X(i*15),Y(v)) for i,v in enumerate(vals)]
        d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
        for i in range(len(pts)-1):
            p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
            c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
            d+=f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
        return d,pts
    dl,dp=path(det); bl,bp=path(blk)
    area=bl+f' L{X(1440):.1f},{B} L{X(0):.1f},{B} Z'
    g=''
    for v in (0,20,40,60,80):
        g+=f'<line x1="{L}" x2="{W-Rr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#ECE9E3" stroke-width="1"/><text x="{L-10}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="12" fill="#A5A199">{v}</text>'
    ticks=[(198,'06:00','Oct 25'),(378,'09:00',''),(558,'12:00',''),(738,'15:00',''),(918,'18:00',''),(1098,'21:00',''),(1278,'00:00','Oct 26'),(1398,'02:00','')]
    for m,a,b in ticks:
        g+=f'<text x="{X(m):.1f}" y="{B+18}" text-anchor="middle" font-size="12" fill="#7A776F">{a}</text>'
        if b: g+=f'<text x="{X(m):.1f}" y="{B+32}" text-anchor="middle" font-size="12" fill="#A5A199">{b}</text>'
    labs={418:('Suspicious login spike','',1),808:('Public storage exposed','INC-2026-0833',1),1248:('Credentials exposed','INC-2026-0836',1),1420:('Data exfiltration attempt','INC-2026-0837',2)}
    mk=''
    for em,h in ev:
        idx=round(em/15); x=X(em); y=dp[idx][1]
        t1,t2,_=labs[em]
        anchor='end' if em>1300 else 'middle'; tx=x+(8 if em>1300 else 0)
        mk+=f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y+6:.1f}" y2="{B}" stroke="#CFCBC2" stroke-dasharray="3 4"/>'
        ty=y-26 if t2 else y-16
        mk+=f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="12.5" fill="#1C1B19" font-weight="500">{t1}</text>'
        if t2: mk+=f'<text x="{tx:.1f}" y="{ty+15:.1f}" text-anchor="{anchor}" font-size="12" fill="#7A776F">{t2}</text>'
        big=em==1420
        mk+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{8 if big else 5.5}" fill="{"#EAD6E1" if big else "#fff"}" opacity="{1 if big else 0}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if big else 4.5}" fill="#6B1D4A" stroke="#fff" stroke-width="2"/>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="SG, sans-serif"><defs><linearGradient id="ba" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6B1D4A" stop-opacity=".16"/><stop offset="1" stop-color="#6B1D4A" stop-opacity=".02"/></linearGradient></defs>{g}<path d="{area}" fill="url(#ba)"/><path d="{bl}" fill="none" stroke="#C7A3B8" stroke-width="1.5"/><path d="{dl}" fill="none" stroke="#1C1B19" stroke-width="1.8" stroke-linejoin="round"/>{mk}</svg>'
def DASH(css,CW,CH):
    extra='''
.it.on{background:var(--side2);color:var(--ink)}
.yt{height:60px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 40px 0 56px;border-bottom:1px solid var(--line)}
.ysr{width:420px;height:36px;justify-content:flex-start!important;gap:10px}
.yhd{display:flex;justify-content:space-between;align-items:center;padding:20px 40px 0 56px}.yh1{display:flex;align-items:center;gap:26px}.yup{font-size:13.5px;color:var(--mut)}
.yhd h1{font-size:40px}
.ysc{display:flex;align-items:center;gap:16px;margin-top:10px;font-size:14px;color:var(--mut)}
.ych{height:34px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 11px 0 12px;color:var(--ink);font-size:14px}.ych .i14{color:var(--mut);width:15px;height:15px}
.ybs{display:flex;gap:10px;align-items:center}.ybo,.ybp{height:40px;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 16px;font-size:14.5px;white-space:nowrap}.ybo{border:1px solid #D8D4CB;color:var(--ink)}.ybp{background:var(--pr);color:#fff;font-weight:520}.ybo .i14,.ybp .i14{width:16px;height:16px}
.ybody{flex:1;min-height:0;display:flex;flex-direction:column;padding:18px 40px 0 56px;gap:16px;padding-bottom:20px}
.ykp{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:4px;flex:none}
.yk{display:flex;align-items:center;gap:14px;padding:16px 18px;position:relative}.yk+.yk{border-left:1px solid var(--line)}
.yk .yg{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx);flex:none}.yk .yg .i{width:19px;height:19px}
.yk label{display:block;font-size:13px;color:var(--mut)}.yk b{display:block;font-size:30px;font-weight:420;letter-spacing:-.03em;line-height:1.1;margin-top:1px}.yk small{display:block;font-size:12.5px;color:var(--mut);margin-top:2px;white-space:nowrap}
.yk .yc{margin-left:auto;color:var(--mut2)}
.yk.yw .yg{color:#8A5A12;border-color:#EBD6A8;background:#FBF4E3}.yk.yw small{color:#8A5A12}
.ygr{flex:1;min-height:0;display:grid;grid-template-columns:1fr 380px;gap:24px}
.ycol{display:flex;flex-direction:column;gap:16px;min-height:0}
.ycd{border:1px solid var(--line);border-radius:4px;display:flex;flex-direction:column;min-height:0}
.ych2{display:flex;justify-content:space-between;align-items:center;padding:0 20px;height:48px;flex:none}
.ych2 h3{font-size:16.5px;font-weight:480;letter-spacing:-.015em;display:flex;align-items:baseline;gap:10px}.ych2 h3 small{font-size:13px;color:var(--mut);font-weight:400}
.ych2 a{font-size:13px;color:var(--mut);display:flex;align-items:center;gap:4px}
.yth,.yrw{display:grid;grid-template-columns:82px 164px 106px 98px 88px 66px 58px 110px;column-gap:6px;align-items:center;padding:0 18px}
.yth{height:34px;font-size:12.5px;color:var(--mut);border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#FAF9F7}
.yrw{height:52px;border-bottom:1px solid var(--line);font-size:13.5px;color:var(--tx)}.yrw:last-child{border-bottom:0}
.ysv{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:500;border-radius:3px;padding:3px 8px 3px 7px;width:max-content}
.ysv .ybars{display:flex;gap:1.5px;align-items:flex-end;height:11px}.ysv .ybars i{width:2.5px;background:currentColor;opacity:.28}.ysv .ybars i.f{opacity:1}.ysv .ybars i:nth-child(1){height:4px}.ysv .ybars i:nth-child(2){height:6.5px}.ysv .ybars i:nth-child(3){height:9px}.ysv .ybars i:nth-child(4){height:11px}
.ysv.c{background:#F8DDD0;color:#A93B08}.ysv.h{background:#FCEDE5;color:#C0410C}.ysv.m{background:#FBF1D9;color:#8A5A12}
.yin b{display:block;font-weight:480;font-size:13.5px;color:var(--ink);white-space:nowrap}.yin span{display:block;font-size:12.5px;color:var(--mut);line-height:1.25;margin-top:1px}
.yaf{font-size:13px;line-height:1.3}.yaf span{display:block;color:var(--mut);font-size:12.5px}
.yst{display:flex;align-items:center;gap:6px;font-size:13px;white-space:nowrap}.yst .i14{width:14px;height:14px;color:var(--mut)}.yst.ok .i14{color:var(--ok)}
.yct{font-size:13px;line-height:1.3}.yct.nc{color:#B03A08}.yct.mo{color:var(--mut)}
.yac{height:30px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;justify-content:center;gap:8px;padding:0 14px;font-size:13px;color:var(--ink);white-space:nowrap}.yac .i14{width:13px;height:13px}.yac.p{border-color:var(--pr);color:var(--pr);font-weight:500}
.ylg{display:flex;gap:18px;font-size:12.5px;color:var(--mut);align-items:center}.ylg span{display:flex;align-items:center;gap:7px}.ylg u{display:inline-block;width:16px;height:0;border-top:2px solid var(--ink)}.ylg u.b{border-top:2px solid #C7A3B8;height:8px;background:rgba(107,29,74,.12);border-top-width:2px}.ylg i{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--pr)}
.ychart{flex:1;min-height:0;padding:0 20px 14px}
.yds{display:flex;flex-direction:column;flex:1;min-height:0}
.ydc{margin:0 14px;padding:11px 6px 10px 6px;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr;row-gap:2px;flex:1}
.ydc:first-of-type{border-top:0}
.ydr{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut)}.ydr .yrk{display:flex;align-items:center;gap:6px;font-weight:520;font-size:12.5px;border-radius:3px;padding:2px 8px}.ydr .yrk.h{background:#FCEDE5;color:#C0410C}.ydr .yrk.m{background:#FBF1D9;color:#8A5A12}.ydr .yrk .i14{width:13px;height:13px}.ydr .ye{margin-left:auto;display:flex;align-items:center;gap:6px}.ydr .ye .i14{width:13px;height:13px}
.ydc h4{font-size:14.5px;font-weight:480;letter-spacing:-.01em;margin-top:5px}
.ydc p{font-size:12.5px;line-height:1.4;color:var(--mut)}
.ydr .yid{color:var(--tx)}.ydc .ymt>span{white-space:nowrap}.ydc .ymt{font-size:12.5px;color:var(--mut);margin-top:4px;display:flex;align-items:center;justify-content:space-between;gap:8px}.ydc .ymt b{font-weight:450;color:var(--tx)}
.ydb{display:flex;gap:8px}
.ydb .yrv,.ydb .yde{height:28px;width:60px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:13px}.ydb .yrv{background:var(--pr);color:#fff;font-weight:500}.ydb .yde{border:1px solid #D8D4CB;color:var(--ink)}
.yag{display:grid;grid-template-columns:1fr 70px;align-items:center;column-gap:8px}
.yar{display:grid;grid-template-columns:30px minmax(0,1fr) auto;column-gap:10px;align-items:center;padding:0 20px;height:40px;border-top:1px solid var(--line);font-size:13px}
.yar .yav{width:28px;height:28px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--tx)}.yar .yav .i{width:14px;height:14px}
.yar b{display:block;font-weight:450;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.yar span{display:block;font-size:12px;color:var(--mut);white-space:nowrap;margin-top:0;overflow:hidden;text-overflow:ellipsis}
.yar em{font-style:normal;font-size:12px;border-radius:3px;padding:2px 7px;width:max-content;justify-self:end;white-space:nowrap}.yar em.r{}
.yar em.g{background:#EAF3EE;color:var(--ok)}.yar em.w{background:#FBF1D9;color:#8A5A12}
.ycr{position:relative;overflow:hidden}.ycr::after{content:"";position:absolute;left:0;right:0;bottom:0;height:90px;background:linear-gradient(rgba(255,255,255,0),#fff 85%);pointer-events:none}.ycr>.ycd{flex-shrink:0}.ysb{position:absolute;right:-10px;top:0;width:4px;height:300px;border-radius:2px;background:#D8D4CB}.ysm{font-size:12.5px;color:var(--mut)}.yfg{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}.yfg .yfi:nth-child(even){border-left:1px solid var(--line)}.yfg .yfi:nth-child(n+3){border-top:1px solid var(--line)}
.yfo>b{font-size:14.5px;font-weight:480;width:150px}
.yfi{display:flex;align-items:center;gap:11px;padding:0 16px;height:50px}.yfi .yg2{color:var(--tx)}.yfi .yg2 .i{width:20px;height:20px}
.yfi b{display:block;font-size:13.5px;font-weight:480}.yfi span{display:flex;align-items:center;gap:5px;font-size:12.5px;color:var(--mut)}.yfi span .i14{width:14px;height:14px;color:var(--ok)}.yfi span.w{color:#8A5A12}.yfi span.w .i14{color:var(--amb)}
'''
    sev={'c':('Critical',4),'h':('High',3),'m':('Medium',2)}
    def sv(k):
        n,f=sev[k]; return f'<span class="ysv {k}"><span class="ybars">'+''.join(f'<i class="f"></i>' if i<f else '<i></i>' for i in range(4))+f'</span>{n}</span>'
    st=lambda ic,t,ok='':f'<span class="yst {ok}">{ico(ic,"i14")}{t}</span>'
    INC=[('c','INC-2026-0836','Exposed DB credentials','prod-orders-db','AWS, svc-orders',('refresh-cw','Investigating',''),('In progress',''),'P. Shah','14m ago','Investigate',''),
         ('c','INC-2026-0834','Privilege escalation','ops-admin','Azure Entra ID',('clock','Triaging',''),('Not contained','nc'),'A. Kim','42m ago','Investigate',''),
         ('h','INC-2026-0837','Data exfiltration attempt','Maya Chen','prod-ml-workload',('refresh-cw','Investigating',''),('In progress',''),'D. Okafor','2m ago','Review fix','p'),
         ('h','INC-2026-0833','Public storage exposure','brightwell-logs','Azure storage',('circle-check','Confirmed','ok'),('In progress',''),'P. Shah','2h ago','Review fix',''),
         ('m','INC-2026-0831','Suspicious API activity','ci-cd service role','AWS',('refresh-cw','Investigating',''),('Monitoring','mo'),'A. Kim','3h ago','Investigate',''),
         ('m','INC-2026-0829','Policy violation','prod-app cluster','Azure Kubernetes',('clock','Triaging',''),('Not contained','nc'),'J. Diaz','4h ago','Investigate','')]
    assert sum(1 for r in INC if 'in progress' in r[6][0].lower())==3 and sum(1 for r in INC if r[0]=='c')==2
    rows=''
    for s,i,t,a1,a2,inv,ct,ow,lu,na,pc in INC:
        rows+=f'<div class="yrw"><div>{sv(s)}</div><div class="yin"><b>{i}</b><span>{t}</span></div><div class="yaf">{a1}<span>{a2}</span></div>{st(inv[0],inv[1],inv[2])}<div class="yct {ct[1]}">{ct[0]}</div><div>{ow}</div><div style="color:var(--mut)">{lu}</div><div class="yac {pc}">{na}{ico("arrow-right","i14")}</div></div>'
    table=f'<div class="ycd"><div class="ych2"><h3>Incidents requiring attention</h3><a>View all incidents{ico("arrow-right","i14")}</a></div><div class="yth"><span>Severity</span><span>Incident</span><span>Affected</span><span>Investigation</span><span>Containment</span><span>Owner</span><span>Updated</span><span>Next action</span></div>{rows}</div>'
    chart=f'<div class="ycd" style="flex:1"><div class="ych2"><h3>Threat activity<small>Last 24 hours</small></h3><div class="ylg"><span><u></u>Detections</span><span><u class="b"></u>Blocked actions</span><span><i></i>Confirmed incidents</span></div></div><div class="ychart">{_chart(802,292)}</div></div>'
    KP=[('shield-alert','Overall posture','At risk','Deteriorated from Secure, 6h ago','yw'),('triangle-alert','Active incidents','12','2 critical, 4 high, 6 medium',''),('shield-check','Containment in progress','3','2 automated, 1 awaiting approval',''),('user-check','Human decisions required','3','2 high risk, 1 medium risk','')]
    kpi=''.join(f'<div class="yk {w}"><div class="yg">{ico(i)}</div><div><label>{l}</label><b>{v}</b><small>{s}</small></div>{ico("chevron-right","i14 yc")}</div>' for i,l,v,s,w in KP)
    D=[('h','High risk','Expires in 28 min','Retry production secret rotation','Rotate the ml-pipeline key and restart 3 services again.','Remediation Agent','INC-2026-0837'),
       ('h','High risk','Expires in 1 hour','Contain exposed credentials','Revoke svc-orders credentials and rotate them across AWS.','Identity and Asset Agent','INC-2026-0836'),
       ('m','Medium risk','Expires in 3 hours','Block public storage access','Restrict public access and validate with the verification step.','Remediation Agent','INC-2026-0833')]
    dc=''.join(f'<div class="ydc"><div class="ydr"><span class="yrk {k}">{ico("shield-alert" if k=="h" else "shield","i14")}{r}</span><span class="yid">{i}</span><span class="ye">{ico("clock","i14")}{e}</span></div><h4>{t}</h4><p>{d}</p><div class="ymt"><span>{a}</span><div class="ydb"><div class="yde">Deny</div><div class="yrv">Review</div></div></div></div>' for k,r,e,t,d,a,i in D)
    dec=f'<div class="ycd"><div class="ych2"><h3>Needs your decision</h3><a>View all approvals{ico("arrow-right","i14")}</a></div><div class="yds">{dc}</div></div>'
    AG=[('wrench','Remediation Agent','Retrying rotation, INC-2026-0837','Needs approval','w'),('shield','Data Protection Agent','Monitoring egress, INC-2026-0837','Running','g'),('user-round','Identity and Asset Agent','Revoking credentials, INC-2026-0836','Running','g'),('radar','Threat and Exposure Agent','Scoring exposure, INC-2026-0833','Running','g'),('search','Investigation Agent','Reviewing evidence, INC-2026-0836','Running','g')]
    ar=''.join(f'<div class="yar"><div class="yav">{ico(i)}</div><div><b>{n}</b><span>{t}</span></div><em class="{c}">{s}</em></div>' for i,n,t,s,c in AG)
    agents=f'<div class="ycd"><div class="ych2"><h3>Agent operations</h3><a>View all agents{ico("arrow-right","i14")}</a></div>{ar}</div>'
    FO=[('cloud','AWS','Healthy',''),('cloud','Azure','Delayed, 4 min','w'),('database','SIEM','Healthy',''),('key-round','IAM','Healthy',''),('scroll-text','Policy engine','Healthy',''),('shield-check','Audit integrity','Verified','')]
    fo=''.join(f'<div class="yfi"><div class="yg2">{ico(i)}</div><div><b>{n}</b><span class="{w}">{ico("clock" if w else "circle-check","i14")}{s}</span></div></div>' for i,n,s,w in FO)
    ctrl=f'<div class="ycd" style="flex:none"><div class="ych2"><h3>Data and controls</h3><span class="ysm">5 healthy, 1 delayed</span></div><div class="yfg">{fo}</div></div>'
    top=f'<div class="yt"><div class="fld ysr">{ico("search","i14")}<span>Search incidents, assets, identities</span></div><div class="tr"><span class="yup">Last updated Oct 26, 02:42 UTC</span><span class="bell">{ico("bell")}</span><div class="me2"><div class="av" style="background-image:url({ME})"></div>{ico("chevron-down","i14")}</div></div></div>'
    head=f'<div class="yhd"><div class="yh1"><h1>Security operations</h1><div class="ych">{ico("layers","i14")}All environments, AWS and Azure{ico("chevron-down","i14")}</div></div><div class="ybs"><div class="ybo">{ico("sliders-horizontal","i14")}Configure view</div><div class="ybp">{ico("search","i14")}Start investigation</div></div></div>'
    sb=f'''<aside class="sb"><div class="lg"><div><img class="logo" style="height:31px;display:block" src="{LOGO}"></div>{ico("chevrons-left","i c")}</div>
<div class="nv"><div class="it">{ico("inbox")}Inbox</div><div class="it par">{ico("shield-alert")}Security</div><div class="grp"><div class="sub on">Overview</div><div class="sub">Incidents</div><div class="sub">Exposures</div><div class="sub">Identities</div></div>
<div class="it">{ico("bot")}Agents</div><div class="it">{ico("scroll-text")}Policies</div><div class="it">{ico("square-check")}Approvals<em>3</em></div><div class="it">{ico("clipboard-list")}Audit log</div><div class="it">{ico("plug")}Integrations</div></div>
<div class="sp"></div><div class="nv"><div class="it">{ico("settings")}Settings</div><div class="it">{ico("circle-help")}Help</div></div><div class="me"><div class="av" style="background-image:url({ME})"></div><div><b>Katerina B.</b><span>Brightwell, Security</span></div></div></aside>'''
    body=f'<div class="ybody"><div class="ykp">{kpi}</div><div class="ygr"><div class="ycol">{table}{chart}</div><div class="ycol ycr">{dec}{ctrl}{agents}<div class="ysb"></div></div></div></div>'
    return f'<!doctype html><meta charset=utf-8><style>{css}{extra}</style><body><div class="app">{sb}<div class="main">{top}{head}{body}</div></div></body>'

def INCL(css,CW,CH):
    extra='''
.it.on{background:var(--side2)}
.xt{height:60px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 40px 0 56px;border-bottom:1px solid var(--line)}
.xsr{width:420px;height:36px;justify-content:flex-start!important;gap:10px}
.xhd{display:flex;justify-content:space-between;align-items:flex-start;padding:22px 40px 0 56px;flex:none}
.xhd h1{font-size:40px;display:flex;align-items:center;gap:14px}.xhd h1 span.n{font-size:14px;font-weight:500;color:var(--tx);background:#EFEDE8;border-radius:999px;padding:3px 11px;letter-spacing:0}
.xhd .xm{font-size:13.5px;color:var(--mut);margin-top:6px;display:flex;align-items:center;gap:10px}.xhd .xm em{font-style:normal;font-size:12px;color:var(--ok);background:#EAF3EE;border-radius:3px;padding:1px 8px;display:flex;align-items:center;gap:5px}.xhd .xm em .i14{width:12px;height:12px}
.xbs{display:flex;gap:10px;margin-top:4px}.xbo,.xbp{height:40px;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 16px;font-size:14.5px;white-space:nowrap}.xbo{border:1px solid #D8D4CB;color:var(--ink)}.xbp{background:var(--pr);color:#fff;font-weight:520}.xbo .i14,.xbp .i14{width:16px;height:16px}
.xtabs{display:flex;gap:30px;padding:0 40px 0 56px;border-bottom:1px solid var(--line);margin-top:14px;flex:none}
.xtab{height:44px;display:flex;align-items:center;gap:8px;font-size:14.5px;color:var(--mut);position:relative;white-space:nowrap}.xtab small{font-size:12.5px;color:var(--mut2)}
.xtab.on{color:var(--ink)}.xtab.on small{color:var(--pr);font-weight:520}.xtab.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--pr)}
.xbody{flex:1;min-height:0;display:flex}
.xl{flex:1;min-width:0;padding:16px 16px 0 56px;display:flex;flex-direction:column}
.xtb{display:flex;align-items:center;gap:8px;flex:none}
.xsf{width:300px;height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:9px;padding:0 12px;font-size:14px;color:var(--mut);white-space:nowrap}.xsf .i14{color:var(--mut)}
.xfb{height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:8px;padding:0 13px;font-size:14px;color:var(--ink)}.xfb .i14{width:15px;height:15px;color:var(--mut)}.xfb b{font-size:12px;font-weight:520;color:#fff;background:var(--pr);border-radius:999px;min-width:19px;height:19px;display:flex;align-items:center;justify-content:center}
.xsp{flex:1}
.xsort{height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:8px;padding:0 12px;font-size:14px;color:var(--tx);white-space:nowrap}.xsort .i14{color:var(--mut);width:14px;height:14px}
.xch{display:flex;align-items:center;gap:8px;margin-top:12px;flex:none}
.xcp{height:30px;border-radius:3px;background:#F4F3EF;display:flex;align-items:center;gap:8px;padding:0 9px 0 11px;font-size:13px;color:var(--tx);white-space:nowrap}.xcp .i14{width:13px;height:13px;color:var(--mut)}.xcp b{font-weight:450;color:var(--mut);margin-right:-3px}
.xcl{font-size:13px;color:var(--mut);margin-left:6px;border-bottom:1px solid var(--line)}
.xbk{margin-top:14px;height:46px;border-radius:3px;background:var(--prt);border:1px solid var(--prt2);display:flex;align-items:center;gap:10px;padding:0 12px;flex:none;font-size:14px}
.xbk .xck{margin-right:2px}.xbk b{font-weight:520;margin-right:10px;color:var(--ink)}
.xbb{height:30px;border:1px solid #D8D4CB;background:#fff;border-radius:3px;display:flex;align-items:center;gap:7px;padding:0 11px;font-size:13.5px;color:var(--ink)}.xbb .i14{width:13px;height:13px;color:var(--mut)}
.xbk .xx{margin-left:auto;color:var(--mut)}
.xck{width:18px;height:18px;border:1.5px solid #B9B5AB;border-radius:4px;background:#fff;display:flex;align-items:center;justify-content:center;flex:none;color:#fff}.xck.on{background:var(--pr);border-color:var(--pr)}.xck .i14{width:12px;height:12px;stroke-width:2.6}
.xgh,.xrw{display:grid;grid-template-columns:20px 78px 160px 116px 150px 118px 56px 52px 94px;column-gap:6px;align-items:center;padding:0 12px 0 12px}
.xgh{height:36px;font-size:12.5px;color:var(--mut);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:12px;flex:none}
.xrw{height:62px;border-bottom:1px solid var(--line);font-size:13px;color:var(--tx);position:relative}
.xrw.xsx{background:var(--prt)}.xrw.xsx::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--pr)}
.xin b{display:block;font-weight:480;font-size:14px;color:var(--ink);line-height:1.25}.xin span{display:block;font-size:12.5px;color:var(--mut);margin-top:2px}
.xsc b{display:block;font-weight:450;font-size:13px;color:var(--ink)}.xsc span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px;white-space:nowrap}
.xst div{display:flex;align-items:center;gap:7px;font-size:13px;white-space:nowrap}.xst div+div{margin-top:5px;color:var(--mut)}.xst .i14{width:14px;height:14px;flex:none;color:var(--mut)}.xst .xw .i14{color:var(--amb)}.xst div.xw{color:#8A5A12}.xst div.xe{color:#B03A08}.xst div.xe .i14{color:#B03A08}
.xow b{display:block;font-weight:450;font-size:13px;color:var(--ink);white-space:nowrap}.xow span{display:block;font-size:12.5px;color:var(--mut);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.xow b.un{color:var(--mut)}
.xsl b{display:block;font-weight:450;font-size:13px;color:var(--ink)}.xsl span{display:block;font-size:12px;color:var(--mut);margin-top:1px}.xsl b.br{color:#B03A08}
.xna{font-size:13px;line-height:1.3;color:var(--tx)}
.xrw .ysv{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:500;border-radius:3px;padding:3px 8px 3px 7px;width:max-content}
.xrw .ysv .ybars{display:flex;gap:1.5px;align-items:flex-end;height:11px}.xrw .ysv .ybars i{width:2.5px;background:currentColor;opacity:.28}.xrw .ysv .ybars i.f{opacity:1}.xrw .ysv .ybars i:nth-child(1){height:4px}.xrw .ysv .ybars i:nth-child(2){height:6.5px}.xrw .ysv .ybars i:nth-child(3){height:9px}.xrw .ysv .ybars i:nth-child(4){height:11px}
.xrw .ysv.c{background:#F8DDD0;color:#A93B08}.xrw .ysv.h{background:#FCEDE5;color:#C0410C}.xrw .ysv.m{background:#FBF1D9;color:#8A5A12}
.xft{height:44px;margin-top:0;display:flex;align-items:center;justify-content:space-between;font-size:13.5px;color:var(--mut);flex:none}
.xp{width:360px;flex:none;border-left:1px solid var(--line);display:flex;flex-direction:column;position:relative}
.xph{padding:20px 28px 0}
.xp1{display:flex;align-items:center;justify-content:space-between;font-size:13.5px;color:var(--mut)}.xp1 .xi{display:flex;gap:8px}.xp1 .xi div{width:30px;height:30px;border:1px solid var(--line);border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--tx)}
.xp h2{font-size:22px;font-weight:450;letter-spacing:-.025em;margin-top:12px}
.xp2{display:flex;gap:8px;margin-top:12px}.xp2 .xs{height:32px;border-radius:3px;display:flex;align-items:center;padding:0 10px}.xp2 .xd{height:32px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;gap:8px;padding:0 11px 0 12px;font-size:13.5px}.xp2 .xd .i14{color:var(--mut);width:14px;height:14px}
.xpt{display:flex;gap:22px;margin-top:14px;border-bottom:1px solid var(--line);padding:0 28px;margin-left:0}
.xpt div{height:40px;display:flex;align-items:center;font-size:14px;color:var(--mut);position:relative}.xpt div.on{color:var(--ink)}.xpt div.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--pr)}
.xps{flex:1;min-height:0;overflow:hidden;position:relative;padding:0 28px}
.xps::after{content:"";position:absolute;left:0;right:0;bottom:0;height:60px;background:linear-gradient(rgba(255,255,255,0),#fff)}
.xpb{position:absolute;right:8px;top:12px;width:4px;height:120px;border-radius:2px;background:#D8D4CB}
.xsec{padding:18px 0;border-bottom:1px solid var(--line)}.xsec h4{font-size:14px;font-weight:540;color:var(--ink);margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;letter-spacing:-.005em}.xsec h4 a{font-weight:450;font-size:13px;color:var(--pr)}
.xsec p{font-size:13.5px;line-height:1.55;color:var(--mut)}
.xsec .xq{display:flex;align-items:center;gap:10px;font-size:13.5px;color:var(--tx)}.xsec .xq .i14{color:var(--mut)}.xsec .xq span{color:var(--mut)}
.xag{display:grid;grid-template-columns:1fr auto;row-gap:8px;font-size:13.5px}.xag u{color:var(--tx);text-decoration:none}.xag span{color:var(--mut);display:flex;align-items:center;gap:6px}.xag span .i14{width:13px;height:13px}
.xev{display:flex;justify-content:space-between;align-items:baseline;font-size:14px}.xev span{color:var(--mut);font-size:13px}.xbar{height:5px;border-radius:3px;background:#EFEDE8;margin-top:9px}.xbar i{display:block;height:5px;border-radius:3px;background:var(--pr)}
.xtl div{display:grid;grid-template-columns:48px 1fr;font-size:13px;color:var(--tx);padding:5px 0;line-height:1.4}.xtl div span{color:var(--mut)}
.xpf{padding:14px 28px 22px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:10px;flex:none}
.xpf .xo{height:42px;border-radius:3px;background:var(--pr);color:#fff;display:flex;align-items:center;justify-content:center;gap:9px;font-size:14.5px;font-weight:520}.xpf .xo .i14{width:16px;height:16px}
.xpf .xq2{display:flex;gap:10px}.xpf .xq2 div{flex:1;height:38px;border:1px solid #D8D4CB;border-radius:3px;display:flex;align-items:center;justify-content:center;gap:8px;font-size:14px}.xpf .xq2 .i14{color:var(--mut);width:14px;height:14px}
'''
    EXTRA2='''
.xrn{flex:none;margin-bottom:18px}
.xrh{display:flex;align-items:baseline;justify-content:space-between}
.xrh b{font-size:15px;font-weight:540;color:var(--ink);letter-spacing:-.005em}.xrh span.s{font-size:13px;color:var(--mut);margin-left:10px}
.xrl{display:flex;gap:16px;font-size:12.5px;color:var(--mut)}.xrl span{display:flex;align-items:center;gap:7px}.xrl i{display:block;width:16px;height:6px;border-radius:3px}
.xrc{position:relative;height:138px;margin-top:12px}
.xrp{position:absolute;left:118px;right:0;top:0;height:112px}
.xgl{position:absolute;top:-4px;bottom:-4px;width:1px;background:var(--line)}
.xnw{position:absolute;top:-6px;bottom:-4px;width:1.5px;background:var(--pr);left:0}
.xnw::before{content:"Now";position:absolute;top:122px;left:-12px;font-size:12px;color:var(--pr);font-weight:520}
.xtk{position:absolute;top:122px;font-size:12px;color:var(--mut2);transform:translateX(-50%)}
.xln{position:absolute;left:-118px;width:110px;font-size:12px;color:var(--mut);height:14px;line-height:14px;white-space:nowrap}.xln.b{color:var(--pr);font-weight:520}
.xcap{position:absolute;height:7px;border-radius:4px;margin-top:3.5px}
.xcv{position:absolute;font-size:12px;line-height:14px;color:var(--mut);white-space:nowrap}.xcv.u{color:#B03A08;font-weight:520}
.xtbl{flex:1;min-height:0;overflow:hidden;position:relative}
.xtbl::after{content:"";position:absolute;left:0;right:0;bottom:0;height:56px;background:linear-gradient(rgba(255,255,255,0),#fff);pointer-events:none}
'''
    sev={'c':('Critical',4),'h':('High',3),'m':('Medium',2)}
    def sv(k):
        n,f=sev[k]; return f'<span class="ysv {k}"><span class="ybars">'+''.join('<i class="f"></i>' if i<f else '<i></i>' for i in range(4))+f'</span>{n}</span>'
    # (sev,id,title,cloud,scope1,scope2,inv(icon,text,cls),resp(icon,text,cls),owner,agent,age,sla,slabreach,upd,next,check,open)
    R=[('h','INC-2026-0837','Data exfiltration attempt','AWS','1 user','2 resources',('circle-x','Verification failed','xe'),('shield-alert','Approval required','xw'),'Daniel Okafor','Remediation Agent','20m','SLA 8h','','02:41','Review failed step',1,1),
       ('c','INC-2026-0836','Exposed DB credentials','AWS','1 user','3 resources',('file-warning','Evidence incomplete',''),('shield-alert','Approval required','xw'),'Priya Shah','Identity and Asset','1h 05m','SLA 4h','','02:28','Review and approve',0,0),
       ('c','INC-2026-0834','Privilege escalation','Azure','1 user','2 resources',('search','Active investigation',''),('shield-ban','Not contained','xe'),'Alex Kim','Threat and Exposure','2h 10m','SLA 4h','','02:00','Review containment',0,0),
       ('h','INC-2026-0832','Excessive data access','AWS','4 users','12 resources',('file-search','Needs evidence',''),('shield-check','Policy blocked',''),'Jordan Diaz','Data Protection','7h 20m','SLA 8h','br','01:36','Collect missing evidence',0,0),
       ('h','INC-2026-0833','Public storage exposure','Azure','1 resource','',('circle-check','Investigated',''),('shield-alert','Approval required','xw'),'Priya Shah','Remediation','5h 52m','SLA 8h','','00:50','Approve remediation',1,0),
       ('m','INC-2026-0831','Suspicious API activity','AWS','2 users','6 resources',('activity','Analyzing, 2 of 4',''),('eye','Monitoring',''),'Alex Kim','Investigation','9h 03m','SLA 24h','','23:48','Review results',0,0),
       ('m','INC-2026-0829','Policy violation','Azure','3 resources','',('clock','Waiting for telemetry',''),('circle-minus','No action taken',''),'Unassigned','Threat and Exposure','11h 26m','SLA 24h','','22:30','Assign an owner',0,0),
       ('m','INC-2026-0828','Cloud configuration drift','AWS','3 resources','',('clipboard-list','Initial review',''),('eye','Monitoring',''),'Jordan Diaz','Identity and Asset','14h 02m','SLA 24h','','20:15','Review and close',0,0)]
    rows=''
    for s,i,t,cl,s1,s2,inv,rsp,ow,ag,age,sla,br,upd,nx,ck,op in R:
        cls=' xsx' if ck else ''
        chk=f'<div class="xck{" on" if ck else ""}">{ico("check","i14") if ck else ""}</div>'
        sc2=f'<span>{s1}, {s2}</span>' if s2 else f'<span>{s1}</span>'
        rows+=f'<div class="xrw{cls}">{chk}<div>{sv(s)}</div><div class="xin"><b>{t}</b><span>{i}</span></div><div class="xsc"><b>{cl}</b>{sc2}</div><div class="xst"><div class="{inv[2]}">{ico(inv[0],"i14")}{inv[1]}</div><div class="{rsp[2]}">{ico(rsp[0],"i14")}{rsp[1]}</div></div><div class="xow"><b class="{"un" if ow=="Unassigned" else ""}">{ow}</b><span>{ag}</span></div><div class="xsl"><b class="{br}">{age}</b><span>{sla}</span></div><div class="xsl"><b>{upd}</b></div><div class="xna">{nx}</div></div>'
    assert sum(1 for r in R if r[0]=='c')==2 and sum(1 for r in R if r[15])==2 and sum(1 for r in R if 'Approval' in r[7][1])==3
    top=f'<div class="xt"><div class="fld xsr">{ico("search","i14")}<span>Search incidents, assets, identities</span></div><div class="tr"><span class="bell">{ico("bell")}</span><div class="me2"><div class="av" style="background-image:url({ME})"></div>{ico("chevron-down","i14")}</div></div></div>'
    head=f'<div class="xhd"><div><h1>Incidents<span class="n">48</span></h1><div class="xm">Last updated Oct 26, 02:42 UTC<em>{ico("radio","i14")}Live</em></div></div><div class="xbs"><div class="xbo">{ico("sliders-horizontal","i14")}Configure queue</div><div class="xbp">{ico("plus","i14")}Create incident</div></div></div>'
    TB=[('My queue',4),('Needs attention',8),('Unassigned',3),('Awaiting approval',3),('Containment failed',1),('Verification pending',2),('Recently closed',22)]
    tabs='<div class="xtabs">'+''.join(f'<div class="xtab{" on" if n=="Needs attention" else ""}">{n}<small>{c}</small></div>' for n,c in TB)+'</div>'
    tb=f'<div class="xtb"><div class="xsf">{ico("search","i14")}Search users, resources, ATT&amp;CK</div><div class="xfb">{ico("list-filter","i14")}Filter<b>2</b></div><div class="xsp"></div><div class="xsort">{ico("arrow-up-down","i14")}Sort: Last update{ico("chevron-down","i14")}</div><div class="xbo" style="height:38px">{ico("bookmark","i14")}Save view</div></div>'
    chips=f'<div class="xch"><div class="xcp"><b>Status</b>Open{ico("x","i14")}</div><div class="xcp"><b>Environment</b>AWS, Azure{ico("x","i14")}</div><span class="xcl">Clear all</span></div>'
    bulk=f'<div class="xbk"><div class="xck on">{ico("check","i14")}</div><b>2 incidents selected</b><div class="xbb">Assign{ico("chevron-down","i14")}</div><div class="xbb">Change status{ico("chevron-down","i14")}</div><div class="xbb">Add tag{ico("chevron-down","i14")}</div><div class="xbb">Export{ico("chevron-down","i14")}</div><span class="xx">{ico("x","i14")}</span></div>'
    gh=f'<div class="xgh"><div class="xck"></div><span>Severity</span><span>Incident</span><span>Affected scope</span><span>Investigation, response</span><span>Owner</span><span>SLA, age</span><span>Updated</span><span>Next action</span></div>'
    panel=f'''<aside class="xp"><div class="xph"><div class="xp1"><span>INC-2026-0837</span><div class="xi"><div>{ico("external-link","i14")}</div><div>{ico("x","i14")}</div></div></div><h2>Data exfiltration attempt</h2><div class="xp2"><span class="xs ysv h" style="gap:6px;font-size:12.5px;font-weight:500"><span class="ybars" style="display:flex;gap:1.5px;align-items:flex-end;height:11px"><i style="width:2.5px;height:4px;background:currentColor"></i><i style="width:2.5px;height:6.5px;background:currentColor"></i><i style="width:2.5px;height:9px;background:currentColor"></i><i style="width:2.5px;height:11px;background:currentColor;opacity:.28"></i></span>High</span><div class="xd">Investigating{ico("chevron-down","i14")}</div></div></div>
<div class="xpt"><div class="on">Overview</div><div>Evidence</div><div>Agents</div><div>Timeline</div></div>
<div class="xps"><div class="xsec" style="padding-top:20px"><h4>Current finding</h4><p>Upload of restricted customer data to an external IP was blocked. Secret rotation failed verification.</p></div>
<div class="xsec"><h4>Response state</h4><span class="ysv m" style="display:inline-flex;align-items:center;gap:7px;font-size:12.5px;font-weight:500;border-radius:3px;padding:4px 10px 4px 8px;background:#FBF1D9;color:#8A5A12">{ico("shield-alert","i14")}Approval required</span></div>
<div class="xsec"><h4>Evidence completeness<span style="font-weight:450;font-size:13px;color:var(--mut)">12 of 14</span></h4><div class="xbar" style="margin-top:2px"><i style="width:86%"></i></div></div>
<div class="xsec"><h4>Active agents and tasks</h4><div class="xag"><u>Remediation</u><span>Retrying rotation</span><u>Data Protection</u><span>Monitoring egress</span></div></div>
<div class="xsec"><h4>Affected scope<a>View all</a></h4><p>AWS, 1 user, 2 resources</p></div>
<div class="xsec"><h4>Owner and SLA</h4><p>Daniel Okafor, 20m of 8h</p></div>
<div class="xsec" style="border:0"><h4>Latest events<a>View all</a></h4><div class="xtl"><div><span>02:41</span>Rotation verification failed</div><div><span>02:34</span>User account suspended</div><div><span>02:22</span>Outbound transfer blocked</div></div></div><div class="xpb"></div></div>
<div class="xpf"><div class="xo">{ico("external-link","i14")}Open incident</div><div class="xq2"><div>{ico("user-round","i14")}Assign{ico("chevron-down","i14")}</div><div>{ico("ellipsis","i14")}Change status{ico("chevron-down","i14")}</div></div></div></aside>'''
    RN=[('0832',40,'h',0),('0834',110,'c',0),('0833',128,'h',1),('0836',175,'c',0),('0837',460,'h',1),('0828',598,'m',0),('0829',754,'m',0),('0831',897,'m',0)]
    col={'c':'#D9480F','h':'#EE8A55','m':'#E2B24F'}
    W=960.0
    gl=''.join(f'<div class="xgl" style="left:{h*60/W*100}%"></div><div class="xtk" style="left:{h*60/W*100}%">{h}h</div>' for h in (4,8,12,16))
    ln=''
    for k,(i,m,sv_,bo) in enumerate(RN):
        hh,mm=divmod(m,60); lab=(f'{hh}h {mm:02d}m' if hh else f'{mm}m')
        w=m/W*100
        ln+=f'<div class="xln{" b" if bo else ""}" style="top:{k*14}px">INC-2026-{i}</div><div class="xcap" style="top:{k*14}px;left:0;width:{w}%;background:{col[sv_]}"></div><div class="xcv{" u" if m<60 else ""}" style="top:{k*14}px;left:calc({w}% + 9px)">{lab}</div>'
    runway=f'<div class="xrn"><div class="xrh"><div><b>SLA runway</b><span class="s">Time left until breach, next 16 hours</span></div><div class="xrl"><span><i style="background:{col["c"]}"></i>Critical</span><span><i style="background:{col["h"]}"></i>High</span><span><i style="background:{col["m"]}"></i>Medium</span></div></div><div class="xrc"><div class="xrp">{gl}<div class="xnw"></div>{ln}</div></div></div>'
    left=f'<div class="xl">{runway}{tb}{chips}{bulk}{gh}<div class="xtbl">{rows}</div><div class="xft"><span>Showing 8 of 8 incidents</span><span>Page 1 of 1</span></div></div>'
    sb=f'''<aside class="sb"><div class="lg"><div><img class="logo" style="height:31px;display:block" src="{LOGO}"></div>{ico("chevrons-left","i c")}</div>
<div class="nv"><div class="it">{ico("inbox")}Inbox</div><div class="it par">{ico("shield-alert")}Security</div><div class="grp"><div class="sub">Overview</div><div class="sub on">Incidents</div><div class="sub">Exposures</div><div class="sub">Identities</div></div>
<div class="it">{ico("bot")}Agents</div><div class="it">{ico("scroll-text")}Policies</div><div class="it">{ico("square-check")}Approvals<em>3</em></div><div class="it">{ico("clipboard-list")}Audit log</div><div class="it">{ico("plug")}Integrations</div></div>
<div class="sp"></div><div class="nv"><div class="it">{ico("settings")}Settings</div><div class="it">{ico("circle-help")}Help</div></div><div class="me"><div class="av" style="background-image:url({ME})"></div><div><b>Katerina B.</b><span>Brightwell, Security</span></div></div></aside>'''
    return f'<!doctype html><meta charset=utf-8><style>{css}{extra}{EXTRA2}</style><body><div class="app">{sb}<div class="main">{top}{head}{tabs}<div class="xbody">{left}{panel}</div></div></div></body>'

def build(mode,tab='ov'):
    win=mode=='win'; CW,CH=(1600,1200) if win else (1600,1040); AW,AH=(1512,1068) if win else (1600,1040); RW=372 if win else 392
    if win: wincss='''.bgd{position:absolute;inset:0;background:radial-gradient(900px 640px at 8% 0%,#C7D4E6 0%,transparent 70%),radial-gradient(800px 600px at 100% 6%,#D9D1EE 0%,transparent 70%),radial-gradient(900px 700px at 90% 100%,#F3DCCB 0%,transparent 68%),radial-gradient(800px 600px at 0% 100%,#CFE0E4 0%,transparent 70%),#DEE5EE}
.grain{position:absolute;inset:0;opacity:.10;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>")}
.win{position:absolute;left:44px;top:44px;width:__AW__px;height:__WH__px;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 50px 90px -30px rgba(40,30,60,.38),0 0 0 1px rgba(30,20,50,.10)}
.tb{height:44px;border-bottom:1px solid var(--line);background:#F9F8F6;display:flex;align-items:center;padding:0 16px;position:relative}
.dots{display:flex;gap:8px}.dots span{width:12px;height:12px;border-radius:50%}
.url{position:absolute;left:50%;transform:translateX(-50%);height:28px;width:440px;border-radius:8px;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;gap:7px;font-size:12.5px;color:var(--mut)}.url .i{width:13px;height:13px;color:var(--mut2)}
.app{position:relative;display:flex;width:__AW__px;height:__AH__px}'''.replace('__AW__',str(AW)).replace('__WH__',str(AH+44)).replace('__AH__',str(AH))
    else: wincss='.app{position:absolute;inset:0;display:flex}'
    RH,UH,GAP,TOOLH=(64,30,12,70) if win else (60,28,10,66)
    t1=RH/2; h1=6*RH; t2=t1+h1
    css=CSS.replace('__T1__',str(t1)).replace('__H1__',str(h1)).replace('__T2__',str(t2)).replace('__H2__',str(RH/2+GAP+3*UH+UH/2)).replace('__RH__',str(RH)).replace('__UH__',str(UH)).replace('__GAP__',str(GAP)).replace('__TOOLH__',str(TOOLH)).replace('__F__',F).replace('__CW__',str(CW)).replace('__CH__',str(CH)).replace('__BODYBG__','#DEE5EE' if win else '#fff').replace('__WINCSS__',wincss).replace('__RW__',str(RW)).replace('__SP__',('22' if win else '17') if tab=='ov' else (('13' if win else '11') if tab=='rm' else (('26' if win else '22') if tab=='ex' else ('20' if win else '19')))).replace('__GRH__','62' if win else '58').replace('__XRH__','60' if win else '56').replace('__EH__','0').replace('__ARH__','62' if win else '58').replace('__ATH__','48' if win else '52')
    if tab=='pol': return POL(css,CW,CH),CW,CH
    if tab=='aud': return AUD(css,CW,CH),CW,CH
    if tab=='dash': return DASH(css,CW,CH),CW,CH
    if tab=='inc': return INCL(css,CW,CH),CW,CH
    def row(e):
        t,ti,tx,k,s,sl,f,tags=e
        chip={'blk':'<span class="tg ok">Blocked</span>','sev':'<span class="tg hi">High</span>','now':'<span class="tg amb">Revalidation required</span>'}.get(f,'')
        cls={'blk':'blk','now':'cur'}.get(f,'')
        bg='<div class="cr"></div>' if f=='now' else ''
        tg=''.join(f'<span class="tc">{x}</span>' for x in tags.split('|') if x)
        return f'<div class="r {cls}">{bg}<div class="tm">{t}</div><div class="nd"><s></s></div><div class="bd"><div class="ti">{ti}{chip}{tg}</div><div class="ds">{tx}</div></div><div class="src"><div>{glyph(k,13)}{s}</div><small>{sl}</small></div><div class="go">{ico("chevron-right","i14")}</div></div>'
    up=lambda u:f'<div class="r up"><div class="tm"></div><div class="nd"><s></s></div><div class="bd"><div class="ti">{u[0]}<span class="ud">{u[1]}</span></div></div></div>'
    rows=''.join(row(e) for e in EV)+''.join(up(u) for u in UP)
    TLW=AW-236-RW-88
    BODY=(f'''<div class="body"><section class="tl afx"><div class="sh2"><div><h2>Evidence timeline</h2><p>Key events and related evidence from connected sources, UTC</p></div><div class="cs"><div class="fld" style="width:210px"><span>Search events</span>{ico("search","i14")}</div><div class="fld" style="width:140px"><span>All events</span>{ico("chevron-down","i14")}</div><span class="dl">{ico("download","i14")}</span></div></div>
<div class="rb"><div class="rbh"><span>14 signals from 4 sources, {DONE} of {TOTAL} steps done</span><b>8 min to containment</b></div>{ribbon(TLW)}</div>
<div class="th"><span>Time</span><span></span><span>Event</span><span>Source</span><span></span></div><div class="rows">{rows}</div></section>
<aside class="rail"><div class="sec"><div class="sh">Affected identity<a>View details{ico("chevron-right","i14")}</a></div><div class="id"><div class="av" style="background-image:url({MAYA})"></div><div><b>Maya Chen</b><span>Data Scientist, Engineering</span></div><div class="rk"><b>78</b><span>risk score</span></div></div><div class="rkb"><i></i></div><div class="rs"><span>Unusual location</span><span>New device</span><span>Off-hours access</span></div></div>
<div class="sec"><div class="sh">Affected assets<a>View all{ico("chevron-right","i14")}</a></div><div class="as"><div class="g">{ico("server")}</div><div><b>prod-ml-workload</b><span>EC2 instance, Production</span></div>{ico("chevron-right","i14")}</div><div class="as"><div class="g">{ico("database")}</div><div><b>brightwell-customer-data</b><span>S3 bucket, Production</span></div>{ico("chevron-right","i14")}</div></div>
<div class="sec"><div class="sh">Agent findings<a>View all{ico("chevron-right","i14")}</a></div><div class="gr"><div class="gg">{gauge()}<div class="v"><b>{CONF}%</b></div></div><p>High confidence this was a data exfiltration attempt</p></div><div class="fd"><div>File staged for transfer<span class="a">High</span></div><div>Transfer blocked as designed<span class="g">Confirmed</span></div><div>Successful exfiltration<span class="n">None found</span></div></div></div>
<div class="sec"><div class="sh">Missing evidence<a>View list{ico("chevron-right","i14")}</a></div><div class="ms"><div>{ico("square","i14")}Similar files read in the last 7 days</div><div>{ico("square","i14")}Other destinations or retries</div></div></div>
<div class="cta"><div class="btn">Open remediation plan{ico("arrow-right")}</div></div></aside></div>''' if tab=='ov' else (REM(mode,AW,RW,DONE,TOTAL) if tab=='rm' else (EX(mode,AW,RW,DONE,TOTAL) if tab=='ex' else AF(mode,AW,RW,DONE,TOTAL))))
    app=f'''<div class="app"><aside class="sb"><div class="lg"><div><img class="logo" style="height:31px;display:block" src="{LOGO}"></div>{ico("chevrons-left","i c")}</div>
<div class="nv"><div class="it">{ico("inbox")}Inbox</div><div class="it par">{ico("shield-alert")}Security</div><div class="grp"><div class="sub">Overview</div><div class="sub on">Incidents</div><div class="sub">Exposures</div><div class="sub">Identities</div></div>
<div class="it">{ico("bot")}Agents</div><div class="it">{ico("scroll-text")}Policies</div><div class="it">{ico("square-check")}Approvals<em>3</em></div><div class="it">{ico("clipboard-list")}Audit log</div><div class="it">{ico("plug")}Integrations</div></div>
<div class="sp"></div><div class="nv"><div class="it">{ico("settings")}Settings</div><div class="it">{ico("circle-help")}Help</div></div><div class="me"><div class="av" style="background-image:url({ME})"></div><div><b>Katerina B.</b><span>Brightwell, Security</span></div></div></aside>
<div class="main"><div class="top"><div class="bc"><span class="lk">Security</span>{ico("chevron-right","i14")}<span class="lk">Incidents</span>{ico("chevron-right","i14")}<b>INC-2026-0837</b></div><div class="tr"><div class="fld"><span>Search incidents, identities, assets</span>{ico("search","i14")}</div><span class="bell">{ico("bell")}</span><div class="me2"><div class="av" style="background-image:url({ME})"></div>{ico("chevron-down","i14")}</div></div></div>
<div class="hd"><div class="t1"><div><h1>Sensitive data exfiltration attempt</h1><div class="meta">INC-2026-0837, Detected Oct 26, 02:22 UTC, Last updated {"2" if tab=="ex" else "3"} min ago</div></div><div class="acts"><div class="ch"><span class="sev"><i class="f"></i><i class="f"></i><i class="f"></i><i></i></span>High{ico("chevron-down","i14 c")}</div><div class="ch">{ico("refresh-cw","i14 pr")}Investigating{ico("chevron-down","i14 c")}</div><div class="ch">{ico("shield-check","i14 ok")}Transfer blocked{ico("chevron-down","i14 c")}</div><div class="btn2">{ico("ellipsis")}</div></div></div>
<div class="tabs"><div class="tab{" on" if tab=="ov" else ""}">Overview</div><div class="tab">Evidence<small>14</small></div><div class="tab">Affected entities<small>3</small></div><div class="tab{" on" if tab=="af" else ""}">Agent findings<small>5</small></div><div class="tab{" on" if tab=="rm" else ""}">Remediation<small>6</small></div><div class="tab{" on" if tab=="ex" else ""}">Execution and verification</div><div class="tab">Activity log</div></div></div>
{BODY}</div></div>'''
    if win: html=f'<!doctype html><meta charset=utf-8><style>{css}</style><body><div class="bgd"></div><div class="grain"></div><div class="win"><div class="tb"><div class="dots"><span style="background:#FF5F57"></span><span style="background:#FEBC2E"></span><span style="background:#28C840"></span></div><div class="url">{ico("lock","i")}app.wardline.io/incidents/INC-2026-0837</div></div>{app}</div></body>'
    else: html=f'<!doctype html><meta charset=utf-8><style>{css}{QCSS}{KCSS}</style><body>{app}</body>'
    return html,CW,CH
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,mode,sc,tab in (('Incident-1-Overview','flat',1.6,'ov'),('Incident-2-Agent-Findings','flat',1.6,'af'),('Incident-3-Remediation','flat',1.6,'rm'),('Incident-4-Execution','flat',1.6,'ex'),('Incidents','flat',1.6,'inc'),('Agents-Policies-and-Permissions','flat',1.6,'pol'),('Audit-Log','flat',1.6,'aud'),('Security-Operations','flat',1.6,'dash')):
        h,w,hh=build(mode,tab);(D/f'{name}.html').write_text(h)
        pg=b.new_page(viewport={'width':w,'height':hh},device_scale_factor=sc);pg.goto(f'file://{D}/{name}.html');pg.wait_for_timeout(600)
        r=pg.evaluate('''()=>{const o=[...document.querySelectorAll('h1,.ti,.ds,.btn,.ch,.src,.as b,.fd div,.ms div,.hr,.al b,.al span,.pr1 span,.ph b,.ph span.d,.ph .sm2,.mt2,.zar b,.zar span,.zfc,.zer span,.yin b,.yin span,.yaf,.yar b,.yar span,.yk small,.yfi b')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.className+':'+e.textContent.slice(0,30));
        const rows=document.querySelector('.rows')||document.body;const tl=(document.querySelector('.tl')||document.body).getBoundingClientRect();const rl=[];
        const rail=document.querySelector('.zdt2')||document.querySelector('.xps')||document.querySelector('.ycol')||document.querySelector('.rail')||document.querySelector('.rl2')||document.querySelector('.zdt2');const secs=[...rail.children].map(s=>[Math.round(s.scrollHeight),Math.round(s.clientHeight)]);
        return {over:o,rows:rows.scrollHeight+'/'+rows.clientHeight,tlBottom:Math.round(tl.bottom),railOver:rail.scrollHeight>rail.clientHeight,secs,tlOver:0,cc:document.querySelector('.cc')?document.querySelector('.cc').scrollHeight-document.querySelector('.cc').clientHeight:0}}''')
        print(name,r);pg.screenshot(path=str(D/f'{name}.png'))
    b.close()
