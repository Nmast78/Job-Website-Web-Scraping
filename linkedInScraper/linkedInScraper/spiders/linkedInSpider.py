from urllib.parse import urlencode
import scrapy
import re
from linkedInScraper.items import LinkedinscraperItem
from lxml import html

class LinkedinspiderSpider(scrapy.Spider):
    name = "linkedInSpider"

    # Method to build the url that will be used to get the data
    def getRequestUrl(self, keyword, location, pageNum):
        # Define parameters
        parameters = {'keywords': keyword, 'location': location, 'pageNum': pageNum}
        # Return the base url with parameters encoded
        return "https://www.linkedin.com/jobs/search?" + urlencode(parameters)
    
    # CODE STARTS HERE
    # This method calls the request method on a url and sets the callback so the response will go to the parse method
    def start_requests(self):
        # Define keyword and the list of all 50 states
        keyword = "Internship"
        locationList = ["Arkansas"]
        """
        locationList = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
                                      "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                                      "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
                                      "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
                                      "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        """
        # For each state get the url and call scrapy request
        for location in locationList:
            linkedInUrl = self.getRequestUrl(keyword, location, pageNum=0)
            yield scrapy.Request(linkedInUrl, callback=self.parse, meta={'keyword': keyword, 'location' : location})

    def parse(self, response):
        # Accessing the keyword and location from meta
        keyword = response.meta['keyword']
        location = response.meta['location']
        # Get key data from each partial job view
        jobID = response.xpath("//div[@class='base-card relative']/@data-reference-id").extract()
        jobTitle = response.xpath("//h3[@class='base-search-card_title']/text()").extract()
        jobCompany = response.xpath("//a[@class='hidden-nested-link']/text()").extract()
        jobLocation = response.xpath("//span[@class='job-search-card_location']/text()").extract()
        timeAgoPosted = response.xpath("//time[@class='job-search-card_listdate']/text()").extract()
        jobUrl = response.xpath("//a[@class='base-card_full-link']/@href()").extract()

        # Loop through arrays from parsing and build IndeedScraperItems
        for i in range(len(jobTitle)):
            jobItem = LinkedinscraperItem()

            jobItem['jobID'] = jobID[i].strip() if i < len(jobID) else None
            jobItem['title'] = jobTitle[i].strip() if i < len(jobTitle) else None
            jobItem['company'] = jobCompany[i].strip() if i < len(jobCompany) else None
            jobItem['location'] = jobLocation[i].strip() if i < len(jobLocation) else None
            jobItem['time'] = timeAgoPosted[i] if i < len(timeAgoPosted) else None
            jobItem['url'] = jobUrl[i].strip() if i < len(jobUrl) else None

            # List of fields to check
            fields_to_check = ['jobID', 'title', 'company', 'location', 'time', 'url']

            # Check for None fields and send email if any of them are
            for field in fields_to_check:
                if jobItem[field] is None:
                    # send_email(field)
                    pass

            yield jobItem
            # Use this and comment out above yield jobItem to parse each full job
            """
            yield scrapy.Request(url=jobItem["url"], callback=self.parseFullJob, meta={'data' : jobItem})
            """
        
        # Get link to next page if there is one. Call parse on that page
        """
        for i in range(1,20):
            next_page = self.getRequestUrl(keyword, location, i)
            yield scrapy.Request(next_page, callback=self.parse)
        """

    # Go into each job and get things like full job description and external link
    def parseFullJob(self, response):
        pass
 