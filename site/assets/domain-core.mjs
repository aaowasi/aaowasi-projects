export function domainProjects(projects, slug='') { return projects.filter(p=>!slug||p.slug===slug); }
export function domainRecords(records, slug='') { return records.filter(r=>!slug||r.domainSlug===slug); }
export function domainCounts(domains,catalog) { return {domains:domains.length,entities:Object.keys(catalog.entities).length,views:catalog.views.length}; }
