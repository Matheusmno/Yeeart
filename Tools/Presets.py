from yeelight import *
from Funcionalidades import *
from yeelight import transitions
from yeelight import Flow
from yeelight import Bulb
import yeelight as yl
import speech_recognition as sr
import ipywidgets as wdg
import math
import time
import colour
from colour import Color
from pprint import pprint
import synthesizer as synth
from synthesizer import Player, Synthesizer, Waveform
from Classes import *
from Presets import *


def police3(duration=200, brightness=70):
    transitions = [
        RGBTransition(255, 0, 0, brightness=brightness, duration=duration),
        RGBTransition(200, 0, 0, brightness=1, duration=duration),
        RGBTransition(145, 0, 0, brightness=brightness, duration=duration),
        SleepTransition(duration=duration),
        RGBTransition(0, 0, 255, brightness=brightness, duration=duration),
        RGBTransition(0, 0, 200, brightness=1, duration=duration),
        RGBTransition(0, 0, 145, brightness=brightness, duration=duration),
        SleepTransition(duration=duration),
                   ]
    return transitions

def tranquilao(duration_light=5000, duration_sleep=500, brightness=49):
    transitions = [
        RGBTransition(255, 233, 207, brightness=brightness, duration=duration_light),
        SleepTransition(duration=duration_sleep),
        RGBTransition(201, 170, 136, brightness=brightness, duration=duration_light),
        SleepTransition(duration=duration_sleep),
        RGBTransition(74, 112, 139, brightness=brightness, duration=duration_light),
        SleepTransition(duration=duration_sleep),
        RGBTransition(226, 231, 186, brightness=brightness, duration=duration_light),
        SleepTransition(duration=duration_sleep),
        RGBTransition(255, 0, 38, brightness=brightness, duration=duration_light)
                   ]
    return transitions 

def psyched(duration_light=1229, duration_sleep=4500, brightness=27):
    transitions = [
        RGBTransition(255, 94,  27, brightness=brightness, duration=duration_light),
        RGBTransition(107, 255, 107, brightness=27, duration=690),
        RGBTransition(27,  151, 255, brightness=36, duration=duration_light),
        RGBTransition(107, 255, 80, brightness=brightness, duration=duration_light),
        SleepTransition(duration=duration_sleep),
        RGBTransition(255, 52,  224, brightness=brightness, duration=1500),
        RGBTransition(175, 119, 255, brightness=36, duration=duration_light),
        RGBTransition(228, 255, 163, brightness=27, duration=1000),
        RGBTransition(255, 0, 0, brightness=brightness, duration=2000)
                   ]
    return transitions 

def crazy_train(hue_max=359, saturation=100, duration=500):
    return [HSVTransition(hue, saturation=saturation, duration=duration) for hue in range(0, hue_max, math.ceil(hue_max/9))]

def come_down(duration):
    return [RGBTransition(0,195,111, brightness=1, duration=550),
            RGBTransition(0,180,132, brightness=1, duration=duration)]

def mobbin(duration_light=8500, duration_sleep=2300, brightness=12):
    return [RGBTransition(118, 52, 37, brightness=brightness, duration=duration_light),
            SleepTransition(duration=duration_sleep),
            RGBTransition(146, 83, 13, brightness=6, duration=duration_light),
            SleepTransition(duration=duration_sleep),
            RGBTransition(192, 106, 106, brightness=brightness, duration=duration_light),
            SleepTransition(duration=duration_sleep),
            RGBTransition(213, 33, 142, brightness=brightness, duration=duration_light),
            SleepTransition(duration=duration_sleep)]

def RedRedWine(brightness=100, duration_light=1000):
    return [RGBTransition(210, 0, 2, brightness=brightness, duration=440),
            RGBTransition(243, 0, 2, brightness=brightness, duration=440),
            RGBTransition(254, 2, 0, brightness=brightness, duration=duration_light),
            RGBTransition(233, 2, 0, brightness=69, duration=duration_light),
            RGBTransition(209, 0, 2, brightness=69, duration=duration_light),
            RGBTransition(148, 0, 2, brightness=40, duration=duration_light),
            RGBTransition(111, 0, 0, brightness=10, duration=duration_light),
            RGBTransition(52, 0, 0, brightness=5, duration=440),
            RGBTransition(42, 0, 0, brightness=brightness, duration=440)]

def Meditation(brightness=11, duration_light=10000):
    return [RGBTransition(122, 129, 255, brightness=brightness, duration=5000),
            RGBTransition(0, 255, 255, brightness=brightness, duration=4000),
            RGBTransition(0, 144, 81, brightness=brightness, duration=duration_light),
            RGBTransition(122, 129, 255, brightness=5, duration=duration_light),
            RGBTransition(0, 255, 255, brightness=4, duration=duration_light),
            RGBTransition(0, 144, 81, brightness=3, duration=duration_light),
            RGBTransition(77, 255, 41, brightness=1, duration=duration_light),
            RGBTransition(22, 0, 12, brightness=3, duration=4400),
            RGBTransition(0, 25, 255, brightness=brightness, duration=5500)]