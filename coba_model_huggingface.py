import requests

API_URL = "https://api-inference.huggingface.co/models/rizkyds/bert-phb"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
		"question": "dimana rizky tinggal?",
		"context": "nama saya rizky dan saya tinggal di tegal"
	},
})
print(output)