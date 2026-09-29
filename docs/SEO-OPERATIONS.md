# Search discovery operations

The build generates one canonical URL, route-specific description, Open Graph/Twitter metadata, public social image and sitemap entry per indexable page. The 404 page is noindex and excluded from the sitemap. Home/profile structured data describes a WebSite and the actual Person without invented job titles, degrees, client claims or credentials. SHA-256 hashes authorize only the generated JSON-LD payloads under the existing strict CSP; executable unsafe-inline is not enabled.

Sitemaps are at `/sitemap.xml` on each domain and linked from robots.txt. After changes, run the build and site checks before publication. These features support discovery and correct presentation; they do not guarantee indexing, search rank, enquiries or hiring.

Owner actions, if not already completed: add each deployed domain as a URL-prefix property in Google Search Console; verify ownership using a method available to the site owner; submit its sitemap URL; inspect key public routes and review coverage reports. No Search Console verification, sitemap submission or indexing request was performed by this code change. Keep verification credentials out of public source. Search Console access remains an owner step because no authenticated access is configured here.

Primary references checked by the implementation team:

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/appearance/structured-data/profile-page
