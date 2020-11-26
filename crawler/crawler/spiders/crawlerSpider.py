import scrapy
import os

# Use command: "py -m scrapy crawl crawlerSpider" or "scrapy crawl crawlerSpider"

class crawlerspiderSpider(scrapy.Spider):
      name = 'crawlerSpider'
      allowed_domains = ['thanhnien.vn']
      start_urls = ['https://thanhnien.vn']
      dir_name = 'data'

      # Create target Directory if don't exist
      if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print("Directory " , dir_name ,  " created ")
      else:
            print("Directory " , dir_name ,  " already exists")

      def parse(self, response):
            article = {}
            article['title']  = response.css("h2 a::attr(title)").getall()
            article['link'] = response.css("h2 a::attr(href)").getall()

            for content in range(len(article['title'])):
                  title =article['title'][content]
                  link = article['link'][content].split('/')

                  if link[0] == '':
                        file_name = link[1]
                        file = open(self.dir_name + '/' + '{file_name}.json'.format(file_name = file_name), 'a')
                        link[0] = 'https:/'
                        link.insert(1, 'thanhnien.vn')
                        link = '/'.join(link) + '/'
                  else:
                        file_name = link[3]
                        file = open(self.dir_name + '/' + '{file_name}.json'.format(file_name = file_name), 'a')
                        link = '/'.join(link) + '/'

                  file.write('\n{' + '\"Title\" : \"{title}\" , \"Link\" : \"{link}\"'.format(title = title, link = link) + '},')
                  file.close()

                  a = link.split('/')
                  if len(a) == 6:
                        del a[4]
                        sub_link_1 = '/'.join(a)
                        self.start_urls.append(sub_link_1)
                  elif len(a) == 7:
                        del a[5]
                        sub_link_2 = '/'.join(a)
                        self.start_urls.append(sub_link_2)

            start_urls = set(self.start_urls)
            for url in start_urls:
                  yield scrapy.http.Request(url = '{content}'.format(content = url), callback = self.parse)