# ENCT Version & Changelog

**Current Version:** v1.3.0  
**Release Date:** 2026-04-05  
**Status:** Phase 1 Design Baseline

---

## Versioning Scheme

ENCT uses **Semantic Versioning (SemVer)** format: `MAJOR.MINOR.PATCH`

### Version Component Meaning

| Component | When to Increment | Example |
| --- | --- | --- |
| **MAJOR** | Axiom changes, fundamental Loop restructuring, base indicator set changes | v1.3.0 → v2.0.0 (breaking change) |
| **MINOR** | New domain added, new indicator (non-base), domain threshold tightened | v1.3.0 → v1.4.0 (additive feature) |
| **PATCH** | Bug fixes, typos in docs, confidence gate tweak (0.70 → 0.71) | v1.3.0 → v1.3.1 (minor fix) |

### Change Classification

**MAJOR (Breaking):**
- Override or disable an axiom
- Modify 5-phase Loop structure
- Change four primitives definitions
- Remove or fundamentally alter indicator

**MINOR (Compatible):**
- Add new domain
- Add new metric/indicator (extension)
- Tighten gate threshold (e.g., confidence 0.7 → 0.75)
- Add new verification method

**PATCH (Bugfix):**
- Fix gate enforcement bug
- Correct documentation error
- Adjust threshold by <0.05 (minor tweak)
- Performance optimization

---

## Changelog

### v1.3.0 — 2026-04-05 (Phase 1 Design Baseline)

**Status:** Complete — Phase 1 Design ready for Phase 2 Training

**New:**
- ENCT v1.3 framework established: 4 primitives, 4 axioms, 5-phase Loop
- 8 quantitative indicators defined (Compliance Rate, Homeostasis Score, etc.)
- 4 verification approaches specified (model checking, sandbox, audit, red-team)
- 7 defined domains: Authentication, API Rate Limiting, Data Validation, Access Control, Audit Logging, Performance, Compliance
- Autonomy Gates specification: confidence thresholds, domain boundaries, rate limits
- LLM-Assisted Bootstrap Pattern framework (CandidateModule, quality gates, sandbox)

**Modified:**
- None (baseline release)

**Removed:**
- None (baseline release)

**Known Issues:**
- None (baseline release)

**Upcoming in v1.4.0:**
- Additional domains (Data Retention, API Security)
- New indicator: Policy Success Rate
- Audit agent implementation (Phase 4)

---

## Axiom Version Tracking

Each axiom has its own version for independent evolution:

### Axiom 1 (Immutability)
**Current Version:** v1.3.0  
**Definition:** Foundational rules (axioms, primitives, Loop structure, base indicators) are immutable  
**Enforcement:** Pre-commit hook, CI gate  
**Last Changed:** 2026-04-05 (baseline)  

### Axiom 2 (Determinism)
**Current Version:** v1.3.0  
**Definition:** Same input + state → same output (within uncertainty bounds)  
**Enforcement:** Test suite, reproducibility checks  
**Last Changed:** 2026-04-05 (baseline)  

### Axiom 3 (Enforcement)
**Current Version:** v1.3.0  
**Definition:** All constraints mechanically enforced (no soft enforcement)  
**Enforcement:** Linters, CI/CD gates, runtime checks  
**Last Changed:** 2026-04-05 (baseline)  

### Axiom 4 (Resilience)
**Current Version:** v1.3.0  
**Definition:** Adaptations are versioned, auditable, reversible  
**Enforcement:** Git tracking, CHANGELOG updates, rollback procedures  
**Last Changed:** 2026-04-05 (baseline)  

---

## Indicator Version Tracking

### Base Indicator Set (Immutable per Axiom 1)
- Compliance Rate (v1.3.0)
- Homeostasis Score (v1.3.0)
- Traceability Coverage (v1.3.0)
- Bootstrap Confidence Avg (v1.3.0)
- Adaptation Resilience (v1.3.0)
- Provenance Overhead (v1.3.0)
- Axiom Violation Rate (v1.3.0)
- Policy Rollback Rate (v1.3.0)

**Extensions (can be added without breaking change):**
- (None yet in v1.3.0)

---

## Domain Version Tracking

### Defined Domains (v1.3.0)

| Domain | Version | Confidence Gate | Approval Authority |
| --- | --- | --- | --- |
| Authentication | v1.3.0 | >0.75 | Security team |
| API Rate Limiting | v1.3.0 | >0.70 | Ops team |
| Data Validation | v1.3.0 | >0.70 | Product team |
| Access Control | v1.3.0 | >0.75 | Security team |
| Audit Logging | v1.3.0 | >0.70 | Compliance team |
| Performance | v1.3.0 | >0.65 | Ops team |
| Compliance & Governance | v1.3.0 | >0.80 | Legal team |

**Pending Domains (planned for v1.4.0):**
- Data Retention (Legal, Compliance)
- API Security (Security)

---

## Release Tagging Convention

All releases are tagged in Git:

