import marko 

print(marko.__doc__)

all_content = ''

with open('./4.Data Engineering.md') as md_file:
    all_content = '\n'.join(md_file.readlines())

print(type(all_content))
parsed = marko.Parser().parse(all_content)

print(parsed)
print(dir(parsed))