from bs4 import BeautifulSoup
import requests
import subprocess
import os
from rich.console import Console
from rich.markdown import Markdown
from urllib.parse import quote
import sys
from pathlib import Path

# function partially from claude (commented by me)
# to handle syntax and proper display of chars
def handle_syntax(text: str) -> str:
    # get each line of the text
    lines = text.split("\n")
    result = [] # where to save processed

    for line in lines:
        result.append(line) # add to results

        # if not in blockquotes and line isn't empty
        if (not line.startswith(">")) and line.strip() != "":
            result.append("") # double newline

    done = "\n".join(result) # concatenate

    # replace nbsp and ellipsis in test
    return done.replace("\u00A0", " ").replace("\u2026", "...")



# === Constants ===
SCP = 2

URL = f"https://scp-wiki.wikidot.com/scp-{SCP:03d}"



# === Webscrape ===

# get page content
req = requests.get(URL)
soup = BeautifulSoup(req.content, "html.parser")



# === Processing ===

# remove images
for img in soup.find_all("div", class_="scp-image-block"):
    img.decompose()

# remove footnotes
for fn in soup.find_all("sup", class_="footnoteref"):
    fn.decompose()

# remove rating box
for rb in soup.find_all("div", class_="page-rate-widget-box"):
    rb.decompose()

# nothing invisible is important
for invs in soup.find_all("div", class_="display: none"):
    invs.decompose()

# info containers are out-of universe, remove
for ic in soup.find_all("div", class_="info-container"):
    ic.decompose()

# iframes don't have text
for ifm in soup.find_all("iframe"):
    ifm.decompose()

# filter just key div
pc = soup.find("div", id="page-content")

