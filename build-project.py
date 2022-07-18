
import PyInstaller.__main__
from distutils.dir_util import copy_tree
from shutil import copyfile
import os
import shutil
import json

version = "0.9"
progName = "Periodic Screen Capture "

abs_path = os.path.abspath(os.getcwd())

# delete dist and build folders if exists
try:
    shutil.rmtree(abs_path + '\\build')
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

try:
    shutil.rmtree(abs_path + '\\dist')
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

try:
    new_dir_name = abs_path + '\\{}-v{}-windows\\'.format(progName,version)
    shutil.rmtree(new_dir_name)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

try:
    zip_file_name = abs_path +  '\\{}-v{}-windows.zip'.format(progName,version)
    os.remove(zip_file_name)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

# create build - one file
# os.system('pyinstaller -w --onefile main.py --icon=logo.ico')

version_str = '-n{}-v{}'.format(progName,version)

# create build - one directory (-w hide background command prompt)
PyInstaller.__main__.run([
    'periodic-screen-capture.py',
    #'-w', #hide the terminal window
    #'--onedir',
    '--onefile', #
    #'--icon=logo_hawk.ico',
    version_str
])

#copy config fiels, icon files to the output folder
source_file = abs_path + '\\settings.txt'
destination_file = abs_path + '\\dist\\settings.txt'
copyfile(source_file, destination_file)

destination_dir = abs_path + '\\dist\\screen_captures'
os.mkdir(destination_dir)

#rename the folder with new version name
current_dir_name = abs_path + '\\dist\\'
new_dir_name = abs_path + '\\{}-v{}-windows\\'.format(progName,version)
try:
    dest_fpath = os.path.dirname(new_dir_name)
    source_fpath = os.path.dirname(current_dir_name)
    os.rename(source_fpath,dest_fpath)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

#make a zip file from directory
zip_file_name = '{}-v{}-windows'.format(progName,version)

try:
    dest_fpath = os.path.dirname(new_dir_name)
    shutil.make_archive(zip_file_name, 'zip', dest_fpath)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


