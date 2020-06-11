import unittest


def read_yaml(filename):
    '''
    loads a yml file for its contained parameters
    :param fn: file name to read
    :return: loaded result as a dictionary
    '''
    with open(filename) as f:
        result = yaml.load(f, Loader=yaml.SafeLoader)
    return result


class TestProject(unittest.TestCase):

    def test_bg(self):
        dict = read_yaml('config.yml')
        from bg_manager import tk_manager
        bg = tk_manager()
        bg.run(dict)
        self.assertTrue(True)

    def test_download(self):
        from mq_manager import MQManager
        with open('mqresult.txt') as f:
            data = json.load(f)

        url = data['content']['putintoTask']['url']
        fileName = data['content']['putintoTask']['materialName']

        mq = MQManager()

        result = mq.download(url, fileName)
        print(result)