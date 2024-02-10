ORIGIN_DIR_PATH = "./DAMMY"
DEST_DIR_PATH = "./DAMMY_FORMATTED"

import os
import shutil
import xml.etree.ElementTree as ET

xml_names = []
labels = []
each_label_file_counts = []

def create_dest_dir():
    if os.path.exists(DEST_DIR_PATH):
        print("Directory " + DEST_DIR_PATH + " already exists. Data will be deleted.")
        should_continue = input("Do you want to continue? [yes/no]: ")

        while should_continue.lower() not in ["yes", "no"]:
            should_continue = input("Please enter yes or no: ")

        if should_continue.lower() == "no":
            print("Exiting...")
            exit()

        print("Deleting directory...")
        shutil.rmtree(DEST_DIR_PATH)

    print("Creating directory... " + DEST_DIR_PATH)
    os.makedirs(DEST_DIR_PATH + "/images")
    os.makedirs(DEST_DIR_PATH + "/xml")


def get_xml_name_list():
    print("Getting xml names...")

    global xml_names
    xml_names = [
        xml_name
        for xml_name in os.listdir(ORIGIN_DIR_PATH + "/annotations")
        if os.path.isfile(os.path.join(ORIGIN_DIR_PATH + "/annotations", xml_name))
    ]


def copy_xml_files(xml_name):
    xml_content = ET.parse(ORIGIN_DIR_PATH + "/annotations/" + xml_name)

    label = xml_content.find(".//name")

    xml_dest_dir = DEST_DIR_PATH + "/xml/" + label.text + "/"

    if label.text not in labels:
        labels.append(label.text)
        each_label_file_counts.append(0)

        os.mkdir(xml_dest_dir)

    xml_dest_name = str(each_label_file_counts[labels.index(label.text)]) + ".xml"

    # Change image file path
    xml_content.find(".//filename").text = xml_dest_name.replace(".xml", ".jpg")

    # Copy xml file
    print("Copying " + xml_name + " to " + xml_dest_dir + xml_dest_name)
    xml_content.write(xml_dest_dir + str(xml_dest_name))

    return label.text


def copy_image_files(xml_name, label):
    image_src_name = xml_name.replace(".xml", ".jpg")
    image_src_dir = ORIGIN_DIR_PATH + "/images/"

    image_dest_dir = DEST_DIR_PATH + "/images/" + label + "/"
    image_dest_name = str(each_label_file_counts[labels.index(label)]) + ".jpg"

    if not os.path.exists(image_dest_dir):
        os.makedirs(image_dest_dir)

    print(
        "Copying "
        + image_src_dir
        + image_src_name
        + " to "
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

        print("")

    print("Done")


__main__()
