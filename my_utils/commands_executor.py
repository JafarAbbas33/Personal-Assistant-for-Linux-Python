import subprocess


def shutdown():
    test = subprocess.Popen(["shutdown"], stdout=subprocess.PIPE)
    output = int(test.communicate()[0].decode())
