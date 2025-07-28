# AI Instructions Tool Makefile
# Deploy AI instructions to current project

CLI_PATH = tools/ai_instructions_tool/cli.py

# Default target
.PHONY: help
help:
	@echo "AI Instructions Tool - Deploy AI instructions to current project"
	@echo ""
	@echo "Usage:"
	@echo "  make deploy              Interactive deployment (select tools)"
	@echo "  make deploy-all          Deploy all AI tools (claude, cursor, gemini)"
	@echo "  make deploy-claude       Deploy Claude instructions only"
	@echo "  make deploy-cursor       Deploy Cursor rules only"
	@echo "  make deploy-gemini       Deploy Gemini instructions only"
	@echo "  make list                List available templates"
	@echo ""
	@echo "Instruction Modes:"
	@echo "  make deploy-slim         Deploy with minimal instructions"
	@echo "  make deploy-optimal      Deploy with optimal instructions (default)"
	@echo "  make deploy-full         Deploy with all instructions"
	@echo ""
	@echo "Custom Rules Position:"
	@echo "  make deploy-custom-end   Deploy with custom rules at the end"
	@echo ""
	@echo "Options:"
	@echo "  make deploy-all-no-tech  Deploy without tech stack information"
	@echo ""
	@echo "Examples:"
	@echo "  make deploy              # Interactive mode - choose which tools"
	@echo "  make deploy-claude       # Just add CLAUDE.md to current directory"
	@echo "  make deploy-all          # Add all instruction files"

# Interactive deployment
.PHONY: deploy
deploy:
	uv run typer $(CLI_PATH) run deploy --interactive

# Deploy all tools
.PHONY: deploy-all
deploy-all:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --no-interactive

# Deploy specific tools
.PHONY: deploy-claude
deploy-claude:
	uv run typer $(CLI_PATH) run deploy --tool claude --no-interactive

.PHONY: deploy-cursor
deploy-cursor:
	uv run typer $(CLI_PATH) run deploy --tool cursor --no-interactive

.PHONY: deploy-gemini
deploy-gemini:
	uv run typer $(CLI_PATH) run deploy --tool gemini --no-interactive

# Deploy with different instruction modes
.PHONY: deploy-slim
deploy-slim:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --mode slim --no-interactive

.PHONY: deploy-optimal
deploy-optimal:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --mode optimal --no-interactive

.PHONY: deploy-full
deploy-full:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --mode full --no-interactive

# Deploy with custom rules at different positions
.PHONY: deploy-custom-end
deploy-custom-end:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --custom-position end --no-interactive

# Deploy without tech stack
.PHONY: deploy-all-no-tech
deploy-all-no-tech:
	uv run typer $(CLI_PATH) run deploy --tool claude --tool cursor --tool gemini --no-tech-stack --no-interactive

# List available templates
.PHONY: list
list:
	uv run typer $(CLI_PATH) run list-templates

# Development targets
.PHONY: test-cli
test-cli:
	@echo "Testing CLI tool..."
	uv run typer $(CLI_PATH) run --help

.PHONY: check-templates
check-templates:
	@echo "Checking template files..."
	@ls -la resources/llm_prompts/ai_tools/
	@echo ""
	@ls -la resources/llm_prompts/tech_stack/