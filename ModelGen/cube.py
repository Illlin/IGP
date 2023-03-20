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

    # Bottom faces of the cube
    vertices.append([0,0,0])
    vertices.append([0,1,0])
    vertices.append([1,0,0])
    vertices.append([1,1,0])

    # Top of the cube is an NxN
    for x in range(n):
        for y in range(n):
            vertices.append([x/(n-1),y/(n-1),1])

    return np.array(vertices)


def generate_cube_faces(n):
    # Bottom face is hard coded
    faces = [[1,2,0], [1,3,2]]
    for x in range(n-1):
        for y in range(n-1):
            v0 = y*n + 4 + x
            v1 = y*n + 4 + x + n
            v2 = y*n + 4 + x + 1
            v3 = y*n + 4 + x + 1 + n

            faces.append([v1, v2, v0])
            faces.append([v1, v3, v2])

    for i in range(n-1):
        # Front
        v0 = 0
        v1 = 4 + n*i
        v2 = 4 + n*(i+1)

        faces.append([v1, v0, v2])
        if i == n-2:
            faces.append([v2, 0, 2])

        # back
        v0 = 3
        v1 = 4 + (n-1) + n*i
        v2 = 4 + (n-1) + n*(i+1)

        faces.append([v1, v2, v0])
        if i == 0:
            faces.append([v1, 3, 1])

        # Right
        v0 = 2
        v1 = 4 + n*(n-1) + i
        v2 = 4 + n*(n-1) + i + 1 

        faces.append([v1, v0, v2])
        if i == n-2:
            faces.append([v2, 2, 3])

        # Left
        v0 = 1
        v1 = 4 + i
        v2 = 4 + i + 1

        faces.append([v1, v2, v0])
        if i == 0:
            faces.append([v1, 1, 0])


    #return np.array([])
    return np.array(faces)

if __name__ == "__main__":
    n = 3
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