#!/usr/bin/env python

# Python imports.
# import cv2
import time
import os
import random
from collections import defaultdict

# Other imports.
# from detect import detect_markers
# from button import *
from generate_poem import generate_poem_line_from_markov_model
from make_model import load_count_dict
from save_object_words import load_object_dict
# import pygame
# pygame.mixer.init()

# capture = cv2.VideoCapture(0)

# def _play_sound(note):
#     pygame.mixer.music.load("sounds/" + note + ".wav")
#     pygame.mixer.music.play()

def _check_for_markers():
    '''
    Returns:
        (list): Contains PhysicalObject instances.

    Summary:
        Activates the camera and looks for AR tags
    '''

    if capture.isOpened():
        frame_captured, frame = capture.read()
    else:
        frame_captured = False

    (thresh, im_bw) = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    tries = 0
    while frame_captured and tries < 10:
        markers = detect_markers(im_bw)
        if len(markers) > 0:
            return markers
        for marker in markers:
            marker.highlite_marker(im_bw)
        cv2.imshow('Test Frame', im_bw)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, im_bw = capture.read()

        tries += 1

    return []

def get_objects_in_scene(object_dict):
    '''
    Args:
        object_dict (dict): Contains PhysicalObjects to look for.

    Returns:
        (list): Containing any detected PhysicalObject items in the scene.
    '''
    markers = _check_for_markers()
    obj_list = []

    for m in markers:
        obj_list.append(object_dict[m.id])

    return obj_list


def button_pressed(object_dict, markov_models, should_print=False):
    '''
    Args:
        object_dict (dict)
        markov_models (list)
        should_print (bool)

    Summary:
        Scans the image from global:@capture and generates a poem based on
        the detected objects and the given @markov_models. Saves the poem to
        "poem.txt".
    '''
    
    # Get objects in scene.
    # objects_in_scene = get_objects_in_scene(object_dict)
    objects_in_scene = [random.choice(object_dict.values())]
    
    if len(objects_in_scene) > 0:
        print("Detected:",) 
        for o in objects_in_scene:
            print(o.name,)
            # _play_sound(o.get_note())

    # Generate poem.
    poem_str = "\n" + ("~"*10) + "\n"
    num_lines = random.choice([1,2,2,2,3,3,3,3,4,4,4,5,5,6,7,8])
    for i in range(num_lines):
        poem_str += generate_poem_line_from_markov_model(markov_models, objects_in_scene) + "\n"
    poem_str += "~"*10 + "\n\n\n"
    
    out_file = open("poem.txt", "w+")
    out_file.write(poem_str)
    out_file.close()

    if should_print:
        print(poem_str)
        # time.sleep(min(2 * num_lines, 4))

    # Send to printer.
    # os.system("lpr poem.txt -P Welquic")
    
if __name__ == '__main__':

    # Setup object dict and markov model.
    unigram_model = load_count_dict(model_name="unigram")
    bigram_model = load_count_dict(model_name="bigram")
    trigram_model = load_count_dict(model_name="trigram")
    fourgram_model = load_count_dict(model_name="fourgram")
    fivegram_model = load_count_dict(model_name="fivegram")

    markov_models = [unigram_model, bigram_model, trigram_model, fourgram_model, fivegram_model]
    object_dict = load_object_dict()
    
    # button = Button(10)

    print "Ready!"
    done = False
    while not done:

        # if button.is_pressed():
        poem = button_pressed(object_dict, markov_models, should_print=True)
        
        # Wait for nex round
        # time.sleep(0.2)

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
