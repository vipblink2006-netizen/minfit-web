import re
text = "7x tr/m"
m2_price_match = re.search(r'(\d+(?:[\.,]\d+)?)([xX])?\s*(?:-|đến|–)?\s*(\d+(?:[\.,]\d+)?)?([xX])?\s*(?:tr(?:iệu)?(?:/m[2²]?)?|tr/m)', text, re.IGNORECASE)
print(m2_price_match.groups())
