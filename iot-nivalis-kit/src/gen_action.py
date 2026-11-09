s=open('incident.py').read()
cut=s.index("    lk=[('Hypothesis'")
head=s[:cut]
eq=open('/home/claude/nivalis/tail_equip.txt').read()
a=eq.index('    css+="""')
b=eq.index('"""\n',a+14)
cssblock=eq[a:b+4]
tail=open('/home/claude/nivalis/tail_action.txt').read()
open('action.py','w').write(head+cssblock+tail)
