#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to generate a PDF book with all cheat sheets from the "OWASP Cheat Sheet Series" project.

Python dependencies:
    pip install pdfkit requests termcolor colorama tqdm beautifulsoup4 PyPDF2

System dependency needed by "pdfkit":
    Linux   : sudo apt-get install wkhtmltopdf
    Windows : https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_msvc2015-win64.exe
    OSX     : https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_osx-cocoa-x86-64.pkg

"""

import requests
import hashlib
import pdfkit
import os
import colorama
import shutil
from tqdm import tqdm
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger
from termcolor import colored

# Define script constants
OWASP_WIKI_BASE_HOME = "https://www.owasp.org/"
CS_LIST_PAGE = "https://www.owasp.org/index.php/Category:Cheatsheets"
CS_TEMPLATE_URL = "https://www.owasp.org/index.php?title=%s&printable=no"
WORK_TEMP_FOLDER = "work"

# CS ignored PDF because the current format is not compatible :(
CS_SKIPPED_LIST = ["Access_Control_Cheat_Sheet", "AppSensor_Cheat_Sheet"]


def is_draft_cs(html):
    """
    Determine if a CS is in draft or not
    :param html: HTML content of the CS
    :return: True is the CS is in draft
    """
    return "DRAFT CHEAT SHEET" in html.upper()


def extract_cs_list():
    """
    Extract the list of CS from the CS list page. Take in account the choice in terms of skipping of some CS for which current format is not compatible.
    :return: The list of CS identifier
    """
    cs_list_identifiers = []
    response = requests.get(CS_LIST_PAGE)
    if response.status_code != 200:
        raise Exception("Cannot obtains the list of CS, HTTP '" + response.status_code + "' received when calling the url '" + CS_LIST_PAGE + "' !")
    for section in BeautifulSoup(response.content, "html.parser").find_all(attrs={"class": "mw-category-group"}):
        for ref_link in section.find_all("a"):
            cs_id = ref_link.get("href").replace("/index.php/", "").strip()
            if cs_id not in CS_SKIPPED_LIST:
                cs_list_identifiers.append(cs_id)
    return cs_list_identifiers


def convert_cs_to_pdf_file(cs_identifier, skip_cs_in_draft=True):
    """
    Create a PDF file in the WORK_TEMP_FOLDER for the specified CS identifier.
    :param cs_identifier: Identifier of the CS that must be used with CS_TEMPLATE_URL to obtains the CS HTML content
    :param skip_cs_in_draft: Flag to indicate if CS in draft must be skipped (default to TRUE), if enabled the function return NONE if the current CS is a draft
    :return: The name (with path) of the PDF file created or NONE if the CS is in draft mode and the flag "skip_cs_in_draft" is enabled
    """
    if cs_identifier is None or cs_identifier.strip() == "":
        raise Exception("CS identifier cannot be NONE or empty !")
    cs_url = CS_TEMPLATE_URL % cs_identifier
    # Get the CS HTML content and clean it by removing the content after the section "Other Cheatsheets"
    response = requests.get(cs_url)
    if response.status_code != 200:
        raise Exception("Cannot obtains the HTML content of the CS '" + cs_identifier + "', HTTP '" + response.status_code + "' received when calling the url '" + cs_url + "' !")
    cs_html = response.text
    if skip_cs_in_draft and is_draft_cs(cs_html):
        pdf_file = None
    else:
        cs_html = cs_html.replace("</head>", "<base href=\"" + OWASP_WIKI_BASE_HOME + "\" target=\"_blank\"></head>")
        content_to_remove_position = cs_html.rfind("Other Cheatsheets")
        cs_html = cs_html[0:content_to_remove_position]
        cs_html = cs_html.replace("<div id=\"siteSub\">From OWASP</div>", "")
        cs_html = cs_html.replace("<a href=\"#mw-head\">navigation</a>", "")
        cs_html = cs_html.replace("<a href=\"#p-search\">search</a>", "")
        cs_html = cs_html.replace("<a href=\"#mw-head\">navigation</a>,", "")
        cs_html = cs_html.replace("Jump to:					,", "")
        cs_html += "</span></h1></body></html>"
        # Generate the PDF from the cleaned HTML
        options = {}
        pdf_file = WORK_TEMP_FOLDER + "/" + hashlib.md5(cs_identifier.encode("utf-8")).hexdigest() + ".pdf"
        # Use "force" mode because there an issue with rendering from HTML string: Link cannot be resolved event if network access is OK
        try:
            pdfkit.from_string(input=cs_html, output_path=pdf_file, options=options)
        except:
            pass
    return pdf_file


def merge_all_cs_pdf_files(cs_pdf_files_paths, merged_pdf_file_name="book.pdf"):
    """
    Merge all CS pdf files in order to create the CS pdf book
    :param cs_pdf_files_paths: List of PDF file to merge
    :param merged_pdf_file_name: Name of the output file representing the result of the merge
    """
    if cs_pdf_files_paths is None:
        raise Exception("List of PDF files to merge cannot be NONE !")
    merger = PdfFileMerger()
    for cs_pdf_files_path in cs_pdf_files_paths:
        merger.append(cs_pdf_files_path, import_bookmarks=False)
    merger.write(merged_pdf_file_name)


if __name__ == "__main__":
    colorama.init()
    print(colored("[*] Initialization...", "cyan", attrs=[]))
    if os.path.exists(WORK_TEMP_FOLDER):
        shutil.rmtree(WORK_TEMP_FOLDER)
    os.mkdir(WORK_TEMP_FOLDER)
    print(colored("[*] Extract the list of all CS...", "cyan", attrs=[]))
    cs_list = extract_cs_list()
    print("%s found." % len(cs_list))
    print(colored("[*] Convert each CS to a PDF file...", "cyan", attrs=[]))
    pdf_files = []
    for i in tqdm(range(0, len(cs_list))):
        pdf_file = convert_cs_to_pdf_file(cs_list[i])
        if pdf_file is not None:
            pdf_files.append(pdf_file)
    print(colored("[*] Merge all PDF files to a single one...", "cyan", attrs=[]))
    if len(pdf_files) > 0:
        book_name = "owasp-cs-book.pdf"
        merge_all_cs_pdf_files(pdf_files, merged_pdf_file_name=book_name)
        print(colored("[*] CS books generated in file '%s'" % book_name, "green", attrs=["bold"]))
    else:
        print(colored("[!] There no CS pdf file to merge !", "red", attrs=["bold"]))

