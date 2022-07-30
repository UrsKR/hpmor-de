#!/usr/bin/env python3

# by Torben Menke https://entorb.net


import os
import re
import sys

os.chdir(os.path.dirname(sys.argv[0]) + "/..")

source_file = "hpmor-epub-5-html-1.html"
target_file = "hpmor-epub-6-html-2.html"

print("=== 6. HTML modifications ===")


with open(source_file, mode="r", encoding="utf-8", newline="\n") as fhIn:
    cont = fhIn.read()

# remove strange leftovers between header and Disclaimer
cont = re.sub(
    r"(</header>).*?<p>Basierend",
    r"\1<p>Fanfiction basierend",
    cont,
    flags=re.DOTALL | re.IGNORECASE,
)


# doc structure (not needed any more, using calibi --level1-toc flag instead)
# sed -i 's/<h1 /<h1 class="part"/g' $target_file
# sed -i 's/<h2 /<h2 class="chapter"/g' $target_file
# sed -i 's/<h3 /<h3 class="section"/g' $target_file

# remove ids from chapters since umlaute cause problem
cont = re.sub(
    r'(<h\d) id="[^"]+"',
    r"\1",
    cont,
    flags=re.DOTALL | re.IGNORECASE,
)
cont = re.sub(
    r'(<h\d class="unnumbered") id="[^"]+"',
    r"\1",
    cont,
    flags=re.DOTALL | re.IGNORECASE,
)

# add part numbers
part_no = 0
while "<h1>" in cont:
    part_no += 1
    cont = cont.replace("<h1>", f"<h1_DONE>{part_no}. ", 1)
cont = cont.replace("<h1_DONE>", "<h1>")

# add chapter numbers
chapter_no = 0
while "<h2>" in cont:
    chapter_no += 1
    cont = cont.replace("<h2>", f"<h2_DONE>{chapter_no}. ", 1)
cont = cont.replace("<h2_DONE>", "<h2>")

# fix double rules
# cont = cont.replace("<hr />\n<hr />", "<hr />")
cont = re.sub(
    r"<hr */>\n<hr */>",
    r"<hr />",
    cont,
    flags=re.DOTALL | re.IGNORECASE,
)
# fixing linebreak at author's comment
cont = cont.replace("<p>E. Y.: </p>\n<p>", "<p>E.Y.: ")

# converting "color-marked" styles of 1.sh back to proper style classes
cont = re.sub(
    r'<(div|span) style="color: (parsel|writtenNote|McGonagallWhiteBoard|headline)"',
    r'<\1 class="\2"',
    cont,
)

# add css style file format for \emph in \emph
with open("ebook/html.css", mode="r", encoding="utf-8", newline="\n") as fhIn:
    css = fhIn.read()
cont = cont.replace("</style>\n", css + "\n</style>\n")


with open(target_file, mode="w", encoding="utf-8", newline="\n") as fhOut:
    fhOut.write(cont)

with open("hpmor.html", mode="w", encoding="utf-8", newline="\n") as fhOut:
    fhOut.write(cont)
