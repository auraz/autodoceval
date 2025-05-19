.PHONY: all generate grade improve clean

# Default input file
FILE ?= docs/sample.md

all: generate grade improve
	@echo "✅ Closed loop completed: see output in docs/$(basename $(notdir $(FILE)))_improved.md"

generate:
	@echo "▶️ Running generate_qa.py with $(FILE)"
	@python scripts/generate_qa.py $(FILE)

grade:
	@echo "▶️ Running grade_docs.py with $(FILE)" 
	@python scripts/grade_docs.py $(FILE)

improve:
	@echo "▶️ Running improve_docs.py with $(FILE)"
	@python scripts/improve_docs.py $(FILE)

clean:
	@rm -f data/questions.jsonl
	@rm -f results/scores.json
	@rm -f docs/*_improved.md
	@echo "✅ Cleaned up generated files"