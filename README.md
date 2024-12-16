# J.A.R.V.I.S - Inspired by Conspet Bytes
Youtube: https://www.youtube.com/@concept_bytes
Instagram: https://www.instagram.com/concept_bytes/?hl=en

This J.A.R.V.I.S is made using the Gemini API. It will be made to mimic Jarvis from the Ironman movies. It will be able to understand human speech and respond with intelligent answers to your questions with many more features yet to come. 
I am making this project specifically to fit my needs as I work, so some of its features may be too niche for others, such as the 3D rendering part (coming soon) or the circuit design element (also coming soon). 

## Visualizer 
The visualizer is purely for aesthetic purposes and will help show when you or Jarvis are speaking. Version 1 uses **pygame** to make a window with a few arcs that change length depending on when the sound is detected. It probably will be changed to something else because it doesn't look too great

## Visualizer Update
The visualizer has been updated. It now uses OpenGL in Python to make better faster and better visuals. Credits to https://www.youtube.com/watch?v=f4s1h2YETNY, https://www.youtube.com/playlist?list=PLi-ukGVOag_2FRKHY5pakPNf9b9KXaYiD and https://www.shadertoy.com/view/ls3BDH, where I learned how to use this program and where I used the shader code. You shadertoy.com to find other shaders and paste them into shader.py where the original fragment_shader_code is.

## Hand Gesture Control
This feature allows you to control the mouse cursor with your hands. The cursor is bound to your index finger, and the program uses the distance between your fingertips to identify clicks. Besides being cool, this could possibly be used to interact with 3D models that would ideally be projected onto my desk (code for rendering 3D models coming soon). 

## 3D Rendering
The 3D rendering feature is now complete. Soon, J.A.R.V.I.S will be able to render STL files and project them onto my desk, and I'll be able to visualize them in the real world with a more accurate scale. (I still have to implement this into the jarvis.py file; I'm probably going to get to that after school's finished.)
