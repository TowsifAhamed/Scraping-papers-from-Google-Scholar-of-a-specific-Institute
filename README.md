# Scraping-papers-from-Google-Scholar-of-a-specific-Institute
A Scrapy project to scrape all data regarding publications enlisted in Google Scholar where at least one of the author is from a specific institute.

At first, you need to make a virtual environment for scrapy.
Inside the virtual env , using the command "scrapy crawl UniPaperCrawler" will start crawling Google Scholar.

The settings has been tweaked to crawl in a BFS manner.

In the start url,
start_urls = ['https://scholar.google.com/citations?view_op=view_org&hl=en&org=6404276033455020430']
Please use organization ID of your required institute from Google Scholar

The scraping is enabled through all the documents of the specific institute, where it is based on the relation of the authors to the specific institute.
If at least one of the authors are from the specific institute then it will be included to the results.

All the data are saved in the "papers.csv" file to do further process.
Please check, "https://github.com/TowsifAhamed/Creating-Inverted-Index-file-and-construct-a-Browser/" to see how to convert this data to an inverted indexed file for a faster query process.
