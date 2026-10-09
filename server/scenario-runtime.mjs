import {configs,catalog} from './scenario-definitions.mjs';
import {evaluateScenario} from '../site/assets/scenario-core.mjs';
export const formats={scenarioVersion:1,workspaceVersion:1,decisionLabSchemaVersion:'1.0',decisionPackVersion:2};
export function scenarioInput(value){if(value.authorized!==true||Object.keys(value).some(k=>!['scenario','authorized'].includes(k)))throw Object.assign(Error('Scenario evaluation requires authorized metadata and no unsupported API fields.'),{status:400});return evaluateScenario(value.scenario,configs,catalog);}
export const scenarioReady=env=>!!(env.GRC_DB&&env.ACCESS_ISSUER&&env.ACCESS_AUDIENCE);
