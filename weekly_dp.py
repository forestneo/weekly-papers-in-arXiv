import re
import arxiv
import argparse
import requests
import datetime


def get_page_content(link: str):
    """
    获得网页对应的源代码
    """
    return requests.get(link).content.decode('utf-8').split('\n')


def get_arxiv_ids_from_content(page_content):
    """
    从网页源代码中，获取到 arxiv_id 列表，如 ['2212.00306', '2212.00292']
    """
    arxiv_ids = []
    for item in page_content:
        r = r'href="/pdf/(\d*.\d*)"'
        m = re.search(r, item)
        if m:
            arxiv_ids.append(m.group(1))
    return arxiv_ids


def is_related(abstract, keywords):
    related_flag = False
    for keyword in keywords:
        if keyword in abstract.lower():
            related_flag = True
    return related_flag


def get_weekly_papers(keywords: str, filename: str, link: str):
    page_content = get_page_content(link)
    arxiv_ids = get_arxiv_ids_from_content(page_content)

    papers = arxiv.Search(id_list=arxiv_ids)

    papers_info = []

    for paper in papers.results():
        abstract = paper.summary
        abstract = re.sub(r'\n {2}', r'\n###', abstract)
        abstract = re.sub(r'\n', r' ', abstract)
        abstract = re.sub(r'###', r'\n', abstract)

        if is_related(abstract, keywords):
            paper_info = {
                'time': str(paper.updated.year).zfill(4) + str(paper.updated.month).zfill(2) + str(
                              paper.updated.day).zfill(2), 'title': paper.title,
                'link': str(paper.links[-1]),
                'authors': ', '.join([author.name for author in paper.authors]),
                'abstract': abstract
            }
            papers_info.append(paper_info)

    time_list = sorted(list(set([paper_info['time'] for paper_info in papers_info])))
    time_papers = {}
    for time in time_list:
        time_papers[time] = [paper_info for paper_info in papers_info if paper_info['time'] == time]

    write_markdown(time_list, time_papers, filename)


def write_markdown(time_list, time_papers, filename):
    f = open(filename, 'wb')
    for time in time_list:
        f.write('# {}\n\n'.format(time).encode())
        papers_info = time_papers[time]
        for paper in papers_info:
            md = '## [{}]({})\n\n*{}*\n\n{}\n\n'.format(paper['title'], paper['link'], paper['authors'], paper['abstract'])
            f.write('{}\n'.format(md).encode())
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for weekly dp')
    parser.add_argument('--keywords', type=str, default="'differential privacy', 'differentially private'")
    parser.add_argument('--filename', type=str, default="None")
    parser.add_argument('--link', type=str, default="https://arxiv.org/list/cs.CR/pastweek?show=120")

    keywords = parser.parse_args().keywords.replace('\'', '').split(', ')
    filename = parser.parse_args().filename
    link = parser.parse_args().link

    # 如果不指定文件名，则获取时间作为文件名，如 20221209_0009.md
    if filename == 'None':
        cur_time = str(datetime.datetime.now())
        filename = ''.join(cur_time.split(':')[0:2]).replace('-', '').replace(' ', '_') + '.md'

    print('output filename = ', filename)
    print('searching ', keywords)
    get_weekly_papers(keywords, filename, link)
