# GGC corporate website

The bilingual production site at https://ggcgames.com/ is built from the reviewed source in [ggc-global PR #11](https://github.com/minyajing-rgb/ggc-global/pull/11). This repository owns the GitHub Pages build and hosting configuration. The design, copy and assets remain in `ggc-global`.

## Publish

Run [Publish GGC corporate site](https://github.com/minyajing-rgb/ggc-corporate-site/actions/workflows/publish.yml) manually with a reviewed `ggc-global` commit SHA. The workflow runs `build_ready.py --mode release --google-form`, verifies 98 localized pages, 94 indexable URLs and the Google Forms contact links, removes review artifacts, then deploys to GitHub Pages.

The production workflow is pinned to source commit `5d0f63a17f498fc28c0eb459f1ee3ae775282646`. [Publish run #10](https://github.com/minyajing-rgb/ggc-corporate-site/actions/runs/38374031573) succeeded on 13 October 2026. Live ZH/EN contact and privacy pages returned HTTP 200, and the Chinese contact call-to-action opened the published form.

Business enquiries use a bilingual Google Form owned by `minyajing@gmail.com`. Visitors supply name, reply email, optional company, enquiry type, message and explicit consent. Responses enter a private Google Sheet and new-response email notifications go to the owner. Two synthetic submissions reached the Sheet; the second generated a Gmail notification. The production site does not use the disabled FormSubmit candidate in the source PR. Updates-interest remains an email draft and there is no CRM or automated mailing-list subscription.

The production domain is `ggcgames.com`, with `www.ggcgames.com` routed to the same GitHub Pages account. Alibaba Cloud remains the authoritative DNS provider. The apex has the four GitHub Pages A addresses; `www` is a CNAME to `minyajing-rgb.github.io`. Mail, `biz`, `opsgo`, and other subdomain records are independent.

## Release checks

- Check the latest workflow run, then open both language homepages, contact and privacy pages, a detail page, and an unknown URL on the production domain.
- Confirm canonical/hreflang, `robots.txt`, `sitemap.xml`, HTTPS enforcement and the HTTP-to-HTTPS redirect after a fresh build or DNS change.
- Submit a synthetic form enquiry only when testing the collection path; confirm Sheet row and owner notification, and label the row clearly as QA.
- Keep PR #11 source changes and this workflow's pinned SHA in sync. A successful Actions run alone is not final visual or legal acceptance.

## DNS recovery

An Alibaba Cloud export was saved before cutover. To restore the previous routing, change only the apex A records back to `75.2.60.5` and `www` CNAME back to `site-dns.bolt.host`; leave MX/TXT and all other hostnames intact. This is routing recovery, not a rollback of content in the previous hosting project.
