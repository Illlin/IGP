import requests

url = "http://localhost:5000/api/sculpt"

filepath = "FlaskServer/test_files/"
filename = "blank.wav"

r = requests.post(url, files={"file": open(filepath+filename, "rb")})

print(r.status_code)
print(r.json())