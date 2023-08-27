import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_publisher(publisher_data):
    publisher_dict = {}
    publisher_dict['id'] = urlparse(publisher_data['id']).path.split('/')[-1]
    publisher_dict['name'] = publisher_data['display_name']
    publisher_dict['hierarchy_level'] = publisher_data['hierarchy_level']
    publisher_dict['parent_publisher'] = publisher_data['parent_publisher']
    # lineage
    if (not publisher_data['lineage']):
        publisher_dict['lineage'] = None
    else:
        parts = [
            urlparse(url).path.split('/')[-1]
            for url in publisher_data['lineage']
        ]
        publisher_dict['lineage'] = ",".join(parts)
    # country_code
    if (len(publisher_data['country_codes']) == 0):
        publisher_dict['country_code'] = None
    else:
        publisher_dict['country_code'] = publisher_data['country_codes'][0]
    publisher_dict['works_count'] = publisher_data['works_count']
    publisher_dict['cited_by_count'] = publisher_data['cited_by_count']
    publisher_dict['2yr_mean_citedness'] = publisher_data['summary_stats'][
        '2yr_mean_citedness']
    publisher_dict['h_index'] = publisher_data['summary_stats']['h_index']
    publisher_dict['i10_index'] = publisher_data['summary_stats']['i10_index']
    # roles
    publisher_dict['institution_role'] = None
    publisher_dict['funder_role'] = None
    publisher_dict['publisher_role'] = None
    if (publisher_data['roles']):
        for r in publisher_data['roles']:
            if (r['role'] == 'institution'):
                publisher_dict['institution_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'funder'):
                publisher_dict['funder_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'publisher'):
                publisher_dict['publisher_role'] = urlparse(
                    r['id']).path.split('/')[-1]
    publisher_dict['sources_api_url'] = publisher_data['sources_api_url']
    publisher_dict['updated_date'] = publisher_data['updated_date'][:10]
    publisher_dict['created_date'] = publisher_data['created_date']
    return publisher_dict


def get_publisher_csv():
    publisher_path = "../openalex-snapshot/data/publishers"
    publisher_list = process_files(publisher_path, txt_to_list,
                                   reformat_publisher)
    publisher_csv_path = "../csv_results/publishers.csv"
    field_names = [
        'id', 'name', 'hierarchy_level', 'parent_publisher', 'lineage',
        'country_code', 'works_count', 'cited_by_count',
        '2yr_mean_citedness', 'h_index', 'i10_index', 'institution_role',
        'funder_role', 'publisher_role', 'sources_api_url', 'updated_date',
        'created_date'
    ]
    with open(publisher_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(publisher_list)


if __name__ == "__main__":
    get_publisher_csv()