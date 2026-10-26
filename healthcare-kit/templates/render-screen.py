import base64,os
s=open('ui8.src.html').read()
for k,n in [('__MARK__','elyra-mark.png'),('__WORD__','elyra-word.png')]:
    s=s.replace(k,'data:image/png;base64,'+base64.b64encode(open(n,'rb').read()).decode())
open('ui8.html','w').write(s)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1.6)
    for h,o in [('','main'),('#fail','fail')]:
        pg.goto('file://'+os.getcwd()+'/ui8.html'+h); pg.reload(); pg.wait_for_timeout(700)
        if o=='main':
            r=pg.evaluate('''()=>{const bad=[];document.querySelectorAll('.nav,.pill,.g>div,.btn,.field').forEach(e=>{if(e.scrollWidth>e.clientWidth+1)bad.push(e.textContent.trim().slice(0,30)+' '+e.scrollWidth+'>'+e.clientWidth)});
            const pan=document.getElementById('pan');const ch=[...pan.children];const last=ch[ch.length-1].getBoundingClientRect(), pr=pan.getBoundingClientRect();
            const g=[...pan.children].map(c=>[Math.round(c.getBoundingClientRect().top),Math.round(c.getBoundingClientRect().bottom)]);
            return {bad,panBottom:pr.bottom,lastBottom:last.bottom,g}}''')
            print(r)
        pg.screenshot(path=f'/mnt/user-data/outputs/PA-screen8-{o}.png')
    b.close()
