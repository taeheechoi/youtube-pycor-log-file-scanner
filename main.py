from mmap import mmap, ACCESS_READ
from glob import glob
from multiprocessing.dummy import Pool # from multiprocessing is not working 
from pathlib import Path

SOURCE_DIR = 'source' # source folder
WORDS = ['where are you?', 'pycor'] # search word


def file_list():
    # return list of files within a specific directory
    path = Path(SOURCE_DIR)
    return list(path.glob('*.log'))  # file extension log only


def find_word(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:  # open file as read mode, encoding is optional.
        with mmap(file.fileno(), length=0, access=ACCESS_READ) as mp:  # length 0 means whole file
            for word in WORDS:  # search each word in words list
                if mp.find(bytes(word, 'utf-8')) != -1:
                    return file_name, word  # return file name and first matched word


def word_search_from_source():
    results = []

    with Pool() as pool:
        results += pool.map(find_word, file_list())

    for result in results:
        if result:
            file_name, word = result
            print(file_name, word)


if __name__ == '__main__':
    word_search_from_source()
