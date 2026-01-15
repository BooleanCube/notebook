import os, json, re


def parse_markdown_headers(markdown_text):
    """
    Parses a markdown string and extracts headers with level, id, and title.
    Ignores headers found inside code blocks.
    """
    headers = []
    lines = markdown_text.split('\n')
    in_code_block = False

    # Regex to match a header: 1-6 hashes, a space, then the title
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    for line in lines:
        stripped_line = line.strip()

        # Check for code block fences (``` or ~~~)
        # We toggle the state if we see a fence
        if stripped_line.startswith('```') or stripped_line.startswith('~~~'):
            in_code_block = not in_code_block
            continue

        # If we are in a code block, skip processing this line
        if in_code_block:
            continue

        # Check if the line is a header
        match = header_pattern.match(line)
        if match:
            hashes, raw_title = match.groups()
            level = len(hashes)
            title = raw_title.strip()

            # Generate ID (slug format)
            # 1. Lowercase
            # 2. Remove non-alphanumeric characters (excluding spaces/hyphens)
            # 3. Replace spaces with hyphens
            slug = title.lower()
            slug = re.sub(r'[^\w\s-]', '', slug) # Remove special chars
            slug = re.sub(r'\s+', '-', slug)     # Replace spaces with -

            headers.append({
                "level": level,
                "id": slug,
                "title": title
            })

    return headers


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
        meta['toc'] = parse_markdown_headers(content)

        pages.append(meta)

data = {
    "pages": pages
}

with open('./directory.json', 'w') as file:
    file.write(json.dumps(data, indent=2))
