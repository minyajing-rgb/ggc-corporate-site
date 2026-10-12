#!/usr/bin/env python3
"""Production-only safeguards for the reviewed GGC static site."""
from pathlib import Path
import re
import sys

site = Path(sys.argv[1])
privacy = {
    'zh': {
        'title': '隐私与联系说明',
        'eyebrow': 'PRIVACY / CONTACT',
        'intro': '了解本网站当前如何处理联系与订阅意向。',
        'sections': [
            ('联系表单', '联系表单只在你的浏览器中生成邮件草稿。只有你打开邮箱、核对并自行发送后，GGC 才会收到邮件；网站没有自动提交询单或保存表单的后台。'),
            ('动态与订阅', '动态页面目前只生成订阅意向邮件草稿。网站尚未提供自动订阅、确认或退订系统；提交意向不会使你自动加入邮件名单。'),
            ('你主动发送的信息', '邮件可能包含你填写的姓名、公司、回复邮箱和业务问题。GGC 用这些信息回复你的询问。请勿发送与询问无关的敏感资料。'),
            ('网站与外部服务', '网站由 GitHub Pages 托管。访问服务可能处理必要的技术数据；外部链接及你使用的邮箱服务适用各自的隐私做法。'),
            ('联系与请求', '如需询问你主动发送给 GGC 的邮件信息，或请求删除，请发邮件至 <a href="mailto:minyajing@gmail.com">minyajing@gmail.com</a>。'),
        ],
        'updated': '更新日期：2026 年 10 月 13 日',
        'link': '隐私说明',
        'noscript': '此表单需要 JavaScript 才能生成邮件草稿。你也可以直接发邮件至 minyajing@gmail.com。',
    },
    'en': {
        'title': 'Privacy and contact',
        'eyebrow': 'PRIVACY / CONTACT',
        'intro': 'How this version of the site handles inquiries and updates interest.',
        'sections': [
            ('Contact form', 'The contact form creates an email draft in your browser. GGC receives it only if you open your email app, review the draft, and send it yourself. The site has no automatic inquiry submission or form storage backend.'),
            ('Updates interest', 'The updates page currently creates an interest email draft only. There is no automatic subscription, confirmation, or unsubscribe system; expressing interest does not add you to a mailing list.'),
            ('Information you choose to send', 'Your email may contain the name, company, reply address, and business question you entered. GGC uses that information to respond to your inquiry. Please avoid sending unrelated sensitive information.'),
            ('Hosting and external services', 'The site is hosted on GitHub Pages. Providing access may involve processing necessary technical data. External links and your email provider follow their own privacy practices.'),
            ('Contact and requests', 'For questions about information you emailed to GGC, or to request deletion, email <a href="mailto:minyajing@gmail.com">minyajing@gmail.com</a>.'),
        ],
        'updated': 'Updated 13 October 2026',
        'link': 'Privacy',
        'noscript': 'This form needs JavaScript to create an email draft. You can email minyajing@gmail.com directly.',
    },
}

form_count = 0
for locale, copy in privacy.items():
    folder = site / locale
    assert (folder / 'contact.html').exists(), locale
    for page in folder.glob('*.html'):
        html = page.read_text(encoding='utf-8')
        # A JS-disabled form must never fall back to GET with personal data in the URL.
        html, n = re.subn(r'<form\b(?![^>]*\bmethod\s*=)', '<form method="post"', html, flags=re.I)
        form_count += n
        if n:
            html = re.sub(r'(<form\b[^>]*>)', r'\1<noscript><p class="note">' + copy['noscript'] + '</p></noscript>', html, count=n, flags=re.I)
        if 'href="privacy.html"' not in html:
            assert '<div class="footer-bottom">' in html, page
            html = html.replace('<div class="footer-bottom">', '<div class="footer-bottom"><a href="privacy.html">' + copy['link'] + '</a>', 1)
        page.write_text(html, encoding='utf-8')

    target = folder / 'privacy.html'
    if target.exists():
        continue
    template = (folder / 'contact.html').read_text(encoding='utf-8')
    body = '<main id="main"><section class="pagehero"><div class="shell"><p class="eyebrow">' + copy['eyebrow'] + '</p><h1>' + copy['title'] + '</h1><p>' + copy['intro'] + '</p></div></section><section class="section white"><div class="shell" style="max-width:900px">'
    for heading, paragraph in copy['sections']:
        body += '<article class="card" style="margin-bottom:18px"><h2 style="font-size:22px">' + heading + '</h2><p style="margin-top:12px">' + paragraph + '</p></article>'
    body += '<p>' + copy['updated'] + '</p></div></section></main>'
    template, n = re.subn(r'<main id="main">.*?</main>', lambda _: body, template, count=1, flags=re.S)
    assert n == 1, locale
    template = template.replace('href="../' + ('en' if locale == 'zh' else 'zh') + '/contact.html"', 'href="../' + ('en' if locale == 'zh' else 'zh') + '/privacy.html"', 1)
    template = re.sub(r'<div class="page-tools">.*?</div></div></div>', '', template, count=1, flags=re.S)
    template = re.sub(r'<title>.*?</title>', '<title>' + copy['title'] + ' · GGC</title>', template, count=1, flags=re.S)
    target.write_text(template, encoding='utf-8')

# GitHub Pages serves the root 404 document for any missing URL. Reuse the
# accepted branded 404 and resolve its relative links from the zh directory.
branded_404 = (site / 'zh' / '404.html').read_text(encoding='utf-8')
assert '<head>' in branded_404
branded_404 = branded_404.replace('<head>', '<head><base href="https://ggcgames.com/zh/">', 1)
(site / '404.html').write_text(branded_404, encoding='utf-8')

# On mobile the menu button follows the hidden nav in DOM order. Move focus to
# the opened nav so a keyboard user can reach its links immediately.
js = site / 'assets' / 'production-nav.js'
js.write_text("document.addEventListener('DOMContentLoaded',()=>{const b=document.querySelector('[data-menu]'),n=document.querySelector('[data-nav]');if(!b||!n)return;b.addEventListener('click',()=>{if(n.dataset.open==='true')n.querySelector('a')?.focus();});});\n", encoding='utf-8')
for page in site.glob('??/*.html'):
    html = page.read_text(encoding='utf-8')
    if 'production-nav.js' not in html:
        html = html.replace('</head>', '<script defer src="../assets/production-nav.js"></script></head>', 1)
        page.write_text(html, encoding='utf-8')
assert form_count >= 2, form_count
print(f'Hardened forms: {form_count}; privacy pages: 2')
