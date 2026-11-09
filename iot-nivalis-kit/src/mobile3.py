import sys, math; sys.path.insert(0,'/home/claude/nivalis')
from mobile2 import *
CSS3=CSS2+'''
.fr{display:flex;justify-content:space-between;align-items:center;min-height:50px;border-top:1px solid #D5DDE2;font-size:15px}
.fr span{color:var(--muted)}.fr b{font-weight:600;text-align:right}
.h2{font-size:20px;font-weight:600;line-height:26px}
.ttl{font-family:var(--disp);font-weight:600;font-size:26px;line-height:31px;letter-spacing:-.02em;color:#0A3B49;margin-top:12px}
.dsc{font-size:15px;line-height:21px;color:#2F5E6B;margin-top:8px}
.ar{margin-top:14px;border-radius:18px;background:#EAF6EE;padding:16px 18px 6px}
.ar .t{display:flex;gap:12px;align-items:center}
.ar .ck{width:40px;height:40px;border-radius:50%;background:#1B6B3A;display:flex;align-items:center;justify-content:center;flex:none}
.ar .t b{display:block;font-size:17px;line-height:22px;font-weight:600;color:#12452A}.ar .t em{display:block;font-style:normal;font-size:13.5px;color:#3E6A4E;line-height:18px}
.ar .k{display:flex;justify-content:space-between;align-items:center;min-height:44px;border-top:1px solid #CBE5D3;margin-top:14px;font-size:15px;color:#3E6A4E}.ar .k+.k{margin-top:0}.ar .k b{color:#12452A;font-weight:600}
.ov{z-index:50;position:absolute;inset:0;background:rgba(10,24,30,.46)}
.sheet{z-index:60;position:absolute;left:0;right:0;bottom:0;background:#fff;border-radius:24px 24px 0 0;padding:8px 16px 34px}
.gr{width:40px;height:5px;border-radius:3px;background:#CBD3D9;margin:0 auto 12px}
.sheet .ov2{font-size:13px;color:var(--muted)}
.sheet h4{font-family:var(--disp);font-weight:600;font-size:23px;line-height:28px;letter-spacing:-.015em;margin-top:2px}
.sheet p{font-size:15px;line-height:21px;color:var(--muted);margin-top:6px}
.sheet .fr{min-height:44px;font-size:14.5px}
.sheet .fr b{font-size:14.5px}
.cb{display:flex;gap:12px;align-items:flex-start;margin-top:14px;font-size:15px;line-height:21px}
.cb i{flex:none;width:26px;height:26px;border-radius:8px;border:1.5px solid #8A97A1;background:#fff;display:flex;align-items:center;justify-content:center;margin-top:-2px}
.cb i.on{background:#11181C;border-color:#11181C}
.sb{display:flex;gap:10px;margin-top:16px}
.sb .b2{height:52px}.sb .b2.p{flex:1}
.sb .b2.off{background:#C9D0D5;color:#fff}
.who{font-size:13px;color:var(--muted);margin-top:14px;line-height:18px}.who b{color:var(--ink);font-weight:600}
.live{margin-top:12px;border-radius:20px;background:linear-gradient(160deg,#D2EBEE,#EAF7F6);box-shadow:inset 0 0 0 1.5px #8CC6CF;padding:16px 16px 6px;position:relative;overflow:hidden}
.live:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(12,74,92,.06) 0 1px,transparent 1px 9px)}
.live>*{position:relative}
.qb{display:flex;gap:12px;align-items:flex-start}.qb .ci{flex:none;width:40px;height:40px;border-radius:50%;background:#0C4A5C;display:flex;align-items:center;justify-content:center;color:#fff}
.qb b{display:block;font-size:17px;line-height:22px;font-weight:600;color:#0A3B49}.qb p{font-size:14px;line-height:19px;color:#2F5E6B;margin-top:3px}
.tl{margin-top:14px}
.tr{display:flex;align-items:center;gap:12px;min-height:48px;position:relative;font-size:15px}
.tr:not(:last-child):after{content:'';position:absolute;left:11px;top:36px;bottom:-12px;width:2px;background:#9FCBD3}
.mk{flex:none;width:24px;height:24px;border-radius:50%;border:2px solid #9FB4BC;background:#fff;display:flex;align-items:center;justify-content:center}
.mk.d{background:#1B6B3A;border-color:#1B6B3A}.mk.n{background:#0C4A5C;border-color:#0C4A5C}
.tr b{font-weight:600;flex:1}.tr em{font-style:normal;color:#4B7580;font-size:13.5px;text-align:right;line-height:17px}.tr em s{display:block;text-decoration:none;color:#0A3B49;font-weight:600;font-size:14px}
.tr.p b{font-weight:500;color:#4B6A74}
'''
def page3(body,extra=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS3}</style></head><body>{body}{extra}</body></html>'
CHK=icon('close',0,0) if False else ''
def check(sz=16):
    return f'<svg width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'

