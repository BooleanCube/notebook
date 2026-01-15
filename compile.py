import os, json

pages = []

for entry in os.scandir('.'):
    if entry.is_dir() and not entry.name.startswith("."):
        content_path = entry.path + "/index.md"
        content_file = open(content_path, 'r')
        content = content_file.read()

        meta_path = entry.path + "/metadata.json"
        meta_file = open(meta_path, 'r')
        meta = json.loads(meta_file.read())

        meta['slug'] = entry.name
        meta['content'] = content

        pages.append(meta)

data = {
    "pages": pages
}

with open('./directory.json', 'w') as file:
    file.write(json.dumps(data, indent=2))
