# users/picture_handler.py
import os
import secrets

# -*- coding: utf-8 -*-
from PIL import Image
from flask import current_app, url_for


def add_profile_pic(pic_file, username):
    """
    Adds a profile username to  picture and saves it
    """
    filename = pic_file.filename
    _, f_ext = os.path.splitext(filename)
    picture_fn = str(username) + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(pic_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
