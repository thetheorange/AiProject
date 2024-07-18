import json

import requests

r = requests.post(url=r'http://47.121.115.252:8193/textModel/stream',
                  headers={
                      "Content-Type": "application/json"
                  },
                  data=json.dumps({
                      "uuid": r'de09d5ac58da5c0c856bd4a38dc71acf',
                      "username": 'wly',
                      "dialog": [{"role": "system", "content": "数学小助手"},
                                 {"role": "user", "content": "请教我三角函数"}]
                  }))
print(r.json())
