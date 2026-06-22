import os

# ── Root of your cloned repo ────────────────────────────────────────────────
# Change this to the path where you cloned nlp-lab, or leave "." to run the
# script from inside the repo folder.
ROOT = "."

# ── Folder structure ─────────────────────────────────────────────────────────
STRUCTURE = {
    "projects": {
        "01_text_preprocessing": ["notebooks", "data/raw", "data/processed", "outputs"],
        "02_text_classification": {
            "spam_detection":       ["notebooks", "data/raw", "data/processed", "outputs"],
            "sentiment_analysis":   ["notebooks", "data/raw", "data/processed", "outputs"],
            "topic_classification": ["notebooks", "data/raw", "data/processed", "outputs"],
        },
        "03_named_entity_recognition": ["notebooks", "data/raw", "data/processed", "outputs"],
        "04_text_generation":          ["notebooks", "data/raw", "data/processed", "outputs"],
        "05_transformers":             ["notebooks", "data/raw", "data/processed", "outputs"],
    },
    "shared": {
        "src":     [],          # Python files added below
        "models":  ["checkpoints", "final"],
        "configs": [],
    },
    "resources": ["papers", "references", "datasets"],
}

# ── Files to create (path relative to ROOT) ──────────────────────────────────
FILES = [
    # shared src
    "shared/src/__init__.py",
    "shared/src/preprocessing.py",
    "shared/src/features.py",
    "shared/src/utils.py",
    # shared configs
    "shared/configs/config.yaml",
    # per-project READMEs
    "projects/01_text_preprocessing/README.md",
    "projects/02_text_classification/README.md",
    "projects/02_text_classification/spam_detection/README.md",
    "projects/02_text_classification/sentiment_analysis/README.md",
    "projects/02_text_classification/topic_classification/README.md",
    "projects/03_named_entity_recognition/README.md",
    "projects/04_text_generation/README.md",
    "projects/05_transformers/README.md",
]

# ── File default contents ─────────────────────────────────────────────────────
FILE_CONTENTS = {
    "shared/src/__init__.py": "# shared source package\n",
    "shared/src/preprocessing.py": (
        "# Text cleaning & preprocessing utilities\n\n"
        "def clean_text(text: str) -> str:\n"
        "    \"\"\"Basic text cleaner — extend as needed.\"\"\"\n"
        "    return text.strip().lower()\n"
    ),
    "shared/src/features.py": (
        "# Feature engineering utilities\n\n"
        "def extract_features(text: str) -> dict:\n"
        "    \"\"\"Placeholder — add your feature logic here.\"\"\"\n"
        "    return {}\n"
    ),
    "shared/src/utils.py": (
        "# General helper functions\n\n"
        "def load_data(path: str):\n"
        "    \"\"\"Load a dataset from the given path.\"\"\"\n"
        "    pass\n"
    ),
    "shared/configs/config.yaml": (
        "# Global configuration\n"
        "data:\n"
        "  raw_path: data/raw\n"
        "  processed_path: data/processed\n\n"
        "model:\n"
        "  save_path: shared/models/final\n"
    ),
}

# Default README template
README_TEMPLATE = """\
# {project_name}

## Overview
Brief description of this project.

## Dataset
- Source:
- Size:

## Approach
Describe the NLP technique used.

## Results
| Metric | Score |
|--------|-------|
| Accuracy | - |
| F1 Score | - |

## How to Run
```bash
jupyter notebook notebooks/
```
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def make_dirs(base: str, structure: dict | list) -> None:
    """Recursively create directories from the structure definition."""
    if isinstance(structure, list):
        for sub in structure:
            path = os.path.join(base, sub)
            os.makedirs(path, exist_ok=True)
            keep = os.path.join(path, ".gitkeep")
            if not os.listdir(path):          # only add .gitkeep to empty dirs
                open(keep, "w").close()
        return
    for name, children in structure.items():
        path = os.path.join(base, name)
        os.makedirs(path, exist_ok=True)
        make_dirs(path, children)


def make_files(base: str, files: list[str]) -> None:
    """Create stub files with sensible default content."""
    for rel_path in files:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if os.path.exists(full_path):
            print(f"  [skip]   {rel_path}  (already exists)")
            continue
        content = FILE_CONTENTS.get(rel_path)
        if content is None and rel_path.endswith("README.md"):
            project_name = os.path.basename(os.path.dirname(rel_path)).replace("_", " ").title()
            content = README_TEMPLATE.format(project_name=project_name)
        with open(full_path, "w") as f:
            f.write(content or "")
        print(f"  [create] {rel_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n🚀  Building nlp-lab structure inside: {os.path.abspath(ROOT)}\n")
    make_dirs(ROOT, STRUCTURE)
    make_files(ROOT, FILES)
    print("\n✅  Done! Your nlp-lab folder structure is ready.\n")
    print("Next steps:")
    print("  1. cd into your repo   →  cd nlp-lab")
    print("  2. Run this script     →  python setup_nlp_lab.py")
    print("  3. Stage everything    →  git add .")
    print('  4. Commit              →  git commit -m "chore: scaffold project structure"')
    print("  5. Push                →  git push origin main\n")


if __name__ == "__main__":
    main()
