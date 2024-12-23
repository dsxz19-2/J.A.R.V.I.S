import glfw
from OpenGL.GL import *
import numpy as np
import pyaudio
import time
from scipy.fftpack import fft

# Credits to
# https://www.youtube.com/watch?v=f4s1h2YETNY
# https://www.youtube.com/playlist?list=PLi-ukGVOag_2FRKHY5pakPNf9b9KXaYiD
# https://www.shadertoy.com/view/4tGXzt

# Class to handle audio input and processing
class AudioCapture:
    # Initialize PyAudio for capturing audio
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16, # 16-bit audio
            channels=1, # Mono audio
            rate=16000, # Sample rate of 16kHz
            input=True, # Enable input (microphone)
            frames_per_buffer=1024 # Buffer size
        )
        
    def get_audio_data(self):
        # Capture audio data and convert to numpy array
        self.data = self.stream.read(1024)
        self.audio_data = np.frombuffer(self.data, dtype=np.int16)
        return self.audio_data

    def close(self):
        # Stop and close the audio stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Function to create an OpenGL texture from audio data
def create_texture_from_audio(audio_data):
    # Normalize the audio data to the range [0.0, 1.0]
    # Random testing reveled, devide by 32768.0 to make the final product less sensative 
    audio_data = np.clip(audio_data / 32768.0, 0.0, 1.0)
    texture_data = np.repeat(audio_data[:, np.newaxis], 3, axis=1)  # Convert to RGB format
    texture_data = np.tile(texture_data, (1, 1, 3))  # Repeat data to fill texture and for OpenGL texture compatibility

    # Generate and bind OpenGL texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_data.shape[1], texture_data.shape[0], 0, GL_RGB, GL_FLOAT, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

# Compile a shader from source code
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode('utf-8'))
    return shader

# Link vertex and fragment shaders into a shader program
def create_program(vertex_source, fragment_source):
    program = glCreateProgram()
    vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program).decode('utf-8'))
    
    # General Cleanup
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

# Main function to run the visualizer
def main():

    # Vertex shader code
    vertex_shader_code = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    void main()
    {
        gl_Position = vec4(aPos, 1.0);
    }
    """

    # Fragment Shader code
    fragment_shader_code = """
    #version 330 core
    #define BEATMOVE 1

    const float FREQ_RANGE = 128.0;
    const float PI = 3.1415;
    const float RADIUS = 0.5;
    const float BRIGHTNESS = 0.15;
    const float SPEED = 0.5;

    uniform sampler2D iChannel0;
    uniform vec2 iResolution;
    uniform float iTime;
    uniform float uAmplitude;

    //convert HSV to RGB
    vec3 hsv2rgb(vec3 c){
        vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
    }

    float luma(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
    }

    float getfrequency(float x) {
        return texture(iChannel0, vec2(floor(x * FREQ_RANGE + 1.0) / FREQ_RANGE, 0.25)).x + 0.06;
    }

    float getfrequency_smooth(float x) {
        float index = floor(x * FREQ_RANGE) / FREQ_RANGE;
        float next = floor(x * FREQ_RANGE + 1.0) / FREQ_RANGE;
        return mix(getfrequency(index) * 10, getfrequency(next) * 10, smoothstep(0.0, 1.0, fract(x * FREQ_RANGE)));
    }

    float getfrequency_blend(float x) {
        return mix(getfrequency(x), getfrequency_smooth(x), 0.5);
    }

    vec3 doHalo(vec2 fragment, float radius) {
        float dist = length(fragment);
        float ring = 1.0 / abs(dist - radius);
        
        float b = dist < radius ? BRIGHTNESS * 0.3 : BRIGHTNESS;
        
        vec3 col = vec3(0.0);
        
        float angle = atan(fragment.x, fragment.y);
        col += hsv2rgb( vec3( ( angle + iTime * 0.25 ) / (PI * 2.0), 1.0, 1.0 ) ) * ring * b;
        
        float frequency = max(getfrequency_blend(abs(angle / PI)) - 0.02, 0.0);
        col *= frequency;
        
        // Black halo
        col *= smoothstep(radius * 0.5, radius, dist);
        
        return col;
    }

    vec3 doLine(vec2 fragment, float radius, float x) {
        vec3 col = hsv2rgb(vec3(x * 0.23 + iTime * 0.12, 1.0, 1.0));
        
        float freq = abs(fragment.x * 0.5);
        
        col *= (1.0 / abs(fragment.y)) * BRIGHTNESS * getfrequency(freq);	
        col = col * smoothstep(radius, radius * 1.8, abs(fragment.x));
        
        return col;
    }


    void main() {
        vec2 fragPos = gl_FragCoord.xy / iResolution.xy;
        fragPos = (fragPos - 0.5) * 2.0;
        fragPos.x *= iResolution.x / iResolution.y;
        
        vec3 color = vec3(0.0134, 0.052, 0.1);
        color += doHalo(fragPos, RADIUS);

        float c = cos(iTime * SPEED);
        float s = sin(iTime * SPEED);
        vec2 rot = mat2(c,s,-s,c) * fragPos;
        color += doLine(rot, RADIUS, rot.x);
        
        color += max(luma(color) - 1.0, 0.0);
        
        gl_FragColor = vec4(color, 1.0);
    }
    """

    # Initialize GLFW for window management
    if not glfw.init():
        raise Exception("GLFW could not be initialized!")

    # Use the primary monitor and get its video mode for fullscreen
    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    window = glfw.create_window(mode.size.width, mode.size.height, "Audio Visualizer", monitor, None)

    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created!")

    # Set up OpenGL context
    glfw.make_context_current(window)
    glViewport(0, 0, mode.size.width, mode.size.height)
    glClearColor(0, 0, 0, 1)

    # Compile shaders and create a shader program
    program = create_program(vertex_shader_code, fragment_shader_code)
    glUseProgram(program)

    # Define the screen-filling quad (vertices)
    vertices = np.array([
        -1.0, -1.0, 0.0,
        1.0, -1.0, 0.0,
        -1.0,  1.0, 0.0,
        1.0, -1.0, 0.0,
        1.0,  1.0, 0.0,
        -1.0,  1.0, 0.0,
    ], dtype=np.float32)

    # Create and bind OpenGL vertex array and buffer objects
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Initialize audio capture
    audio_capture = AudioCapture()
    start_time = time.time()

    # Main rendering loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Capture audio data and create a texture
        audio_data = audio_capture.get_audio_data()
        texture_id = create_texture_from_audio(audio_data)

        # Bind the texture for rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Pass uniforms to the shader program
        glUseProgram(program)
        glUniform1i(glGetUniformLocation(program, "iChannel0"), 0)
        glUniform2f(glGetUniformLocation(program, "iResolution"), mode.size.width, mode.size.height)
        glUniform1f(glGetUniformLocation(program, "iTime"), time.time() - start_time)

        # Clear the screen and draw the quad
        glClear(GL_COLOR_BUFFER_BIT)

        # Swap front and back buffers
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    # Cleanup resources
    audio_capture.close()
    glfw.terminate()


main()