def fc(approved=False,W=361,H=168):
    L=4;R=W-4
    ys=lambda v:12+(70-v)/30*(H-52)
    X=lambda f:L+(R-L)*f
    now=0.5
    hist=[]
    for i in range(31):
        f=i/30*now
        v=46+3*math.sin(f*14)+ (i/30)**2*1.5
        hist.append((X(f),ys(min(v,48.2)+0)))
    hist[-1]=(X(now),ys(48.2))
    s=f'<line x1="{L}" x2="{R}" y1="{ys(66.8):.1f}" y2="{ys(66.8):.1f}" stroke="#E5533D" stroke-width="1.4"/><text x="{R}" y="{ys(66.8)-6:.1f}" text-anchor="end" font-size="12" fill="#B3321D">Capacity 66.8 kW</text>'
    x0=X(now);x1=X(0.78)
    y1=ys(51.7);y0=ys(48.2)
    st='fill="rgba(229,83,61,.10)" stroke="#E5533D" stroke-width="2" stroke-dasharray="5 4"' if approved else 'fill="rgba(229,83,61,.22)" stroke="#E5533D" stroke-width="2"'
    s+=f'<path d="M{x0:.1f},{y0:.1f} L{x0:.1f},{y1:.1f} L{x1:.1f},{y1:.1f} L{x1:.1f},{y0:.1f}" {st}/>'
    s+=f'<line x1="{x1:.1f}" x2="{R}" y1="{y0:.1f}" y2="{y0:.1f}" stroke="#9AA7B0" stroke-dasharray="3 4"/>'
    s+=f'<path d="{smooth(hist)}" fill="none" stroke="#0C4A5C" stroke-width="2.6" stroke-linecap="round"/><circle cx="{x0:.1f}" cy="{y0:.1f}" r="5" fill="#fff" stroke="#0C4A5C" stroke-width="2.4"/>'
    s+=f'<text x="{(x0+x1)/2:.1f}" y="{y1-9:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#B3321D">51.7 kW{" projected" if approved else ""}</text>'
    for f,lab,a in ((0,'10:11','start'),(now,'Now','middle'),(0.78,'10:54','middle')):
        s+=f'<text x="{X(f):.1f}" y="{H-6}" text-anchor="{a}" font-size="12" fill="{"#11181C" if lab=="Now" else "#66727C"}" {"font-weight=600" if lab=="Now" else ""}>{lab}</text>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{s}</svg>'

def fr(a,b,extra=''): return f'<div class="fr"><span>{a}</span><b>{b}{extra}</b></div>'
def demand(approved):
    return f'''<section style="margin-top:30px"><div class="h2">Demand impact</div><div style="font-size:15px;line-height:21px;color:var(--muted);margin-top:4px"><b style="color:var(--ink);font-weight:600">Low risk.</b> +3.5 kW, 15.1 kW below capacity.</div><div style="margin-top:12px">{fc(approved)}</div></section>'''
def hero(pills,note=''):
    return f'''<section class="lt" style="margin-top:12px"><div class="tags">{pills}</div><div class="ttl">Activate backup evaporator mode</div><div class="dsc">Backup sequence for EVAP-FZB-02 and EVAP-FZB-03, up to 30 min while EF-3 is inspected.</div></section>'''
