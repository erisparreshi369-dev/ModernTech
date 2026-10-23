"""Build ModernTech 3D models, textures and thumbnails with Blender.

Run from the mod folder:
    blender -b -P tools/build_models.py

Writes:
    HardwareDesign/MT_GPU, HardwareDesign/MT_CPU   (product designs: .obj + textures)
    extras/Furniture/ModernTech PCs                (office computers: .obj + textures + thumbnails)

Every model is one mesh. Each part's UVs point at one solid block of a small
texture atlas, so the game can recolor parts the same way it does vanilla furniture:
main texture R/G/B = primary/secondary/tertiary color, extra texture
R = smoothness, G = glow when switched on, B = 1 to use the player's colors.
"""
import math
import os

import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FURN_DIR = os.path.join(ROOT, "extras", "Furniture", "ModernTech PCs")
DESIGN_DIR = os.path.join(ROOT, "HardwareDesign")

# name: (albedo RGB, extra RGB, thumbnail preview RGB)
BLOCKS = {
    "primary":   ((255, 0, 0), (128, 0, 255), (0.17, 0.18, 0.20)),
    "secondary": ((0, 255, 0), (128, 0, 255), (0.55, 0.57, 0.60)),
    "tertiary":  ((0, 0, 255), (128, 0, 255), (0.05, 0.75, 0.85)),
    "glow":      ((0, 0, 255), (128, 255, 255), (0.10, 0.90, 1.00)),
    "screen":    ((22, 40, 70), (210, 255, 0), (0.12, 0.30, 0.55)),
    "black":     ((16, 16, 19), (60, 0, 0), (0.03, 0.03, 0.035)),
    "metal":     ((150, 152, 158), (190, 0, 0), (0.55, 0.56, 0.60)),
    "glass":     ((32, 34, 40), (235, 0, 0), (0.10, 0.11, 0.13)),
    "gold":      ((205, 165, 70), (200, 0, 0), (0.80, 0.65, 0.28)),
    "pcb":       ((0, 255, 0), (90, 0, 255), (0.05, 0.35, 0.18)),
}
GRID = 4  # 4x4 blocks
TEX = 64  # texture size in pixels (power of two)


