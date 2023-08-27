from scholarly import scholarly
import pandas as pd
import requests
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def possible_name_list(name):
    cleared_name = name.replace('PhD','').replace('MS','').strip() # remove PhD and MS
    name_list = [cleared_name]
    temp_name = re.sub(r'\b[A-Za-z]\b[ .]*', '', cleared_name).strip()
    if temp_name != cleared_name:
        name_list.append(temp_name)
    # get different parts of name splitted by ' '
    if ' ' in cleared_name:
        name_split = cleared_name.split(' ')
        for part in name_split:
            # if part is not a single letter
            if len(part) > 1:
                name_list.append(part)
    return name_list

def google_scholar_get_one_author(name, affiliation, email):
    alternative_name_list = possible_name_list(name)
    if '@' in email:  # only keep email after @
        email0 = email.split('@')[1]
    elif email == 'Missing':
        email0 = None
    else:
        email0 = email

    # search by name and affiliation
    for possible_name in alternative_name_list:
        search_query = possible_name + ' ' + affiliation
        author = next(scholarly.search_author(search_query), None)
        if author:
            return (author.get('scholar_id'), author.get('url_picture'))
    if email0 is None:
        return (None,None)
    # search by name and email
    for possible_name in alternative_name_list:
        search_query = possible_name + ' ' + email0
        author = next(scholarly.search_author(search_query), None)
        if author:
            return (author.get('scholar_id'), author.get('url_picture'))

    return (None,None)

def openalex_get_one_author(name, institution):
    name_list = possible_name_list(name)
    for n in name_list:
        url = "https://api.openalex.org/authors?filter=display_name.search:{},last_known_institution.country_code:US&per-page=200".format(n)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['meta']['count'] == 0:
                # print('here')
                return None
            elif data['meta']['count'] >= 1:
                # collect authors' institutions list
                inst_list = []
                for author in data['results']:
                    # if author has no institution, skip
                    if author['last_known_institution'] is not None:
                        inst_list.append(author['last_known_institution']['display_name'])
                    else:
                        inst_list.append(None)

                # find the best match
                best_match = process.extractOne(institution,inst_list,scorer=fuzz.token_sort_ratio)
                if best_match is None:
                    print(f'No match found for {name} from {institution}\n')
                    return None

                if best_match[1] > 80:  # if there is a match, return the author object
                    # print(f'Match Score: {best_match[1]}, Matched Institution: {best_match[0]}\n')
                    return data['results'][inst_list.index(best_match[0])]
                else:  # if there is no match, return None
                    # print(f'Match Score: {best_match[1]}, Matched Institution: {best_match[0]}\n')
                    return None

        else:
            return None
        

df = pd.read_csv("./faculty_data/Faculty_CS_ECE-20230806.csv")
df_cs_original = df[df['Department_Id'] == 0].copy()  # filter df to only include faculty with department_id = 0
df_cs_original = df_cs_original.reset_index(drop=True)
df_cs_original['scholar_id'] = None
df_cs_original['image_url'] = None
df_cs_original['openalex_id'] = None
df_cs_original['gender'] = None
df_cs_original['age'] = None
df_cs = df_cs_original.copy()

for i in range(45,55):
    name = df_cs['Name'][i]
    affiliation = df_cs['University_Name'][i]
    email = df_cs['Email'][i]

    # google scholar search
    (scholar_id,image_url) = google_scholar_get_one_author(name, affiliation, email)
    if scholar_id is not None:
        df_cs.loc[i,'scholar_id'] = scholar_id
        df_cs.loc[i,'image_url'] = image_url
        continue

    # openalex search
    openalex_author = openalex_get_one_author(name, affiliation)
    if openalex_author is not None:
        df_cs.loc[i,'openalex_id']= openalex_author['id']
    
# store the result to csv file
df_cs.to_csv('./result.csv',index=False)