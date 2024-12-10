import os
import re
import markdown

# Adjust working directory if needed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # T-PORTAL directory

# Paths
FAQ_MD_PATH = os.path.join(ROOT_DIR, "markdown", "faq.md")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
OUTPUT_DIR = os.path.join(ROOT_DIR, "support-pages")

def load_template(name):
    with open(os.path.join(TEMPLATES_DIR, name), 'r', encoding='utf-8') as f:
        return f.read()

index_template = load_template("index.html")
category_template = load_template("category.html")
question_template = load_template("question.html")

with open(FAQ_MD_PATH, "r", encoding="utf-8") as f:
    faq_content = f.read()

category_pattern = re.compile(
    r"## Category:\s*(?P<category_name>.*?)\n"
    r"slug:\s*(?P<category_slug>.*?)\n"
    r"description:\s*(?P<category_desc>.*?)\n"
    r"pages_folder:\s*(?P<pages_folder>.*?)\n"
    r"(?P<questions>(?:(?!## Category).)*)",
    re.DOTALL
)

question_pattern = re.compile(
    r"### Question:\s*(?P<question_title>.*?)\n"
    r"slug:\s*(?P<question_slug>.*?)\n"
    r"answer:\n?(?P<question_answer>.*?)(?=### Question|## Category|$)",
    re.DOTALL
)

categories = []
for c_match in category_pattern.finditer(faq_content):
    category_data = {
        "title": c_match.group("category_name").strip(),
        "slug": c_match.group("category_slug").strip(),
        "description": c_match.group("category_desc").strip(),
        "folder": c_match.group("pages_folder").strip(),
        "questions": []
    }

    questions_block = c_match.group("questions")
    for q_match in question_pattern.finditer(questions_block):
        q_title = q_match.group("question_title").strip()
        q_slug = q_match.group("question_slug").strip()
        q_answer_md = q_match.group("question_answer").strip()
        q_answer_html = markdown.markdown(q_answer_md)
        category_data["questions"].append({
            "title": q_title,
            "slug": q_slug,
            "answer_html": q_answer_html
        })
    categories.append(category_data)

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Generate index.html (FAQ categories)
cat_links = []
for cat in categories:
    cat_links.append({
        "link": f"{cat['folder']}/index.html",
        "title": cat['title'],
        "description": cat['description']
    })

index_html = index_template
category_list_html = ""
for cat in cat_links:
    category_list_html += f'<li><a href="{cat["link"]}">{cat["title"]}</a>: {cat["description"]}</li>\n'

index_html = index_html.replace(
    "<!-- BEGIN CATEGORIES -->\n<li><a href=\"{{ category_link }}\">{{ category_title }}</a>: {{ category_description }}</li>\n<!-- END CATEGORIES -->",
    category_list_html.strip()
)

with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# Generate category and question pages
for cat in categories:
    cat_dir = os.path.join(OUTPUT_DIR, cat['folder'])
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)
    # Category page
    cat_html = category_template
    cat_html = cat_html.replace("{{ category_title }}", cat["title"])
    cat_html = cat_html.replace("{{ category_description }}", cat["description"])

    question_list_html = ""
    for q in cat["questions"]:
        q_link = f"{q['slug']}.html"
        question_list_html += f'<li><a href="{q_link}">{q["title"]}</a></li>\n'

    cat_html = cat_html.replace(
        "<!-- BEGIN QUESTIONS -->\n<li><a href=\"{{ question_link }}\">{{ question_title }}</a></li>\n<!-- END QUESTIONS -->",
        question_list_html.strip()
    )

    with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cat_html)

    # Question pages
    for q in cat["questions"]:
        q_html = question_template
        q_html = q_html.replace("{{ question_title }}", q["title"])
        q_html = q_html.replace("{{ category_title }}", cat["title"])
        q_html = q_html.replace("{{ question_answer }}", q["answer_html"])
        with open(os.path.join(cat_dir, f"{q['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(q_html)

print("Site generated in 'support-pages' directory.")
