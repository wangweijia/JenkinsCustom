import jenkins
from xml.etree import ElementTree as ET

import re
from six.moves.urllib.parse import urlparse


class JenkinsCustomServer:
    def str2bool(self, str):
        return 'true' == str.lower()

    def jenkins_server(self):
        # server = jenkins.Jenkins(self.rootURL, username=self.userName, password=self.password)
        name = 'admin'
        token = 'ef6b51132237b4b14f5de8b025b1c844'
        server = jenkins.Jenkins('http://192.168.16.221:8080/jenkins', name, token)
        return server

    def jenkins_login(self):
        server = self.jenkins_server()
        try:
            server.get_jobs()
            return True
        except BaseException as e:
            print(e)
            return False

    def jenkins_jobs(self):
        server = self.jenkins_server()
        jobs = server.get_jobs()

        newJobs = []
        for job in jobs:
            jobName = job['name']
            if not self.jenkins_job_test(jobName):
                newJobs.append(job)
        return newJobs

    def jenkins_job_os(self, jobName):
        info = self.jenkins_job_info(jobName)
        descriptionXMLstr = '<base>' + info['description'] + '</base>'
        xml_tree = ET.ElementTree(element=ET.fromstring(descriptionXMLstr))

        for elem in xml_tree.iter(tag='description_os'):
            return elem.text
        return None

    def jenkins_job_project(self, jobName):
        info = self.jenkins_job_info(jobName)
        descriptionXMLstr = '<base>' + info['description'] + '</base>'
        xml_tree = ET.ElementTree(element=ET.fromstring(descriptionXMLstr))

        for elem in xml_tree.iter(tag='description_project'):
            return elem.text
        return None

    def jenkins_job_test(self, jobName):
        info = self.jenkins_job_info(jobName)
        descriptionXMLstr = '<base>' + info['description'] + '</base>'
        xml_tree = ET.ElementTree(element=ET.fromstring(descriptionXMLstr))

        for elem in xml_tree.iter(tag='description_test'):
            return self.str2bool(elem.text)
        return True

    def jenkins_job_project(self, jobName):
        info = self.jenkins_job_info(jobName)
        descriptionXMLstr = '<base>' + info['description'] + '</base>'
        xml_tree = ET.ElementTree(element=ET.fromstring(descriptionXMLstr))

        for elem in xml_tree.iter(tag='description_project'):
            return elem.text
        return None

    def jenkins_job_config_xml(self, jobName, tags):
        server = self.jenkins_server()
        config_xml = server.get_job_config(jobName)
        xml_tree = ET.ElementTree(element=ET.fromstring(config_xml))
        elem = xml_tree
        for aTag in tags:
            for item in elem.iter(tag=aTag):
                elem = item
                break
        return {'tag': elem.tag, 'text': elem.text}

    def jenkins_new_job_config_xml(self, jobName, tags, text):
        server = self.jenkins_server()
        config_xml = server.get_job_config(jobName)
        xml_tree = ET.ElementTree(element=ET.fromstring(config_xml))
        elem = xml_tree
        for aTag in tags:
            for item in elem.iter(tag=aTag):
                elem = item
                break
        elem.text = text
        newconfigxml = ET.tostring(element=xml_tree.getroot(), encoding='utf-8')
        return newconfigxml.decode()

    def jenkins_change_job_config(self, configXml, jobName):
        server = self.jenkins_server()
        server.reconfig_job(jobName, configXml)

    def jenkins_build_project(self, jobName):
        if self.jenkins_job_buildable(jobName):
            server = self.jenkins_server()
            server.build_job(jobName)

    def jenkins_job_info(self, jobName):
        server = self.jenkins_server()
        return server.get_job_info(name=jobName)

    def jenkins_job_buildable(self, jobName):
        info = self.jenkins_job_info(jobName)
        return info['buildable']

    def jenkins_job_building(self, jobName):
        server = self.jenkins_server()

        nodes = server.get_nodes()
        for node in nodes:
            print('nodes')
            # the name returned is not the name to lookup when
            # dealing with master :/
            if node['name'] == 'master':
                node_name = '(master)'
            else:
                node_name = node['name']
            try:
                info = server.get_node_info(node_name, depth=2)
            except:
                print('except')
                # # Jenkins may 500 on depth >0. If the node info comes back
                # # at depth 0 treat it as a node not running any jobs.
                # if ('[500]' in str(e) and
                #         self.get_node_info(node_name, depth=0)):
                #     continue
                # else:
                #     raise
            for executor in info['executors']:
                executable = executor['currentExecutable']
                if executable:
                    executor_number = executor['number']
                    build_number = executable['number']
                    url = executable['url']
                    print(urlparse(url).path)
                    m = re.match(r'.*?/job/([^/]+)/.*', urlparse(url).path)
                    job_name = m.group(1)
                    if job_name == jobName:
                        return True
        return False

# if __name__ == '__main__':
#     j = JenkinsCustomServer()
#     server = j.jenkins_server()
#
#     builds = []
#     nodes = server.get_nodes()
#     for node in nodes:
#         print('nodes')
#         # the name returned is not the name to lookup when
#         # dealing with master :/
#         if node['name'] == 'master':
#             node_name = '(master)'
#         else:
#             node_name = node['name']
#         try:
#             info = server.get_node_info(node_name, depth=2)
#         except :
#             print('except')
#             # # Jenkins may 500 on depth >0. If the node info comes back
#             # # at depth 0 treat it as a node not running any jobs.
#             # if ('[500]' in str(e) and
#             #         self.get_node_info(node_name, depth=0)):
#             #     continue
#             # else:
#             #     raise
#         for executor in info['executors']:
#             executable = executor['currentExecutable']
#             if executable:
#                 executor_number = executor['number']
#                 build_number = executable['number']
#                 url = executable['url']
#                 print(urlparse(url).path)
#                 m = re.match(r'.*?/job/([^/]+)/.*', urlparse(url).path)
#                 job_name = m.group(1)
#                 builds.append({'name': job_name,
#                                'number': build_number,
#                                'url': url,
#                                'node': node_name,
#                                'executor': executor_number})
#
#     print(builds)
