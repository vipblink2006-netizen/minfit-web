with open('workflow_api.py', 'r') as f:
    content = f.read()

injection = """    project_name = re.sub(r'[\:\-–🔥🌟👉✨💥]+$', '', project_name).strip()

    if (not project_name or project_name.startswith("http") or "drive.google.com" in project_name) and (links["drive"] or links["sheets"]):
        import urllib.request
        try:
            url_to_fetch = links["drive"] if links["drive"] else links["sheets"]
            req = urllib.request.Request(url_to_fetch, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                fetched_title = title_match.group(1).replace("- Google Drive", "").replace("- Google Sheets", "").strip()
                if fetched_title and fetched_title not in ["Google Drive", "Google Sheets", "Meet Google Drive – One place for all your files"]:
                    project_name = fetched_title
        except Exception:
            pass"""

content = content.replace("    project_name = re.sub(r'[\\:\\-–🔥🌟👉✨💥]+$', '', project_name).strip()", injection)

with open('workflow_api.py', 'w') as f:
    f.write(content)
