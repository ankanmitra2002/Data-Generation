import subprocess
scripts = ['multiUserMaximize.py','heuristic_destination_time.py', 'heuristic_groups.py', 'heuristic_mix.py']

processes = []
for script in scripts:
    print(f"Starting {script}...")
    p = subprocess.Popen(['python', script])
    processes.append(p)

for p in processes:
    p.wait()
