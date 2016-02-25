# -*- coding: utf-8 -*-

__author__ = 'yutao'

from ..items import PersonProfileItem
# from bs4 import UnicodeDammit
from w3lib.url import url_query_cleaner
import random
from . import LinkedinParser
import urlparse


class HtmlParser:
    @staticmethod
    def extract_person_profile(response):
        personProfile = PersonProfileItem()
        ## Person name
        nameSpan = response.xpath("//h1[@class='fn']/text()")
        if nameSpan and len(nameSpan) == 1:
            personProfile['name'] = nameSpan.extract()[0].strip()
        else:
            return None

        photo = response.xpath("//div[@class='profile-picture']/a/img/@src").extract()
        if len(photo) > 0:
            personProfile['photo'] = photo[0]

        headline = response.xpath("//div[@id='headline']")
        if headline and len(headline) == 1:
            title = headline.xpath("//p[@class='title']/text()").extract()
            if title and len(title) == 1:
                personProfile['title'] = title[0].strip()

        demographic = response.xpath("//div[@id='demographics']")
        if demographic and len(demographic) == 1:
            ## locality
            locality = demographic.xpath("div/div/dl/dd/span[@class='locality']/text()").extract()
            if locality and len(locality) == 1:
                personProfile['locality'] = locality[0].strip()
            ## industry
            industry = demographic.xpath("div/div/dl/dd[@class='industry']/text()").extract()
            if industry and len(industry) == 1:
                personProfile['industry'] = industry[0].strip()

        # ## overview
        # overview = response.xpath("//dl[@id='overview']").extract()
        # if overview and len(overview) == 1:
        #     personProfile['overview_html'] = overview[0]
        #     homepage = LinkedinParser.parse_homepage(overview[0])
        #     if homepage:
        #         personProfile['homepage'] = homepage

        ## summary
        summary = response.xpath("//div[@id='summary-item-view']/div[@class='summary']/p/text()").extract()
        if summary and len(summary) > 0:
            personProfile['summary'] = '\n'.join(x.strip() for x in summary)

        ## specilities
        specilities = response.xpath("//div[@id='profile-specialties']/p/text()").extract()
        if specilities and len(specilities) == 1:
            specilities = specilities[0].strip()
            personProfile['specilities'] = specilities

        ## skills
        skills = response.xpath("//div[@id='profile-skills']/ul/li/span/span/span/text()").extract()
        if skills and len(skills) > 0:
            personProfile['skills'] = [x.strip() for x in skills]
        #
        # additional = response.xpath("//div[@id='profile-additional']")
        # if additional and len(additional) == 1:
        #     additional = additional[0]
        #     ## interests
        #     interests = additional.select("div[@class='content']/dl/dd[@class='interests']/p/text()").extract()
        #     if interests and len(interests) == 1:
        #         personProfile['interests'] = interests[0].strip()
        #     ## groups
        #     g = additional.select("div[@class='content']/dl/dd[@class='pubgroups']")
        #     if g and len(g) == 1:
        #         groups = {}
        #         g = g[0]
        #         member = g.select("p/text()").extract()
        #         if member and len(member) > 0:
        #             groups['member'] = ''.join(member[0].strip())
        #         gs = g.select("ul[@class='groups']/li[contains(@class,'affiliation')]/div/a/strong/text()").extract()
        #         if gs and len(gs) > 0:
        #             groups['affilition'] = gs
        #         personProfile['group'] = groups
        #     ## honors
        #     honors = additional.select("div[@class='content']/dl/dd[@class='honors']/p/text()").extract()
        #     if honors and len(honors) > 0:
        #         personProfile['honors'] = [x.strip() for x in honors]

        ## education
        education = response.xpath("//div[@id='background-education']")
        schools = []
        if education and len(education) == 1:
            education = education[0]
            school_list = education.select("div[contains(@id,'education')]/div")
            if len(school_list) > 0:
                for e in school_list:
                    s = {}
                    name = e.xpath("div/header/h4/a/text()").extract()
                    if name and len(name) == 1:
                        s['name'] = name[0].strip()
                    else:
                        name = e.xpath("div/header/h4/text()").extract()
                        if name and len(name) == 1:
                            s['name'] = name[0].strip()
                    url = e.xpath("div/header/h4/a/@href").extract()
                    if url and len(url) == 1:
                        s['url'] = urlparse.urljoin(response.url, url[0])
                    degree = e.select("div/header/h5/span[@class='degree']/text()").extract()
                    if degree and len(degree) == 1:
                        s['degree'] = degree[0].strip().strip(",")
                    major = e.select("div/header/h5/span[@class='major']/a/text()").extract()
                    if major and len(major) == 1:
                        s['major'] = major[0].strip()
                    logo = e.xpath("div/a/h5[@class='education-logo']//img/@src").extract()
                    if len(logo) > 0:
                        s['logo'] = logo[0].strip()
                    time = e.select("div/span[@class='education-date']/time/text()").extract()
                    if len(time) > 0:
                        s['start'] = time[0].strip()
                        if len(time) == 2:
                            s['end'] = time[1].replace(u"\u2013", "").strip()
                    schools.append(s)
                personProfile['education'] = schools

        ## experience
        experience = response.xpath("//div[@id='background-experience']")
        if experience and len(experience) == 1:
            es = []
            experience = experience[0]
            exps = experience.xpath("div[contains(@id,'experience')]")
            if len(exps) > 0:
                for e in exps:
                    je = {}
                    title = e.xpath("div/header/h4/text()").extract()
                    if len(title) > 0:
                        je['title'] = title[0].strip()
                    else:
                        title = e.xpath("div/header/h4/a/text()").extract()
                        if len(title) > 0:
                            je['title'] = title[0].strip()
                    logo = e.xpath("div/header/h5[@class='experience-logo']/a/img/@src").extract()
                    if len(logo) > 0:
                        je['logo'] = logo[0].strip()
                    org = e.xpath("div/header/h5[not(@class)]/a/text()").extract()
                    if len(org) > 0:
                        je['org'] = org[0].strip()
                    else:
                        org = e.xpath("div/header/h5/span/text()").extract()
                        if org and len(org) == 1:
                            je['org'] = org[0].strip()
                    time = e.select("div/span[@class='experience-date-locale']/time/text()").extract()
                    if len(time) > 0:
                        je['start'] = time[0].strip()
                        if len(time) == 2:
                            je['end'] = time[1].replace(u"\u2013", "").strip()
                    # duration = e.select("div/span[@class='experience-date-locale']/text()").extract()
                    # if len(duration) > 0:
                    #     je['duration'] = duration[0].strip().split("(")[1].strip(")")
                    location = e.select("div/span[@class='experience-date-locale']/span[@class='locality']/text()").extract()
                    if len(location) > 0:
                        je['location'] = location[0].strip()
                    desc = e.xpath("div/p[@class='description']/text()").extract()
                    if len(desc) > 0:
                        je['desc'] = "".join(x.strip() for x in desc)
                    es.append(je)
            personProfile['experience'] = es

        honors = response.xpath("//div[@id='honors-additional-item-view']/div/p/text()").extract()
        if len(honors) > 0:
            personProfile["honoraward"] = {"additional": [h.strip() for h in honors]}

        pubs = response.xpath("//div[@id='background-publications']/div/div")
        pub_items = []
        if len(pubs) > 0:
            for pub in pubs:
                p = {}
                title = pub.xpath("hgroup/h4/a/span/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0]
                else:
                    title = pub.xpath("hgroup/h4/span/text()").extract()
                    if len(title) > 0:
                        p["title"] = title[0]
                url = pub.xpath("hgroup/h4/a/@href").extract()
                if len(url) > 0:
                    p["url"] = url[0]
                venue = pub.xpath("hgroup/h5/span/text()").extract()
                if len(venue) > 0:
                    p["venue"] = venue[0]
                year = pub.xpath("span[@class='publication-date']/text()").extract()
                if len(year) > 0:
                    p["year"] = year[0]
                abstract = pub.xpath("p[@class='description']/text()").extract()
                if len(abstract) > 0:
                    p["abstract"] = abstract[0]
                coauthors = pub.xpath("dl/dd/ul/li")
                if len(coauthors) > 0:
                    authors = []
                    for au in coauthors:
                        a = {}
                        aa = au.xpath("a")
                        if len(aa) > 0:
                            name = aa.xpath("text()").extract()
                            if len(name) > 0:
                                a["name"] = name[0]
                            url = aa.xpath("@href").extract()
                            if len(url) > 0:
                                a["url"] = url[0]
                                a["id"] = HtmlParser.get_linkedin_id(a["url"])
                        else:
                            name = au.xpath("text()").extract()
                            if len(name) > 0:
                                a["name"] = name[0].strip().strip(u"、").strip(",")
                        authors.append(a)
                    p["authors"] = authors
                pub_items.append(p)
            personProfile["pubs"] = pub_items


        ## Also view
        alsoViewProfileList = []
        divExtra = response.xpath("//div[@class='insights-browse-map']/ul/li")
        for item in divExtra:
            p = {}
            photo = item.xpath("a/img/@src").extract()
            if len(photo) > 0:
                p["photo"] = photo[0]
            name = item.xpath("h4/a/text()").extract()
            if len(name) > 0:
                p["name"] = name[0].strip()
            title = item.xpath("p[@class='browse-map-title']/text()").extract()
            if len(title) > 0:
                p["title"] = title[0].strip()
            url = item.xpath("h4/a/@href").extract()
            if len(url) > 0:
                p["url"] = HtmlParser.remove_url_parameter(url[0])
                p["id"] = HtmlParser.get_linkedin_id(p["url"])
            alsoViewProfileList.append(p)
        personProfile['also_view'] = alsoViewProfileList

        return personProfile

    @staticmethod
    def get_also_view_item(dirtyUrl):
        item = {}
        url = HtmlParser.remove_url_parameter(dirtyUrl)
        item['linkedin_id'] = HtmlParser.get_linkedin_id(url)
        item['url'] = url
        return item


    @staticmethod
    def remove_url_parameter(url):
        return url_query_cleaner(url)

    @staticmethod
    def get_linkedin_id(url):
        find_index = url.find("linkedin.com/")
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None