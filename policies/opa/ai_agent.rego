package grc.agent

default allow := false

high_risk_tool(tool) if tool in {"delete_vendor", "approve_exception", "publish_policy", "change_control_status"}

allow if {
  input.actor.authenticated == true
  input.actor.mfa == true
  input.action.read_only == true
}

allow if {
  input.actor.authenticated == true
  input.actor.mfa == true
  input.action.read_only == false
  not high_risk_tool(input.action.tool)
  input.action.ticket_id != ""
}

allow if {
  input.actor.authenticated == true
  input.actor.mfa == true
  high_risk_tool(input.action.tool)
  input.action.ticket_id != ""
  input.action.human_approval == true
  input.action.approver != input.actor.id
}

deny contains msg if {
  not input.actor.authenticated
  msg := "actor must be authenticated"
}

deny contains msg if {
  input.actor.authenticated
  not input.actor.mfa
  msg := "MFA is required"
}

deny contains msg if {
  high_risk_tool(input.action.tool)
  input.action.human_approval != true
  msg := "high-risk MCP write requires human approval"
}
