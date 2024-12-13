import pyglet
from pyglet import shapes
import math
import pygame
import pyaudio
import numpy as np
import speech_recognition as sr

def audio_proccesing(stream, chunk):
    data = stream.read(chunk, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.short)
    amplitudes = sum(np.abs(audio_data)) / len(data)

    return amplitudes

pygame.init()

screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h

window = pyglet.window.Window(width, height)
batch = pyglet.graphics.Batch()

arc = shapes.Arc(radius=25, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(0), thickness=2, color=(0, 255, 0), batch=batch)
arc_1 = shapes.Arc(radius=50, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(30), thickness=3, color=(255, 255, 0), batch=batch)
arc_2 = shapes.Arc(radius=125, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(90), thickness=4, color=(0, 255, 255), batch=batch)
arc_3 = shapes.Arc(radius=175, x=width/2 + 150, y=height/2, angle=math.radians(30), start_angle=math.radians(0), thickness=5, color=(255, 255, 255), batch=batch)
arc_4 = shapes.Arc(radius=175, x=width/2 - 150, y=height/2, angle=math.radians(-30), start_angle=math.radians(180), thickness=5, color=(255, 255, 255), batch=batch)

arc_5 = shapes.Arc(radius=175, x=width/2 + 150, y=height/2, angle=math.radians(30), start_angle=math.radians(180), thickness=5, color=(255, 255, 255), batch=batch)
arc_6 = shapes.Arc(radius=175, x=width/2 - 150, y=height/2, angle=math.radians(30), start_angle=math.radians(0), thickness=5, color=(255, 255, 255), batch=batch)

arc_7 = shapes.Arc(radius=50, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(210), thickness=3, color=(255, 255, 0), batch=batch)
arc_8 = shapes.Arc(radius=125, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(270), thickness=4, color=(0, 255, 255), batch=batch)

arc_9 = shapes.Arc(radius=25, x=width/2, y=height/2, angle=math.radians(30), start_angle=math.radians(180), thickness=2, color=(0, 255, 0), batch=batch)


image = pyglet.resource.image('hexagon.png')
sprite = pyglet.sprite.Sprite(image)
sprite.opacity = 50
sprite.scale = 1.5

p = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 16000  
FRAME_DURATION_MS = 30  
FRAME_SIZE = int(RATE * FRAME_DURATION_MS / 1000)  
PADDING_DURATION_MS = 300  

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAME_SIZE)

count = 0

recognizer = sr.Recognizer()

@window.event

def on_draw():
     window.clear()
     sprite.draw()
     batch.draw()

def update(dt):

     global count, recognizer

     # arc.angle = math.radians(random.randint(0, 360))
     # arc_1.angle = math.radians(random.randint(0, 360))
     # arc_2.angle = math.radians(random.randint(0, 360))
     # arc_3.angle = math.radians(random.randint(0, 360)) + 100
     # arc_4.angle = math.radians(random.randint(0, 360)) + 100
     

     R = round(225 * abs(math.cos(count)))
     B = round(225 * abs(math.sin(count)))

     amp = audio_proccesing(stream, 1024) // 10

     arc.rotation -= 1
     arc_1.rotation += 2
     arc_2.rotation -= 2
     arc_3.rotation += 3
     arc_4.rotation -= 3
     arc_5.rotation += 3
     arc_6.rotation -= 3
     arc_7.rotation += 2
     arc_8.rotation -= 2
     arc_9.rotation -=1
     
     arc.angle = math.radians(amp+50)
     arc_1.angle = math.radians(amp+60)
     arc_2.angle = math.radians(amp+60)
     arc_3.angle = math.radians(amp+70)
     arc_4.angle = math.radians(amp+70)
     arc_5.angle = math.radians(amp+70)
     arc_6.angle = math.radians(amp+70)
     arc_7.angle = math.radians(amp+70)
     arc_8.angle = math.radians(amp+60)
     arc_9.angle = math.radians(amp+50)

     arc.color = (B, 255, B)
     arc_1.color = (B, 255, R)
     arc_2.color = (R, 255, B)
     arc_3.color = (B, 255, R)
     arc_4.color = (R, 255, B)
     arc_5.color = (B, 255, R)
     arc_6.color = (R, 255, B)
     arc_7.color = (B, 255, R)
     arc_8.color = (R, 255, B)
     arc_9.color = (B, 255, B)



     count = count + 0.1

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()

