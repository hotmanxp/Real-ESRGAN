import os
import glob
import pyheif
from PIL import Image
import argparse

img_tmp_ext = 'jpeg'

last_trans_images = []


def list_map(list, fn):
    result = []
    for item in list:
        result.append(fn(item))
    return result


def get_file_by_path(path: str):
    index = path.rindex('/')
    return path[index + 1:]


def gen_png_from_heic(input_folder: str):

    heic_files = sorted(glob.glob(os.path.join(input_folder, '*.[hH][eE][iI][cC]')))

    for heic_img in heic_files:
        target_img_path = f'{heic_img[:-5]}.{img_tmp_ext}'
        if (os.path.exists(target_img_path)):
            print(f'Exsis File: {target_img_path}')
        else:
            img = pyheif.read_heif(heic_img)
            img_bytes = Image.frombytes(img.mode, img.size, img.data, "raw", img.mode, img.stride)
            img_bytes.save(target_img_path, format=img_tmp_ext)
        last_trans_images.append(target_img_path)


def clean_pngs_from_heic():

    global last_trans_images

    if (len(last_trans_images) == 0):
        return

    for heic_img in last_trans_images:
        if (os.path.exists(heic_img)):
            print(f'Delete File: {heic_img}')
            os.remove(heic_img)
        else:
            print(f'File: {heic_img} not exist')
    # clean list
    last_trans_images = []


def clean_by_folder(input_folder: str):
    heic_files = sorted(glob.glob(os.path.join(input_folder, '*.[hH][eE][iI][cC]')))
    png_files = sorted(glob.glob(os.path.join(input_folder, '*.[pP][nN]*[gG]')))
    for png_file in png_files:
        if ((f'{png_file[:-4]}.heic' in heic_files) or (f'{png_file[:-4]}.HEIC' in heic_files)):
            os.remove(png_file)
            print(f'Delete: {png_file}')


def remove_inferred_source(source_list: list, dist_dir: str):
    result = []
    resulted_list = sorted(glob.glob(os.path.join(dist_dir, '*.[jJpP][pPnN]*[gG]')))
    resulted_list = list_map(resulted_list, lambda item: item.lower())

    for img_src in source_list:
        img = get_file_by_path(img_src).lower()
        print(img)
        if not (f'{dist_dir.lower()}/{img}' in resulted_list):
            result.append(img_src)
        else:
            print(f'File: {img_src}, already transformed!')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, help='Input image, video or folder. Default: inputs/whole_imgs')
    parser.add_argument('-c', '--clear', type=str, help='if clear')

    args = parser.parse_args()
    if (args.clear is None):
        gen_png_from_heic(args.input_path)
    else:
        clean_by_folder(args.input_path)
