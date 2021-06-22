import scrapy

class UniPaperSpider(scrapy.Spider):
    name = "UniPaperCrawler"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../papers.csv'
    }
    #urls for my institution Khulna University of Engineering and Technology, Khulna, Bnagladesh
    #Please change the org code of the url for your targeted institute
    start_urls = ['https://scholar.google.com/citations?view_op=view_org&hl=en&org=6404276033455020430']

    def parse(self, response):
        #gets every person linked to the specified university
        for person in response.css("h3.gs_ai_name > a::attr('href')"):
            #goes to the profile of the linked person to scrape papers
            yield scrapy.Request(url="https://scholar.google.com"+person.get(), callback=self.parsePages)
        #next page url
        next_page = response.css("button.gsc_pgn_pnx::attr(onclick)").get()
        #response.xpath("//button[@class='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx']/@onclick").re('href(.*)')[0]
        # iterate through next pages if found
        if next_page is not None:
            # add `domain` and remove `window.location='` and `'` at the end
            url = "https://scholar.google.com" + next_page[17:-1]
            # converting some codes to chars
            url = url.encode('utf-8').decode('unicode_escape')
            yield response.follow(url,self.parse)

    def parsePages(self, response):
        #all paper linkes found from the specified person
        for paper in response.css("a.gsc_a_at::attr('data-href')"):
            yield scrapy.Request(url="https://scholar.google.com"+paper.get(), callback=self.parsePapers)

    def parsePapers(self, response):
        #scrape through all papers
        description = ""
        paperlink = response.css("a.gsc_vcd_title_link::attr(href)").get()
        papertitle = response.css("a.gsc_vcd_title_link::text").get()
        authors = response.css("div.gsc_vcd_value::text")[0].get()
        publication_date = response.css("div.gsc_vcd_value::text")[1].get()
        des = response.css("div.gsh_csp::text").get()
        for index, dess in enumerate(des):
            description = description + dess
        description_summary = response.css("div.gsh_csp::text")[0].get()
        citation = response.xpath('.//a[starts-with(text(),"Cited")]/text()').extract_first()
        #saving all information about the scraped paper
        all_paper_info = {
            # key:value
            'link': paperlink,
            'title': papertitle,
            'authors': authors,
            'date': publication_date,
            'description': description,
            'summary': description_summary,
            'citation': citation,
        }
        # yield or give the scraped info to Scrapy
        yield all_paper_info