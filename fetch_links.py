import urllib.request
import re

urls = [
    "https://docs.google.com/spreadsheets/d/1FR-qtrHfuSu3jJfOvEE-fxpXfYAR3iMF4p6vgOfyHH8/edit?gid=0#gid=0",
    "https://drive.google.com/drive/folders/1YE91uX3yISmaruQVmVMsa-ZTSAcnlH6l",
    "https://drive.google.com/drive/folders/1gYXso2YUoGHcOPQQt-DSVA-pLF9I9Ece",
    "https://drive.google.com/drive/folders/1IxWcdCEJ4xzcSaoMTFPk0FFVqkSqjhpQ"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        print(f"URL: {url}\nTITLE: {title_match.group(1) if title_match else 'None'}\n")
    except Exception as e:
        print(f"URL: {url}\nERROR: {e}\n")
