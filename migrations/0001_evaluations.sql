CREATE TABLE IF NOT EXISTS tenants (
 id TEXT PRIMARY KEY, name TEXT NOT NULL, allowance INTEGER NOT NULL DEFAULT 2 CHECK(allowance >= 0 AND allowance <= 10000), active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
CREATE TABLE IF NOT EXISTS members (
 issuer TEXT NOT NULL, subject TEXT NOT NULL, tenant_id TEXT NOT NULL REFERENCES tenants(id), active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)), PRIMARY KEY(issuer,subject)
);
CREATE TABLE IF NOT EXISTS evaluations (
 tenant_id TEXT NOT NULL REFERENCES tenants(id), request_id TEXT NOT NULL, input_hash TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('pending','complete','failed')), created_at TEXT NOT NULL, report TEXT, PRIMARY KEY(tenant_id,request_id)
);
CREATE INDEX IF NOT EXISTS evaluations_usage ON evaluations(tenant_id,status);
