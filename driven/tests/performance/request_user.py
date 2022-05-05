import os
import traceback
import yaml
from locust import HttpUser, between, task


class RequestUser(HttpUser):
    request_url_file = os.environ['LOCUST_REQUEST_FILE']
    if not os.path.exists(request_url_file):
        raise Exception(
            'failed to find request url file with environ variable LOCUST_REQUEST_FILE')

    try:
        with open(request_url_file, mode='r') as cf:
            urls = yaml.load(cf, Loader=yaml.FullLoader)
            print(urls)
    except Exception as ex:
        print('failed to load yaml file [%s]' % request_url_file)
        traceback.print_exc()
        raise ex

    wait_time = between(urls['wait_time']['min'], urls['wait_time']['max'])

    @task
    def request(self):
        for k in self.urls['requests']:
            r = self.urls['requests'][k]
            if 'get' == r['method']:
                if 'param' in r:
                    self.client.get(r['path'], params=r['param'])
                else:
                    self.client.get(r['path'])
            elif 'post-json' == r['method']:
                self.client.post(r['path'], json=r['data'])
            else:
                raise Exception(
                    'request method [%s] not support yet' % r['method'])
