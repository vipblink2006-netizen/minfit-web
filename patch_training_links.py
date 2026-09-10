with open('workflow_api.py', 'r') as f:
    content = f.read()

# 1. Add "training" to links dict
content = content.replace(
    '        "perspective": "",\n        "general": []',
    '        "perspective": "",\n        "training": "",\n        "general": []'
)

# 2. Add elif for training
content = content.replace(
    '        elif any(k in l_lower for k in ["tài liệu", "tai lieu", "drive", "tổng hợp"]):\n            links["drive"] = u',
    '        elif any(k in l_lower for k in ["tài liệu", "tai lieu", "drive", "tổng hợp"]):\n            links["drive"] = u\n        elif any(k in l_lower for k in ["slide", "đào tạo", "dao tao", "training", "presentation"]):\n            links["training"] = u'
)

# 3. Add fallback for training
content = content.replace(
    '    if not links["drive"]:\n        for u in urls:\n            if "drive.google.com" in u and u != links.get("sheets"):\n                links["drive"] = u\n                break',
    '    if not links["drive"]:\n        for u in urls:\n            if "drive.google.com" in u and u != links.get("sheets"):\n                links["drive"] = u\n                break\n    if not links["training"]:\n        for u in urls:\n            if "docs.google.com/presentation" in u:\n                links["training"] = u\n                break'
)

# 4. Add "slide" to skip list in fallback loop
content = content.replace(
    '["tổng hợp", "bảng hàng", "mặt bằng", "link 360", "layout", "tài liệu", "tiện ích", "giá bán", "diện tích"]',
    '["tổng hợp", "bảng hàng", "mặt bằng", "link 360", "layout", "tài liệu", "tiện ích", "giá bán", "diện tích", "slide", "đào tạo"]'
)

# 5. Update the URL title fetcher
old_fetch = 'if (not project_name or project_name.startswith("http") or "drive.google.com" in project_name or "docs.google.com" in project_name) and (links["drive"] or links["sheets"]):'
new_fetch = 'if (not project_name or project_name.startswith("http") or "drive.google.com" in project_name or "docs.google.com" in project_name) and (links.get("drive") or links.get("sheets") or links.get("training")):'
content = content.replace(old_fetch, new_fetch)

old_url_to_fetch = 'url_to_fetch = links["drive"] if links["drive"] else links["sheets"]'
new_url_to_fetch = 'url_to_fetch = links.get("training") or links.get("drive") or links.get("sheets")'
content = content.replace(old_url_to_fetch, new_url_to_fetch)

content = content.replace('replace("- Google Sheets", "")', 'replace("- Google Sheets", "").replace("- Google Slides", "")')
content = content.replace('"Google Sheets", "Meet Google Drive', '"Google Sheets", "Google Slides", "Meet Google Drive')

with open('workflow_api.py', 'w') as f:
    f.write(content)