# apply Perl filter
result = subprocess.run(
    ["perl", "scps_filter.pl"], # we're running a perl script called scps_filter.pl
    input=str(pc).encode("utf-8"), # convert html to a str, encode, and pass as input
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# check for errors
if result.returncode != 0:
    print(f"Error with Perl filtering: {result.stderr.decode()}")
    sys.exit()

else:
    # decode output
    filtered_pc = result.stdout.decode("utf-8")

    with open("scp.html", "w", encoding="utf-8") as f:
        f.write(filtered_pc)

    # convert back to soup
    pearled_pc = BeautifulSoup(filtered_pc, "html.parser")

# format <hr>s
for hr in pearled_pc.find_all("hr"):
    hr.replace_with(BeautifulSoup("---", "html.parser"))

# format blockquotes - Thank you ChatGPT! (comments by me)
for bq in pearled_pc.find_all("blockquote"):
    # store markdown-ified lines
    lines = ["<blockquote>", ">"]
    # for each line in the blockquote
    for child in bq.children: # type: ignore

        # convert PageElement to
        # str so we can change it
        child = str(child).strip()
        if child != "":
            # remove <p> tags from text
            child = child.replace("<p>", "").replace("</p>", "")

            # add markdown-ified line to lines
            lines.append(f"> {child}\n>")
    lines.append("</blockquote>")

    # compile markdown-ified lines and replace original blockquote
    compiled = "\n".join(lines)
    #print(compiled) # DEBUG
    bq.replace_with(BeautifulSoup(compiled, "html.parser"))



# === Extract text ===

# get all text tags
tags = pearled_pc.find_all(["p", "li", "blockquote"])

# get all page text
text: list[str] = []

for tag in tags:
   #print (f"Tag: {tag.name} | Attributes: {tag.attrs}")
   for txt in tag.stripped_strings:
        #print(txt)
        text.append(txt)

'''
with open("scp.txt", "w", encoding="utf-8") as f:
    for txt in text:
        f.write(f"{txt}\n")

#sys.exit(0)
'''


# === Parse text ===

# vars to store what matter
item_num = ""
obj_class = ""
SCPs = ""
desc = ""
addenda: list[str] = []
addenda_names: list[str] = []

# current writing flags
curr_section = None # "SCPs", "desc", "addendum"
curr_addendum = ""
curr_addendum_name = ""

for i, string in enumerate(text):
    # check for bottom of page
    if string == "«":
        break

    # get item num
    if "**Item #:**" in string:
        item_num = string.split(" ")[2].split("-")[1]

    # get object class
    elif "**Object Class:**" in string:
        obj_class = string.split(" ")[2]

    # check for main sections

    elif "**Special Containment Procedures:**" in string:
        # update flags
        curr_section = "SCPs"

        # check for procedures on same line
        remainder = string.replace("**Special Containment Procedures:**", "").strip()
        SCPs = f"{remainder}\n" if remainder else ""

    elif "**Description:**" in string:
        # update flags
        curr_section = "desc"

        # check for desc on same line
        remainder = string.replace("**Description:**", "").strip()
        desc = f"{remainder}\n" if remainder else ""

    # check for addenda (Twas a pain, thank you for writing most of it claude)
    elif string.startswith("**Addendum"):
        #print(string) # DEBUG

        # save previous addendum if extant
        if curr_section == "addendum" and curr_addendum:
            addenda.append(curr_addendum)
            addenda_names.append(curr_addendum_name)

        curr_section = "addendum"

        # handle addenda formats (man I wish they could just be consistent)
        if ":" in string:
            # format: "**Addendum 049.1:** Discovery" or "**Addendum:** content"
            c_idx = string.find(":")
            addendum_part = string[:c_idx].strip().replace("**", "") # Addendum 049.1
            title_part = string[c_idx+1:].replace("**", "").strip() # Discovery

            #print(f"AP: {addendum_part!r} | TP: {title_part!r}") # DEBUG

            # differentiate between title and content
            if title_part and len(title_part.split()) <= 3:
                # prolly title
                curr_addendum_name = f"{addendum_part}: {title_part}"
                curr_addendum = ""
            else:
                # content is after colon
                curr_addendum_name = addendum_part
                curr_addendum = f"{title_part}\n" if title_part else ""
        else:
            # format: "**Addendum 046-A** content"
            parts = string.split("**") # ["", "Addendum 046-A", " content..."]

            if len(parts) >= 3:
                curr_addendum_name = parts[1] # "Addendum 046-A"
                remainder = "**".join(parts[2:]).strip() # "content..."
                curr_addendum = f"{remainder}\n" if remainder else ""

    # continue writing to current section
    else:
        if curr_section == "SCPs":
            SCPs = f"{SCPs}{string}\n"
        elif curr_section == "desc":
            desc = f"{desc}{string}\n"
        elif curr_section == "addendum":
            curr_addendum = f"{curr_addendum}{string}\n"

if curr_section == "addendum" and curr_addendum:
    addenda.append(curr_addendum)
    addenda_names.append(curr_addendum_name)

# format stuff
SCPs = handle_syntax(SCPs)
desc = handle_syntax(desc)

for addendum in addenda:
    addendum = handle_syntax(addendum)



# === Save ===

# make dirs

path_to_scp = Path(__file__).parent / "deepwell" / "scps" / str(SCP)

os.makedirs(path_to_scp, exist_ok=True)

os.makedirs(path_to_scp / "SCPs", exist_ok=True)
os.makedirs(path_to_scp / "descs", exist_ok=True)
os.makedirs(path_to_scp / "addenda", exist_ok=True)

# populate dirs

# special containment procedures
with open(path_to_scp / "SCPs" / "main.md", "w") as file:
    file.write(SCPs)

# description
with open(path_to_scp / "descs" / "main.md", "w") as file:
    file.write(desc)

# addenda
for i, addendum in enumerate(addenda):
    # sanize filename
    fname = quote(addenda_names[i], safe="")
    with open(path_to_scp / "addenda" / f"{fname}.md", "w") as file:
        file.write(addendum)

# display md in terminal
console = Console()

# print headings
console.print(Markdown(f"# **Item #:** SCP-{SCP:03d}"))
console.print(Markdown(f"## **Object Class:** {obj_class}"))

print() # separator

# print SCPs
console.print(Markdown(f"## **Special Containment Procedures:**\n{SCPs}"))

# print description
console.print(Markdown(f"## **Description:**\n{desc}"))

# print addenda
if addenda:
    for i, addendum in enumerate(addenda):
        console.print(Markdown(f"## **{addenda_names[i]}:**\n{addendum}"))
