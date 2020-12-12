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

class Menu():
    def __init__(self, flows, statics, *bulbs):
        self.bulbs = [bulb for bulb in bulbs]
        self.bulb = bulbs[0]
        self.flows = flows
        self.flows_icons = flows_icons
        self.statics = statics
        self.comandos_de_voz = {'fiat lux' : self.bulb.turn_on, 'good night' : self.bulb.turn_off, 'toggle' : self.bulb.toggle}
        self.botoes_flow = [wdg.Button(description=word, layout=wdg.Layout( width='auto' ), button_style='warning', icon=self.flows_icons[word]) for word in self.flows.keys()]
        self.botoes_cores = [wdg.Button(description='', tooltip=word, layout=wdg.Layout(width='50%', height='90%'), style= {'button_color': rgb2hex(*map(lambda x : int(x), corgb)), 'font_weight' : 'normal'}) for word, corgb in self.statics.items()]
        self.botao_voz = wdg.Button(
                                    #description='Controle de voz',
                                    disabled=False,
                                    button_style='warning',
                                    tooltip="Controle de voz\n----------------\nComandos:\n----------------\n'Fiat lux'\n'Toggle'\n'Good night'",
                                    icon='microphone',    # (FontAwesome names without the `fa-` prefix)
                                    layout=wdg.Layout(width='50%', height='80%')
                                    )
        self.botao_toggle = wdg.ToggleButton(
                                    value=False,
                                    #description='',
                                    disabled=False,
                                    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
                                    tooltip='Toggle',
                                    #border = 'dashed',
                                    icon='power-off',      # (FontAwesome names without the `fa-` prefix)
                                    layout=wdg.Layout(width='50%', height='90%'))
        self.botao_renomear = wdg.Button(
                                    description='Renomear dispositivo',
                                    disabled=False,
                                    button_style='info',
                                    tooltip='Mude este nome!',
                                    icon='',
                                    layout=wdg.Layout(width='50%', height='90%')
                                    )
        self.slider = wdg.IntSlider(min=1, max=100, value=50, description='', continuous_update=False,
                                    orientation='vertical',
                                    readout=True)
        self.slider.style.handle_color = 'red'
        
        self.box_cores = wdg.HBox(self.botoes_cores)
        self.box_header = wdg.VBox([wdg.HBox([self.botao_toggle, self.botao_voz, self.botao_renomear]), self.box_cores])
        self.box_flow = wdg.Box(children=self.botoes_flow, layout= wdg.Layout(#display='flex',
                                                                                flex_flow='column',
                                                                                align_items='stretch',
                                                                                border='ridge',
                                                                                width='90%'))
        #self.box_cores = wdg.Box(children=self.botoes_cores, layout= wdg.Layout(#display='flex',
         #                                                                       flex_flow='column',
          #                                                                      align_items='stretch',
           #                                                                     border='ridge', #groove
            #                                                                    width='90%'
             #                                                                   ))
        self.paleta_cores = wdg.ColorPicker(
                                            concise=True,
                                            description='',
                                            value='#efefef',
                                            height='100%',
                                            width='75%'
                                            )
        # Atribui a cada botão uma ação
        self.slider.observe(self.slider_brilho_handler)
        self.botao_toggle.observe(self.menu_toggle_handler)
        self.botao_renomear.on_click(self.menu_renomear_handler)
        self.botao_voz.on_click(self.menu_voz_handler)
        self.observa_botoes(self.botoes_flow, self.menu_flow_handler)
        self.observa_botoes(self.botoes_cores, self.menu_cores_handler)
        self.paleta_cores.observe(self.menu_paleta_handler)
        # ===============================================================

    def observa_botoes(self, botoes, handler):
        for botao in botoes:
            botao.on_click(handler)
                                  
    def slider_brilho_handler(self, botao):
        if botao['name'] == 'value':
            if botao['new'] <= 100:
                for bulb in self.bulbs:
                    bulb.set_brightness(botao['new'])
        
    def menu_toggle_handler(self, botao):
        for bulb in self.bulbs:
            bulb.toggle()
        
    def menu_cores_handler(self, botao):
        try:
            for bulb in self.bulbs:
                if silent == False:
                    toca_acorde(rgb2chord(statics[botao.tooltip]), 1.5)  # Toca acorde pela biblioteca synthesizer
                bulb.set_rgb(*statics[botao.tooltip])
                
        except:
            print("A conexão com a lâmpada foi encerrada.\nReconectando...")
            
    def menu_flow_handler(self, botao):
        flow = self.flows[botao.description]
        try:
            for bulb in self.bulbs:
                bulb.start_flow(flow)
        except:
            print("A conexão com a lâmpada foi encerrada.\nReconectando...")
                
    def menu_voz_handler(self, comandos):
        resultado = reconhece_voz()
        if resultado != -1:                                 # Se não houve nenhuma exceção
            if resultado in self.comandos_de_voz:
                self.comandos_de_voz[resultado]()
            else:
                print("Comando não reconhecido.")
    
    def menu_renomear_handler(self, botao):
        novo_nome = wdg.Textarea(
                                value=self.bulbs[0].get_properties()['name'],
                                placeholder='Escolha um novo nome para o seu dispositivo!',
                                description='',
                                disabled=False,
                                continuous_update=False
                                )
        display(novo_nome)
        def value_changed(change):
            if self.bulbs[0].get_properties()['name'] is not None:
                if self.bulbs[0].get_properties()['name'].lower() != change.new.lower():
                    self.bulbs[0].set_name(change.new)
                    print("Dispositivo renomeado com sucesso.")
                else: print("Entre com um nome diferente de {}".format(change.new))
            else: 
                try:
                    self.bulb.set_name(change.new)
                    print("Dispositivo renomeado com sucesso.")
                except:
                    print("Falha ao renomear o dispositivo.")
            
        novo_nome.observe(value_changed, 'value')

    def menu_paleta_handler(self, botao):
        if botao['name'] == 'value':
            cor_atual_rgb = tuple(int(botao['new'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            #cor_atual_rgb = colour.hex2rgb(botao['new'])
            #print(botao['new'])
            #print(cor_atual_rgb)
            for bulb in self.bulbs:
                bulb.set_rgb(*cor_atual_rgb)
            
    def piano_keyboard(self):
        chunks = range(0,len(self.botoes_cores),7)
        black_tile = wdg.Button(description='', tooltip='black', layout=wdg.Layout(width='1%', height='15%'), style= {'button_color': '#000000', 'font_weight' : 'normal'})
        piano_keyboard = []
        for i in chunks:                                     
            chunk = self.botoes_cores[i:i+7]                 # Separa grupos de oitavas
            for tile in chunk:
                if (chunk.index(tile) + 1) not in [3, 7]:    # Acidentes semitonais
                    piano_keyboard.append(tile)
                    piano_keyboard.append(black_tile)
                else:
                    piano_keyboard.append(tile)
        return piano_keyboard

    
class App():
    def __init__(self, menu, header_button=None, left_button=None, center_button=None, right_button=None, footer_button=None):
        self.menu = menu
        self.header_button = header_button
        self.left_button = left_button
        self.center_button = center_button
        self.right_button = right_button
        self.footer_button = footer_button
        
    def layout(self):
        return wdg.AppLayout(   header=self.header_button,
                                left_sidebar=self.left_button,
                                center=self.center_button,
                                right_sidebar=self.right_button,
                                footer=self.footer_button,
                                #height="200px", width="50%",
                                grid_gap='45px',
                                justify_items='center', 
                                align_items='center', # 'flex-start', 'baseline', 'stretch'
                                pane_widths=[1, 1, 1],
                                pane_heights=[1, 5, 1] #[1, 5, '60px']
                            )