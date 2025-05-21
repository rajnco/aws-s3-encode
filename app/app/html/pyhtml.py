from jinja2 import Environment, FileSystemLoader
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.append("./app/app/pycsv")
from pycsv import PYCSV 


def generate_pdf(url: str, output_file: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.pdf(
            path=output_file,
            format="A4",
            print_background=True,  # Ensures background colors and images are included
            margin={"top": "20px", "right": "20px", "bottom": "20px", "left": "20px"}
        )
        browser.close()


def main():
    """ """
    env = Environment(loader = FileSystemLoader("./app/template"))
    template = env.get_template("toplist.jinja")

    current_directory = os.getcwd()
    csv_infile = "app/in/pg_catalog_100.csv"
    csv_file_path = os.path.join(current_directory, csv_infile)
    pycsv = PYCSV(csv_file_path)
    #books = pycsv.data

    #output = template.render(book_count=len(pycsv.data), books=pycsv.data)
    #print(output)

    html_out_file = os.path.join(current_directory, "app/render", os.path.basename(csv_infile).replace("csv", "html"))
    with open(html_out_file, "w") as f:
        print(template.render(book_count=len(pycsv.data), books=pycsv.data), file=f)

    pdf_out_file = html_out_file.replace("html", "pdf")
    generate_pdf("file://"+html_out_file, pdf_out_file)    



if __name__ == "__main__":
    main()