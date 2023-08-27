import csv
from urllib.parse import urlparse
from json_to_csv import process_files, txt_to_list


def reformat_concept(concept_data):
    concept_dict = {}
    concept_dict['id'] = urlparse(concept_data['id']).path.split('/')[-1]
    concept_dict['name'] = concept_data['display_name']
    concept_dict['level'] = concept_data['level']
    concept_dict['description'] = concept_data['description']
    concept_dict['works_count'] = concept_data['works_count']
    concept_dict['cited_by_count'] = concept_data['cited_by_count']
    concept_dict['wikidata'] = concept_data['wikidata']
    concept_dict['2yr_mean_citedness'] = concept_data['summary_stats']['2yr_mean_citedness']
    concept_dict['h_index'] = concept_data['summary_stats']['h_index']
    concept_dict['i10_index'] = concept_data['summary_stats']['i10_index']
    # ancestors
    if (not concept_data['ancestors']):
        concept_dict['ancestors'] = None
    else:
        ancestors_list = []
        for ancestor in concept_data['ancestors']:
            ancestors_list.append(urlparse(ancestor['id']).path.split('/')[-1])
        concept_dict['ancestors'] = ",".join(ancestors_list)

    # related_concepts
    if (not concept_data['related_concepts']):
        concept_dict['related_concepts'] = None
    else:
        related_concepts_list = []
        for related_concept in concept_data['related_concepts']:
            related_concepts_list.append(urlparse(related_concept['id']).path.split('/')[-1])
        concept_dict['related_concepts'] = ",".join(related_concepts_list)

    concept_dict['works_api_url'] = concept_data['works_api_url']
    concept_dict['updated_date'] = concept_data['updated_date'][:10]  # ignore the accurate hours, keep the date
    concept_dict['created_date'] = concept_data['created_date']
    return concept_dict

def get_concept_csv():
    concept_path = "../openalex-snapshot/data/concepts"
    concept_list = process_files(concept_path, txt_to_list, reformat_concept)
    concept_csv_path = "../csv_results/concepts.csv"
    field_names = [
        'id', 'name','level','description', 'works_count', 'cited_by_count', 'wikidata','2yr_mean_citedness',
        'h_index', 'i10_index', 'ancestors', 'related_concepts',
        'works_api_url', 'updated_date', 'created_date'
    ]
    with open(concept_csv_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(concept_list)


if __name__ == "__main__":
    get_concept_csv()