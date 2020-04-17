#!/bin/python3
from random import shuffle
from pathlib import Path

rowLength = 6
web_directory = "web"
sourceDir = "source"
percentage = 100 // rowLength


def StartHtml(write_path):
    with write_path.open(mode="w") as dest:
        dest.write('''<HTML>
<head>
    <meta charset="UTF-8">
    <title>Diamant</title>
</head>
<body bgcolor="2F51CC">''')


def StartTable(write_path, width=100):
    with write_path.open(mode="a") as dest:
        dest.write(f'<table border="0" align="center" width="{width}%">\n')


def EndHtml(write_path):
    with write_path.open(mode="a") as dest:
        dest.write('</body>\n</HTML>\n')


def EndTable(write_path):
    with write_path.open(mode="a") as dest:
        dest.write(f'</table>\n')


def InsertCell(write_path, image_name=None, link=None, columns_count=1):
    if columns_count:
        with write_path.open(mode="a") as dest:
            dest.write(f'<td width="{100 // columns_count}%">\n')
    if link:
        with write_path.open(mode="a") as dest:
            dest.write(f'<a href="{link}">\n')
    if image_name:
        with write_path.open(mode="a") as dest:
            dest.write(f'<img src="{image_name}" width="100%">\n')
    if link:
        with write_path.open(mode="a") as dest:
            dest.write('</a>\n')
    if columns_count:
        with write_path.open(mode="a") as dest:
            dest.write('</td>')


def InsertNavigationArrows(write_path, left_link, right_link):
    StartTable(write_path, width=80)
    if left_link:
        InsertCell(write_path, image_name="../source/home.png", link="./0.html", columns_count=5)
        InsertCell(write_path, image_name="../source/prev.png", link=left_link, columns_count=3)
    if right_link:
        InsertCell(write_path, image_name="../source/next.png", link=right_link, columns_count=3)
    EndTable(write_path)


here = Path('.')
if sourceDir not in [x.name for x in here.iterdir() if x.is_dir()]:
    raise FileNotFoundError("No source directory!")
if not (here/web_directory).exists():
    (here/web_directory).mkdir()
here /= sourceDir
if "cards" not in [x.name for x in here.iterdir() if x.is_dir()]:
    raise FileNotFoundError("No cards directory!")

listOfFiles = [fil for fil in (here/"cards").iterdir() if fil.is_file()]
listOfRelics = [fil for fil in listOfFiles if "relic" in fil.name]
listOfTraps = [fil for fil in listOfFiles if "trap" in fil.name]
listOfRegulars = [fil for fil in listOfFiles if "diamant" in fil.name]

shuffle(listOfFiles)

for pageNumber in range(len(listOfFiles)):
    write_path = here.parent / web_directory / (str(pageNumber) + ".html")
    StartHtml(write_path)
    StartTable(write_path)
    for i in range(rowLength):
        InsertCell(write_path, columns_count=rowLength)
    for cardNumber, filePath in enumerate(listOfFiles[:pageNumber + 1]):
        if cardNumber % rowLength == 0:
            with write_path.open(mode="a") as dest:
                dest.write('<tr>\n')
        InsertCell(write_path, image_name=f'../{filePath}', columns_count=rowLength)
        if cardNumber % rowLength == rowLength - 1:
            with write_path.open(mode="a") as dest:
                dest.write('\t</tr>\n')
    EndTable(write_path)
    InsertNavigationArrows(write_path, left_link=f"./{pageNumber - 1}.html" if pageNumber > 0 else None,
                           right_link=f"./{pageNumber + 1}.html" if pageNumber + 1 < len(listOfFiles) else None)
    EndHtml(write_path)
    print(f"here is {pageNumber}!")

import webbrowser
webbrowser.open(str(here.parent / web_directory / "0.html"))
