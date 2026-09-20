package grc.evidence_publication

default publish := false

restricted_classification if input.classification in {"CONFIDENTIAL", "RESTRICTED", "SECRET"}

publish if {
  not restricted_classification
  input.contains_personal_data != true
  input.contains_secrets != true
  input.sha256 != ""
  input.owner_approved == true
}

deny contains "restricted evidence must not be published" if restricted_classification
deny contains "personal data must be removed or access-controlled" if input.contains_personal_data == true
deny contains "secrets must never enter the evidence archive" if input.contains_secrets == true
deny contains "a SHA-256 digest is required" if input.sha256 == ""
deny contains "evidence owner approval is required" if input.owner_approved != true
