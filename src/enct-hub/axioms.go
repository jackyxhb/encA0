package main

type AxiomQuestion struct {
	ID      int
	Text    string
	Options []string
}

var Axioms = []AxiomQuestion{
	{
		ID:   1,
		Text: "Does this policy attempt to override or modify the foundational ENCT primitives or the 5-phase loop structure? (Axiom 1)",
		Options: []string{"No, it follows foundational rules", "Yes, it modifies the core loop (Violation)"},
	},
	{
		ID:   2,
		Text: "Are the outcomes of this policy deterministic and bounded by declared uncertainty intervals? (Axiom 2)",
		Options: []string{"Yes, results are reproducible", "No, outcomes are random/unbounded (Violation)"},
	},
	{
		ID:   3,
		Text: "Is there a mechanical enforcement mechanism (Tier 1/2/3) associated with this constraint? (Axiom 3)",
		Options: []string{"Yes, it is mechanically enforced", "No, it is documentation only (Violation)"},
	},
	{
		ID:   4,
		Text: "Is this adaptation versioned, audited, and fully reversible? (Axiom 4)",
		Options: []string{"Yes, it is resilient and reversible", "No, it is a one-way change (Violation)"},
	},
}
