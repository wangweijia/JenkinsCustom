import jenkins
import re
from xml.etree import ElementTree as ET

class JenkinsCustomServer:
    def __init__(self, url, userName, password):
        self.rootURL = url
        self.userName = userName
        self.password = password

    def jenkins_server(self):
        server = jenkins.Jenkins(self.rootURL, username=self.userName, password=self.password)
        # name = 'admin'
        # token = 'ef6b51132237b4b14f5de8b025b1c844'
        # server = jenkins.Jenkins('http://192.168.16.221:8080/jenkins', name, token)
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
        return server.get_jobs()

    def jenkins_project_os(self, jobName):
        server = self.jenkins_server()
        config_xml = server.get_job_config(jobName)

        patLeft = re.compile(r'&lt;')
        patRight = re.compile(r'&gt;')
        config_xml = re.sub(patLeft, '<', config_xml)
        config_xml = re.sub(patRight, '>', config_xml)

        xml_tree = ET.ElementTree(element=ET.fromstring(config_xml))
        elem = xml_tree
        for item in elem.iter(tag='os'):
            return item.text

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
        server = self.jenkins_server()
        server.build_job(jobName)

    def jenkins_job_status(self, jobName):
        server = self.jenkins_server()

        for item in server.get_running_builds():
            if item['name'] == jobName:
                return True
        return False




# if __name__ == '__main__':
#     j = JenkinsCustomServer(url='http://localhost:8080/', userName='wwj', password='123456')
#
#     info = j.jenkins_job_status('test02')
#     print(info)
#     s = j.jenkins_job_config_xml('wwj01', ['builders', 'au.com.rayh.XCodeBuilder', 'configuration'])
#
#     print(s)
#     j = JenkinsCustomServer(url='http://localhost:8080/', userName='wwj', password='123456')
#     server = j.jenkins_server()
#
#     xml = server.get_job_config('test02')
#     patLeft = re.compile(r'&lt;')
#     patRight = re.compile(r'&gt;')
#     xml = re.sub(patLeft, '<', xml)
#     xml = re.sub(patRight, '>', xml)
#
#     xml_tree = ET.ElementTree(element=ET.fromstring(xml))
#
#     print(xml)
#
#     for item in xml_tree.iter(tag='os'):
#         print(item.tag + ',' + item.text + '\n')

