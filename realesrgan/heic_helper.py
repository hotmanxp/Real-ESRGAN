import os
import glob
import pyheif
import piexif
import pillow_heif
from PIL import Image


img_tmp_ext = 'jpeg'

last_trans_images = []


def get_file_by_format(dir: str, formatStr: str) -> list:
    return sorted(glob.glob(os.path.join(dir, f'*.{formatStr}')))


def get_img_files(dir: str):
    return get_file_by_format(dir, '[pPjJ][nNpP]*[gG]')


def get_heic_files(dir: str):
    return get_file_by_format(dir, '[hH][eE][iI][cC]')


def get_file_by_path(file_path: str):
    return os.path.basename(file_path)


def get_name_by_file(file_name: str):
    name, _ = os.path.splitext(file_name)
    return name


def get_name_by_path(file_path: str):
    return get_name_by_file(get_file_by_path(file_path))


def trans_heic(heic_img: str):
    target_img_path = f'{heic_img[:-5]}.{img_tmp_ext}'
    img = pyheif.read_heif(heic_img)
    img_bytes = Image.frombytes(img.mode, img.size, img.data, "raw", img.mode, img.stride)
    img_bytes.save(target_img_path, format=img_tmp_ext)
    print(f'Generated file for heic: {target_img_path}')
    return target_img_path


def get_img_to_trans(input_folder: str, dist_folder: str):
    img_files = get_img_files(input_folder)
    heic_files = get_heic_files(input_folder)
    dist_files = get_img_files(dist_folder) if dist_folder is not None else []
    img_file_names = list(map(get_name_by_path, img_files))
    dist_file_names = list(map(get_name_by_path, dist_files))

    # handle heic file
    for heic_img in heic_files:
        heic_file_name = get_name_by_path(heic_img)
        if heic_file_name in dist_file_names:
            print(f'File: {heic_img}, already transformed!')
        elif heic_file_name in img_file_names:
            print(f'File: {heic_img}, already exits!')
        else:
            img_files.append(trans_heic(heic_img))

    return list(filter(lambda img: not get_name_by_path(img) in dist_file_names, img_files))


def clean_by_folder(input_folder: str):
    heic_files = get_heic_files(input_folder)
    png_files = get_img_files(input_folder)
    for png_file in png_files:
        _, extension = os.path.splitext(os.path.basename(png_file))
        if (
            (f'{png_file[:-len(extension)]}.heic' in heic_files)
                or (f'{png_file[:-len(extension)]}.HEIC' in heic_files)):
            os.remove(png_file)
            print(f'Delete: {png_file}')


def remove_inferred_source(source_list: list, dist_dir: str):
    result = []
    transformed_files = [file.lower() for file in get_img_files(dist_dir)]

    for img_src in source_list:
        img = get_file_by_path(img_src).lower()
        if f'{dist_dir.lower()}/{img}' not in transformed_files:
            result.append(img_src)
        else:
            print(f'File: {img_src}, already transformed!')
    return result


def copy_exif(img_path: str, target_img_path: str):
    if not os.path.exists(img_path):
        print(f'Not exists: {img_path}, exit')
        return

    target_img = Image.open(target_img_path)

    # Check if target image already has exif info and skip if it does
    if 'exif' in target_img.info:
        print(f'File: {target_img_path} already have exif info, skipped')
        return

    # Load the image info depending on the file type
    img = pillow_heif.read_heif(img_path) if img_path.lower().endswith('.heic') else Image.open(img_path)

    exif = piexif.load(img.info['exif'])
    target_img.save(target_img_path, exif=piexif.dump(exif))
    print(f'Sucessfully recover exif info: {target_img_path}')


def recover_exif(dist_dir: str, source_dir: str):
    imgs = get_img_files(dist_dir)
    source_imgs = get_heic_files(source_dir) + get_img_files(source_dir)

    for img in imgs:
        dist_img_name = get_name_by_path(img)
        may_have_source_list = list(filter(
            lambda src_img: (get_name_by_path(src_img) == dist_img_name),
            source_imgs))
        if len(may_have_source_list) > 0:
            copy_exif(may_have_source_list[0], img)
        else:
            print(f'Can not file source for: {img}')


if __name__ == '__main__':
    testImg = '/Users/ethan/Downloads/improve'
    testTargetImg = '/Users/ethan/Downloads/improve_resultR'
    recover_exif(testTargetImg, testImg)