def prow(n,sub,tag,cls='g'):
    return f'<div class="lrow" style="min-height:64px;border-top:1px solid #D5DDE2;padding:0"><div><b>{n}</b><em>{sub}</em></div><span class="tg2 {cls}">{tag}</span></div>'
PILL_REQ='<span class="pill w">Approval required</span><span class="pill n">ACT-1184</span>'
PILL_APP='<span class="pill" style="background:#E1F2E7;color:#1B6B3A">Approved</span><span class="pill n">Awaiting dispatch</span>'
PILL_Q='<span class="pill n" style="background:#0C4A5C;color:#fff;box-shadow:none">Queued</span><span class="pill n">ACT-1184</span>'

def pending_body():
    facts=fr('Controller','CTRL-FZB-03')+fr('Maximum run time','30 min')+fr('Automatic end','10:54')+fr('Setpoints and interlocks','No changes')
    pol=f'''<section style="margin-top:30px"><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:6px"><span class="h2">Policy checklist</span><span style="font-size:13px;color:var(--faint)">3 passed, 1 after run</span></div>{prow("Target and limits","Both evaporators approved","Passed")}{prow("Policy","POL-COLD-07 allows backup mode","Passed")}{prow("Rollback","Stop and restore previous state","Passed")}{prow("Verification","Airflow response within 3 min","After run","")}</section>'''
    return f'<div class="pg">{nav2("Remote action")}{hero(PILL_REQ)}<section style="margin-top:20px">{facts}</section>{demand(False)}{pol}</div>'
def approved_body():
    ar=f'''<section class="ar"><div class="t"><span class="ck">{check(20)}</span><div><b>Approved by Felix Whitaker</b><em>Facility Operations Manager, 10:25 EST</em></div></div>
<div class="k"><span>Policy</span><b>POL-COLD-07, Passed</b></div><div class="k"><span>Approved parameters</span><b>Locked</b></div><div class="k"><span>Next step</span><b>Awaiting dispatch</b></div></section>'''
    facts=fr('Controller','CTRL-FZB-03')+fr('Controller state','No command sent')+fr('Automatic end','After dispatch')
    pol=f'''<section style="margin-top:30px"><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:6px"><span class="h2">Before execution</span><span style="font-size:13px;color:var(--faint)">Completed</span></div>{prow("Target and limits","Both evaporators approved","Passed")}{prow("Policy","POL-COLD-07 allows backup mode","Passed")}{prow("Rollback","Stop and restore previous state","Passed")}</section>'''
    return f'<div class="pg">{nav2("Remote action")}{hero(PILL_APP)}{ar}<section style="margin-top:20px">{facts}</section>{demand(True)}{pol}</div>'
def queued_body():
    def row(c,name,who,t,cls=''):
        mk={'d':f'<span class="mk d">{check(12)}</span>','n':'<span class="mk n"><span style="width:8px;height:8px;border-radius:50%;background:#fff"></span></span>','':'<span class="mk"></span>'}[c]
        right=f'<em><s>{t}</s>{who}</em>' if who else f'<em>{t}</em>'
        return f'<div class="tr {"p" if not c else ""}">{mk}<b>{name}</b>{right}</div>'
    live=f'''<section class="live"><div class="qb"><span class="ci">{icon("clock",20,1.75)}</span><div><b>ACT-1184 queued for dispatch</b><p>Waiting for the control integration. No controller acknowledgement yet.</p></div></div>
<div class="tl">{row("d","Approved","Felix Whitaker","10:25:00")}{row("n","Queued","Luis Ortega","10:26:00")}{row("","Sent","","Pending")}{row("","Controller acknowledgement","","Pending")}{row("","Physical verification","","Pending")}</div></section>'''
    ap=f'''<section style="margin-top:30px"><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:6px"><span class="h2">Approval and policy</span><span style="font-size:13px;color:var(--faint)">Read only</span></div>{prow("Approval record","Felix Whitaker, 10:25 EST","Locked")}{prow("Policy checklist","3 passed, 1 after dispatch","Read only","")}</section>'''
    return f'<div class="pg">{nav2("Remote action")}{hero(PILL_Q)}{live}{ap}{demand(True)}</div>'

