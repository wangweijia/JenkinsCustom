import time
import os
from json import *


class MyCommit:

    def __init__(self, userId, userDepartment, jobName):
        self.userId = userId
        self.userDepartment = userDepartment
        self.jobName = jobName

    def file_path(self):
        return './archiveSetting/CommitData/' + str(self.userId)

    def all_commit(self):
        path = os.path.abspath(os.curdir) + '/archiveSetting/CommitData/'
        dic = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for fileName in filenames:
                filePath = path + fileName
                fh = open(file=filePath, mode='r')
                commitDic = JSONDecoder().decode(fh.readlines()[0])
                fh.close()
                dic[fileName] = commitDic
        return dic

    def commit_by_user(self):
        try:
            file = self.file_path()
            fh = open(file=file, mode='r')
            commitDic = JSONDecoder().decode(fh.readlines()[0])
            fh.close()
        except:
            commitDic = {}
        return commitDic

    def add_commit(self, commitTxt):
        timeStr = str(time.time())
        commitDic = self.commit_by_user()
        try:
            commitDic[self.jobName][timeStr] = commitTxt
        except:
            tdic = {timeStr: commitTxt}
            commitDic[self.jobName] = tdic

        return self.save_commit(commitDic)

    def dele_commit(self, commitKey):
        commitDic = self.commit_by_user()
        jobCommitDic = commitDic.get(self.jobName, None)
        if jobCommitDic:
            jobCommitDic.pop(commitKey, None)
        return self.save_commit(commitDic)

    def dele_job_commit(self):
        path = os.path.abspath(os.curdir) + '/archiveSetting/CommitData/'
        for dirpath, dirnames, filenames in os.walk(path):
            for fileName in filenames:
                filePath = path + fileName
                fh = open(file=filePath, mode='r')
                commitDic = JSONDecoder().decode(fh.readlines()[0])
                fh.close()
                commitDic.pop(self.jobName, None)
                fh = open(file=filePath, mode='w')
                commitJson = JSONEncoder().encode(commitDic)
                fh.write(commitJson)
                fh.close()

    def save_commit(self, commitDic):
        try:
            file = self.file_path()
            fh = open(file=file, mode='w', encoding='utf-8')
            commitJson = JSONEncoder().encode(commitDic)
            fh.write(commitJson)
            fh.close()
            return True
        except:
            return False

# if __name__ == '__main__':
#     c = MyCommit(1, '开发部门', 'test01')
#     d = c.all_commit()
#     print(d)
#     # c.add_commit('test')
#     file = ''
#     ssss = open(file='./CommitData/bbbb', mode='w', encoding='utf-8')