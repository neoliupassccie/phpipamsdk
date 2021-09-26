""" configuration class """


class Configuration(object):
    """ class used to store configuration """
    def __init__(self):
        # """ constructor """
        self.api_uri = 'http://127.0.0.1/api/admin/'
        self.api_username = 'admin'
        self.api_password = 'root@123'
        # self.api_uri = 'http://ipdb.sumscope.com/api/admin/'
        # self.api_username = 'xiang.liu'
        # self.api_password = 'yhx@1314'
        # if using app code authentication instead of user/pass set app code
        self.api_appcode = ''
        self.api_verify_ssl = False
        # self.api_verify_ssl = True
