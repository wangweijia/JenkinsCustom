import jenkins
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

    def jenkins_new_job_config_xml(self, jobName, tags, text):
        server = self.jenkins_server()
        config_xml = server.get_job_config(jobName)
        xmlTree = ET.ElementTree(element=ET.fromstring(config_xml))
        elem = xmlTree
        for aTag in tags:
            for item in elem.iter(tag=aTag):
                elem = item
                break
        elem.text = text
        newconfigxml = ET.tostring(element=xmlTree.getroot(), encoding='utf-8')
        return newconfigxml.decode()

    def jenkins_change_job_config(self, configXml, jobName):
        server = self.jenkins_server()
        server.reconfig_job(jobName, configXml)

    def jenkins_build_project(self, jobName):
        server = self.jenkins_server()
        server.build_job(jobName)


# if __name__ == '__main__':
#     j = JenkinsCustomServer(url='http://localhost:8080/', userName='wwj', password='1234')
#     server = j.jenkins_server()
#     jobs = j.jenkins_login()
# print(jobs)
#     s = jenkins_new_job_config_xml('wwj01', ['builders', 'au.com.rayh.XCodeBuilder', 'configuration'], 'release')
#     jenkins_change_job_config(s, 'wwj01')
#     jenkins_build_project('wwj01')
