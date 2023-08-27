import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_work(work_data):
    work_dict = {}
    work_dict['id'] = urlparse(work_data['id']).path.split('/')[-1]
    work_dict['name'] = work_data['display_name']
    work_dict['doi'] = work_data['doi']
    work_dict['publication_date'] = work_data['publication_date']
    work_dict['type'] = work_data['type']
    # open access
    work_dict['is_oa'] = work_data['open_access']['is_oa']
    work_dict['oa_status'] = work_data['open_access']['oa_status']
    work_dict['oa_url'] = work_data['open_access']['oa_url']
    # authorships
    if (not work_data['authorships']):
        work_dict['authorships'] = None
    else:
        author_list = []
        for a in work_data['authorships']:
            author_list.append(urlparse(a['author']['id']).path.split('/')[-1])
        work_dict['authorships'] = ",".join(author_list)
    work_dict['cited_by_count'] = work_data['cited_by_count']
    work_dict['is_retracted'] = work_data['is_retracted']
    work_dict['is_paratext'] = work_data['is_paratext']
    # concepts
    if (not work_data['concepts']):
        work_dict['concepts'] = None
    else:
        concept_list = []
        for c in work_data['concepts']:
            concept_list.append(urlparse(c['id']).path.split('/')[-1])
        work_dict['concepts'] = ",".join(concept_list)
    # work_dict['locations_count'] = work_data['locations_count']
    # locations
    if (not work_data['locations']):
        work_dict['locations'] = None
    else:
        location_list = []
        for l in work_data['locations']:
            if (l['source'] is not None):
                location_list.append(
                    urlparse(l['source']['id']).path.split('/')[-1])
        work_dict['locations'] = ",".join(location_list)
    # best_oa_location
    if (not (work_data['best_oa_location'])):
        work_dict['best_oa_location'] = None
    else:
        if (work_data['best_oa_location']['source'] is not None):
            work_dict['best_oa_location'] = urlparse(
                work_data['best_oa_location']['source']['id']).path.split(
                    '/')[-1]
    # referenced_works
    parts = [
        urlparse(url).path.split('/')[-1]
        for url in work_data['referenced_works']
    ]
    work_dict['referenced_works'] = ",".join(parts)
    # related_works
    parts = [
        urlparse(url).path.split('/')[-1] for url in work_data['related_works']
    ]
    work_dict['related_works'] = ",".join(parts)
    # work_dict['ngrams_url'] = work_data['ngrams_url']
    work_dict['cited_by_api_url'] = work_data['cited_by_api_url']
    work_dict['updated_date'] = work_data['updated_date'][:10]
    work_dict['created_date'] = work_data['created_date']
    return work_dict


def get_work_csv():
    work_path = "../openalex-snapshot/data/works"
    work_list = process_files(work_path, txt_to_list, reformat_work)
    work_list = [item for item in work_list if item is not None]
    work_csv_path = "../csv_results/works.csv"
    field_names = [
        'id', 'name', 'doi', 'publication_date', 'type', 'is_oa', 'oa_status',
        'oa_url', 'authorships', 'cited_by_count', 'is_retracted',
        'is_paratext', 'concepts', 'locations',
        'best_oa_location', 'referenced_works', 'related_works', 'ngrams_url',
        'cited_by_api_url', 'updated_date', 'created_date'
    ]
    with open(work_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(work_list)


if __name__ == "__main__":
    get_work_csv()