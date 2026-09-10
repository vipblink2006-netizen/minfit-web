import urllib.request
import re
url = "https://drive.google.com/drive/folders/1739fM6O4Yt4v7yW3G0vYgIqfE2-r1o"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if title_match:
        print("TITLE:", title_match.group(1))
    else:
        print("No title found.")
except Exception as e:
    print("Error:", e)
