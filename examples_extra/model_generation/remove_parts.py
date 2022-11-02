import re

regex = r"(\*PART)(.+?)(\*)(?!PART)"

with open('mesh.k', 'r+') as file:
    text = re.sub(regex, "*", file.read(), flags=re.DOTALL)
    file.seek(0, 0) # seek to beginning
    file.write(text)
    file.truncate()  # get rid of any trailing characters

# matches = re.search(regex, file, re.DOTALL)
print(text[:1000])