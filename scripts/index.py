import os

DOCS_DIR = "docs"
INDEX_PATH = "docs/index.md"

def build_tree():
    tree = {}
    for root, _, files in os.walk(DOCS_DIR):
        rel_root = os.path.relpath(root, DOCS_DIR)
        parts = [] if rel_root == "." else rel_root.split(os.sep)

        node = tree
        for part in parts:
            node = node.setdefault(part, {})

        for f in sorted(files):
            if f == "index.md" or not f.endswith(".md"):
                continue
            rel_path = os.path.join(rel_root, f) if rel_root != "." else f
            title = f[:-3]
            node.setdefault("__files__", []).append((title, rel_path.replace(os.sep, "/")))

    return tree

def render_tree(tree, depth=0):
    lines = []
    indent = "  " * depth

    for title, rel_path in sorted(tree.get("__files__", [])):
        lines.append(f"{indent}- [{title}]({rel_path})")

    subfolders = sorted(k for k in tree if k != "__files__")
    for folder in subfolders:
        lines.append(f"{indent}- **{folder}**")
        lines.extend(render_tree(tree[folder], depth + 1))

    return lines

def generate_index():
    tree = build_tree()
    lines = ["# Index\n"]
    lines.extend(render_tree(tree))
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    generate_index()