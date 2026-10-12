# GGC corporate website

The published bilingual website is built from the reviewed source in [ggc-global PR #11](https://github.com/minyajing-rgb/ggc-global/pull/11). This repository owns only the production build and hosting configuration. The original design, copy, assets, and 96-page source remain in `ggc-global`.

## Publish

Run [Publish GGC corporate site](https://github.com/minyajing-rgb/ggc-corporate-site/actions/workflows/publish.yml) manually with the reviewed `ggc-global` commit SHA. The workflow verifies source and asset hashes, builds the pages, removes the review-only UI, adds production SEO, privacy and safe form fallbacks, and deploys to GitHub Pages. The currently pinned source SHA is visible in the workflow input; update it only after source review and checks.

The production domain is `ggcgames.com`, with `www.ggcgames.com` routed to the same GitHub Pages account. Alibaba Cloud remains the authoritative DNS provider. The apex has the four GitHub Pages A addresses; `www` is a CNAME to `minyajing-rgb.github.io`. Mail, `biz`, `opsgo`, and other subdomain records are independent.

## Release checks

- Check the latest workflow run, then open both language homepages, a detail page, contact, privacy, and an unknown URL through the production domain.
- Confirm canonical/hreflang, `robots.txt`, and `sitemap.xml` after a fresh build.
- Verify HTTPS certificate issuance and enable **Enforce HTTPS** in GitHub Pages settings. DNS and certificate provisioning can lag the record change.
- Contact and updates forms only prepare email drafts for the visitor to review and send. There is no automatic inquiry submission, CRM, or mailing-list subscription.
- Keep PR #11 source changes and this workflow's pinned SHA in sync. A preview or successful Actions run alone is not visual or production acceptance.

## DNS recovery

An Alibaba Cloud export was saved before cutover. To restore the previous routing, change only the apex A records back to `75.2.60.5` and `www` CNAME back to `site-dns.bolt.host`; leave MX/TXT and all other hostnames intact. This is routing recovery, not a rollback of the content in the previous hosting project.
