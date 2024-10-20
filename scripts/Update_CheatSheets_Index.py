#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python3 script to generate the index markdown page that
reference all cheat sheets grouped by the first letter.

The index markdown page is located on the root folder
and is named "Index.md".
"""
import os
from collections import OrderedDict

# Define utility functions
def extract_languages_snippet_provided(cheatsheet):
    markers = ["javascript", "java", "csharp", "c", "cpp", "html", "xml", "python",
               "ruby", "php", "json", "sql", "bash", "shell", "coldfusion", "perl",
               "vbnet"]
    with open(f"../cheatsheets/{cheatsheet}", encoding="utf8") as cs_file:
        cs_content = cs_file.read().lower().replace(" ","")
    return [
        marker.capitalize()
        for marker in markers
        if f"```{marker}" + "\n" in cs_content
    ]

# Define templates
cs_md_link_template = "[%s](cheatsheets/%s)."
language_md_link_template = "![%s](assets/Index_%s.png)"
header_template = "## %s\n\n"
top_menu_template = "[%s](Index.md#%s)"
cs_count_template = "**%s** cheat sheets available."
cs_index_title_template = "# Index Alphabetical\n\n"

# Scan all CS files
index = {}
cs_count = 0
cheatsheets = [f.name for f in os.scandir("../cheatsheets") if f.is_file()]
for cheatsheet in cheatsheets:
    letter = cheatsheet[0].upper()
    if letter not in index:
        index[letter] = [cheatsheet]
    else:
        index[letter].append(cheatsheet)
    cs_count += 1
index = OrderedDict(sorted(index.items()))

# Generate the index file
with open("../Index.md", "w") as index_file:
    index_file.write(cs_index_title_template)
    index_count = len(index)
    index_file.write(cs_count_template % cs_count)
    index_file.write("\n\n*Icons beside the cheat sheet name indicate in which language(s) code snippet(s) are provided.*")
    index_file.write("\n\n")
    # Generate the top menu
    for letter in index:
        index_file.write(top_menu_template % (letter, letter.lower()))
        index_file.write(" ")
    index_file.write("\n\n")
    for j, letter in enumerate(index, start=1):
        cs_count =  len(index[letter])
        index_file.write(header_template % letter)
        for i, cs_file in enumerate(index[letter], start=1):
            cs_name = cs_file.replace("_", " ").replace(".md", "").strip()
            index_file.write(cs_md_link_template % (cs_name, cs_file))
            languages = extract_languages_snippet_provided(cs_file)
            if len(languages) > 0:
                index_file.write(" ")
                for language in languages:
                    index_file.write(language_md_link_template % (language, language))
                    index_file.write(" ")
            index_file.write("\n")
            if i != cs_count:
                index_file.write("\n")
        if j != index_count:
            index_file.write("\n")

print("Index updated.")