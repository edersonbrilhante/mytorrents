from tornado.ioloop import IOLoop
import logging
import tornado.httpclient
import tornado.gen
from lxml import etree, html
from io import BytesIO, StringIO
from tornado import gen, httpclient
import zipfile
import torrent
from os import listdir
import uuid
import json
import shutil
from multiprocessing import Pool
from functools import partial


log = logging.getLogger(__name__)


class Series(object):

    list_json = list()

    def get_link_downlad(self, url):
        return IOLoop.instance().run_sync(lambda: self._get_link_downlad(url))

    @gen.coroutine
    def _get_link_downlad(self, url):

        try:
            http_client = httpclient.HTTPClient()
            request = tornado.httpclient.HTTPRequest(
                url, method='GET', validate_cert=0)
            response = http_client.fetch(request)
        except Exception as e:
            # Other errors are possible, such as IOError.
            log.error("Error: {}".format(e))
        else:
            http_client.close()
            try:
                filecontent = response.body.decode('utf-8')
            except UnicodeDecodeError:
                log.error('ERROR: unicode')
            else:
                parser = html.HTMLParser()
                try:
                    tree = html.parse(StringIO(filecontent), parser)
                except etree.XMLSyntaxError as details:
                    print('ERROR: parser', details.error_log)
                except Exception as e:
                    log.exception(e)
                else:
                    try:

                        e = tree.xpath('//div[@class="post-inner"]//div[@class="entry"]//a[contains(@href,"https://seriestorrent.tv/wp-content/uploads")]')

                        link = e[-1].items()[0][1]
                    except etree.XPathEvalError as details:
                        log.error('ERROR: XPath expression', details.error_log)
                    except Exception as e:
                        log.exception(e)
                    else:
                        return link

    @gen.coroutine
    def get_files(self, link):
        try:
            http_client = httpclient.HTTPClient()
            request = tornado.httpclient.HTTPRequest(
                link, method='GET', validate_cert=0)
            response = http_client.fetch(request)

            folder_name = str(uuid.uuid4())
            folder_name = '/tmp/{}'.format(folder_name)
            z = zipfile.ZipFile(BytesIO(response.body))
            z.extractall(folder_name)
        except Exception as e:
            log.error('{},{}'.format(folder_name, e))
        else:
            http_client.close()
            try:
                files = listdir(folder_name)
                files_1080 = [x for x in files if '1080' in x]
                files_720 = [x for x in files if '720' in x]
                if files_1080:
                    files = files_1080
                elif files_720:
                    files = files_720
                files.sort()

                torrent_file = '{}/{}'.format(folder_name, files[1])
                subtitle_file = '{}/{}'.format(folder_name, files[0])
                new_subtitle_file = files[0]

                tor = torrent.Torrent()
                tor.start(torrent_file, subtitle_file, new_subtitle_file)

                shutil.rmtree(folder_name)

            except Exception as e:
                log.error(e)

    def load_json(self, file_path):
        with open(file_path) as json_data:
            data = json.loads(json_data.read())
            json_data.close()
            return data

    def write_json(self,):
        with open('series.json', 'w') as outfile:
            json.dump(self.list_json, outfile)

    def get_list(self):
        self.list_json = self.load_json('series.json')
        return self.list_json

    def exec_one(self, serie):
        key = self.list_json.index(serie)
        link = self.get_link_downlad(serie['link'])
        if serie.get('last_download') != link and link is not None:
            self.list_json[key]['last_download'] = link
            self.get_files(link)
        else:
            print('Ignoring Serie %s' % serie['link'])


def exec_one_help(inst, serie):
    inst.exec_one(serie)


def main():
    processes = 5

    inst = Series()
    list_json = inst.get_list()

    pool = Pool(processes=processes)

    func = partial(exec_one_help, inst)

    pool.map(func, list_json)
    pool.close()
    pool.join()

    inst.write_json()

if __name__ == "__main__":
    main()