```bash
git tag -a v1.3.0-phase1-complete -m "Phase 1 Design complete"
git tag -a v1.3.0-phase2-complete -m "Phase 2 Training complete"
git tag -a v1.3.0-phase3-complete -m "Phase 3 Testing complete"
git tag -a v1.3.0-phase4-release -m "Phase 4 Deployment released"
git tag -a v1.3.0-phase5-golive -m "Phase 5 Monitoring go-live"
```

**Viewing tags:**
```bash
git log --oneline --decorate | head -10  # Shows tagged commits
git tag --list v1.3.*                     # Lists all v1.3 tags
```

---

## Compatibility Matrix

Which versions are compatible?

| Version | Phase | Bootstrap Pattern | Loop Cycles | Axioms | Domains | Compatible With |
| --- | --- | --- | --- | --- | --- | --- |
| v1.3.0 | 1–5 | ✓ Implemented | ✓ 5-phase | ✓ All 4 | ✓ 7 | Itself only (baseline) |
| v1.4.0 | Planned | ✓ Enhanced | ✓ 5-phase | ✓ All 4 | ✓ 9 (2 new) | v1.3.x (minor bump) |
| v2.0.0 | Future | ✓ Redesign | ? Maybe | ? Maybe | TBD | Not compatible with v1.x |

**Rollback Compatibility:**
- v1.3.1 → v1.3.0: Yes (patch rollback)
- v1.4.0 → v1.3.0: Yes (minor rollback, may lose new domain data)
- v2.0.0 → v1.3.x: No (major breaking change)

---

## Bootstrap Policy Version Tracking

Every bootstrapped policy carries version metadata:

```json
{
  "policy_id": "auth_pwd_complexity_v1",
  "policy_version": "v1.0.0",
  "enct_version": "v1.3.0",
  "bootstrap_date": "2026-04-10T14:32:00Z",
  "domain": "Authentication",
  "axiom_versions": {
    "axiom_1": "v1.3.0",
    "axiom_2": "v1.3.0",
    "axiom_3": "v1.3.0",
    "axiom_4": "v1.3.0"
  },
  "indicator_versions": [
    "compliance_rate@v1.3.0",
    "homeostasis_score@v1.3.0",
    "bootstrap_confidence@v1.3.0"
  ]
}
```

**Why:** If ENCT is upgraded from v1.3.0 to v1.4.0, the policy's validation results can be replayed using the same ENCT version it was created with.

---

## Upgrade Path

### Phase 2 → v1.3.1 (Bugfix)
- No breaking changes to v1.3.0
- Code optimizations, documentation fixes
- All v1.3.0 policies remain valid

### Phase 3 → v1.4.0 (Minor Enhancement)
- Add 2 new domains (Data Retention, API Security)
- Add new indicator: Policy Success Rate
- All v1.3.0 policies still work
- New policies can target new domains

### Phase 5 → v2.0.0 (Major Redesign)
- If fundamental Loop changes needed
- All v1.x policies must be re-validated
- Major version bump, incompatible with v1.x

---

## Version Pinning in Phase Rollouts

Each ALM phase pins a version:

| Phase | Version | Reason |
| --- | --- | --- |
| Phase 1 (Design) | v1.3.0 | Baseline |
| Phase 2 (Training) | v1.3.0 | Code implements v1.3.0 spec |
| Phase 3 (Testing) | v1.3.0 | Verification tests v1.3.0 axioms |
| Phase 4 (Deploy) | v1.3.0 | Release package is v1.3.0 |
| Phase 5 (Monitor) | v1.3.0+ | May patch to v1.3.1 for bugs; v1.4.0 after optimization |

**Why:** Prevents version creep during a phase. Each phase completes against a single version. Upgrades happen between phases.

---

## Version History Log

Executed git tag commands:

```
2026-04-05 10:00 UTC  git tag -a v1.3.0-phase1-complete
                      "Phase 1 Design baseline"
                      → HE-SCOPE.md, HE-CLUES.md, HE-PRIORITIES.md, 
                        HE-IMPLEMENTATION-PLAN.md all created and committed
```

(Subsequent phase completions will be tagged here)

---

## Accessing Past Versions

To checkout an old version for inspection or rollback:

```bash
# View Phase 1 baseline
git checkout v1.3.0-phase1-complete

# List all files at that version
git ls-tree -r --name-only HEAD

# Compare current vs Phase 1
git diff v1.3.0-phase1-complete HEAD

# Rollback entire repo to Phase 1
git reset --hard v1.3.0-phase1-complete  # WARNING: Destructive

# Restore single file from Phase 1
git checkout v1.3.0-phase1-complete -- ENCT-REFERENCE.md
```

---

## Summary

**ENCT v1.3.0:**
- ✓ Baseline established and tagged
- ✓ All components versioned (axioms, indicators, domains, bootstrap policies)
- ✓ Rollback procedures documented
- ✓ Upgrade path to v1.4.0 planned
- ✓ Phase-specific versions pinned
- ✓ Changelog maintained per convention

**Next:** Phase 2 → v1.3.0 (code implementation), Phase 3 → v1.3.0 (testing), Phase 4 → v1.3.0 (deployment), Phase 5 → v1.3.0+ (production optimization, possible v1.3.1 patches or v1.4.0 upgrade)
