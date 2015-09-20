#encoding: utf-8
import re
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from items import MovieItem

TV_RUNTIME_RE = re.compile(ur'单集片长: (\d+)')
LANGUAGES_RE = re.compile(ur"语言:</span> (.+?)<br>")
COUNTRIES_RE = re.compile(ur"制片国家/地区:</span> (.+?)<br>")
NUM_RE = re.compile(r"(\d+)")


class MovieSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]

    # rules = (
    #     Rule(LinkExtractor(allow=r"/subject/\d+/($|\?\w+)"),
    #         callback="parse"),
    # )

    # def __init__(self):
    start_urls = ["http://movie.douban.com/subject/4904662/"]

    def parse(self, response):
        cur_url = response.url.split("?")[0]
        urls = []
        for u in response.xpath("//a/@href").extract():
            u = u.split("?")[0]
            if "movie.douban.com/subject/" in u:
                if u.split("/")[-3] == "subject" and u.split("/")[-1] == "":
                    urls.append(u)
        for u in set(urls):
            print("Add:" + u)
            yield Request(u, callback=self.parse)
        if not cur_url.split("/")[-3] == "subject":
            return
        print("Item:" + cur_url)
        item = MovieItem()
        item["subject_id"] = response.url.split("/")[-2]
        urls = self.get_seasons(response, item)
        for u in urls:
            yield Request(u, callback=self.parse)

        self.get_poster(response, item)
        self.get_website(response, item)
        self.get_name(response, item)
        self.get_year(response, item)
        self.get_directors(response, item)
        self.get_actors(response, item)
        self.get_genres(response, item)
        self.get_runtime(response, item)
        self.get_languages(response, item)
        self.get_countries(response, item)
        self.get_average(response, item)
        self.get_vote(response, item)
        self.get_tags(response, item)
        self.get_watched(response, item)
        self.get_wish(response, item)
        self.get_summary(response, item)
        self.get_stars(response, item)
        self.get_comment(response, item)
        self.get_question(response, item)
        self.get_review(response, item)
        self.get_discussion(response, item)
        self.get_image(response, item)
        self.get_type(response, item)
        yield item

    def get_seasons(self, response, item):
        items = response.xpath("//select[@id='season']/option")
        season = 0
        seasons = []
        urls = []
        for p in items:
            seasons.append({
                "sid": p.xpath("@value").extract()[0],
                "s": int(p.xpath("text()").extract()[0])
            })
            if len(p.xpath("@selected").extract()) > 0:
                season = int(p.xpath("text()").extract()[0])
            urls.append("http://movie.douban.com/subject/%s/" % p.xpath("@value").extract()[0])
        item["season"] = season
        item["seasons"] = seasons
        return urls




    def get_poster(self, response, item):
        url = response.xpath("//a[@class='nbgnbg']/img/@src").extract()
        if len(url):
            item["poster"] = url[0].strip()

    def get_stars(self, response, item):
        if not item.get("vote", None): return

        xpath = response.xpath("//div[@class='rating_wrap clearbox']/text()").extract()
        stars = "".join( map(unicode.strip, xpath ) ).split("%")[:-1]
        stars = [ int( round((float( "%.3f" % (float(star)/100))) * item["vote"]) )  for star in stars ]
        item["stars"] = stars

    def get_name(self, response, item):
        name = response.xpath("//title/text()").extract()
        if name: item["name"] = name[0].replace(u" (豆瓣)", "").strip()

    def get_website(self, response, item):
        url = response.xpath("//div[@id='info']/a[@target='_blank']/text()").extract()
        if len(url) > 0:
            item['website'] = url

    def get_type(self, response, item):
        tmp = response.xpath("//div[@id='related-pic']/h2/i/text()")
        if "电视" in tmp:
            item['type'] = "tv"
        elif "电影" in tmp:
            item['type'] = "movie"


    def get_year(self, response, item):
        year = response.xpath("//span[@class='year']").re(NUM_RE)
        if year: item["year"] = int( year[0] )

    def get_directors(self, response, item):
        directors = response.xpath("//a[@rel='v:directedBy']/text()").extract()
        url = response.xpath("//a[@rel='v:directedBy']/@href").extract()
        if directors:
            item["directors"] = [{
                "name": directors[i],
                "id": url[i].split("/")[-2]
            } for i in range(len(directors))]

    def get_actors(self, response, item):
        stars = response.xpath("//a[@rel='v:starring']/text()").extract()
        url = response.xpath("//a[@rel='v:starring']/@href").extract()
        if stars:
            item["actors"] = [{
                "name": stars[i],
                "id": url[i].split("/")[-2]
            } for i in range(len(stars))]


    def get_genres(self, response, item):
        genres = response.xpath("//span[@property='v:genre']/text()").extract()
        if genres: item["genres"] = genres

    def get_runtime(self, response, item):
        if not self.parse_tv(response, item):
            runtime = response.xpath("//span[@property='v:runtime']/text()").re(NUM_RE)
            if runtime:
                item["channel"] = "mv"
                item["runtime"] =  int( runtime[0] )

    def get_average(self, response, item):
        average = response.xpath("//strong[@property='v:average']/text()").extract()
        if average and average[0] != "": item["average"] = float( average[0] ) + 0.0

    def get_vote(self, response, item):
         votes = response.xpath("//span[@property='v:votes']/text()").extract()
         if votes and votes[0] != "": item["vote"] = int( votes[0] )

    def get_tags(self, response, item):
        T = []
        tags = response.xpath("//div[@class='tags-body']/a")
        for tag in tags:
            t = tag.xpath("text()").extract()
            if t: T.append(t[0])
        if T: item["tags"] = T

    def get_watched(self, response, item):
        spec = "//div[@class='subject-others-interests-ft']/a[re:test(@href, 'collections$')]/text()"
        collections = response.xpath(spec).re(NUM_RE)
        if collections: item["watched"] = int( collections[0] )

    def get_wish(self, response, item):
        spec = "//div[@class='subject-others-interests-ft']/a[re:test(@href, 'wishes$')]/text()"
        wishes = response.xpath(spec).re(NUM_RE)
        if wishes: item["wish"] = int( wishes[0] )

    def get_languages(self, response, item):
        S = "".join(response.xpath("//div[@id='info']").extract() )
        M = LANGUAGES_RE.search(S)
        if M is not None:
            item["languages"] = [ lang.strip() for lang in M.group(1).split("/") ]

    def get_countries(self, response, item):
        S = "".join(response.xpath("//div[@id='info']").extract() )
        M = COUNTRIES_RE.search(S)
        if M is not None:
            item["countries"] = [ country.strip() for country in M.group(1).split("/") ]

    def get_summary(self, response, item):
        summary = response.xpath("//span[@property='v:summary']/text()").extract()
        if summary: item["summary"] = "<br/>".join( summary )

    def get_image(self, response, item):
        image = response.xpath("//a[re:test(@href, 'all_photos$')]/text()").re(NUM_RE)
        if image: item["image"] = int( image[0] )

    def get_comment(self, response, item):
        comment = response.xpath("//a[re:test(@href, '/comments$')]/text()").re(NUM_RE)
        if comment: item["comment"] = int( comment[0] )

    def get_question(self, response, item):
        question = response.xpath("//a[re:test(@href, '/questions/\?from=subject$')]/text()").re(NUM_RE)
        if question: item["question"] = int( question[0] )

    def get_review(self, response, item):
        review = response.xpath("//a[re:test(@href, '/reviews$')]/text()").re(NUM_RE)
        if review: item["review"] = int( review[0] )

    def get_discussion(self, response, item):
         discussion =  response.xpath("//a[re:test(@href, 'discussion/')]/text()").re(NUM_RE)
         if discussion: item["discussion"] = int( discussion[0] )

    def parse_tv(self, response, item):
        S = "".join( response.xpath("//div[@id='info']//text()").extract() )
        M = TV_RUNTIME_RE.search(S)
        if M is not None:
            item["channel"] = "tv"
            item["runtime"] = int(M.group(1))
            return True
        return False


class MovieReviewSpider(CrawlSpider):
    name = "movie_review"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["http://movie.douban.com"]

    rules = (
        Rule(LinkExtractor(allow=r"/subject/\d+/($|\?\w+)"), 
            callback="parse_review", follow=True),
    )

    def parse_review(self, response):
        pass