def block_uv(name):
    i = list(BLOCKS).index(name)
    cell = 1.0 / GRID
    return ((i % GRID + 0.5) * cell, 1.0 - (i // GRID + 0.5) * cell)


def write_textures(folder):
    os.makedirs(folder, exist_ok=True)
    for kind, chan in (("mt_albedo.png", 0), ("mt_extra.png", 1)):
        img = bpy.data.images.new(kind, TEX, TEX, alpha=True)
        px = [0.0] * (TEX * TEX * 4)
        cell = TEX // GRID
        for i, vals in enumerate(BLOCKS.values()):
            r, g, b = (c / 255 for c in vals[chan])
            bx, by = i % GRID, GRID - 1 - i // GRID  # image rows start at the bottom
            for y in range(by * cell, (by + 1) * cell):
                for x in range(bx * cell, (bx + 1) * cell):
                    px[(y * TEX + x) * 4:(y * TEX + x) * 4 + 4] = [r, g, b, 1.0]
        img.pixels = px
        img.filepath_raw = os.path.join(folder, kind)
        img.file_format = "PNG"
        img.save()
        bpy.data.images.remove(img)


def preview_material(name):
    mat = bpy.data.materials.get("prev_" + name)
    if mat is None:
        mat = bpy.data.materials.new("prev_" + name)
        mat.diffuse_color = (*BLOCKS[name][2], 1.0)
    return mat


def finish_part(obj, block):
    """Point every UV of the part at its color block and give it a preview color."""
    mesh = obj.data
    if not mesh.uv_layers:
        mesh.uv_layers.new()
    uv = block_uv(block)
    for loop_uv in mesh.uv_layers.active.data:
        loop_uv.uv = uv
    mesh.materials.clear()
    mesh.materials.append(preview_material(block))
    return obj


def box(size, loc, block, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=[math.radians(a) for a in rot])
    obj = bpy.context.active_object
    obj.scale = size
    return finish_part(obj, block)


def cyl(radius, depth, loc, block, rot=(0, 0, 0), verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc,
                                        rotation=[math.radians(a) for a in rot])
    return finish_part(bpy.context.active_object, block)


def monitor(width, height, x=0.0, y=0.03, turn=0.0):
    """Flat panel facing -Y (towards the employee) standing on the desk."""
    parts = []
    pivot = (x, y)
    def place(px, py):
        a = math.radians(turn)
        return (pivot[0] + px * math.cos(a) - py * math.sin(a), pivot[1] + px * math.sin(a) + py * math.cos(a))
    cz = 0.12 + height / 2
    parts.append(box((width, 0.025, height), (*place(0, 0), cz), "black", (0, 0, turn)))
    parts.append(box((width - 0.03, 0.004, height - 0.03), (*place(0, -0.0145), cz), "screen", (0, 0, turn)))
    parts.append(box((0.05, 0.03, 0.13), (*place(0, 0.03), 0.07), "metal", (0, 0, turn)))
    parts.append(box((0.22, 0.16, 0.012), (*place(0, 0.02), 0.006), "metal", (0, 0, turn)))
    return parts


def keyboard(y=-0.21, glow=False):
    parts = [box((0.42, 0.13, 0.018), (0, y, 0.009), "primary"),
             box((0.39, 0.10, 0.008), (0, y, 0.022), "black")]
    if glow:
        parts.append(box((0.425, 0.135, 0.004), (0, y, 0.001), "glow"))
    return parts


def mouse(x=0.29, y=-0.21):
    return [box((0.06, 0.10, 0.03), (x, y, 0.015), "primary")]


def build_minipc():
    return (monitor(0.56, 0.34) + keyboard() + mouse() +
            [box((0.13, 0.13, 0.045), (0.43, 0.05, 0.0225), "primary"),
             box((0.012, 0.002, 0.006), (0.40, -0.0155, 0.03), "glow")])


def build_workstation():
    tower = [box((0.20, 0.42, 0.44), (0.52, 0.0, 0.22), "primary"),
             box((0.20, 0.01, 0.44), (0.52, -0.215, 0.22), "secondary"),
             box((0.012, 0.002, 0.012), (0.52, -0.221, 0.40), "glow")]
    return monitor(0.66, 0.38) + keyboard() + mouse() + tower


def build_ai_workstation():
    tower = [box((0.25, 0.48, 0.50), (0.70, 0.04, 0.25), "primary"),
             box((0.006, 0.40, 0.40), (0.574, 0.04, 0.26), "glass")]
    for i in range(3):  # front intake fans with lit rings
        z = 0.10 + i * 0.15
        tower.append(cyl(0.055, 0.008, (0.70, -0.204, z), "glow", (90, 0, 0)))
        tower.append(cyl(0.045, 0.010, (0.70, -0.205, z), "black", (90, 0, 0)))
    tower.append(box((0.004, 0.36, 0.02), (0.569, 0.04, 0.45), "glow"))  # light strips framing the glass
    tower.append(box((0.004, 0.36, 0.02), (0.569, 0.04, 0.07), "glow"))
    return (monitor(0.56, 0.33, x=-0.29, turn=15) + monitor(0.56, 0.33, x=0.29, turn=-15) +
            keyboard(glow=True) + mouse(x=0.30) + tower)


def build_ultrabook():
    y0 = -0.20
    parts = [box((0.40, 0.28, 0.014), (0, y0, 0.007), "primary"),
             box((0.34, 0.11, 0.002), (0, y0 + 0.03, 0.015), "black"),
             box((0.11, 0.07, 0.001), (0, y0 - 0.085, 0.0145), "black")]
    lid_tilt = 15  # degrees past vertical
    hinge_y, lid_h = y0 + 0.14, 0.26
    a = math.radians(lid_tilt)
    cy, cz = hinge_y + math.sin(a) * lid_h / 2, 0.014 + math.cos(a) * lid_h / 2
    parts.append(box((0.40, 0.008, lid_h), (0, cy, cz), "primary", (-lid_tilt, 0, 0)))
    parts.append(box((0.37, 0.002, lid_h - 0.03), (0, cy - 0.005 * math.cos(a), cz + 0.005 * math.sin(a)),
                     "screen", (-lid_tilt, 0, 0)))
    return parts


def build_gpu():
    """Graphics card for the hardware design editor: fits the 2x2x2 cube."""
    parts = [box((1.90, 0.06, 0.80), (0, 0.12, 0), "pcb"),
             box((1.90, 0.30, 0.78), (0, -0.06, 0), "primary"),
             box((1.90, 0.02, 0.80), (0, 0.16, 0), "secondary"),
             box((0.10, 0.36, 0.82), (-0.98, 0.0, 0), "metal"),
             box((0.40, 0.04, 0.10), (0.30, 0.12, -0.44), "gold"),
             box((1.50, 0.01, 0.03), (0.0, -0.215, 0.36), "glow")]
    for x in (-0.48, 0.48):
        parts.append(cyl(0.33, 0.02, (x, -0.22, 0), "black", (90, 0, 0), verts=32))
        parts.append(cyl(0.10, 0.03, (x, -0.225, 0), "tertiary", (90, 0, 0), verts=20))
    return parts


def build_cpu():
    """Processor package lying flat: substrate, heat spreader, contact edge."""
    return [box((1.60, 1.60, 0.10), (0, 0, -0.10), "pcb"),
            box((1.20, 1.20, 0.16), (0, 0, 0.03), "primary"),
            box((0.80, 0.30, 0.01), (0, -0.30, 0.115), "secondary"),
            box((1.56, 1.56, 0.02), (0, 0, -0.16), "gold")]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def join(parts, name):
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def export_obj(obj, path):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.wm.obj_export(filepath=path, export_selected_objects=True, export_uv=True,
                          export_normals=True, export_materials=False, export_triangulated_mesh=True,
                          forward_axis="NEGATIVE_Z", up_axis="Y")


def render_thumbnail(obj, path):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = 128
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    cam_data = bpy.data.cameras.new("thumb")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("thumb", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    corners = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo = [min(c[i] for c in corners) for i in range(3)]
    hi = [max(c[i] for c in corners) for i in range(3)]
    center = [(a + b) / 2 for a, b in zip(lo, hi)]
    size = max(b - a for a, b in zip(lo, hi))
    cam.location = (center[0] - size * 1.2, center[1] - size * 1.6, center[2] + size * 1.1)
    direction = [c - l for c, l in zip(center, cam.location)]
    cam.rotation_euler = _look_rotation(direction)
    cam_data.ortho_scale = size * 1.25
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)


def _look_rotation(d):
    from mathutils import Vector
    return Vector(d).to_track_quat("-Z", "Y").to_euler()


FURNITURE = {
    "minipc": build_minipc,
    "workstation": build_workstation,
    "aiworkstation": build_ai_workstation,
    "ultrabook": build_ultrabook,
}
DESIGNS = {"MT_GPU": build_gpu, "MT_CPU": build_cpu}


def main():
    write_textures(FURN_DIR)
    for name, build in FURNITURE.items():
        clear_scene()
        obj = join(build(), name)
        export_obj(obj, os.path.join(FURN_DIR, name + ".obj"))
        render_thumbnail(obj, os.path.join(FURN_DIR, name + "_thumb.png"))
    for name, build in DESIGNS.items():
        folder = os.path.join(DESIGN_DIR, name)
        write_textures(folder)
        clear_scene()
        obj = join(build(), name)
        dims = obj.dimensions
        assert max(dims) <= 2.0 + 1e-6, f"{name} must fit the 2x2x2 design cube, got {tuple(dims)}"
        export_obj(obj, os.path.join(folder, name.lower() + ".obj"))
    print("ModernTech models built")


main()
