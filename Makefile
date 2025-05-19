.PHONY: all grade improve compare auto-improve clean

# Default input file
FILE ?= docs/sample.md

all: grade improve
	@echo "✅ Closed loop completed: see output in docs/$(basename $(notdir $(FILE)))_improved.md"

grade:
	@echo "▶️ Running grade_docs.py with $(FILE)"
	@python scripts/grade_docs.py $(FILE)

improve:
	@echo "▶️ Running improve_docs.py with $(FILE)"
	@python scripts/improve_docs.py $(FILE)

compare:
	@echo "▶️ Comparing documents"
	@python scripts/compare_docs.py $(FILE) $(dir $(FILE))$(basename $(notdir $(FILE)))_improved.md

auto-improve:
	@echo "▶️ Running auto-improvement loop (max 3 iterations, target 70% quality)"
	@python scripts/auto_improve.py $(FILE)

clean:
	@rm -f docs/*_improved.md
	@rm -f results/*_scores.json
	@echo "✅ Cleaned up generated files"
