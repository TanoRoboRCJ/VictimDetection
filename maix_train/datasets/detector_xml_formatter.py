ORIGIN_DIR_PATH = './DAMMY'
DEST_DIR_PATH = './DAMMY_FORMATTED'

import os

def create_dest_dir():
    if os.path.exists(DEST_DIR_PATH):
        print('Directory {DEST_DIR_PATH} already exists. Data will be deleted.')
        should_continue = input('Do you want to continue? [yes/no]: ')

        while should_continue.lower() not in ['yes', 'no']:
            should_continue = input('Please enter yes or no: ')
        
        if should_continue.lower() == 'no':
            print('Exiting...')
            exit()
        
        print('Deleting directory...')
        os.rmdir(DEST_DIR_PATH)
    
    os.makedirs(DEST_DIR_PATH)
        


def __main__():
    create_dest_dir()
    print('Done')

__main__()