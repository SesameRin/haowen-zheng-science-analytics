import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_institution(institution_data):
    institution_dict = {}
    institution_dict['id'] = urlparse(institution_data['id']).path.split(
        '/')[-1]
    institution_dict['ror'] = institution_data['ror']
    institution_dict['name'] = institution_data['display_name']
    institution_dict['type'] = institution_data['type']
    institution_dict['homepage_url'] = institution_data['homepage_url']
    # repos
    if (not institution_data['repositories']):
        institution_dict['repos'] = None
    else:
        repos_list = []
        for repo in institution_data['repositories']:
            repos_list.append(urlparse(repo['id']).path.split('/')[-1])
        institution_dict['repos'] = ",".join(repos_list)

    institution_dict['works_count'] = institution_data['works_count']
    institution_dict['cited_by_count'] = institution_data['cited_by_count']
    institution_dict['2yr_mean_citedness'] = institution_data['summary_stats'][
        '2yr_mean_citedness']
    institution_dict['h_index'] = institution_data['summary_stats']['h_index']
    institution_dict['i10_index'] = institution_data['summary_stats'][
        'i10_index']
    # geo
    institution_dict['country_code'] = institution_data['geo']['country_code']
    institution_dict['country'] = institution_data['geo']['country']
    institution_dict['region'] = institution_data['geo']['region']
    institution_dict['city'] = institution_data['geo']['city']
    institution_dict['latitude'] = institution_data['geo']['latitude']
    institution_dict['longitude'] = institution_data['geo']['longitude']
    # associated_institutions
    if (not institution_data['associated_institutions']):
        institution_dict['associated_institutions'] = None
    else:
        associated_institutions_list = []
        for associated_institution in institution_data[
                'associated_institutions']:
            associated_institutions_list.append(
                urlparse(associated_institution['id']).path.split('/')[-1])
        institution_dict['associated_institutions'] = ",".join(
            associated_institutions_list)
    # roles
    institution_dict['institution_role'] = None
    institution_dict['funder_role'] = None
    institution_dict['publisher_role'] = None
    if (institution_data['roles']):
        for r in institution_data['roles']:
            if (r['role'] == 'institution'):
                institution_dict['institution_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'funder'):
                institution_dict['funder_role'] = urlparse(
                    r['id']).path.split('/')[-1]
            elif (r['role'] == 'publisher'):
                institution_dict['publisher_role'] = urlparse(
                    r['id']).path.split('/')[-1]

    # x_concepts
    if (not institution_data['x_concepts']):
        institution_dict['x_concepts'] = None
    else:
        x_concepts_list = []
        for x_concept in institution_data['x_concepts']:
            x_concepts_list.append(urlparse(x_concept['id']).path.split('/')[-1])
        institution_dict['x_concepts'] = ",".join(x_concepts_list)

    institution_dict['works_api_url'] = institution_data['works_api_url']
    institution_dict['updated_date'] = institution_data['updated_date'][:10]
    institution_dict['created_date'] = institution_data['created_date']
    return institution_dict


def get_institution_csv():
    institution_path = "../openalex-snapshot/data/institutions"
    institution_list = process_files(institution_path, txt_to_list,
                                     reformat_institution)
    institution_list = [item for item in institution_list if item is not None]
    institution_csv_path = "../csv_results/institutions.csv"
    field_names = [
        'id', 'ror', 'name', 'type', 'homepage_url', 'repos', 'works_count',
        'cited_by_count', '2yr_mean_citedness', 'h_index', 'i10_index',
        'country_code', 'country', 'region', 'city', 'latitude', 'longitude',
        'associated_institutions', 'institution_role', 'funder_role',
        'publisher_role', 'x_concepts', 'works_api_url', 'updated_date',
        'created_date'
    ]
    with open(institution_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(institution_list)


if __name__ == "__main__":
    get_institution_csv()