import requests
import json
import ast
# x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
#
# block = x.split(';;')
# chunks = []
# jsontest = json.loads(block[1])
# print(jsontest[0]['crypto'])
# print(jsontest[0]['balance'])

# api_calls = []
# def farmr_api_call():
#     x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
#     blocks = x.split(';;')
#     for block in blocks:
#         try:
#             json_dict = json.loads(block)
#             api_calls.append(json_dict[0])
#         except:
#             pass



api_calls = {}
def farmr_api_call():
    x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
    blocks = x.split(';;')
    for block in blocks:
        try:
            json_dict = json.loads(block)
            api_calls[json_dict[0]['crypto']] = json_dict[0]['balance']
        except:
            pass

farmr_api_call()