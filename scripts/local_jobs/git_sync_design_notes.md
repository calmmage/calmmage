# Git Sync Automation - Design Challenges

## User Requirements and Concerns

**Direct user quote:**
> "if there are uncommitted changes, I want those changes to be applied on top of the pulled version (basically rebase). But if we just call rebase, we might find ourselves in a merge state which we need to manually resolve - which is not what I want to have here."

**Direct user quote:**
> "I don't want for example to automatically commit and push because who knows maybe I forgot to gitignore something and maybe there are sensitive data and maybe whatnot. Therefore, for such automations we need to run an AI analysis of potential leaks or tokens or passwords or whatever."

**Direct user quote:**
> "Another tricky layer here is that we are running the AI updater, and therefore we are running like we are having changes in our repo at least to gitignore from the beginning. So we will always kind of have changes, and what do we do with them?"

## Complex Scenarios to Handle

### 1. The AI Instructions Problem
- AI instructions sync creates/updates `.gitignore` files
- This means repos ALWAYS have changes after AI sync
- Git sync runs after AI sync → always dealing with uncommitted changes
- Risk: Auto-committing AI-generated changes without review

### 2. Security Concerns
- Auto-commit might include sensitive data
- Need AI analysis for potential leaks (tokens, passwords, keys)
- Risk of forgetting to gitignore sensitive files
- Push vs no-push dilemma: both have risks

### 3. Rebase Complexity
**User's proposed flow:**
1. Create temp branch
2. Commit changes there
3. Switch back to original branch  
4. Pull origin
5. Apply changes back (non-commit cherry-pick style)

**Problems with this approach:**
- Step 5 is basically a rebase operation anyway
- Still risk of merge conflicts requiring manual resolution
- Complex state management across branches

## Potential Solutions

### Option A: Conservative Approach
```python
def git_sync_conservative():
    """Ultra-safe git sync - just pull, no auto-commit"""
    if has_uncommitted_changes():
        print("⚠️ FINAL STATUS: requires_attention - Uncommitted changes present")
        print("📝 FINAL NOTES: Manual intervention needed, run git stash/commit first")
        return
    
    # Only pull if clean working directory
    git_pull()
```

### Option B: Stash-Based Approach  
```python
def git_sync_with_stash():
    """Safer approach using git stash"""
    if has_uncommitted_changes():
        # Stash changes
        git_stash_push()
        git_pull()
        # Try to apply stash back
        if git_stash_pop_conflicts():
            print("🎯 FINAL STATUS: requires_attention - Merge conflicts after pull")
            return
    else:
        git_pull()
```

### Option C: AI-Assisted Commit Analysis
```python
def git_sync_with_ai_analysis():
    """Analyze changes before committing"""
    if has_uncommitted_changes():
        changes = get_git_diff()
        
        # AI analysis for sensitive data
        if contains_sensitive_data(changes):
            print("🎯 FINAL STATUS: requires_attention - Potential sensitive data detected")
            return
            
        # AI-generated changes vs manual changes
        if is_ai_generated_only(changes):
            auto_commit_ai_changes()
        else:
            print("🎯 FINAL STATUS: requires_attention - Manual changes require review")
            return
    
    git_pull()
```

## Recommended Approach

Given the complexity and risks, I recommend starting with **Option A (Conservative)**:

1. **Phase 1**: Only sync clean repos (no uncommitted changes)
2. **Phase 2**: Add stash-based approach after testing
3. **Phase 3**: Consider AI analysis for auto-commit decisions

This teaches good git hygiene while avoiding automation pitfalls.

## AI Instructions Integration Issue

**Problem**: AI instructions sync always creates changes, git sync always finds uncommitted changes

**Solutions**:
1. **Separate timing**: Run AI sync and git sync on different schedules
2. **Integrated workflow**: AI sync includes its own commit/push logic
3. **Skip AI-only changes**: Git sync recognizes and auto-commits AI-generated files

## Question About Custom Rules

> "what happens if there is no custom rules? Did you account for that?"

In current AI instructions sync:
```python
def should_deploy_ai_instructions(project_path: Path) -> bool:
    # Skip if project already has custom LLM_RULES.md
    if (project_path / "LLM_RULES.md").exists():
        return False  # ✅ Correctly skips
```

**Answer**: Yes, if no `LLM_RULES.md` exists, it deploys base templates. If `LLM_RULES.md` exists, it skips deployment entirely. The AI instructions tool itself handles missing custom rules gracefully by using only base templates.