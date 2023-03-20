import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft
import matplotlib.pyplot as plt

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

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

def generate_cube_vertices(n):
    vertices = []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                vertices.append((x, y, z))
    return np.array(vertices)

def generate_cube_faces(n):
    faces = []
    for x in range(n - 1):
        for y in range(n - 1):
            for z in range(n - 1):
                # Generate the indices of the vertices for each face
                v1 = x + y * n + z * n * n
                v2 = v1 + 1
                v3 = v1 + n
                v4 = v3 + 1
                v5 = v1 + n * n
                v6 = v5 + 1
                v7 = v5 + n
                v8 = v7 + 1
                # Generate the triangles for the top and bottom faces
                faces.append((v1, v2, v4))
                faces.append((v1, v4, v3))
                faces.append((v5, v7, v6))
                faces.append((v6, v7, v8))
                # Generate the triangles for the front and back faces
                faces.append((v1, v5, v6))
                faces.append((v1, v6, v2))
                faces.append((v3, v4, v8))
                faces.append((v3, v8, v7))
                # Generate the triangles for the left and right faces
                faces.append((v1, v3, v7))
                faces.append((v1, v7, v5))
                faces.append((v2, v6, v8))
                faces.append((v2, v8, v4))
    return np.array(faces)

if __name__ == "__main__":
    n = 32
    vertices = generate_cube_vertices(n)
    faces = generate_cube_faces(n)
    print("Vertices:", vertices)
    print("Faces:", faces)

    # Create a new plot
    figure = pyplot.figure()
    axes = figure.add_subplot(projection='3d')

    # Load the STL files and add the vectors to the plot
    # Create the mesh
    faces = generate_cube_faces(n)
    vertices = generate_cube_vertices(n)

    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save('cube.stl')
    
    # Plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

    # Auto scale to the mesh size
    scale = cube.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

    print("fin")

if __name__ == "__main__":
    num_points = 32

    fs, amplitude = read("ModelGen/test_files/test_happy.wav")
    amplitude = [sample[0] for sample in amplitude] # Force mono (could blend, but would likely have little effect)
    freqencies = fft(amplitude)

    amplitude = sub_sample_point(amplitude, num_points)
    freqencies = sub_sample_point(freqencies, num_points)

    print(len(amplitude))
    plt.figure()
    plt.plot(amplitude)
    plt.show()

    print(len(freqencies))
    plt.figure()
    plt.plot(freqencies)
    plt.show()
    print("done")