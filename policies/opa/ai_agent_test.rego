package grc.agent_test

import data.grc.agent

test_read_only_allowed if {
  agent.allow with input as {"actor":{"id":"u1","authenticated":true,"mfa":true},"action":{"tool":"get_risk","read_only":true,"ticket_id":"","human_approval":false,"approver":""}}
}

test_high_risk_denied_without_approval if {
  not agent.allow with input as {"actor":{"id":"u1","authenticated":true,"mfa":true},"action":{"tool":"approve_exception","read_only":false,"ticket_id":"GRC-42","human_approval":false,"approver":""}}
}
