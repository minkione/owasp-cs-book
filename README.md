[![Build Status](https://travis-ci.org/righettod/owasp-cs-book.svg?branch=master)](https://travis-ci.org/righettod/owasp-cs-book)

[![Requirements Status](https://requires.io/github/righettod/owasp-cs-book/requirements.svg?branch=master)](https://requires.io/github/righettod/owasp-cs-book/requirements/?branch=master)

[![Known Vulnerabilities](https://snyk.io/test/github/righettod/owasp-cs-book/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/righettod/owasp-cs-book?targetFile=requirements.txt)

# Objective

This project provide a utility script to build a PDF book gathering all Cheat Sheets from the project [OWASP Cheat Sheet Series](https://www.owasp.org/index.php/OWASP_Cheat_Sheet_Series).

# Limitation

After several requests to OWASP people using different channels (email, slack channels, mailing-list), it was not possible to known if the OWASP wiki has a feature (or plan to add it) to obtain a PDF version of a wiki article.
I have then decided (in last resort) to build the PDF version of a page from the HTML content of the page with all the caveats that it will bring.

Several iterations on this project will be needed in order to reach an optimal version of the generated book...

# Book publishing

A version of the book is generated every week by the TravisCI job and the PDF file is published in the [RELEASE](https://github.com/righettod/owasp-cs-book/releases) section of the project.

# Requirements

## Python

The script need **Python** version **>= 3.5.3**.

```
$ python --version
Python 3.5.3
```

## System dependency

Needed by **pdfkit** (library used to act on PDF content).

Install **wkhtmltopdf** (software used by **pdfkit** underneath to generate PDF content from HTML content):
* Linux : `sudo apt-get install wkhtmltopdf`
* Windows : [Download and install this bundle](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_msvc2015-win64.exe)
* OSX : [Download and install this bundle](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_osx-cocoa-x86-64.pkg)

### Important notice

**wkhtmltopdf** must be in **PATH** before to run the generation script!

You can use the following command to test if it's the case: 

```
$ wkhtmltopdf --version
wkhtmltopdf 0.12.4 (with patched qt)
```

# Python dependencies

Install dependencies packages using the following command:

```
pip install -r requirements.txt
```

# Generate the book

Run the following command:

```
$ python book-generator.py
[*] Initialization...
[*] Extract the list of all CS...
74 found.
[*] Convert each CS to a PDF file...
100%|#######################| 74/74
[*] Merge all PDF files to a single one...
[*] CS books generated in file 'owasp-cs-book.pdf'
```
