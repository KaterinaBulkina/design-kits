s=open('incident.py').read()
cut=s.index("    lk=[('Hypothesis'")
head=s[:cut]
head=head.replace("on' if n=='Incidents' else ''","X")  # no-op safeguard
head=head.replace('"on" if n=="Incidents" else ""','"on" if n=="Refrigeration" else ""')
tail=open('/home/claude/nivalis/tail_equip.txt').read()
open('equip.py','w').write(head+tail)
