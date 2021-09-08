import requests
import json
import urllib.parse

mmr = 4100 


query = """
SELECT count(1)
FROM public_matches 
WHERE TRUE
AND game_mode IN (1,2,3,4,22)
AND avg_mmr >= {}
AND start_time >= extract(epoch from timestamp '2020-01-26')
"""

parsedQuery = urllib.parse.quote(query.format(mmr))

call = 'https://api.opendota.com/api/explorer?sql=' + parsedQuery

ans_get = requests.get(call)
ans_json = json.loads(ans_get.text)

if 'rows' in ans_json :
    print(ans_json['rows'])
else:
    print(ans_json)