# Git Sync Decision Flow

## Factors Analysis

```
Factor 1: Local Changes (uncommitted)
├─ YES: Has uncommitted changes in working directory
└─ NO:  Clean working directory

Factor 2: Remote Changes (to be pulled)  
├─ YES: Remote has commits ahead of local
└─ NO:  Local is up-to-date with remote
```

## Decision Matrix

```
                    │ Remote Changes │ No Remote Changes │
                    │      YES       │        NO         │
────────────────────┼────────────────┼───────────────────┤
Local Changes: YES  │   🔥 COMPLEX   │   💾 LOCAL ONLY   │
                    │   (tricky)     │   (no action)     │
────────────────────┼────────────────┼───────────────────┤
Local Changes: NO   │   🟢 SIMPLE    │   ✅ CLEAN        │
                    │   (just pull)  │   (all good)     │
```

## Flow Implementation

### Phase 1: Simple Flows (Implement Now)

```
┌─────────────────┐
│  Git Sync Start │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Check Git Status│
│ & Remote Status │
└─────────┬───────┘
          │
          ▼
   ┌─────────────┐
   │ Has Local   │◄─── git status --porcelain
   │ Changes?    │
   └──────┬──────┘
          │
    ┌─────▼─────┐
    │    NO     │
    └─────┬─────┘
          │
          ▼
   ┌─────────────┐
   │ Has Remote  │◄─── git fetch && git rev-list HEAD..origin/main
   │ Changes?    │
   └──────┬──────┘
          │
    ┌─────▼─────┐         ┌─────▼─────┐
    │    NO     │         │    YES    │
    └─────┬─────┘         └─────┬─────┘
          │                     │
          ▼                     ▼
┌─────────────────┐    ┌─────────────────┐
│ ✅ CLEAN        │    │ 🟢 SIMPLE PULL  │
│ Status: success │    │ Create backup   │
│ Notes: "up to   │    │ → git pull      │
│ date, no action"│    │ Status: success │
└─────────────────┘    └─────────────────┘


   ┌─────▼─────┐
   │    YES    │  ◄─── Has Local Changes
   └─────┬─────┘
         │
         ▼
  ┌─────────────┐
  │ Has Remote  │
  │ Changes?    │
  └──────┬──────┘
         │
   ┌─────▼─────┐         ┌─────▼─────┐
   │    NO     │         │    YES    │
   └─────┬─────┘         └─────┬─────┘
         │                     │
         ▼                     ▼
┌─────────────────┐    ┌─────────────────┐
│ 💾 LOCAL ONLY   │    │ 🔥 COMPLEX      │
│ Status: no_change│    │ Status: requires│
│ Notes: "local   │    │ _attention      │
│ changes present,│    │ Notes: "both    │
│ no remote updt" │    │ local & remote  │
└─────────────────┘    │ changes - TODO" │
                       └─────────────────┘
```

### Phase 2: Complex Flow (Future Implementation)

```
🔥 COMPLEX Case: Both local AND remote changes

┌─────────────────┐
│ Create backup   │
│ branch with     │
│ timestamp       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ git stash push  │
│ (save local)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ git pull        │
│ (get remote)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ git stash pop   │
│ (restore local) │
└─────────┬───────┘
          │
    ┌─────▼─────┐
    │ Conflicts?│
    └─────┬─────┘
          │
    ┌─────▼─────┐         ┌─────▼─────┐
    │    NO     │         │    YES    │
    └─────┬─────┘         └─────┬─────┘
          │                     │
          ▼                     ▼
┌─────────────────┐    ┌─────────────────┐
│ ✅ SUCCESS      │    │ ⚠️  CONFLICTS   │
│ Auto-resolved   │    │ Manual resolve  │
│ merge conflicts │    │ required        │
└─────────────────┘    └─────────────────┘
```

## Backup Branch Strategy

```
Branch name format: daily-snapshots/{YYYY-MM-DD}
If exists: daily-snapshots/{YYYY-MM-DD}-{N}

Examples:
- daily-snapshots/2025-07-28
- daily-snapshots/2025-07-28-1  (if first exists)
- daily-snapshots/2025-07-28-2  (if both exist)
```

## Implementation Plan

1. ✅ **Phase 1a**: CLEAN case (no local, no remote changes)
2. ✅ **Phase 1b**: SIMPLE PULL case (no local, has remote changes)  
3. ✅ **Phase 1c**: LOCAL ONLY case (has local, no remote changes)
4. ⏳ **Phase 1d**: COMPLEX case placeholder (warning message)
5. 🔄 **Phase 2**: Implement complex stash-based flow (future)

## Error Handling

- Git command failures → FINAL STATUS: fail
- Network issues during fetch → FINAL STATUS: fail  
- Backup branch creation issues → FINAL STATUS: fail
- Stash conflicts (Phase 2) → FINAL STATUS: requires_attention