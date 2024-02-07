ORIGIN_DIR_PATH = './DAMMY'
DEST_DIR_PATH = './DAMMY_FORMATTED'

import os
import shutil
import xml.etree.ElementTree as ET

xml_names = []
labels = []

def create_dest_dir():
    if os.path.exists(DEST_DIR_PATH):
        print('Directory ' + DEST_DIR_PATH + ' already exists. Data will be deleted.')
        should_continue = input('Do you want to continue? [yes/no]: ')

        while should_continue.lower() not in ['yes', 'no']:
            should_continue = input('Please enter yes or no: ')
        
        if should_continue.lower() == 'no':
            print('Exiting...')
            exit()
        
        print('Deleting directory...')
        shutil.rmtree(DEST_DIR_PATH)
    
    print('Creating directory... ' + DEST_DIR_PATH)
    os.makedirs(DEST_DIR_PATH)
    os.makedirs(DEST_DIR_PATH + '/images')
    os.makedirs(DEST_DIR_PATH + '/xml')

def get_xml_name_list():
    print('Getting xml names...')

    global xml_names
    xml_names = [
        xml_name for xml_name in os.listdir(ORIGIN_DIR_PATH + '/annotations') if os.path.isfile(os.path.join(ORIGIN_DIR_PATH + '/annotations', xml_name))
    ]

def copy_xml_files(xml_name):
    xml_content = ET.parse(ORIGIN_DIR_PATH + '/annotations/' + xml_name)

    label = xml_content.find(".//name")
    print(label.text)

def __main__():
    create_dest_dir()
    get_xml_name_list()

    for xml_name in xml_names:
        copy_xml_files(xml_name)
        print('Copying xml file...' + xml_name)


    print('Done')

__main__()