package grc.article50_test

import data.grc.article50

test_release_allowed_with_verified_controls if {
  article50.release_allowed with input as {
    "interacts_directly_with_natural_persons": true,
    "obvious_ai_interaction": false,
    "generates_synthetic_content": true,
    "standard_editing_only": false,
    "authorized_law_enforcement_exception": false,
    "interaction_disclosure_verified": true,
    "machine_readable_marking_verified": true,
    "legal_review": {"approved": true}
  }
}

test_release_denied_without_marking if {
  not article50.release_allowed with input as {
    "interacts_directly_with_natural_persons": true,
    "obvious_ai_interaction": false,
    "generates_synthetic_content": true,
    "standard_editing_only": false,
    "authorized_law_enforcement_exception": false,
    "interaction_disclosure_verified": true,
    "machine_readable_marking_verified": false,
    "legal_review": {"approved": true}
  }
}
