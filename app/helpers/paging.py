# Author : Alex Ksikes

import urllib

def get_paging(start, max_results, query=False, results_per_page=15, window_size=15):
    c_page = start / results_per_page + 1
    if not start:
        c_page = 1
    nb_pages = max_results / results_per_page
    if max_results % results_per_page != 0:
        nb_pages += 1
    
    left_a = right_a = ''
    if c_page > 1:
        left_a = (c_page - 2) * results_per_page
    if c_page < nb_pages:
        right_a = start + results_per_page
        
    leftmost_a = rightmost_a = ''
    if (c_page - 3) >= 0:
        leftmost_a = 0
    if (c_page + 1) < nb_pages:
        rightmost_a = (nb_pages -1) * results_per_page

    left = c_page - window_size / 2
    if left < 1:
        left = 1
    right = left + window_size - 1
    if right > nb_pages:
        right = nb_pages
    
    pages = []
    for i in range(left, right + 1):
        pages.append({
            'number' : i,
            'start' : (i - 1) * results_per_page
        })
    
    return {
        'start' : start,
        'max_results' : max_results,
        'c_page' : c_page,
        'nb_pages' : nb_pages,
        'pages' : pages,
        'leftmost_a' : leftmost_a,
        'left_a' : left_a,
        'right_a' : right_a,
        'rightmost_a' : rightmost_a,
        'query_enc' : query and urllib.quote(query) or ''
    }

def get_paging_results(start, max_results, id, results, results_per_page):
    index = 0
    results = list(results)
    for i, r in enumerate(results):
        if r.id == id: index = i
    pager = dict(left_start=start, right_start=start, max_results=max_results, 
        number=start + index, left=False, middle=results[index], right=False)
    
    if index > 0 or start > 0:
        pager['left'] = results[index-1]
    if index < len(results) - 1:
        pager['right'] = results[index+1]
    if index == results_per_page - 1:
        pager['right_start'] = start + results_per_page
    if index == 0 and start > 0:
        pager['left_start'] = start - results_per_page
    if start != 0:
        pager['number'] = start + index -1
    
    return pager   

