import os
import subprocess
import tempfile
import sys
import time


class BaseHang(object):
    @staticmethod
    def get_tmp_name():
        fd, file_name = tempfile.mkstemp()
        os.close(fd)
        return file_name

    def __init__(self):
        self.tmp_file = BaseHang.get_tmp_name()

        self.kwargs = {
            'stderr': subprocess.PIPE,
            'stdout': subprocess.PIPE}

        self.text = None

    def _write_file(self):
        with open(self.tmp_file, 'w+') as _file:
            _file.write(self.text)

    def _in_the_middle(self):
        pass

    def run(self):
        self._write_file()
        print("\nStart process...\n")
        self._in_the_middle()
        print('Done.\n')


class PipHang(BaseHang):
    """ win, py3: 4K
        lin, py2/py3: never
    """

    def __init__(self):
        super(PipHang, self).__init__()
        self.kwargs['shell'] = True
        self.kwargs['args'] = u'pip install -r %s' % self.tmp_file
        self.text = """apiritif>=0.6.7
       astunparse
       colorama; sys_platform == 'win32'
       colorlog
       cssselect
       hdrpy>=0.3.3
       ipaddress; python_version < '3.0'
       nose
       lxml
       terminaltables
       selenium
       urwid
       progressbar33
       pytest>=3
       """

    def _in_the_middle(self):
        proc = subprocess.Popen(**self.kwargs)
        proc.wait()  # cause #1
        out, err = proc.communicate()
        print("OUT:[%s]\n%s\n\nERR:\n%s\n" % (len(out), out, err))


class TypeHang(BaseHang):
    """
    win, py3, type: wait && 4K
    lin py2/py3, cat(int)/tail(ext): shell || (wait && 64K)
    """

    def __init__(self):
        super(TypeHang, self).__init__()
        self.kwargs['shell'] = True
        if sys.platform == "win32":
            cmd = ['cmd', '/c', 'type']
        else:
            cmd = ['tail']
        self.kwargs['args'] = cmd + [self.tmp_file]
        self.kwargs['args'] = 'tail ' + self.tmp_file
        self.text = '*' * 6000
        #self.kwargs['stderr'] = open(BaseHang.get_tmp_name(), 'at')
        #self.kwargs['stdout'] = open(BaseHang.get_tmp_name(), 'at')

    def _in_the_middle(self):
        proc = subprocess.Popen(**self.kwargs)
        #time.sleep(5)
        proc.wait()  # cause #1
        #proc.stdout.close()
        #proc.stderr.close()
        #out, err = proc.communicate()

        #time.sleep(1)
        #proc.stderr.close()

        #proc.stdout.close()

        out, err = proc.communicate()
        print("OUT:[%s]\n%s\n\nERR:\n%s\n" % (len(out), out, err))


# PipHang().run()
TypeHang().run()
