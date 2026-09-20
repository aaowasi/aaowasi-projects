export interface Env { ALLOWED_ORIGIN?: string }

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (!env.ALLOWED_ORIGIN) return Response.json({ error: "origin_not_configured" }, { status: 503 });
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return cors(new Response(null, { status: 204 }), env.ALLOWED_ORIGIN);
    if (url.pathname !== "/api/status") return cors(Response.json({ error: "not_found" }, { status: 404 }), env.ALLOWED_ORIGIN);
    const upstream = new URL("/data/control-status.json", env.ALLOWED_ORIGIN);
    const r = await fetch(upstream, { cf: { cacheTtl: 60, cacheEverything: true } });
    if (!r.ok) return cors(Response.json({ error: "upstream_unavailable", status: r.status }, { status: 502 }), env.ALLOWED_ORIGIN);
    return cors(new Response(await r.text(), { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=60" } }), env.ALLOWED_ORIGIN);
  }
};

function cors(response: Response, origin: string): Response {
  const h = new Headers(response.headers);
  h.set("access-control-allow-origin", origin);
  h.set("access-control-allow-methods", "GET,OPTIONS");
  h.set("vary", "Origin");
  return new Response(response.body, { status: response.status, headers: h });
}
