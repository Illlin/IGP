import requests

url = "http://localhost:5000/api/sculpt"

filepath = "test_files/"
filename = "test_happy.wav"

r = requests.post(url, files={"file": open(filepath+filename, "rb")})

print(r.status_code)
