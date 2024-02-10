ORIGIN_DIR_PATH = './dataset/DAMMY'
DEST_DIR_PATH = './dataset/DAMMY_FORMATTED'

START_INDEX = 0

import os
import shutil
import xml.etree.ElementTree as ET

xml_names = []
labels = []
each_label_file_counts = []

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
    os.makedirs(DEST_DIR_PATH + '/images')
    os.makedirs(DEST_DIR_PATH + '/xml')

def get_xml_name_list():
    print('Getting xml names...')

    global xml_names
    xml_names = [
        xml_name
        for xml_name in os.listdir(ORIGIN_DIR_PATH + '/annotations')
        if os.path.isfile(os.path.join(ORIGIN_DIR_PATH + '/annotations', xml_name))
    ]

def get_label(xml_content):
    label = xml_content.find('.//name').text

    return label

def create_xml_dest_dir(label):
    xml_dest_dir = DEST_DIR_PATH + '/xml/' + label + '/'

    if label not in labels:
        labels.append(label)
        each_label_file_counts.append(START_INDEX)
        os.mkdir(xml_dest_dir)
    
    return xml_dest_dir

def edit_xml_content(xml_content, xml_dest_name, label):
    root = xml_content.getroot()

    # Change image file path
    root.find('.//filename').text = xml_dest_name.replace('.xml', '.jpg')

    # add folder tag
    folder = ET.SubElement(root, 'folder') 
    folder.text = label

    # add path tag
    path = ET.SubElement(root, 'path')
    path.text = DEST_DIR_PATH + '/images/' + label + '/' + xml_dest_name.replace('.xml', '.jpg')

def copy_xml_files(xml_name):
    xml_content = ET.parse(ORIGIN_DIR_PATH + '/annotations/' + xml_name)

    label = get_label(xml_content)

    xml_dest_dir = create_xml_dest_dir(label)
    xml_dest_name = str(each_label_file_counts[labels.index(label)]) + '.xml'

    edit_xml_content(xml_content, xml_dest_name, label)

    # Copy xml file
    print('Copying ' + xml_name + ' to ' + xml_dest_dir + xml_dest_name)
    xml_content.write(xml_dest_dir + str(xml_dest_name))

    return label


def copy_image_files(xml_name, label):
    image_src_name = xml_name.replace('.xml', '.jpg')
    image_src_dir = ORIGIN_DIR_PATH + '/images/'

    image_dest_dir = DEST_DIR_PATH + '/images/' + label + '/'
    image_dest_name = str(each_label_file_counts[labels.index(label)]) + '.jpg'

    if not os.path.exists(image_dest_dir):
        os.makedirs(image_dest_dir)

    print(
        'Copying '
        + image_src_dir
        + image_src_name
        + ' to '
        + image_dest_dir
        + image_dest_name
    )

    shutil.copy(image_src_dir + image_src_name, image_dest_dir + image_dest_name)


def __main__():
    create_dest_dir()
    get_xml_name_list()

    for xml_name in xml_names:
        label = copy_xml_files(xml_name)
        copy_image_files(xml_name, label)

        each_label_file_counts[labels.index(label)] += 1

        print('')

    label_text = open(DEST_DIR_PATH + '/labels.txt', 'x')
    for label in labels:
        label_text.write(label + '\n')
    label_text.close()

    print('Done')


__main__()
