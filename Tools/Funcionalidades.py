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


def define_tom(num):
    def tom(num):
        if 0 <= num <= 36: return 'A'
        if 36 < num <= 72: return 'B'
        if 72 < num <= 108: return 'C'
        if 108 < num <= 144: return 'D'
        if 144 < num <= 180: return 'E'
        if 180 < num <= 216: return 'F'
        if 216 < num <= 255: return 'G'
    letra = tom(num)
    def altura(octave):
        if 0 <= octave <= 6: return 2
        if 6 < octave <= 12: return 3
        if 12 < octave <= 18: return 4
        if 18 < octave <= 24: return 5
        if 24 < octave <= 30: return 6
        if 30 < octave <= 36: return 7
    numero = altura(num%37)
    return letra + str(numero)

def toca_acorde(chord, tempo):
    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=0.4, use_osc2=True) # Waveform.sawtooth, Waveform.sine, Waveform.square, Waveform.triangle 
    # Play A4
    #player.play_wave(synthesizer.generate_constant_wave(440.0, 1.5))
    #chord = ["C7","E7","G7"]
    player.play_wave(synthesizer.generate_chord(chord, tempo))

def rgb2chord(rgb_tuple):
    return [define_tom(num) for num in rgb_tuple]

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def escolhe_flow(preset):    
    flow = Flow(count=0,                                                        #Roda flow indefinidamente (até comando stop_flow() ou turn_off())
            transitions=preset)
    return flow
        
def escada(span, teto):                                                         #Utilizar span máximo de 4*teto
    escadaria = list()
    for i in range(span):
        if i < teto:
            escadaria.append(i%teto+1)
        if i > teto and i < 2*teto:
            escadaria.append(((teto-1)-i)%teto+1)
        if i > 2*teto and i < 3*teto:
            escadaria.append(i%teto+1)
        if i > 3*teto and i < 4*teto:
            escadaria.append(((3*teto-1)-i)%teto+1)        
    return escadaria

def reconhece_voz():
    r = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            print("Iniciando reconhecimento...")
            r.adjust_for_ambient_noise(source)
            time.sleep(.250)
            print("Fale!")
            audio = r.listen(source)
            transcript = r.recognize_google(audio)
            return transcript.lower()
    except sr.UnknownValueError:
        print("Falha no reconhecimento de voz.")
        return -1
    except sr.RequestError:
        print("API fora do ar.")
        return -1

def main():
    dispositivos = dispositivos_na_rede()
    if len(dispositivos) > 1:
        menu_master = Menu(flows, statics, *dispositivos)
        menus_individuais = [Menu(flows, statics, dispositivo) for dispositivo in dispositivos]
        menus = (*menus_individuais, menu_master)
    else:
        menus = [Menu(flows, statics, dispositivo) for dispositivo in dispositivos]
    apps = [App(menu,header_button=menu.box_header,
                     left_button=menu.box_flow,
                     center_button=menu.slider,
                     right_button=menu.paleta_cores
                     #footer_button=menu.box_cores
               )
            for menu in menus]
    tabs = wdg.Tab()
    children = [app.layout() for app in apps]
    tabs.children = children
    for i in range(len(dispositivos)):
        tabs.set_title(i, dispositivos[i].get_properties()['name'])
    tabs.set_title(len(dispositivos), "Master")
    display(tabs)
    return apps, menus