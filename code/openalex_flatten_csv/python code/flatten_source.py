import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list

def reformat_source(source_data):
    source_dict = {}
    source_dict['id'] = urlparse(source_data['id']).path.split('/')[-1]
    source_dict['name'] = source_data['display_name']
    source_dict['issn_l'] = source_data['issn_l']
    # host organizations
    source_dict['host_org_publisher'] = None
    source_dict['host_org_institution'] = None
    if (source_data['host_organization']):
        org_id = urlparse(source_data['host_organization']).path.split('/')[-1]
        if org_id.startswith('P'):
            source_dict['host_org_publisher'] = org_id
        elif org_id.startswith('I'):
            source_dict['host_org_institution'] = org_id
    source_dict['works_count'] = source_data['works_count']
    source_dict['cited_by_count'] = source_data['cited_by_count']
    source_dict['2yr_mean_citedness'] = source_data['summary_stats'][
        '2yr_mean_citedness']
    source_dict['h_index'] = source_data['summary_stats']['h_index']
    source_dict['i10_index'] = source_data['summary_stats']['i10_index']
    source_dict['is_oa'] = source_data['is_oa']
    source_dict['is_in_doaj'] = source_data['is_in_doaj']
    source_dict['homepage_url'] = source_data['homepage_url']
    source_dict['apc_usd'] = source_data['apc_usd']
    source_dict['country_code'] = source_data['country_code']
    source_dict['type'] = source_data['type']
    # x_concepts
    if (not source_data['x_concepts']):
        source_dict['x_concepts'] = None
    else:
        x_concepts_list = []
        for x_concept in source_data['x_concepts']:
            x_concepts_list.append(
                urlparse(x_concept['id']).path.split('/')[-1])
        source_dict['x_concepts'] = ",".join(x_concepts_list)
    source_dict['works_api_url'] = source_data['works_api_url']
    source_dict['updated_date'] = source_data['updated_date'][:10]
    source_dict['created_date'] = source_data['created_date']
    return source_dict


def get_source_csv():
    source_path = "../openalex-snapshot/data/sources"
    source_list = process_files(source_path, txt_to_list, reformat_source)
    source_list = [item for item in source_list if item is not None]
    source_csv_path = "../csv_results/sources.csv"
    field_names = [
        'id', 'name', 'issn_l', 'host_org_publisher', 'host_org_institution',
        'works_count', 'cited_by_count', '2yr_mean_citedness', 'h_index',
        'i10_index', 'is_oa', 'is_in_doaj', 'homepage_url', 'apc_usd',
        'country_code', 'type', 'x_concepts', 'works_api_url', 'updated_date',
        'created_date'
    ]
    with open(source_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(source_list)


if __name__ == "__main__":
    get_source_csv()