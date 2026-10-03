import {identity,json} from '../../server/evaluation-runtime.mjs';
export async function onRequestGet({request,env}){try{await identity(request,env);return Response.redirect(new URL('/evaluate/',request.url).href,302);}catch(e){return json({error:e.message,contact:'https://aaowasi.pages.dev/contact/'},e.status||500);}}
