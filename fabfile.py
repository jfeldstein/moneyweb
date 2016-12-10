from fabric.operations import *


def serve():
    local('python runserver.py')
