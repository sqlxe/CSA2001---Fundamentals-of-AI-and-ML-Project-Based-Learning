import os, csv, time, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(__file__))
MAPS = os.path.join(ROOT, 'maps')
out = os.path.join(ROOT, 'experiments_output.csv')
cases = [
    ('maps/small.map','astar',(0,0),(4,4)),
    ('maps/medium.map','ucs',(0,0),(9,9)),
    ('maps/large.map','bfs',(0,0),(19,19)),
    ('maps/dynamic.map','astar',(0,0),(7,11)),
    ('maps/dynamic.map','local',(0,0),(7,11)),
]
rows = []
for m,algo,start,goal in cases:
    cmd = [sys.executable, '-m', 'src.cli', '--map', m, '--algo', algo, '--start', str(start[0]), str(start[1]), '--goal', str(goal[0]), str(goal[1])]
    print('Running:', ' '.join(cmd))
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT, text=True)
    outp, err = p.communicate(timeout=20)
    t1 = time.time()
    print(outp)
    if err:
        print('ERR:', err)
    rows.append({'map':m,'algo':algo,'start':start,'goal':goal,'runtime':t1-t0,'output':outp.replace('\n',' | '),'stderr':err.replace('\n',' | ') if err else ''})
with open(out,'w',newline='',encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
print('Wrote', out)
