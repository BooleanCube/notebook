# 🧠 BooleanCube's Notebook

> Diving into STEM topics, sharing research, and exploring a world of interesting ideas. A space for curiosity, learning, and interaction.

**[View the Live Notebook](https://booleancube.space/notebook)**

This repository serves as the source of truth for my personal knowledge base. It hosts Markdown notes and metadata which are compiled into a JSON directory for the frontend.

## 🌲 Repository Structure

The notebook is organized by topic. Each topic exists in its own directory containing the note content and associated metadata.

```text
notebook/
├── chaos-theory/
│   ├── index.md           # Note content
│   └── metadata.json      # Tags and render info
├── cpp-compiler/
│   ├── index.md
│   └── metadata.json
├── non-lazy-rurq/
│   ├── index.md
│   └── metadata.json
├── ...                    # Other topic folders
├── compile.py             # Build script
├── directory.json         # Generated output for frontend
└── README.md
```

## 🛠️ Usage

This project uses a Python script to aggregate the individual notes into a single data source.

### 1. Create a Note

First things first, create a new branch for the note you are creating/updating.
This is important because for every push made to the main branch, the redis notebook cache on the live server is invalidated.

Create a new folder for your topic (e.g., `new-topic-name/`) and add two files:

**`index.md`**

```markdown
# My New Topic
Content goes here...

```

**`metadata.json`**

```json
{
  "title": "My New Topic",
  "summary": "Quick one line summary of topic",
  "tags": [
    "topic-tag-1",
    "topic-tag-2",
    "topic-tag-3"
  ],
  "date": 1768447120000,
  "cover": "https://i.imgur.com/a4jEurY.jpeg",
  "hidden": false
}
```

#### Metadata Reference

| Field | Type | Description |
| --- | --- | --- |
| `title` | String | The display title of the note. |
| `summary` | String | A brief description used for SEO and the note index card. |
| `tags` | Array | Keywords for categorization (e.g., "Math", "Algorithms"). |
| `date` | Number | **Unix Timestamp (ms)**. The creation or publication date. |
| `cover` | String | URL to a cover image (e.g., Imgur link). |
| `hidden` | Boolean | If `true`, the note is excluded from the live directory. |

### 2. Build the Directory

Run the compilation script to update `directory.json`. This traverses all subfolders and aggregates the metadata.

```bash
python compile.py
```

## 🤝 Contribution

If you spot an error in the logic (especially in the math or algorithm sections) or want to add resources:

1. Fork the repository.
2. Make your changes to the relevant `.md` file.
3. Run `python compile.py` to ensure the build passes.
4. Open a Pull Request.

---

*Created by BooleanCube :]*

dummy commit
