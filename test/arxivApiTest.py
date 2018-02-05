import pyarxiv
# import query, download_entries

from pyarxiv.arxiv_categories import ArxivCategory, arxiv_category_map

#query(max_results=100, ids=[], categories=[],
#                title='', authors='', abstract='', journal_ref='',
#                querystring='')
entries = pyarxiv.query(title='light field')
# extract title
titles = map(lambda x: x['title'], entries)

# print
for title in list(titles):
    print(title + '\n')


#download_entries(entries_or_ids_or_uris=[], target_folder='.',
#                     use_title_for_filename=False, append_id=False,
#                     progress_callback=(lambda x, y: id))

# pyarxiv.download_entries(entries, 'download')


#print(arxiv_category_map(ArxivCategory.cs_AI))