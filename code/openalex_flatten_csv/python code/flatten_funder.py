import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_funder(funder_data):
    funder_dict = {}
    funder_dict['id'] = urlparse(funder_data['id']).path.split('/')[-1]
    funder_dict['name'] = funder_data['display_name']
    funder_dict['country_code'] = funder_data['country_code']
    funder_dict['description'] = funder_data['description']
    funder_dict['homepage_url'] = funder_data['homepage_url']
    # grants_count
    if ('grants_count' not in funder_data):
        funder_dict['grants_count'] = None
    else:
        funder_dict['grants_count'] = funder_data['grants_count']
    funder_dict['works_count'] = funder_data['works_count']
    funder_dict['cited_by_count'] = funder_data['cited_by_count']
    funder_dict['2yr_mean_citedness'] = funder_data['summary_stats'][
        '2yr_mean_citedness']
    funder_dict['h_index'] = funder_data['summary_stats']['h_index']
    funder_dict['i10_index'] = funder_data['summary_stats']['i10_index']

    # roles
    funder_dict['institution_role'] = None
    funder_dict['funder_role'] = None
    funder_dict['publisher_role'] = None
    if (funder_data['roles']):
        for r in funder_data['roles']:
            if (r['role'] == 'institution'):
                funder_dict['institution_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'funder'):
                funder_dict['funder_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'publisher'):
                funder_dict['publisher_role'] = urlparse(
                    r['id']).path.split('/')[-1]

    funder_dict['updated_date'] = funder_data['updated_date'][:10]
    funder_dict['created_date'] = funder_data['created_date']
    return funder_dict


def get_funder_csv():
    funder_path = "../openalex-snapshot/data/funders"
    funder_list = process_files(funder_path, txt_to_list, reformat_funder)
    funder_csv_path = "../csv_results/funders.csv"
    field_names = [
        'id', 'name', 'country_code', 'description', 'homepage_url',
        'grants_count', 'works_count', 'cited_by_count', '2yr_mean_citedness',
        'h_index', 'i10_index', 'institution_role', 'funder_role',
        'publisher_role', 'updated_date', 'created_date'
    ]
    with open(funder_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(funder_list)


if __name__ == "__main__":
    get_funder_csv()