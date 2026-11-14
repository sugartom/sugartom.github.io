#!/usr/bin/env python3
"""Render the static homepage; Python 3 standard library only."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent.parent

def e(value):
    return escape(str(value), quote=True)

def author_name(name):
    if ',' in name:
        family, given = name.split(',', 1)
        return given.strip() + ' ' + family.strip()
    return name

def bibtex(paper):
    if paper.get('bibtex'):
        return paper['bibtex']
    citation = paper.get('citation')
    if not citation or not paper['authors']:
        return ''
    def tex(value):
        return str(value).replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('−', '-')
    kind = citation.get('type', 'misc')
    fields = [('title', '{' + paper['title'] + '}'), ('author', ' and '.join(paper['authors'])), ('year', citation['year'])]
    if citation.get('container'):
        fields.append(('journal' if kind == 'article' else 'booktitle', citation['container']))
    fields.extend((key, citation[key]) for key in ['volume','number','pages','doi','eprint','archivePrefix','url'] if citation.get(key))
    key = re.sub('[^a-z0-9]', '', author_name(paper['authors'][0]).split()[-1].lower()) + str(citation['year']) + paper['id'].replace('-', '')[:18]
    return '@' + kind + '{' + key + ',\n' + ',\n'.join('  ' + key + ' = {' + tex(value) + '}' for key, value in fields) + '\n}'

def paper_html(paper):
    pid = paper['id']
    title = e(paper['title'])
    link = paper['links'].get('paper')
    if link:
        title = f'<a href="{e(link)}" target="_blank" rel="noopener noreferrer">{title}</a>'
    badges = f'<span class="ccf">CCF-{e(paper["ccf"])}</span>' if paper.get('ccf') else ''
    if paper.get('award'):
        badges += f'<span class="award">{e(paper["award"])}</span>'
    names = [author_name(name) for name in paper['authors']]
    corresponding = set(paper.get('corresponding_authors', []))
    assert corresponding.issubset(names), f'Unknown corresponding author in {pid}'
    # The owner wants correspondence marks displayed only for his own name;
    # retain the complete verified author roles in the data for provenance.
    corresponding &= {'Yitao Hu'}
    author_items = []
    for name in names:
        rendered = '<strong class="own-name">' + e(name) + '</strong>' if name == 'Yitao Hu' else e(name)
        if name in corresponding:
            label = e(paper.get('corresponding_author_label', 'Corresponding author'))
            rendered += f'<sup class="corresponding" aria-label="{label}" title="{label}">*</sup>'
        author_items.append(rendered)
    authors = ', '.join(author_items)
    if not authors:
        authors = '<span class="unverified">Author information forthcoming.</span>'
    tools, panels = [], []
    def disclosure(label, content):
        panel_id = f'{pid}-{label.lower()}'
        tools.append(f'<button class="detail-toggle" type="button" hidden aria-expanded="false" aria-controls="{panel_id}" aria-label="{label} for {e(paper["title"])}">{label}</button>')
        panels.append(f'<details class="paper-detail" id="{panel_id}"><summary>{label}</summary><div class="detail-content">{content}</div></details>')
    if paper.get('abstract'):
        disclosure('Abstract', f'<p class="detail-heading">Abstract</p><p>{e(paper["abstract"])}</p>')
    elif link:
        disclosure('Abstract', f'<p>Read the abstract on the <a href="{e(link)}" target="_blank" rel="noopener noreferrer">paper’s official page</a>.</p>')
    bib = bibtex(paper)
    if bib:
        disclosure('BibTeX', f'<div class="bib-toolbar"><span class="detail-heading">BibTeX</span><button class="copy-bib" type="button" data-copy="bib-{pid}" aria-label="Copy BibTeX for {e(paper["title"])}">Copy</button></div><pre class="bibtex" id="bib-{pid}">{e(bib)}</pre>')
    for key, label in [('paper','Paper'),('code','Code'),('slides','Slides'),('huggingface','Dataset')]:
        if paper['links'].get(key):
            tools.append(f'<a class="resource-link" href="{e(paper["links"][key])}" target="_blank" rel="noopener noreferrer" aria-label="{label} for {e(paper["title"])}">{label}</a>')
    if not tools:
        tools.append('<span class="status">Manuscript · resources forthcoming</span>')
    return f'<li class="paper" id="paper-{pid}"><span class="venue">{e(paper["venue"])}</span><div class="paper-body"><h4 class="paper-title">{title} {badges}</h4><p class="authors">{authors}</p><div class="paper-resources"><div class="paper-tools">{"".join(tools)}</div><div class="paper-panels">{"".join(panels)}</div></div></div></li>'

def publications_html(papers):
    output = []
    for year in sorted({paper['year'] for paper in papers}, reverse=True):
        year_papers = [paper for paper in papers if paper['year'] == year]
        venues = {}
        for paper in year_papers:
            venues.setdefault((paper['publication_type'], paper['venue']), []).append(paper)
        venue_groups = list(venues.values())
        # Whole venue groups move together. Dates and source order break ties
        # within the conference, journal, and preprint categories.
        venue_groups.sort(key=lambda items: min(p['order'] for p in items))
        venue_groups.sort(key=lambda items: max(p.get('sort_date', p.get('date', '')) for p in items), reverse=True)

        def priority(items):
            paper = items[0]
            if year == 2025 and paper['venue'] == 'Nature':
                return (-1, 0)
            category = {'conference': 0, 'journal': 1, 'preprint': 2}[paper['publication_type']]
            grade = min({'A': 0, 'B': 1, 'C': 2}.get(p.get('ccf'), 3) for p in items) if category == 0 else 0
            return (category, grade)

        venue_groups.sort(key=priority)
        output.append(f'<h3 class="year-heading">{year}</h3><ul class="paper-list">')
        for items in venue_groups:
            items.sort(key=lambda p: (p.get('sort_date', p.get('date', '')), -p['order']), reverse=True)
            output.extend(paper_html(paper) for paper in items)
        output.append('</ul>')
    return '\n'.join(output)


def news_html(news):
    def rows(items):
        return '<ul class="news-list">' + ''.join(f'<li><span class="news-date">{e(item["label"])}</span><div>{item["html"]}</div></li>' for item in items) + '</ul>'
    output = rows(news[:6])
    if len(news)>6:
        output += '<details class="older-news"><summary>Earlier news</summary>' + rows(news[6:]) + '</details>'
    return output

def main():
    papers = json.loads((ROOT/'data/publications.json').read_text())
    news = json.loads((ROOT/'data/news.json').read_text())
    assert len({p['id'] for p in papers}) == len(papers), 'Duplicate paper IDs'
    for p in papers:
        assert p['title'] and p['venue'] and 2000 <= p['year'] <= 2100
        assert p['publication_type'] in {'conference', 'journal', 'preprint'}
        assert all(not re.match(r'(?i)(javascript|data):', url) for url in p['links'].values())
    template = (ROOT/'templates/index.html').read_text()
    result = template.replace('{{PUBLICATIONS}}', publications_html(papers)).replace('{{NEWS}}', news_html(news))
    result = '\n'.join(line.rstrip() for line in result.splitlines()) + '\n'
    assert not re.search(r'\{\{[A-Z]+\}\}', result), 'Unexpanded template'
    (ROOT/'index.html').write_text(result)
    print(f'Built index.html: {len(papers)} selected papers, {len(news)} news items.')

if __name__ == '__main__':
    main()
