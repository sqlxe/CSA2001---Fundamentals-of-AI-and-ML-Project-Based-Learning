import subprocess, sys, os, time
ROOT = os.path.dirname(os.path.dirname(__file__))
cases = [
    (['-m','src.cli','--map','maps/small.map','--algo','astar','--start','0','0','--goal','4','4'],'A* on Small Map'),
    (['-m','src.cli','--map','maps/medium.map','--algo','ucs','--start','0','0','--goal','9','9'],'UCS on Medium Map'),
    (['-m','src.cli','--map','maps/large.map','--algo','bfs','--start','0','0','--goal','19','19'],'BFS on Large Map'),
    (['-m','src.cli','--map','maps/dynamic.map','--algo','astar','--start','0','0','--goal','7','11'],'Dynamic A*'),
    (['-m','src.cli','--map','maps/dynamic.map','--algo','local','--start','0','0','--goal','7','11'],'Local on Dynamic'),
]
ok = True
for args,desc in cases:
    cmd = [sys.executable] + args
    print('RUNNING', desc, '->', ' '.join(cmd))
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out,err = p.communicate(timeout=10)
    print('STDOUT:\n', out)
    if err:
        print('STDERR:\n', err)
    if p.returncode != 0:
        ok = False
print('OK' if ok else 'FAILED')
