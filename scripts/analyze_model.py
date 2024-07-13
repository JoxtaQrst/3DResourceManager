import os
import numpy as np
import open3d as o3d

def analyze_3d_model(file_path):
    try:
        mesh = o3d.io.read_triangle_mesh(file_path)
        if not mesh.has_triangles():
            point_cloud = o3d.io.read_point_cloud(file_path)
            num_vertices = len(np.asarray(point_cloud.points))
            num_faces = 0

        else:
            num_vertices = len(np.asarray(mesh.vertices))
            num_faces = len(np.asarray(mesh.triangles))


        file_size = os.path.getsize(file_path) / 1024  # Size in KB

        details = {
            "num_vertices": num_vertices,
            "num_faces": num_faces,
            "file_size": file_size,
        }

        return True, details
    except Exception as e:
        return False, f"An error occurred while fetching model details: {e}"
