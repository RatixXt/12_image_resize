# -*- coding:utf-8 -*-
from PIL import Image
from os import path
import argparse


class WrongArguments(Exception):
    pass


class FileNotFound(Exception):
    pass


class NotEnoughArgs(Exception):
    pass


def argument_parsing():
    descript = '%(prog)s need for resizing image. You can resize image using only width or height of image with ' \
               'saving proportions of the original image, or you can use scale that multiply proportions of ' \
               'original image. Also you can fully determine the size of new image. If you not define output path, ' \
               'new image will be save in original directory with new size in filename.'
    parser = argparse.ArgumentParser(description=descript)
    parser.add_argument(action='store', type=str, dest='path_to_original', help='path to original image')
    parser.add_argument('--width', action='store', type=int, dest='width', help='width of new image')
    parser.add_argument('--scale', action='store', type=float, dest='scale', help='scale of image resizing')
    parser.add_argument('--height', action='store', type=int, dest='height', help='height of new image')
    parser.add_argument('--output', action='store', type=str, dest='output', help='path to result image')
    return parser.parse_args()


def load_image(filepath):
    if path.exists(filepath):
        image = Image.open(filepath)
        return image
    raise FileNotFound


def get_new_size(args, image_size):
    save_image_proportions = True
    proportion = image_size[0] / image_size[1]

    if (args.scale and args.width) or (args.scale and args.height):
        raise WrongArguments
    elif args.width and args.height:
        if args.width / args.height != proportion:
            save_image_proportions = False
        return (args.width, args.height), save_image_proportions
    elif args.width:
        return (args.width, int(args.width / proportion)), save_image_proportions
    elif args.height:
        return (int(args.height * proportion), args.height), save_image_proportions
    elif args.scale:
        return (int(image_size[0] * args.scale), int(image_size[1] * args.scale)), save_image_proportions
    raise NotEnoughArgs


def get_path_to_result(filepath, path_to_result):
    if path_to_result is not None:
        return path_to_result
    else:
        filepath_and_ext = path.splitext(filepath)
        return '{}__{}x{}{}'.format(filepath_and_ext[0], new_size[0], new_size[1],
                                   filepath_and_ext[1])

if __name__ == '__main__':
    args = argument_parsing()
    path_to_original = args.path_to_original
    try:
        image = load_image(path_to_original)
        image_size = image.size
        new_size, save_image_proportions = get_new_size(args, image_size)
    except WrongArguments:
            print(u'Error! If you using scale argument you can\'t use width or height.')
    except FileNotFound:
            print('Image not found, please, check file path.')
    except NotEnoughArgs:
            print(u'Not enough arguments.')
    else:
            if not save_image_proportions:
                print(u'Image proportions changed.')
            path_to_result = get_path_to_result(path_to_original, args.output)
            image.resize(new_size).save(path_to_result)
            print('Original image size: {}x{}'.format(image_size[0], image_size[1]))
            print('Saved new image with size:{}x{} at {}'.format(new_size[0], new_size[1], path_to_result))
            image.close()
