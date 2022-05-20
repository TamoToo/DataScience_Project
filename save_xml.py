def extract_xml_data(xml_string, home_team, away_team, card_type='y'):
    root = ET.fromstring(xml_string)
    home_team_stat = 0
    away_team_stat = 0

    if root.tag == 'possession':
        try:
            home_team_stat = root[-1][0].text
            away_team_stat = str(100 - int(home_team_stat))
        except:
            home_team_stat, away_team_stat = None, None

    elif root.tag == 'card':
        for page in list(root):
            try:
                if page.find('card_type').text == card_type:
                    if page.find('team').text == home_team:
                        home_team_stat += 1
                    else:
                        away_team_stat += 1
            except:
                pass

    else:
        for page in list(root):
            try:
                if page.find('team').text == home_team:
                    home_team_stat += 1
                else:
                    away_team_stat += 1
            except:
                print('test')
                pass
                
    return home_team_stat, away_team_stat



stats_columns = ['shoton', 'shotoff', 'foulcommit', 'card', 'cross', 'corner', 'possession']
new_stats_columns = {old_name: [old_name + '_home_team', old_name + '_away_team'] for old_name in stats_columns}

for index, row in match_data.iterrows():
    for old, new in new_stats_columns.items():
        home_team = row['home_team_api_id']
        away_team = row['away_team_api_id']
        if old == 'card':
            match_data['yellow_card_home_team'], match_data['yellow_card_away_team'] = extract_xml_data(match_data[old][index], home_team, away_team, card_type='y')
            match_data['red_card_home_team'], match_data['red_card_away_team'] = extract_xml_data(match_data[old][index], home_team, away_team, card_type='r')
        else:
            match_data[new[0]], match_data[new[1]] = extract_xml_data(match_data[old][index], home_team, away_team)


match_data.drop(columns=stats_columns, inplace=True)