def sheet(kicker,title,desc,rows,tail,btns):
    rr=''.join(fr(a,b) for a,b in rows)
    return f'<div class="ov"></div><div class="sheet"><div class="gr"></div><div class="ov2">{kicker}</div><h4>{title}</h4><p>{desc}</p><div style="margin-top:12px">{rr}</div>{tail}{btns}</div>'

def s_approve(checked):
    rows=[('Equipment','EVAP-FZB-02, EVAP-FZB-03'),('Controller','CTRL-FZB-03'),('Maximum run time','30 minutes'),('Added demand','+3.5 kW'),('Policy','POL-COLD-07, Passed'),('Setpoints','Unchanged')]
    tail=f'<div class="cb"><i class="{"on" if checked else ""}">{check(16) if checked else ""}</i><span>I reviewed the equipment, limits and verification.</span></div><div class="who">Approving as <b>Felix Whitaker, Facility Operations Manager</b></div>'
    btns=f'<div class="sb"><span class="b2 s" style="width:110px">Cancel</span><span class="b2 p {"" if checked else "off"}">Approve ACT-1184{icon("arrow",18,1.75)}</span></div>'
    body=pending_body()+bar2("Reject proposal","Approve ACT-1184")
    return page3(body+sheet('ACT-1184 for EXC-2417, Frozen Zone B','Approve backup evaporator mode','Authorizes dispatch by a control-room operator. Approval does not start the equipment.',rows,tail,btns))
def s_send():
    rows=[('Controller','CTRL-FZB-03'),('Equipment','EVAP-FZB-02, EVAP-FZB-03'),('Maximum duration','30 minutes'),('Added demand','+3.5 kW'),('Approval','Felix Whitaker, 10:25 EST')]
    chips='<div style="font-size:13px;color:var(--muted);margin-top:14px">Rechecked before sending</div><div class="chips2" style="padding:8px 0 0"><span class="chip3">Permission</span><span class="chip3">Data freshness</span><span class="chip3">Approval validity</span><span class="chip3">Safety policy</span></div><div class="who" style="margin-top:14px;color:#2F5E6B">Sending does not confirm that the equipment worked. The airflow response is checked after the controller acknowledges.</div><div class="who" style="margin-top:10px">Sending as <b>Luis Ortega, Control-room Operator</b></div>'
    btns='<div class="sb"><span class="b2 s" style="width:110px">Cancel</span><span class="b2 p">Send to controller'+icon("arrow",18,1.75)+'</span></div>'
    body=approved_body()+bar2("Review approval","Send to controller",False)
    return page3(body+sheet('ACT-1184 for EXC-2417, Frozen Zone B','Send backup mode to controller?','ACT-1184 will request the approved backup sequence for Frozen Zone B.',rows,chips,btns))

def screen(bodyhtml,bar): return page3(bodyhtml+bar)
if __name__=='__main__':
    O=ROOT+'/out/'
    render(screen(pending_body(),bar2("Reject proposal","Approve ACT-1184")),O+'mr-1-pending.png',393,852,3)
    render(s_approve(False),O+'mr-2-approve-sheet.png',393,852,3)
    render(s_approve(True),O+'mr-2b-approve-sheet-checked.png',393,852,3)
    render(screen(approved_body(),bar2("Review approval","Send to controller",False)),O+'mr-3-approved.png',393,852,3)
    render(s_send(),O+'mr-4-send-sheet.png',393,852,3)
    dis='<div class="bar2"><span class="b2 s">Review approval</span><span class="b2 p" style="background:#C9D0D5;color:#fff">Dispatch pending</span></div>'
    render(screen(queued_body(),dis),O+'mr-5-queued.png',393,852,3)
