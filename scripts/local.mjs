import {spawnSync} from 'node:child_process';
import {readdirSync} from 'node:fs';
const candidates=process.platform==='win32'?[['py','-3'],['python'],['python3']]:[['python3'],['python']];
const py=candidates.find(([cmd,...args])=>{const r=spawnSync(cmd,[...args,'-c','import sys; assert sys.version_info >= (3,10)'],{stdio:'ignore'});return !r.error&&r.status===0;});
if(!py){console.error('Install Python 3.10+ and add it to PATH.');process.exit(1);}
function run(cmd,args){const r=spawnSync(cmd,args,{stdio:'inherit',env:{...process.env,PYTHONUTF8:'1'}});if(r.error){console.error(r.error.message);process.exit(1);}if(r.status!==0)process.exit(r.status||1);}
function python(args){run(py[0],[...py.slice(1),...args]);}
const action=process.argv[2];
if(action==='build')python(['scripts/build_site.py']);
else if(action==='serve')python(['-m','http.server','8000','--directory','site']);
else if(action==='test'){python(['scripts/check_site.py']);python(['scripts/check_contract.py']);if(readdirSync('tests').length){python(['-m','unittest','discover','-s','tests','-v']);}const files=readdirSync('tests/browser').filter(f=>f.endsWith('.test.mjs')).sort().map(f=>'tests/browser/'+f);run(process.execPath,['--test',...files]);}
else{console.error('Use build, test or serve.');process.exit(1);}
