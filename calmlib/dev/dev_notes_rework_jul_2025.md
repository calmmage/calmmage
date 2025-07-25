# Calmlib Rework - Development Notes

## Current State Assessment

The calmlib library has grown organically and needs restructuring. Currently it contains useful utilities but has some
organizational and integration challenges that need addressing.

## Issues Identified

### 1. LLM Utilities Organization
- **Current**: Mixed between `llm.py` and `utils/llm_utils/litellm_wrapper.py`
- **Problem**: Confusing import paths, functionality scattered
- **Impact**: Found during job runner integration - imports work but structure is unclear

### 2. Missing Integration Points
- **Telegram API**: Have working Telegram/Telethon integration in separate tools
- **API Consolidation**: Should have unified API discovery (auto-detect keys, model selection)
- **Consistency**: Different tools reinvent similar patterns

### 3. Import Structure
- **Current**: Some relative imports, some absolute
- **Problem**: Breaks when used from different contexts (like job runner)
- **Need**: Consistent absolute import patterns

## Proposed Rework Plan

### Phase 1: LLM Utilities Consolidation
```python
# Target structure:
calmlib /
├── llm /
│   ├── __init__.py  # Main API exports
│   ├── providers /
│   │   ├── litellm.py  # Current litellm wrapper
│   │   ├── openai.py  # Direct OpenAI integration  
│   │   └── anthropic.py  # Direct Anthropic integration
│   ├── utils /
│   │   ├── model_selection.py  # Auto-select best/cheapest model
│   │   ├── api_discovery.py  # Auto-discover API keys
│   │   └── structured_output.py  # Pydantic integration
│   └── config.py  # Configuration management
```

### Phase 2: Telegram Integration
```python
# Move from telegram_downloader to calmlib:
calmlib /
├── telegram /
│   ├── __init__.py
│   ├── telethon_client.py  # From telegram_downloader
│   ├── pyrogram_client.py  # Alternative client
│   ├── message_downloader.py  # Core download logic
│   └── session_manager.py  # Session handling
```

### Phase 3: Unified API Patterns
```python
# Consistent patterns for:
calmlib /
├── patterns /
│   ├── __init__.py
│   ├── api_client.py  # Base API client pattern
│   ├── config_manager.py  # Configuration loading
│   ├── session_manager.py  # Session/auth management  
│   └── error_handling.py  # Consistent error patterns
```

## Implementation Strategy

### 1. LLM Utilities (Immediate - for job runner)
**Priority**: High - needed for job runner AI summarization

**Actions**:
- [ ] Consolidate `query_llm_text`, `query_llm_structured` into single module
- [ ] Add automatic model selection (prefer Claude 3.5 for speed, fallback to others)
- [ ] Add automatic API key discovery (env vars, config files)
- [ ] Improve error handling and fallbacks
- [ ] Add structured output validation

**API Goals**:
```python
from calmlib.llm import query_text, query_structured, configure

# Auto-discovers API keys, selects best model
response = query_text("Summarize this job output...")

# Structured output with Pydantic
analysis = query_structured(prompt, JobAnalysis)

# Manual configuration if needed
configure(preferred_provider="anthropic", fallback_model="gpt-4o")
```

### 2. Telegram Integration (Medium Priority)
**Priority**: Medium - useful for data collection jobs

**Actions**:
- [ ] Extract telegram client code from existing tools
- [ ] Create unified session management
- [ ] Add message filtering and processing utilities
- [ ] Integrate with existing download tools

### 3. General Cleanup (Lower Priority)
**Priority**: Low - improves developer experience

**Actions**:
- [ ] Fix all imports to be absolute
- [ ] Add comprehensive test coverage
- [ ] Improve documentation and examples
- [ ] Standardize configuration patterns

## Benefits of Rework

### For Job Runner
- **Reliable AI**: Better error handling, automatic fallbacks
- **Easy Integration**: Simple imports, auto-configuration
- **Performance**: Smart model selection (speed vs cost)

### For Telegram Tools
- **Reusability**: Shared session management, client patterns
- **Reliability**: Tested, consistent API patterns
- **Maintenance**: Centralized instead of duplicated code

### For Future Tools
- **Consistency**: Standard patterns for API clients, config, auth
- **Speed**: Pre-built utilities for common tasks
- **Reliability**: Well-tested, production-ready components

## Migration Strategy

### Backward Compatibility
- Keep existing imports working during transition
- Add deprecation warnings for old patterns
- Provide migration guide for major changes

### Testing Strategy
- Add tests for all new modules before migration
- Test existing tools still work with new structure
- Add integration tests for cross-module functionality

## TODO Comments in Code

The following locations need attention during rework:

### Job Runner Integration
```python
# In tools/local_job_runner/job_runner.py:236
# TODO: Consider updating the actual outcome in JobResult
# - AI can suggest better outcome assessment than simple heuristics
# - Should we update the JobResult.outcome based on AI analysis?
```

### LLM Model Selection
```python  
# TODO: Add automatic model selection based on:
# - Task complexity (simple vs complex analysis)
# - Speed requirements (job runner needs fast responses)
# - Cost optimization (prefer cheaper models for bulk operations)
# - API availability (fallback if primary model unavailable)
```

### Error Handling Improvements
```python
# TODO: Better error handling for:
# - API rate limits (exponential backoff)
# - Network failures (retry with different models)
# - Invalid API keys (try alternative providers)
# - Model unavailability (graceful degradation)
```

## Success Metrics

### Technical Metrics
- [ ] Import time < 500ms (currently imports are slow)
- [ ] API call reliability > 95% (with fallbacks)
- [ ] Test coverage > 90% for all LLM utilities
- [ ] Zero breaking changes for existing tools

### Usage Metrics
- [ ] Job runner AI summarization works reliably
- [ ] Telegram tools use shared calmlib components
- [ ] New tools can quickly integrate LLM/Telegram features
- [ ] Developer setup time reduced (fewer import issues)

## Timeline Estimate

- **Phase 1 (LLM)**: 1-2 weeks (high priority for job runner)
- **Phase 2 (Telegram)**: 2-3 weeks (medium priority)
- **Phase 3 (Cleanup)**: 1-2 weeks (low priority, ongoing)

**Total**: ~4-7 weeks for complete rework, but Phase 1 delivers immediate value for current job runner needs.

---

*This rework plan prioritizes immediate needs (job runner AI) while planning for long-term library organization and
reusability.*