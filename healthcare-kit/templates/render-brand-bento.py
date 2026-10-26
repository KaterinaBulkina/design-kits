import base64,os
s=open('brand.src.html').read()
for k,n in [('__MARK__','elyra-mark.png'),('__WORD__','elyra-word.png')]:
    s=s.replace(k,'data:image/png;base64,'+base64.b64encode(open(n,'rb').read()).decode())
open('brand.html','w').write(s)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':936},device_scale_factor=2560/1440)
    pg.goto('file://'+os.getcwd()+'/brand.html'); pg.wait_for_timeout(900)
    print(pg.evaluate('''()=>{const r=[];document.querySelectorAll('.chip,.serif,.sc div').forEach(e=>{if(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+2)r.push(e.textContent.trim().slice(0,25)+' '+e.scrollWidth+'x'+e.scrollHeight+' / '+e.clientWidth+'x'+e.clientHeight)});return r}'''))
    pg.screenshot(path='/mnt/user-data/outputs/PA-brand-bento.png'); b.close()
