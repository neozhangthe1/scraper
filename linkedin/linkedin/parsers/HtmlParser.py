# -*- coding: utf-8 -*-

__author__ = 'yutao'

from ..items import PersonProfileItem
# from bs4 import UnicodeDammit
from w3lib.url import url_query_cleaner
import random
from . import LinkedinParser
import urlparse

def remove_url_parameter(url):
    return url_query_cleaner(url)

class HtmlParser:
    @staticmethod
    def extract_person_profile(response):
        personProfile = PersonProfileItem()
        # person name done
        nameSpan = response.xpath("//h1[@class='fn']/text()").extract()
        if nameSpan and len(nameSpan) == 1:
            personProfile['name'] = nameSpan[0].strip()
        else:
            return None

        # done
        photo = response.xpath("//div[@class='profile-picture']/a/img/@data-delayed-url").extract()
        if len(photo) > 0:
            personProfile['photo'] = photo[0]

        # done
        headline = response.xpath("//p[@class='headline title']/text()").extract()
        if headline and len(headline) == 1:
            personProfile['title'] = headline[0].strip()

        # done
        demographic = response.xpath("//dl[@id='demographics']")
        if demographic and len(demographic) == 1:
            # locality
            locality = demographic.xpath("dd/span[@class='locality']/text()").extract()
            if locality and len(locality) == 1:
                personProfile['locality'] = locality[0].strip()
            # industry
            industry = demographic.xpath("dd[@class='descriptor']/text()").extract()
            if industry and len(industry) == 1:
                personProfile['industry'] = industry[0].strip()
            else:
                industry = demographic.xpath("dd[@class='descriptor industry']/text()").extract()
                if industry and len(industry) == 1:
                    personProfile['industry'] = industry[0].strip()
        # ## overview
        # overview = response.xpath("//dl[@id='overview']").extract()
        # if overview and len(overview) == 1:
        #     personProfile['overview_html'] = overview[0]
        #     homepage = LinkedinParser.parse_homepage(overview[0])
        #     if homepage:
        #         personProfile['homepage'] = homepage

        # summary
        summary = response.xpath("//section[@id='summary']/div[@class='description']/p/text()").extract()
        if summary and len(summary) > 0:
            personProfile['summary'] = '\n'.join(x.strip() for x in summary)

        # certifications done
        certifications = []
        cert_elem = response.xpath("//section[@id='certifications']/ul/li")
        for c in cert_elem:
            ce = {}
            title = c.xpath("header/h4/text()").extract()
            if len(title) > 0:
                ce["title"] = title[0]
            else:
                title = c.xpath("a/div/div/span[@class='item-title']/text()").extract()
                if len(title) > 0:
                    ce["title"] = title[0]
                    url = c.xpath("a/@href").extract()
                    if len(url) > 0:
                        ce["url"] = url_query_cleaner(url[0])
                else:
                    title = c.xpath("header/h4/a/text()").extract()
                    if len(title) > 0:
                        ce["title"] = title[0]
                    url = c.xpath("header/h4/a/@href").extract()
                    if len(url) > 0:
                        ce["url"] = url_query_cleaner(url[0])

            sub = c.xpath("a/div/div/span[@class='item-subtitle']/text()").extract()
            if len(sub) > 0:
                ce["sub"] = sub[0]
            else:
                sub = c.xpath("header/h5/a/text()").extract()
                if len(sub) > 0:
                    ce["sub"] = sub[0]
                else:
                    sub = c.xpath("header/h5/text()").extract()
                    if len(sub) > 0:
                        ce["sub"] = sub[0]

            time = c.xpath("a/div/div/span[@class='date-range']/time/text()").extract()
            if len(time) > 0:
                ce['start'] = time[0].strip()
                if len(time) == 2:
                    ce['end'] = time[1].replace(u"\u2013", "").strip()
            else:
                time = c.xpath("header/div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    ce['start'] = time[0].strip()
                    if len(time) == 2:
                        ce['end'] = time[1].replace(u"\u2013", "").strip()
            certifications.append(ce)
        personProfile["certifications"] = certifications

        # # specilities
        # specilities = response.xpath("//div[@id='profile-specialties']/p/text()").extract()
        # if specilities and len(specilities) == 1:
        #     specilities = specilities[0].strip()
        #     personProfile['specilities'] = specilities

        # skills done
        skills = response.xpath("//section[@id='skills']/ul/li/a/span/text()").extract()
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

        # education done
        education = response.xpath("//section[@id='education']/ul/li")
        schools = []
        for e in education:
            s = {}
            if len(e.xpath("header")) > 0:
                name = e.xpath("header/h4/a/text()").extract()
                if name and len(name) == 1:
                    s['name'] = name[0].strip()
                else:
                    name = e.xpath("header/h4/text()").extract()
                    if name and len(name) == 1:
                        s['name'] = name[0].strip()

                url = e.xpath("header/h4/a/@href").extract()
                if url and len(url) == 1:
                    s['url'] = url_query_cleaner(urlparse.urljoin(response.url, url[0]))
                sub = e.xpath("header/h5[@class='item-subtitle']/text()").extract()
                if sub and len(sub) == 1:
                    s['sub'] = sub[0].strip().strip(",")
                    sub = s["sub"].split(",")
                    if len(sub) > 0:
                        s['degree'] = sub[0].strip()
                    if len(sub) > 1:
                        s['major'] = sub[1].strip()
                # major = e.select("div/header/h5/span[@class='major']/a/text()").extract()
                # if major and len(major) == 1:
                #     s['major'] = major[0].strip()
                # if degree and len(degree) == 1:
                #     s['degree'] = degree[0].strip().strip(",")
                logo = e.xpath("h5[@class='logo']/a/img/@data-delayed-url").extract()
                if len(logo) > 0:
                    s['logo'] = logo[0].strip()
                time = e.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    s['start'] = time[0].strip()
                    if len(time) == 2:
                        s['end'] = time[1].replace(u"\u2013", "").strip()
                schools.append(s)
            else:
                name = e.xpath("div/div/span[@class='item-title']/a/text()").extract()
                if name and len(name) == 1:
                    s['name'] = name[0].strip()
                else:
                    name = e.xpath("div/div/span[@class='item-title']/text()").extract()
                    if name and len(name) == 1:
                        s['name'] = name[0].strip()

                url = e.xpath("div/div/span[@class='item-title']/a/@href").extract()
                if url and len(url) == 1:
                    s['url'] = url_query_cleaner(urlparse.urljoin(response.url, url[0]))
                sub = e.xpath("div/div/span[@class='item-subtitle']/text()").extract()
                if sub and len(sub) == 1:
                    s['sub'] = sub[0].strip().strip(",")
                    sub = s["sub"].split(",")
                    if len(sub) > 0:
                        s['degree'] = sub[0].strip()
                    if len(sub) > 1:
                        s['major'] = sub[1].strip()
                # major = e.select("div/header/h5/span[@class='major']/a/text()").extract()
                # if major and len(major) == 1:
                #     s['major'] = major[0].strip()
                # if degree and len(degree) == 1:
                #     s['degree'] = degree[0].strip().strip(",")
                logo = e.xpath("div/span[@class='logo']/img/@data-delayed-url").extract()
                if len(logo) > 0:
                    s['logo'] = logo[0].strip()
                time = e.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    s['start'] = time[0].strip()
                    if len(time) == 2:
                        s['end'] = time[1].replace(u"\u2013", "").strip()
                schools.append(s)
        personProfile['education'] = schools

        # experience done
        experience = response.xpath("//section[@id='experience']/ul/li")
        es = []
        for e in experience:
            je = {}
            if len(e.xpath("header")) > 0:
                title = e.xpath("header/h4/text()").extract()
                if len(title) > 0:
                    je['title'] = title[0].strip()
                else:
                    title = e.xpath("header/h4/a/text()").extract()
                    if len(title) > 0:
                        je['title'] = title[0].strip()
                logo = e.xpath("header/h5[@class='logo']/a/img/@data-delayed-url").extract()
                if len(logo) > 0:
                    je['logo'] = logo[0].strip()
                org = e.xpath("header/h5[@class='item-subtitle']/a/text()").extract()
                if len(org) > 0:
                    je['org'] = org[0].strip()
                else:
                    org = e.xpath("header/h5/text()").extract()
                    if org and len(org) == 1:
                        je['org'] = org[0].strip()
                url = e.xpath("header/h5[@class='item-subtitle']/a/@href").extract()
                if url and len(url) == 1:
                    je['url'] = url_query_cleaner(urlparse.urljoin(response.url, url[0]))
                time = e.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    je['start'] = time[0].strip()
                    if len(time) == 2:
                        je['end'] = time[1].replace(u"\u2013", "").strip()
                # duration = e.select("div/span[@class='experience-date-locale']/text()").extract()
                # if len(duration) > 0:
                #     je['duration'] = duration[0].strip().split("(")[1].strip(")")
                location = e.xpath("div/span[@class='location']/text()").extract()
                if len(location) > 0:
                    je['location'] = location[0].strip()
                desc = e.xpath("p[@class='description']/text()").extract()
                if len(desc) > 0:
                    je['desc'] = "".join(x.strip() for x in desc)
                es.append(je)
            else:
                title = e.xpath("a/div/div/span[@class='item-title']/text()").extract()
                if title and len(title) == 1:
                    je['title'] = title[0].strip()
                else:
                    title = e.xpath("div/div/span[@class='item-title']/text()").extract()
                    if title and len(title) == 1:
                        je['title'] = title[0].strip()

                url = e.xpath("a/@href").extract()
                if url and len(url) == 1:
                    je['url'] = url_query_cleaner(urlparse.urljoin(response.url, url[0]))
                sub = e.xpath("a/div/div/span[@class='item-subtitle']/text()").extract()
                if sub and len(sub) == 1:
                    je['org'] = sub[0].strip().strip(",").strip()
                logo = e.xpath("div/span[@class='logo']/img/@data-delayed-url").extract()
                if len(logo) > 0:
                    je['logo'] = logo[0].strip()
                time = e.xpath("a/div/div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    je['start'] = time[0].strip()
                    if len(time) == 2:
                        je['end'] = time[1].replace(u"\u2013", "").strip()
                es.append(je)
        personProfile['experience'] = es

        honors = []
        honer_elem = response.xpath("//section[@id='awards']/ul/li")
        for h in honer_elem:
            ho = {}
            if len(h.xpath("header")) > 0:
                title = h.xpath("header/h4/text()").extract()
                sub = h.xpath("header/h5/text()").extract()
                des = h.xpath("p/text()").extract()
                time = h.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(title) > 0:
                    ho["title"] = title[0].strip()
                if len(sub) > 0:
                    ho["sub"] = sub[0].strip()
                if len(des) > 0:
                    ho["des"] = des[0].strip()
                if len(time) > 0:
                    ho['start'] = time[0].strip()
                    if len(time) == 2:
                        ho['end'] = time[1].replace(u"\u2013", "").strip()
            else:
                title = h.xpath("div/h4/text()").extract()
                sub = h.xpath("div/h5/text()").extract()
                des = h.xpath("p/text()").extract()
                time = h.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    ho['start'] = time[0].strip()
                    if len(time) == 2:
                        ho['end'] = time[1].replace(u"\u2013", "").strip()
                if len(title) > 0:
                    ho["title"] = title[0].strip()
                if len(sub) > 0:
                    ho["sub"] = sub[0].strip()
                if len(des) > 0:
                    ho["des"] = des[0].strip()
            honors.append(ho)
        personProfile["honors"] = honors

        pubs = response.xpath("//section[@id='publications']/ul/li")
        pub_items = []
        for pub in pubs:
            p = {}
            title = pub.xpath("header/h4[@class='item-title']/a/text()").extract()
            if len(title) > 0:
                p["title"] = title[0]
            else:
                title = pub.xpath("header/h4[@class='item-title']/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0]
            url = pub.xpath("header/h4[@class='item-title']/a/@href").extract()
            if len(url) > 0:
                p["url"] = url[0]
            venue = pub.xpath("header/h5/text()").extract()
            if len(venue) > 0:
                p["venue"] = venue[0]
            year = pub.xpath("header/div/span[@class='date-range']/time/text()").extract()
            if len(year) > 0:
                p["year"] = year[0]
            abstract = pub.xpath("p[@class='description']/text()").extract()
            if len(abstract) > 0:
                p["abstract"] = " ".join(abstract)

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
                            a["url"] = url_query_cleaner(url[0])
                            a["id"] = HtmlParser.get_linkedin_id(a["url"])
                    else:
                        name = au.xpath("text()").extract()
                        if len(name) > 0:
                            a["name"] = name[0].strip().strip(u"、").strip(",")
                    if 'name' in a and len(a["name"]) > 0:
                        authors.append(a)
                p["authors"] = authors
            pub_items.append(p)
        personProfile["pubs"] = pub_items

        # language done
        languages = []
        languages_elem = response.xpath("//section[@id='languages']/ul/li/div")
        for l in languages_elem:
            la = {}
            name = l.xpath("h4/text()").extract()
            if len(name) > 0:
                la["name"] = name[0]
            proficiency = l.xpath("p/text()").extract()
            if len(proficiency) > 0:
                la["proficiency"] = proficiency[0]
            languages.append(la)
        personProfile["languages"] = languages

        # also view done
        also_view = []
        also_view_elem = response.xpath("//div[@class='browse-map']/ul/li")
        for item in also_view_elem:
            p = {}
            if len(item.xpath("div/h4/a/text()").extract()) > 0:
                photo = item.xpath("a/img/@data-delayed-url").extract()
                if len(photo) > 0:
                    p["photo"] = photo[0]
                name = item.xpath("div/h4/a/text()").extract()
                if len(name) > 0:
                    p["name"] = name[0].strip()
                title = item.xpath("div/p[@class='headline']/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0].strip()
                url = item.xpath("div/h4/a/@href").extract()
                if len(url) > 0:
                    p["url"] = url_query_cleaner(url[0])
                    # p["id"] = HtmlParser.get_linkedin_id(p["url"])
            else:
                photo = item.xpath("div/a/span/img/@data-delayed-url").extract()
                if len(photo) > 0:
                    p["photo"] = photo[0]
                name = item.xpath("div/a/div/span/text()").extract()
                if len(name) > 0:
                    p["name"] = name[0].strip()
                title = item.xpath("div/a/div/p/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0].strip()
                url = item.xpath("div/a/@href").extract()
                if len(url) > 0:
                    p["url"] = url_query_cleaner(url[0])
            also_view.append(p)
            if p == {}:
                print(item.extract())
        personProfile['also_view'] = also_view


        # project
        projects = []
        projects_elem = response.xpath("//section[@id='projects']/ul/li")
        for pub in projects_elem:
            p = {}
            if len(pub.xpath("header")):
                title = pub.xpath("header/h4[@class='item-title']/a/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0]
                else:
                    title = pub.xpath("header/h4[@class='item-title']/text()").extract()
                    if len(title) > 0:
                        p["title"] = title[0]
                url = pub.xpath("header/h4[@class='item-title']/a/@href").extract()
                if len(url) > 0:
                    p["url"] = url[0]
                time = pub.xpath("div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    ho['start'] = time[0].strip()
                    if len(time) == 2:
                        ho['end'] = time[1].replace(u"\u2013", "").strip()
                des = pub.xpath("p[@class='description']/text()").extract()
                if len(des) > 0:
                    p["des"] = " ".join(des)
                contributors_elem = pub.xpath("dl/dd/ul/li")
                contributors = []
                for au in contributors_elem:
                    a = {}
                    aa = au.xpath("a")
                    if len(aa) > 0:
                        name = aa.xpath("text()").extract()
                        if len(name) > 0:
                            a["name"] = name[0]
                        url = aa.xpath("@href").extract()
                        if len(url) > 0:
                            a["url"] = url_query_cleaner(url[0])
                            a["id"] = HtmlParser.get_linkedin_id(a["url"])
                    else:
                        name = au.xpath("text()").extract()
                        if len(name) > 0:
                            a["name"] = name[0].strip().strip(u"、").strip(",")
                    if 'name' in a and len(a["name"]) > 0:
                        contributors.append(a)
                    p["contributors"] = contributors
            else:
                title = pub.xpath("header/h4[@class='item-title']/a/text()").extract()
                if len(title) > 0:
                    p["title"] = title[0]
                else:
                    title = pub.xpath("header/h4[@class='item-title']/text()").extract()
                    if len(title) > 0:
                        p["title"] = title[0]
                url = pub.xpath("header/h4[@class='item-title']/a/@href").extract()
                if len(url) > 0:
                    p["url"] = url[0]
                venue = pub.xpath("header/h5/text()").extract()
                if len(venue) > 0:
                    p["venue"] = venue[0]
                year = pub.xpath("span[@class='publication-date']/text()").extract()
                if len(year) > 0:
                    p["year"] = year[0]
                abstract = pub.xpath("p[@class='description']/text()").extract()
                if len(abstract) > 0:
                    p["abstract"] = " ".join(abstract)
                time = pub.xpath("header/div/span[@class='date-range']/time/text()").extract()
                if len(time) > 0:
                    ho['start'] = time[0].strip()
                    if len(time) == 2:
                        ho['end'] = time[1].replace(u"\u2013", "").strip()
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
                                a["url"] = url_query_cleaner(url[0])
                                a["id"] = HtmlParser.get_linkedin_id(a["url"])
                        else:
                            name = au.xpath("text()").extract()
                            if len(name) > 0:
                                a["name"] = name[0].strip().strip(u"、").strip(",")
                        if 'name' in a and len(a["name"]) > 0:
                            authors.append(a)
                    p["authors"] = authors
            projects.append(p)
        personProfile["projects"] = projects

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