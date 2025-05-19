import subprocess

print("▶️ Running generate_qa.py")
subprocess.run(["python", "scripts/generate_qa.py"], check=True)

print("▶️ Running grade_docs.py")
subprocess.run(["python", "scripts/grade_docs.py"], check=True)

print("▶️ Running improve_docs.py")
subprocess.run(["python", "scripts/improve_docs.py"], check=True)

print("✅ Closed loop completed: see docs/sample_improved.md")
