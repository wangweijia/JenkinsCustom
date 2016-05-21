from jenkinsapi.jenkins import Jenkins


def get_server_instance():
    jenkins_url = 'http://localhost:8080/'
    server = Jenkins(jenkins_url, username='wwj', password='123456')
    return server


def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print('\n-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('Job Name:%s' % (job_instance.name))
        print('Job Description:%s' % (job_instance.get_description()))
        print('Is Job running:%s' % (job_instance.is_running()))
        print('Is Job enabled:%s' % (job_instance.is_enabled()))


def disable_job():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    job_name = 'test02'
    if (server.has_job(job_name)):
        job_instance = server.get_job(job_name)
        job_instance.disable()
        print('\n-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('Name:%s,Is Job Enabled ?:%s' % (job_name, job_instance.is_enabled()))


def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print('\n-=-=-=-=-=-=-=-=-=-=-=-=-')
        print("Short Name:%s" %(plugin.shortName))
        print("Long Name:%s" %(plugin.longName))
        print("Version:%s" %(plugin.version))
        print("URL:%s" %(plugin.url))
        print("Active:%s" %(plugin.active))
        print("Enabled:%s" %(plugin.enabled))


def getSCMInfroFromLatestGoodBuild():
    J = get_server_instance()
    job = J["test01"]
    lgb = job.get_last_good_build()
    return lgb.get_revision()

if __name__ == '__main__':
    # print(get_server_instance().version)
    # get_job_details()
    # disable_job()
    # get_plugin_details()
    print(getSCMInfroFromLatestGoodBuild())
