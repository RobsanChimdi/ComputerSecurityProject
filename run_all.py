import subprocess
import sys

def run_script(name):
    print(f"\n{'='*60}")
    print(f"RUNNING: {name}")
    print('='*60)
    result = subprocess.run([sys.executable, name], capture_output=False)
    return result

if __name__ == "__main__":
    scripts = ["demo.py", "attack_demo.py", "secure_ecc.py", "performance_test.py"]
    
    for script in scripts:
        try:
            run_script(script)
            input("\nPress Enter to continue...")
        except FileNotFoundError:
            print(f"Error: {script} not found. Run ecc.py first.")
            break