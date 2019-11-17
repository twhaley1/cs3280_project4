from pybuilder.core import use_plugin, init
from pybuilder.core import task
from pybuilder.core import Author
from pybuilder.core import use_bldsup
import os

supportDirectory = os.path.abspath(os.path.join(os.getcwd(), 'src', 'main', 'python'))
use_bldsup(build_support_dir=supportDirectory)
from ess2bmp import saveAllThumbnails

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


default_task = "publish"


@init
def set_properties(project):
    
    # project information
    project.name = 'Project 4'
    project.version = '1.0'
    project.summary = 'Project for CS3280'
    project.description = '''Given a directory, searches each .ess Skyrim save file for its screenshot. Then, it creates a .bmp image file in the same directory from that screenshot.'''
    project.authors = [Author('Thomas Whaley', 'twhaley1@my.westga.edu')]
    
@task
def convertAllIn(project):
    saveAllThumbnails(project.get_property("directory"))
