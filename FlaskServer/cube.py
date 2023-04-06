import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft, ifft
from scipy.ndimage import gaussian_filter1d

from stl import mesh

emotion_settings = {
    "sadness":{
        "width":    64,
        "depth":    0.3,
        "height":   0.0,
        "smooth":   2,
        "curve":    1,
        "highpass": 0,
        "lowpass":  0.35,
        "noise":    0
    },
    "joy":{
        "width":    100,
        "depth":    0.3,
        "height":   0.0,
        "smooth":   1,
        "curve":    0.8,
        "highpass": 0,
        "lowpass":  0,
        "noise":    0
    },
    "fear":{
        "width":    100,
        "depth":    0.3,
        "height":   0.0,
        "smooth":   0,
        "curve":    1,
        "highpass": 0,
        "lowpass":  0.82,
        "noise":    0
    },
    "disgust":{
        "width":    64,
        "depth":    0.3,
        "height":   0.0,
        "smooth":   1,
        "curve":    0.7,
        "highpass": 0,
        "lowpass":  0,
        "noise":    0.12
    },
    "anger":{
        "width":    64,
        "depth":    0.3,
        "height":   0.0,
        "smooth":   0,
        "curve":    0.8,
        "highpass": 0.3,
        "lowpass":  0,
        "noise":    0.14
    }
}

def scale_array(arr, upper=1, lower=0):
    max_val = np.max(arr)
    min_val = np.min(arr)
    scaled_arr = (arr - min_val) * (upper - lower) / (max_val - min_val) + lower
    return scaled_arr

def audio_to_amplitude(location):
    with open(location):
        pass

def sub_sample_point(all_samples, num_points):
    sub_samples = [] # Make array of smaller sample points
    length = len(all_samples)
    for x in range(length//(num_points-1), length, length//(num_points)):
        sub_samples.append(all_samples[x])
    return sub_samples

def sub_sample_rolling(all_samples, num_points):
    sub_samples = [] # Make array of smaller sample points
    length = len(all_samples)
    i = 0
    for next in range(length//(num_points-1), length, length//(num_points)):
        sum = 0
        num = 0
        while i < next:
            sum += all_samples[i]
            num += 1
            i += 1
        sub_samples.append(sum/num) # Assume floats are okay

    return sub_samples

def gen_faces(size):
    n1 = size[0]
    n2 = size[1]
    faces = []

    # Bottom
    for x in range(n1-1):
        for y in range(n2-1):
            v0 = y + x*n2
            v1 = y + x*n2 + n2
            v2 = y + x*n2 + 1
            v3 = y + x*n2 + 1 + n2

            faces.append([v1, v0, v2])
            faces.append([v1, v2, v3])
    
    # Top
    for x in range(n1-1):
        for y in range(n2-1):
            v0 = y + n1*n2 + x*n2
            v1 = y + n1*n2 + x*n2 + n2
            v2 = y + n1*n2 + x*n2 + 1
            v3 = y + n1*n2 + x*n2 + 1 + n2

            faces.append([v1, v2, v0])
            faces.append([v1, v3, v2])

    # Front
    for i in range(n1-1):
        v0 = n2 *  i
        v1 = n2 * (i+1)
        v2 = n2 *  i    + n1*n2
        v3 = n2 * (i+1) + n1*n2

        faces.append([v1, v2, v0])
        faces.append([v1, v3, v2])

    # Back
    for i in range(n1-1):
        v0 = n2 *  i            + n2-1
        v1 = n2 * (i+1)         + n2-1
        v2 = n2 *  i    + n1*n2 + n2-1
        v3 = n2 * (i+1) + n1*n2 + n2-1

        faces.append([v1, v0, v2])
        faces.append([v1, v2, v3])

    # Left
    for i in range(n2-1):
        v0 = i
        v1 = i + 1
        v2 = i     + n1*n2
        v3 = i + 1 + n1*n2

        faces.append([v1, v0, v2])
        faces.append([v1, v2, v3])
            
    # Right
    for i in range(n2-1):
        v0 = i             + n2*(n1-1)
        v1 = i + 1         + n2*(n1-1)
        v2 = i     + n1*n2 + n2*(n1-1)
        v3 = i + 1 + n1*n2 + n2*(n1-1)

        faces.append([v1, v2, v0])
        faces.append([v1, v3, v2])
    
    return faces


def generate_cube(
        wav, 
        mesh_name, 
        width=128,
        depth=0.3,

        height=0.3,
        smooth=3,
        curve=1,
        highpass=0,
        lowpass=0,
        noise=0

        ):
    depth = int(width*depth)
    width = int(width)
    smooth = round(smooth)
    num_points = width
    n1 = width
    n2 = depth

    # Generate Amplitude
    fs, amp = read(wav)
    if type(amp[0]) in (list, np.ndarray):
        amp = [sample[0] for sample in amp] # Force mono (could blend, but would likely have little effect)
    freq = fft(amp)
    for i, c in enumerate(freq):
        if c/len(freq) < highpass:
            freq[i] = 0

    for i, c in enumerate(freq):
        if c/len(freq) > 1-lowpass:
            freq[i] = 0
    amp = ifft(freq)

    # small patch for incorrect number of points:
    amplitude = sub_sample_point(amp, num_points)
    freqencies = sub_sample_point(freq, num_points)
    if len(amplitude) < num_points:
        amplitude = sub_sample_point(amp, num_points+1)
        freqencies = sub_sample_point(freq, num_points+1)

    points = amplitude

    # Pre Process Effects
    # Sacle
    points = scale_array(points, upper=1, lower=height)
    # Blur
    if smooth != 0:
        points = gaussian_filter1d(points, smooth)

    # Height Map Adjustments
    all_heights = []
    # Sample Heights
    point_height = []
    for x in range(n1):
        line = []
        for y in range(n2):
            line.append(points[x])
        point_height.append(line)
    all_heights.append(point_height)

    # Curve
    point_height = []
    for x in range(n1):
        line = []
        for y in range(n2):
            line.append(np.cos(((y/((n2-1)*2)) - 0.5) * curve * np.pi))
        point_height.append(line)
    all_heights.append(point_height)

    # Noise
    all_heights.append(np.random.rand(n1, n2) * noise)


    # Average Heights
    point_height = np.mean(np.array(all_heights), axis=0)
    
    vertices = []
    # Bottom faces of the cube
    for x in range(n1):
        for y in range(n2):
            vertices.append([x/(n1-1),y/(n1-1),0])

    # Top of the cube is an NxN
    for x in range(n1):
        for y in range(n2):
            vertices.append([x/(n1-1),y/(n1-1),point_height[x][y]])

    faces = gen_faces((width,depth))

    # Convert Format
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Save and output
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save(mesh_name)

    print("Done")


def emotion_cube(wav, mesh_name, emotion_set):
    
    weighted_average = {}
    # Initilise to 0
    for i in emotion_settings["joy"]:
        weighted_average[i] = 0
    
    number_of_emotions = 0.0001 # Avoid divide by zero
    for emotion in emotion_set:
        number_of_emotions += emotion_set[emotion]
        for val in emotion_settings[emotion]:
            weighted_average[val] += emotion_settings[emotion][val]*emotion_set[emotion]

    for val in weighted_average:
        weighted_average[val] /= number_of_emotions
    print(weighted_average)
    generate_cube(wav, mesh_name, **weighted_average)

    #top_emotion = max(emotion, key=emotion.get)
    #generate_cube(wav, mesh_name, **setattr[top_emotion])


if __name__ == "__main__":
    generate_cube("FlaskServer/test_files/test_happy.wav", "cube.stl")
    print("fin")