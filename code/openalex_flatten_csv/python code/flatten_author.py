import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_author(author_data):
    author_dict = {}
    author_dict['id'] = urlparse(author_data['id']).path.split('/')[
        -1]  # get the last part of the path eg. A2096939881
    author_dict['name'] = author_data['display_name']
    author_dict['works_count'] = author_data['works_count']
    author_dict['cited_by_count'] = author_data['cited_by_count']
    author_dict['2yr_mean_citedness'] = author_data['summary_stats'][
        '2yr_mean_citedness']
    author_dict['h_index'] = author_data['summary_stats']['h_index']
    author_dict['i10_index'] = author_data['summary_stats']['i10_index']
    if (author_data['last_known_institution'] is None):
        author_dict['last_known_institution'] = None
    else:
        author_dict['last_known_institution'] = urlparse(
            author_data['last_known_institution']['id']).path.split('/')[-1]
    # x_concepts
    if (not author_data['x_concepts']):
        author_dict['x_concepts'] = None
    else:
        x_concepts_list = []
        for concept in author_data['x_concepts']:
            x_concepts_list.append(urlparse(concept['id']).path.split('/')[-1])
        author_dict['x_concepts'] = ",".join(x_concepts_list)

    author_dict['works_api_url'] = author_data['works_api_url']
    author_dict['updated_date'] = author_data[
        'updated_date'][:10]  # ignore the accurate hours, keep the date
    author_dict['created_date'] = author_data['created_date']
    return author_dict


def get_author_csv():
    author_path = "../openalex-snapshot/data/authors"
    author_list = process_files(author_path, txt_to_list, reformat_author)
    author_csv_path = "../csv_results/authors.csv"
    field_names = [
        'id', 'name', 'works_count', 'cited_by_count', '2yr_mean_citedness',
        'h_index', 'i10_index', 'last_known_institution', 'x_concepts',
        'works_api_url', 'updated_date', 'created_date'
    ]
    with open(author_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(author_list)

if __name__ == "__main__":
    get_author_csv()
