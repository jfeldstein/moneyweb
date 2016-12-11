from fabric.operations import *


def serve():
    local('python -m SimpleHTTPServer')
