package grc.cloud_iam

default compliant := false

wildcard_admin(statement) if {
  statement.Effect == "Allow"
  statement.Resource == "*"
  statement.Action == "*"
}

wildcard_admin(statement) if {
  statement.Effect == "Allow"
  statement.Resource == "*"
  "*" in statement.Action
}

violations contains sprintf("policy %s grants wildcard administrative access", [policy.name]) if {
  policy := input.policies[_]
  statement := policy.document.Statement[_]
  wildcard_admin(statement)
}

compliant if count(violations) == 0
