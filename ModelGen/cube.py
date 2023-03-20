import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft
import matplotlib.pyplot as plt

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

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


def generate_cube(points):
    n = len(points)
    p = scale_array(points, upper=1, lower=0.3)
    vertices = []

    # Bottom faces of the cube
    for x in range(n):
        for y in range(n):
            vertices.append([x/(n-1),y/(n-1),0])

    # Top of the cube is an NxN
    for x in range(n):
        for y in range(n):
            vertices.append([x/(n-1),y/(n-1),p[x]])

    faces = []

    # Top
    for x in range(n-1):
        for y in range(n-1):
            v0 = y*n + x
            v1 = y*n + x + n
            v2 = y*n + x + 1
            v3 = y*n + x + 1 + n

            faces.append([v1, v0, v2])
            faces.append([v1, v2, v3])
    
    # Bottom
    for x in range(n-1):
        for y in range(n-1):
            v0 = y*n + n*n + x
            v1 = y*n + n*n + x + n
            v2 = y*n + n*n + x + 1
            v3 = y*n + n*n + x + 1 + n

            faces.append([v1, v2, v0])
            faces.append([v1, v3, v2])

    # Front
    for i in range(n-1):
        v0 = n *  i
        v1 = n * (i+1)
        v2 = n *  i    + n*n
        v3 = n * (i+1) + n*n

        faces.append([v1, v2, v0])
        faces.append([v1, v3, v2])

    # Back
    for i in range(n-1):
        v0 = n *  i          + n-1
        v1 = n * (i+1)       + n-1
        v2 = n *  i    + n*n + n-1
        v3 = n * (i+1) + n*n + n-1

        faces.append([v1, v0, v2])
        faces.append([v1, v2, v3])

    # Left
    for i in range(n-1):
        v0 = i
        v1 = i + 1
        v2 = i     + n*n
        v3 = i + 1 + n*n

        faces.append([v1, v0, v2])
        faces.append([v1, v2, v3])
            
    # Right
    for i in range(n-1):
        v0 = i           + n*(n-1)
        v1 = i + 1       + n*(n-1)
        v2 = i     + n*n + n*(n-1)
        v3 = i + 1 + n*n + n*(n-1)

        faces.append([v1, v2, v0])
        faces.append([v1, v3, v2])

    return np.array(vertices), np.array(faces)

def wav_to_mesh(wav, mesh_name):
    num_points = 32

    # Generate Amplitude
    fs, amplitude = read(wav)
    amplitude = [sample[0] for sample in amplitude] # Force mono (could blend, but would likely have little effect)
    freqencies = fft(amplitude)

    amplitude = sub_sample_point(amplitude, num_points)
    freqencies = sub_sample_point(freqencies, num_points)

    # Generate cube
    vertices, faces = generate_cube(amplitude)
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save(mesh_name)


if __name__ == "__main__":
    wav_to_mesh("ModelGen/test_files/test_happy.wav", "cube.stl")
    print("fin")