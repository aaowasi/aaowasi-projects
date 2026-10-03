import {json,ready} from '../../server/evaluation-runtime.mjs';
export async function onRequestGet({env}){return json({available:ready(env),provider:ready(env)?env.PROVIDER_LABEL:null,contact:'https://aaowasi.pages.dev/contact/'});}
