import pandas as pd
import numpy as np
import open3d as o3d
import time

def define_skeleton_structure():
    joints = [
        'Head', 'Shoulder_Center', 'Shoulder_Left', 'Shoulder_Right',
        'Elbow_Left', 'Elbow_Right', 'Wrist_Left', 'Wrist_Right',
        'Hand_Left', 'Hand_Right', 'Spine', 'Hip_Center', 'Hip_Left',
        'Hip_Right', 'Knee_Left', 'Knee_Right', 'Ankle_Left', 'Ankle_Right',
        'Foot_Left', 'Foot_Right'
    ]

    connections = [
        ('Head', 'Shoulder_Center'),
        ('Shoulder_Center', 'Shoulder_Left'),
        ('Shoulder_Center', 'Shoulder_Right'),
        ('Shoulder_Left', 'Elbow_Left'),
        ('Shoulder_Right', 'Elbow_Right'),
        ('Elbow_Left', 'Wrist_Left'),
        ('Elbow_Right', 'Wrist_Right'),
        ('Wrist_Left', 'Hand_Left'),
        ('Wrist_Right', 'Hand_Right'),
        ('Shoulder_Center', 'Spine'),
        ('Spine', 'Hip_Center'),
        ('Hip_Center', 'Hip_Left'),
        ('Hip_Center', 'Hip_Right'),
        ('Hip_Left', 'Knee_Left'),
        ('Hip_Right', 'Knee_Right'),
        ('Knee_Left', 'Ankle_Left'),
        ('Knee_Right', 'Ankle_Right'),
        ('Ankle_Left', 'Foot_Left'),
        ('Ankle_Right', 'Foot_Right')
    ]
    
    return joints, connections

# The rest of the code remains the same
def create_skeleton_lineset(coordinates):
    lines = [np.array([joints.index(connection[0]), joints.index(connection[1])]) for connection in connections]
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(coordinates), lines=o3d.utility.Vector2iVector(lines))
    return line_set

def rotate_skeleton_around_y(skeleton_coordinates, angle):
    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    rotated_coordinates = {}
    for joint, coord in skeleton_coordinates.items():
        rotated_coordinates[joint] = np.matmul(rotation_matrix, coord)
    return rotated_coordinates

# Read the CSV file
file_path = 'id16-subset-dataset.csv'
df = pd.read_csv(file_path)

# Define the skeleton joints and connections
joints, connections = define_skeleton_structure()

# Specify how many rows to plot
num_rows_to_plot = 1

# Specify how many skeletons should be visible in the same plot
num_skeletons_visible = 3

# Create an Open3D visualization window
vis = o3d.visualization.Visualizer()
vis.create_window()

camera_configured = False

# Initialize an empty list to store the line sets
line_sets = []

# Create a temp variable to control the first frame adjustment
first_frame = True

for row_index in range(min(num_rows_to_plot, len(df))):
    # Extract the coordinates for the current row
    data = df.loc[row_index]
    raw_coordinates = {joint: np.array([data[joint + ' x'], data[joint + ' y'], data[joint + ' z']]) for joint in joints}
    coordinates = rotate_skeleton_around_y(raw_coordinates, np.pi)  # Rotate the skeleton 180 degrees around the Y-axis
    coordinates_list = [coordinates[joint] for joint in joints]

    # Create a line set for the current skeleton and add it to the list
    line_set = create_skeleton_lineset(coordinates_list)
    line_sets.append(line_set)

    # Keep only the specified number of visible skeletons
    if len(line_sets) > num_skeletons_visible:
        vis.remove_geometry(line_sets.pop(0))

    # Add the line sets to the visualization window
    for line_set in line_sets:
        vis.add_geometry(line_set)

    # Update the visualization window
    for line_set in line_sets:
        vis.update_geometry(line_set)
    vis.poll_events()
    vis.update_renderer()

    if first_frame:
        # Manually set the camera parameters
        vis_control = vis.get_view_control()
        vis_control.set_constant_z_far(10000)
        vis_control.set_constant_z_near(1)
        vis_control.set_lookat([0, 0, 0])
        first_frame = False

    # Pause for the specified frame delay
    time.sleep(0.1)

# Keep the visualization window open until the user closes it
while vis.poll_events():
    vis.update_renderer()
    time.sleep(0.01)

# Close the visualization window
vis.destroy_window()