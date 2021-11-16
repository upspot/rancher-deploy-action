import os
import sys
import requests
import re


class DeployRancher:
    def __init__(self, rancher_access_key, rancher_secret_key, rancher_url_api,
                 rancher_service_name, rancher_namespace, rancher_docker_image, rancher_regex):
        self.access_key = rancher_access_key
        self.secret_key = rancher_secret_key
        self.rancher_url_api = rancher_url_api
        self.service_name = rancher_service_name
        self.namespace = rancher_namespace
        self.docker_image = rancher_docker_image
        self.rancher_deployment_path = ''
        self.rancher_namespace = ''
        self.rancher_workload_url_api = ''
        self.rancher_regex = rancher_regex

    def deploy(self):
        rp = requests.get('{}/projects'.format(self.rancher_url_api), auth=(self.access_key, self.secret_key))
        projects = rp.json()

        isVersion = re.search(self.rancher_regex, self.docker_image)
        isLatest = re.search("latest", self.docker_image)
        namespaces = self.namespace.split(',')

        for p in projects['data']:
            w_url = '{}/projects/{}/workloads'.format(self.rancher_url_api, p['id'])
            rw = requests.get(w_url, auth=(self.access_key, self.secret_key))
            workload = rw.json()
            for w in workload['data']:
                if w['name'] == self.service_name and w['namespaceId'] in namespaces:
                    self.rancher_workload_url_api = w_url
                    self.rancher_deployment_path = w['links']['self']
                    self.rancher_namespace = w['namespaceId']
                    rget = requests.get(self.rancher_deployment_path,
                                        auth=(self.access_key, self.secret_key))
                    response = rget.json()
                    if 'status' in response and response['status'] == 404:
                        config = {
                            "containers": [{
                                "imagePullPolicy": "Always",
                                "image": self.docker_image,
                                "name": self.service_name,
                            }],
                            "namespaceId": self.rancher_namespace,
                            "name": self.service_name
                        }

                        requests.post(self.rancher_workload_url_api,
                                    json=config, auth=(self.access_key, self.secret_key))
                    else:
                        actualImage = response['containers'][0]['image']
                        isActualVersion = re.search(self.rancher_regex, actualImage)
                        isActualLatest = re.search("latest", actualImage)

                        if (isActualVersion and isVersion ) or (isLatest and isActualLatest):
                            response['containers'][0]['image'] = self.docker_image

                            requests.put(self.rancher_deployment_path + '?action=redeploy',
                                        json=response, auth=(self.access_key, self.secret_key))

            if self.rancher_deployment_path != '':
                break

        sys.exit(0)


def deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                      rancher_service_name, rancher_namespace, rancher_docker_image, rancher_regex):
    deployment = DeployRancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                               rancher_service_name, rancher_namespace, rancher_docker_image, rancher_regex)
    deployment.deploy()


if __name__ == '__main__':
    rancher_access_key = os.environ['RANCHER_ACCESS_KEY']
    rancher_secret_key = os.environ['RANCHER_SECRET_KEY']
    rancher_url_api = os.environ['RANCHER_URL_API']
    rancher_service_name = os.environ['SERVICE_NAME']
    rancher_docker_image = os.environ['DOCKER_IMAGE']
    rancher_namespace = os.environ['NAMESPACE']
    rancher_regex = os.environ['REGEX']

    try:
        deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                          rancher_service_name, rancher_namespace, rancher_docker_image, rancher_regex)

    except Exception as e:
        print(e)
        sys.exit(1)
