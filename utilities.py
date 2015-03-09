import getpass
import pycurl
import os
import tarfile
import requests
import re
import shutil
import xml.etree.ElementTree as eTree
from build import Build
from distutils.version import LooseVersion
from lxml import html

def download(url, progress_callback):
    filename = url.split('/')[-1]
    print(url)
    print(u'Starting download of {0:s} ...'.format(filename))
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.NOPROGRESS, 0)
    curl.setopt(pycurl.PROGRESSFUNCTION, progress_callback)
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

def extract_tar(filename):
    if tarfile.is_tarfile(filename):
        print('Starting the archive extraction...')
        tar = tarfile.open(filename, 'r:gz')
        tar.extractall()
        directory = os.path.commonprefix(tar.getnames())
        tar.close()
        print('Archive extracted successfully...')
        return directory
    print('File is not a tar...')

def remove_file(filename):
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


def move_directory(directory, ide_directory):
    directory = re.sub('/', '', directory)

    try:
        print("Removing the old directory...")
        shutil.rmtree(ide_directory)
        print("Moving the archive contents...")
        shutil.move(directory, ide_directory)
        print("Operation Complete...")
        user = getpass.getuser()
        shutil.chown(ide_directory, user, user)
    except shutil.Error as err:
        print(err)


def load_installed_versions(data_store):

    ide_list = vars(data_store)
    for ide in ide_list.values():
        try:
            input_file = open('/opt/%s/build.txt' % ide.install_directory, 'r')
            contents = input_file.read()
            m = re.search('[A-Z]{2}-(\d*\.\d*)', contents)
            if m:
                ide.installed_version = m.group(1)
        except OSError as err:
            print("OS Error: {0}".format(err))


def check_for_updates(data_store):

    url = 'https://www.jetbrains.com/updates/updates.xml'
    response = requests.get(url)
    root = eTree.fromstring(response.content)
    ide_list = vars(data_store)

    products = parse_product_xml(root)
    for ide in ide_list.values():
        product = products.get(ide.name)
        for build in product.keys():
            build_info = product[build]
            ide_build = Build()
            ide_build.build_number = build
            ide_build.download_url = build_info['download_url'] if 'download_url' in build_info.keys() else ""
            ide_build.major_version = build_info['major_version']
            ide_build.status = build_info['status']
            if newer_build_available(ide.installed_version, build):
                ide.available_version = build
                print(build)
            ide.builds.append(ide_build)




def parse_product_xml(root):
    products = {}
    for product in root:
        product_name = product.get('name')

        if product_name == "AppCode":
            continue

        products[product_name] = {}

        for channel in product:
            major_version = channel.get('majorVersion')
            if major_version:
                for build in channel:
                    build_number = build.get("number")
                    products[product_name][build_number] = {}
                    products[product_name][build_number]["major_version"] = str(major_version)
                    products[product_name][build_number]["status"] = str(channel.get("status")).lower()
                    for child in build:
                        if child.get("download"):
                            products[product_name][build_number]["download_url"] = child.get("url")

    print(products)
    return products

def newer_build_available(installed_version, available_version):
    if (not installed_version):
        return True
    else:
        return LooseVersion(installed_version) < LooseVersion(available_version)

