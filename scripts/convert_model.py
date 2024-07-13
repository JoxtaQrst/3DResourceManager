import open3d as o3d

def convert_3d_model(input_path, output_path):
    try:
        mesh = o3d.io.read_triangle_mesh(input_path)
        o3d.io.write_triangle_mesh(output_path, mesh)
        return True, f"Model converted successfully and saved to {output_path}"
    except Exception as e:
        return False, f"An error occurred: {e}"
