import jenkins
import re
from xml.etree import ElementTree as ET


class JenkinsCustomServer:
    def str2bool(self, str):
        return 'true' == str.lower()

    def jenkins_server(self):
        # server = jenkins.Jenkins(self.rootURL, username=self.userName, password=self.password)
        name = 'wwj'
        token = 'ab3b3cd0567577077a28102cb612484c'
        server = jenkins.Jenkins('http://127.0.0.1:8080/', name, token)
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


# if __name__ == '__main__':
#     j = JenkinsCustomServer(url='http://localhost:8080/', userName='wwj', password='123456')
#
#     b = j.jenkins_project_test('test02')
#     print(b)
    # jinf = j.jenkins_job_info('test02')
    # print(jinf)
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
