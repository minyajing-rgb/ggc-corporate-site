# GGC corporate website

The published bilingual website is built from the reviewed source in [ggc-global PR #11](https://github.com/minyajing-rgb/ggc-global/pull/11). This repository owns only the production build and hosting configuration. The original design, copy, assets, and 96-page source remain in `ggc-global`.

## Publish

Run [Publish GGC corporate site](https://github.com/minyajing-rgb/ggc-corporate-site/actions/workflows/publish.yml) manually with the reviewed `ggc-global` commit SHA. The workflow runs the source-owned `build_ready.py` release build, verifies the 98 localized pages and 94 indexable URLs, removes review artifacts, and deploys to GitHub Pages. The source build verifies approved assets and provides SEO, privacy, keyboard support, and safe form behavior. The pinned source SHA is `80d3addab65b42eb7d4d206531d68b7c9f064c74`, tested by [PR11 source P0 readiness run #2](https://github.com/minyajing-rgb/ggc-global/actions/runs/38299917109) (10,462 checks, 0 failures) and [production publish run #7](https://github.com/minyajing-rgb/ggc-corporate-site/actions/runs/38300420106). Update it only after source review and checks.

The production domain is `ggcgames.com`, with `www.ggcgames.com` routed to the same GitHub Pages account. Alibaba Cloud remains the authoritative DNS provider. The apex has the four GitHub Pages A addresses; `www` is a CNAME to `minyajing-rgb.github.io`. Mail, `biz`, `opsgo`, and other subdomain records are independent.

## Release checks

- Check the latest workflow run, then open both language homepages, a detail page, contact, privacy, and an unknown URL through the production domain.
- Confirm canonical/hreflang, `robots.txt`, and `sitemap.xml` after a fresh build.
- HTTPS enforcement was enabled on 13 October 2026. Recheck the certificate and HTTP-to-HTTPS redirect after DNS or hosting changes.
- Contact and updates forms only prepare email drafts for the visitor to review and send. There is no automatic inquiry submission, CRM, or mailing-list subscription.
- Keep PR #11 source changes and this workflow's pinned SHA in sync. A preview or successful Actions run alone is not visual or production acceptance.

## DNS recovery

An Alibaba Cloud export was saved before cutover. To restore the previous routing, change only the apex A records back to `75.2.60.5` and `www` CNAME back to `site-dns.bolt.host`; leave MX/TXT and all other hostnames intact. This is routing recovery, not a rollback of the content in the previous hosting project.
