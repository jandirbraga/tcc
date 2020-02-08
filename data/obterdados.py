import requests
import json
import urllib.parse
import time
import pandas as pd

mmr = 4100
quantidade = 200

query = """
WITH match_ids AS (SELECT match_id FROM public_matches
    WHERE TRUE
    condition
    AND public_matches.avg_mmr >= {}
    AND game_mode IN (1,2,3,4,22)
    AND public_matches.start_time >= extract(epoch from timestamp '2020-01-26')
    ORDER BY match_id DESC
    LIMIT 100)
    SELECT * FROM
        (SELECT --*,
            match_id,
            radiant_win,
            avg_mmr,
            duration,
            lobby_type,
            game_mode
            --COLUNS
        FROM public_matches
        WHERE match_id IN (SELECT match_id FROM match_ids)) matches
    JOIN
        (SELECT match_id, string_agg(hero_id::text, ',') radiant_team FROM public_player_matches WHERE match_id IN (SELECT match_id FROM match_ids) AND player_slot <= 127 GROUP BY match_id) radiant_team
        USING(match_id)
    JOIN
        (SELECT match_id, string_agg(hero_id::text, ',') dire_team FROM public_player_matches WHERE match_id IN (SELECT match_id FROM match_ids) AND player_slot > 127 GROUP BY match_id) dire_team
        USING(match_id)
"""

parsedQuery = urllib.parse.quote(query.format(mmr))
call = 'https://api.opendota.com/api/explorer?sql=' + parsedQuery

t = time.localtime()
current_time = time.strftime("%y-%m-%d %Hh%Mm%Ss", t)
nomecsv = current_time + '.csv'

lastId = 0
erros = 0
firstCall = True
for i in range(0, quantidade // 100) :
    time.sleep(2.5)
    condition = ''
    if lastId > 0 :
        condition = 'AND public_matches.match_id < {}'.format(lastId)
        
    ans_get = requests.get(call.replace('condition',condition))
    ans_json = json.loads(ans_get.text)
    if "rows" in ans_json :
        df = pd.io.json.json_normalize(ans_json['rows'])
        lastId = df.iloc[0,:]['match_id']
        df.sort_values(['match_id'],ascending=[0],inplace=True)
        if firstCall :
            df.to_csv(nomecsv)
            firstCall = False
        else :
            df.to_csv(nomecsv, mode='a', header=False)
    else:
        erros+= 1
        print(ans_json)

data = pd.read_csv(nomecsv)

print('Foram obtidas {} partidas e tivemos {} erros'.format(data.shape[0], erros))
