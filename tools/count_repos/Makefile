# Count Repos Tool
# Count and analyze repositories across workspace

.PHONY: help install test count stats analyze

PYTHON := python3
SCRIPT := repo_stats.py
SHELL_SCRIPT := count_repos.sh

help:
	@echo "📊 Count Repos Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo ""
	@echo "Repository Analysis:"
	@echo "  make count          - Count repositories in workspace"
	@echo "  make count PATH=/custom/path - Count repos in custom path"
	@echo "  make stats          - Generate detailed repository statistics"
	@echo "  make analyze        - Run comprehensive repository analysis"
	@echo ""
	@echo "Shell Interface:"
	@echo "  make count-shell    - Use shell script for counting"
	@echo "  make stats-shell    - Use shell script for statistics"
	@echo ""
	@echo "Output Formats:"
	@echo "  make count-json     - Output results in JSON format"
	@echo "  make count-csv      - Output results in CSV format"
	@echo ""
	@echo "Examples:"
	@echo "  make count"
	@echo "  make count PATH=~/work/projects"  
	@echo "  make stats > repo_report.txt"

install:
	@echo "📦 Count Repos dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Count Repos tool..."
	@uv run python $(SCRIPT) --help > /dev/null 2>&1 && echo "✅ Python script working!" || echo "⚠️  Check script implementation"
	@bash $(SHELL_SCRIPT) --help > /dev/null 2>&1 && echo "✅ Shell script working!" || echo "⚠️  Check shell script"

# Main counting commands
count:
	@if [ -n "$(PATH)" ]; then \
		echo "📊 Counting repositories in: $(PATH)"; \
		uv run python $(SCRIPT) --path "$(PATH)"; \
	else \
		echo "📊 Counting repositories in workspace..."; \
		uv run python $(SCRIPT); \
	fi

stats:
	@echo "📈 Generating detailed repository statistics..."
	@uv run python $(SCRIPT) --detailed --stats

analyze:
	@echo "🔍 Running comprehensive repository analysis..."
	@uv run python $(SCRIPT) --analyze --detailed

# Shell script interface  
count-shell:
	@echo "📊 Counting repositories via shell script..."
	@bash $(SHELL_SCRIPT)

stats-shell:
	@echo "📈 Repository statistics via shell script..."
	@bash $(SHELL_SCRIPT) --stats

# Output formats
count-json:
	@echo "📊 Counting repositories (JSON output)..."
	@uv run python $(SCRIPT) --format json

count-csv:
	@echo "📊 Counting repositories (CSV output)..."
	@uv run python $(SCRIPT) --format csv

count-table:
	@echo "📊 Counting repositories (table output)..."
	@uv run python $(SCRIPT) --format table

# Filtering options
count-git-only:
	@echo "📊 Counting only Git repositories..."
	@uv run python $(SCRIPT) --git-only

count-active:
	@echo "📊 Counting recently active repositories..."
	@uv run python $(SCRIPT) --active-only

count-by-language:
	@echo "📊 Counting repositories by programming language..."
	@uv run python $(SCRIPT) --by-language

# Environment-specific counts
count-experiments:
	@echo "📊 Counting repositories in experiments..."
	@make count PATH=../../experiments

count-projects:
	@echo "📊 Counting repositories in projects..."
	@make count PATH=../../projects

count-archive:
	@echo "📊 Counting repositories in archive..."
	@make count PATH=../../archive

# Quick reports
quick-report:
	@echo "⚡ Quick repository report..."
	@echo "==========================="
	@echo ""
	@echo "📁 Total repositories:"
	@make count | grep -E "Total|Found" || echo "  (count not available)"
	@echo ""
	@echo "📈 By location:"
	@echo "  Experiments: $$(make count-experiments 2>/dev/null | grep -o '[0-9]\+' | head -1 || echo 'N/A')"
	@echo "  Projects: $$(make count-projects 2>/dev/null | grep -o '[0-9]\+' | head -1 || echo 'N/A')"
	@echo "  Archive: $$(make count-archive 2>/dev/null | grep -o '[0-9]\+' | head -1 || echo 'N/A')"

detailed-report:
	@echo "📊 Detailed repository report..."
	@echo "=============================="
	@make stats
	@echo ""
	@echo "📈 Analysis by location:"
	@echo ""
	@echo "🧪 Experiments:"
	@make count-experiments
	@echo ""
	@echo "📁 Projects:"  
	@make count-projects
	@echo ""
	@echo "📦 Archive:"
	@make count-archive

# Export reports
export-report:
	@echo "📤 Exporting repository report..."
	@make detailed-report > repo_report_$$(date +%Y%m%d_%H%M%S).txt
	@echo "✅ Report exported!"

export-json:
	@echo "📤 Exporting JSON report..."
	@make count-json > repo_data_$$(date +%Y%m%d_%H%M%S).json
	@echo "✅ JSON data exported!"

# Configuration (if needed)
show-config:
	@echo "⚙️  Count Repos Configuration:"
	@if [ -f sample.env ]; then \
		echo "📄 Sample environment: sample.env"; \
		cat sample.env; \
	else \
		echo "❌ No configuration files found"; \
	fi

# Development helpers
dev-test:
	@echo "🧪 Running development tests..."
	@echo "Testing with current directory..."
	@make count PATH=. > /tmp/count_test.log
	@echo "✅ Development test completed"

# Statistics about the tool itself
tool-stats:
	@echo "📊 Count Repos Tool Statistics:"
	@echo "Python script: $$([ -f $(SCRIPT) ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Shell script: $$([ -f $(SHELL_SCRIPT) ] && echo '✅ Present' || echo '❌ Missing')" 
	@echo "Config files: $$(ls -1 *.env 2>/dev/null | wc -l || echo 0)"
	@echo "Script size: $$([ -f $(SCRIPT) ] && wc -l < $(SCRIPT) || echo 0) lines"

# Clean up
clean:
	@echo "🧹 Cleaning up temporary files..."
	@rm -f /tmp/count_test.log
	@rm -f repo_report_*.txt
	@rm -f repo_data_*.json
	@echo "✅ Cleanup complete!"