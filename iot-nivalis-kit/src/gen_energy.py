s=open('incident.py').read()
cut=s.index("    lk=[('Hypothesis'")
head=s[:cut]
head=head.replace('"on" if n=="Incidents" else ""','"on" if n=="Energy" else ""')
eq=open('/home/claude/nivalis/tail_equip.txt').read()
a=eq.index('    css+="""')
b=eq.index('"""\n',a+14)
cssblock=eq[a:b+4]
tail=open('/home/claude/nivalis/tail_energy.txt').read()
open('energy.py','w').write(head+cssblock+tail)
