#!/usr/bin/env python3
"""
توليد شجرة ملفات بنمط Markdown مع دعم تحديد العمق الأقصى.

مثال للاستخدام:
    python generate_tree_md.py --root . --output tree.md --max-depth 3
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan directories recursively and export a Markdown-formatted tree."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="المجلد الجذر الذي سيتم إنشاء الشجرة منه (القيمة الافتراضية: المجلد الحالي).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("directory_tree.md"),
        help="اسم ملف Markdown الناتج (القيمة الافتراضية: directory_tree.md).",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help=(
            "أقصى عمق للمجلدات. استخدم قيمة موجبة. إذا تُرك فارغًا، سيتم سرد جميع الأعماق."
        ),
    )
    parser.add_argument(
        "--ignore-hidden",
        action="store_true",
        help="تجاهل الملفات والمجلدات المخفية (التي يبدأ اسمها بنقطة).",
    )
    return parser.parse_args()


def should_include(path: Path, ignore_hidden: bool) -> bool:
    if not ignore_hidden:
        return True
    return not path.name.startswith(".")


def get_sorted_children(path: Path, ignore_hidden: bool) -> List[Path]:
    children = [
        child for child in path.iterdir() if should_include(child, ignore_hidden)
    ]
    children.sort(key=lambda p: (p.is_file(), p.name.lower()))
    return children


def build_tree_lines(
    root: Path,
    prefix: str = "",
    is_last: bool = True,
    depth: int = 0,
    max_depth: Optional[int] = None,
    ignore_hidden: bool = False,
) -> Iterable[str]:
    connector = "└── " if is_last else "├── "
    name = root.name + ("/" if root.is_dir() else "")
    yield f"{prefix}{connector}{name}"

    if root.is_dir():
        if max_depth is not None and depth >= max_depth - 1:
            return

        children = get_sorted_children(root, ignore_hidden)
        if not children:
            return

        extension_prefix = f"{prefix}{'    ' if is_last else '│   '}"
        for index, child in enumerate(children):
            child_is_last = index == len(children) - 1
            yield from build_tree_lines(
                child,
                prefix=extension_prefix,
                is_last=child_is_last,
                depth=depth + 1,
                max_depth=max_depth,
                ignore_hidden=ignore_hidden,
            )


def generate_markdown(
    root: Path,
    max_depth: Optional[int],
    ignore_hidden: bool,
) -> str:
    # ضمان استخدام المسار المطلق للعرض في رأس الملف
    root = root.resolve()
    heading = f"# Directory Tree for `{root}`\n\n"
    code_block_start = "```\n"
    code_block_end = "```\n"

    lines = [root.name + "/"]  # إظهار الجذر بشكل واضح على السطر الأول
    children = get_sorted_children(root, ignore_hidden)

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        lines.extend(
            build_tree_lines(
                child,
                prefix="",
                is_last=is_last,
                depth=0,
                max_depth=max_depth,
                ignore_hidden=ignore_hidden,
            )
        )

    tree_str = "\n".join(lines)
    return heading + code_block_start + tree_str + "\n" + code_block_end


def main() -> None:
    args = parse_args()
    root_path = args.root.expanduser().resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"المجلد المحدد غير موجود: {root_path}")

    markdown_content = generate_markdown(
        root=root_path,
        max_depth=args.max_depth,
        ignore_hidden=args.ignore_hidden,
    )

    output_path = args.output.expanduser().resolve()
    output_path.write_text(markdown_content, encoding="utf-8")
    print(f"تم إنشاء الملف: {output_path}")


if __name__ == "__main__":
    main()