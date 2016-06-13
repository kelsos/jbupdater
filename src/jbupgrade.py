#!/usr/bin/python
import getopt
import os
import tarfile
import shutil
import re
import pycurl
import xml.etree.ElementTree as etree
from distutils.version import LooseVersion
import getpass
import sys

from lxml import html
import requests


product_map = {
    'idea': "IntelliJ IDEA",
    'rubymine': "RubyMine",
    'pycharm': "PyCharm",
    'phpstorm': "PhpStorm",
    'webstorm': "WebStorm",
    'clion': "CLion",
    '0xdbe': "0xDBE"
}
folder_names = {
    'pycharm',
    'rubymine',
    'idea',
    'webstorm',
    'phpstorm',
    '0xdbe',
    'clion'
}

directory_map = {
    '.*pycharm.*': 'pycharm',
    '.*RubyMine.*': 'rubymine',
    '.*idea.*': 'idea',
    '.*WebStorm.*': 'webstorm',
    '.*PhpStorm.*': 'phpstorm',
    '.*0xDBE.*': '0xdbe',
    '.*clion.*': 'clion'
}


def main(argv):
    update_checker()


def download(url):
    filename = url.split('/')[-1]
    print(url)
    print(u'Starting download of {0:s} ...'.format(filename))
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.NOPROGRESS, 0)
    curl.setopt(pycurl.PROGRESSFUNCTION, get_progress)
    curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0')

    path = '/tmp/jbupdater'

    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, filename)

    if os.path.exists(filepath):
        f = open(filepath, "ab")
        downloaded = os.path.getsize(filepath)
        curl.setopt(pycurl.RESUME_FROM, downloaded)
    else:
        f = open(filepath, "wb")

    curl.setopt(pycurl.WRITEDATA, f)
    curl.perform()
    curl.close()
    return filename


def get_progress(total, existing, upload_t, upload_d):
    if total and existing:
        percent = (existing / total * 100)
        downloaded_mb = float(existing / 1024 / 1024)
        total_mb = float(total / 1024 / 1024)
        done = int(50 * existing / total)
        sys.stdout.write(
            u"\r[{0:s}{1:s}] {2:.2f} % ({3:.2f} of {4:.2f} MB)".format('=' * done, ' ' * (50 - done), percent,
                                                                       downloaded_mb, total_mb))
        sys.stdout.flush()


def extract(filename):
    if tarfile.is_tarfile(filename):
        print('Starting the archive extraction...')
        tar = tarfile.open(filename, 'r:gz')
        tar.extractall()
        directory = os.path.commonprefix(tar.getnames())
        tar.close()
        print('Archive extracted successfully...')
        return directory
    print('File is not a tar...')
    sys.exit(1)


def remove(filename):
    os.remove(filename)


def get_download_link(page):
    download_link = ""
    content = requests.get(page)
    tree = html.fromstring(content.text)
    for element, attribute, link, pos in tree.iterlinks():
        m = re.search('.*\.tar.gz$', link)
        if m:
            download_link = link
            break

    return download_link


def move(directory):
    directory = re.sub('/', '', directory)
    print("Preparing to move the extracted directory...")
    newdir = '/opt/'
    for regex, dir in directory_map.items():
        if re.search(regex, directory):
            newdir += dir
            break

    print('Moving directory %s to %s' % (directory, newdir))

    try:
        print("Removing the old directory...")
        shutil.rmtree(newdir)
        print("Moving the archive contents...")
        shutil.move(directory, newdir)
        print("Operation Complete...")
        user = getpass.getuser()
        shutil.chown(newdir, user, user)
    except shutil.Error as err:
        print(err)
        sys.exit(1)


def update_checker():
    versions = get_current_versions()
    updates = {}
    url = 'https://www.jetbrains.com/updates/updates.xml'
    response = requests.get(url)
    root = etree.fromstring(response.content)
    for product in root:
        product_name = product.get('name')

        if product_name == "AppCode":
            continue

        installed_version = versions[product_name]

        for version in product:
            if version.get('majorVersion'):
                for build in version:
                    new_build = build.get("number")
                    if LooseVersion(installed_version) < LooseVersion(new_build):

                        print('Found Update for {0}, build {1} is available'.format(product_name, new_build))
                        for child in build:
                            if child.get("download"):
                                updates[product_name] = child.get("url")

    for product, url in updates.items():
        print("Getting download link for {0} -- {1}".format(product, url))
        m = re.search('.*\/download\/.*', url)
        if m:
            url += "download_thanks.jsp?os=linux&edition=prof"
        download_link = get_download_link(url)
        filename = download(download_link)
        directory = extract(filename)
        move(directory)

def get_current_versions():
    versions = {}
    for folder in folder_names:
        inFile = open('/opt/%s/build.txt' % folder, 'r')
        contents = inFile.read()
        m = re.search('[A-Z]{2}-(\d*\.\d*)', contents)
        if m:
            versions[product_map[folder]] = m.group(1)
    return versions


def query_yes_no(question, default="no"):
    valid = {
        "yes": True,
        "y": True,
        "no": False,
        "n": False
    }

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = "[y/N] "
    else:
        raise ValueError("invalid default answer: '%s" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "or ('y' or 'n').\n")


if __name__ == "__main__":
    euid = os.getuid()
    if euid != 0:
        print("This script requires root permissions.\nRunning sudo...\n")
        if query_yes_no("Do you wish to grant root permissions to this script") is False:
            sys.exit(1)
        else:
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            os.execlpe('sudo', *args)
    main(sys.argv[1:])
