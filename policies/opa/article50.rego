package grc.article50

default release_allowed := false

interaction_disclosure_required if {
  input.interacts_directly_with_natural_persons == true
  input.obvious_ai_interaction != true
  input.authorized_law_enforcement_exception != true
}

synthetic_marking_required if {
  input.generates_synthetic_content == true
  input.standard_editing_only != true
  input.authorized_law_enforcement_exception != true
}

violations contains "AI interaction disclosure was not verified" if {
  interaction_disclosure_required
  input.interaction_disclosure_verified != true
}

violations contains "synthetic output marking was not verified as machine-readable and detectable" if {
  synthetic_marking_required
  input.machine_readable_marking_verified != true
}

violations contains "qualified reviewer approval is required for the applicability decision" if {
  input.legal_review.approved != true
}

release_allowed if count(violations) == 0
