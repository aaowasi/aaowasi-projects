export const CONTACT='https://aaowasi.pages.dev/contact/';
export const json=(value,status=200)=>new Response(JSON.stringify(value),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export function ready(env){return !!(env.GRC_DB&&env.ACCESS_ISSUER&&env.ACCESS_AUDIENCE&&env.PROVIDER_URL&&env.PROVIDER_KEY&&env.PROVIDER_LABEL);}
const decode=s=>Uint8Array.from(atob(s.replace(/-/g,'+').replace(/_/g,'/')),c=>c.charCodeAt(0));
export async function identity(request,env,fetcher=fetch){
 if(!env.GRC_DB||!env.ACCESS_ISSUER||!env.ACCESS_AUDIENCE)throw Object.assign(Error('Organization access is not configured.'),{status:503});
 const token=request.headers.get('Cf-Access-Jwt-Assertion');if(!token||token.length>16000)throw Object.assign(Error('Sign in with organization access.'),{status:401});
 try{
  const [a,b,c,...extra]=token.split('.');if(extra.length||!c)throw Error();
  const h=JSON.parse(new TextDecoder().decode(decode(a))),p=JSON.parse(new TextDecoder().decode(decode(b)));
  const issuer=new URL(env.ACCESS_ISSUER);if(issuer.protocol!=='https:'||!issuer.hostname.endsWith('.cloudflareaccess.com')||issuer.pathname!=='/')throw Error();
  const now=Math.floor(Date.now()/1000);const aud=Array.isArray(p.aud)?p.aud:[p.aud];
  if(h.alg!=='RS256'||typeof h.kid!=='string'||p.iss!==env.ACCESS_ISSUER.replace(/\/$/,'')&&p.iss!==env.ACCESS_ISSUER||!aud.includes(env.ACCESS_AUDIENCE)||!Number.isFinite(p.exp)||p.exp<=now||p.nbf!==undefined&&(!Number.isFinite(p.nbf)||p.nbf>now+30)||typeof p.sub!=='string'||!p.sub)throw Error();
  const response=await fetcher(new URL('/cdn-cgi/access/certs',issuer).href,{signal:AbortSignal.timeout(5000)});if(!response.ok)throw Error();
  const keys=await response.json();const jwk=keys.keys?.find(k=>k.kid===h.kid&&k.kty==='RSA');if(!jwk)throw Error();
  const key=await crypto.subtle.importKey('jwk',jwk,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['verify']);
  if(!await crypto.subtle.verify('RSASSA-PKCS1-v1_5',key,decode(c),new TextEncoder().encode(a+'.'+b)))throw Error();
  const member=await env.GRC_DB.prepare('SELECT m.tenant_id, t.name, t.allowance FROM members m JOIN tenants t ON t.id=m.tenant_id WHERE m.subject=? AND m.issuer=? AND m.active=1 AND t.active=1').bind(p.sub,env.ACCESS_ISSUER).first();
  if(!member)throw Object.assign(Error('Request organization access.'),{status:403});return member;
 }catch(e){if(e.status===403)throw e;throw Object.assign(Error('Organization identity could not be verified.'),{status:401});}
}
export function input(value){
 if(!value||typeof value.context!=='string'||value.context.trim().length<20||value.context.length>4000||typeof value.scope!=='string'||!value.scope.trim()||value.scope.length>160||!Array.isArray(value.domains)||value.domains.length<1||value.domains.length>30||value.domains.some(x=>typeof x!=='string'||!x.trim()||x.length>100)||value.authorized!==true)throw Object.assign(Error('Provide a scope, 20–4000 characters of authorized context, and at least one domain.'),{status:400});
 return {scope:value.scope.trim(),context:value.context.trim(),domains:[...new Set(value.domains.map(x=>x.trim()))]};
}
export const RESERVE_SQL=`INSERT INTO evaluations (tenant_id, request_id, input_hash, status, created_at) SELECT ?, ?, ?, 'pending', ? WHERE (SELECT COUNT(*) FROM evaluations WHERE tenant_id=? AND status IN ('pending','complete')) < (SELECT allowance FROM tenants WHERE id=? AND active=1) ON CONFLICT(tenant_id,request_id) DO NOTHING`;
export function report(value){
 if(!value||!Array.isArray(value.findings)||value.findings.length>30||value.findings.length<1)throw Error('Invalid provider report');
 for(const f of value.findings)if(!['domain','finding','evidenceNeeded','nextAction','owner'].every(k=>typeof f[k]==='string'&&f[k].length>0&&f[k].length<=2000))throw Error('Invalid provider finding');
 return {findings:value.findings.map(f=>Object.fromEntries(['domain','finding','evidenceNeeded','nextAction','owner'].map(k=>[k,f[k]]))),contact:CONTACT};
}

export async function boundedText(stream,limit){if(!stream)return '';const reader=stream.getReader();let size=0;const chunks=[];try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>limit){await reader.cancel();throw Object.assign(Error('Request or response exceeds size limit.'),{status:413});}chunks.push(value);}}finally{reader.releaseLock();}const result=new Uint8Array(size);let offset=0;for(const chunk of chunks){result.set(chunk,offset);offset+=chunk.length;}return new TextDecoder().decode(result);}
