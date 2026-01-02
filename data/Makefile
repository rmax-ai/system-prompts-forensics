# Makefile to generate system prompt analysis from JSON payloads
SHELL := /bin/bash

SEED := 20260102
PAYLOAD := $(wildcard payload/*.json)
ANALYSIS := $(patsubst payload/%.json,analysis/%.analysis.yaml,$(PAYLOAD))
GOVERNANCE := $(patsubst payload/%.json,governance/%.json,$(PAYLOAD))

# Use GPT-5.2 for final analysis and GPT-4.1 for testing/debugging
ANALYSIS_MODEL ?= gpt-5.2
DRY_RUN ?= true
DRY_RUN_FLAG := $(if $(filter true,$(DRY_RUN)),--dry-run,)

.PHONY: all clean analyze assistant-reports governance
all: analyze governance primitives.registry.json similarities.csv band-report.csv prompt-families.csv prompt-families-report.md .assistant-reports.stamp final-comparative-report.md final-research-report.md appendix-governance-primitives.md

analyze: $(ANALYSIS)

governance: $(GOVERNANCE)

similarities.csv: $(ANALYSIS)
	uv run --locked scripts/prompt-similarity.py analysis/*.analysis.yaml $(DRY_RUN_FLAG) --csv $@

band-report.csv: similarities.csv
	uv run --locked scripts/band-report-from-csv.py $< $(DRY_RUN_FLAG) --step 0.01 --csv $@

prompt-families.csv: similarities.csv band-report.csv prompts/analyze-prompt-families.md
	uv run --locked scripts/prompt-family-analysis.py \
		--prompt prompts/analyze-prompt-families.md \
		--similarities similarities.csv \
		--bands band-report.csv \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

prompt-families-report.md: prompt-families.csv prompts/prompt-families.prompt.md
	uv run --locked scripts/prompt-families-interpretation.py \
		--prompt prompts/prompt-families.prompt.md \
		--families $< \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

assistant-reports: .assistant-reports.stamp

.assistant-reports.stamp: $(ANALYSIS) prompts/final-assistant-analysis.prompt.md
	uv run --locked scripts/final-assistant-analysis.py \
		--prompt prompts/final-assistant-analysis.prompt.md \
		--analysis-dir analysis \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output-dir .
	@touch $@

final-comparative-report.md: prompt-families-report.md ../methodology.md ../goal.md prompts/final-comparative-analysis-prompt.md
	uv run --locked scripts/final-comparative-analysis.py \
		--prompt prompts/final-comparative-analysis-prompt.md \
		--analysis-dir analysis \
		--similarities similarities.csv \
		--bands band-report.csv \
		--families prompt-families.csv \
		--family-report prompt-families-report.md \
		--methodology ../methodology.md \
		--goal ../goal.md \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

final-research-report.md: .assistant-reports.stamp ../goal.md prompts/final-research-report.prompt.md
	uv run --locked scripts/final-research-report.py \
		--prompt prompts/final-research-report.prompt.md \
		--assistants final-report-*.md \
		--goal ../goal.md \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

appendix-governance-primitives.md: final-research-report.md primitives.registry.json prompts/governance-primitives-appendix.prompt.md
	uv run --locked scripts/governance-primitives-appendix.py \
		--prompt prompts/governance-primitives-appendix.prompt.md \
		--report $< \
		--registry primitives.registry.json \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

analysis/%.analysis.yaml: payload/%.json
	@mkdir -p $(dir $@)
	uv run --locked scripts/system-prompt-analysis.py \
		--prompt ./prompts/normalize-system-prompt.md \
		--schema ./schema/system-prompt.v0.yaml \
		--invocation $< \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

governance/%.json: payload/%.json scripts/governance-primitive-extract.py prompts/governance-primitive-extraction.prompt.md
	@mkdir -p $(dir $@)
	uv run --locked scripts/governance-primitive-extract.py \
		--prompt prompts/governance-primitive-extraction.prompt.md \
		--payload $< \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

primitives.registry.json: $(GOVERNANCE) scripts/governance-primitives-reduce.py prompts/governance-primitives-reducer.prompt.md
	uv run --locked scripts/governance-primitives-reduce.py \
		--prompt prompts/governance-primitives-reducer.prompt.md \
		--inputs governance/*.json \
		$(DRY_RUN_FLAG) \
		--model $(ANALYSIS_MODEL) \
		--output $@

clean:
	@rm -f analysis/*.analysis.yaml governance/*.json primitives.registry.json similarities.csv band-report.csv prompt-families.csv prompt-families-report.md final-comparative-report.md final-research-report.md final-report-*.md appendix-governance-primitives.md .assistant-reports.stamp
	@echo "Cleaned analysis files, governance files, primitives.registry.json, similarities.csv, band-report.csv, prompt-families.csv, prompt-families-report.md, final-comparative-report.md, final-research-report.md, assistant reports, and appendix"
