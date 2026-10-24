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


def build_vr_station():
    headset = [box((0.20, 0.11, 0.09), (-0.40, -0.12, 0.045), "primary"),
               box((0.17, 0.004, 0.06), (-0.40, -0.177, 0.05), "glass"),
               box((0.22, 0.02, 0.02), (-0.40, -0.06, 0.08), "black")]
    controllers = [cyl(0.025, 0.12, (x, -0.30, 0.06), "secondary") for x in (0.36, 0.44)]
    tower = [box((0.18, 0.38, 0.40), (0.55, 0.02, 0.20), "primary"),
             box((0.005, 0.30, 0.30), (0.459, 0.02, 0.22), "glass"),
             box((0.004, 0.30, 0.015), (0.457, 0.02, 0.38), "glow")]
    return monitor(0.60, 0.36) + keyboard(glow=True) + headset + controllers + tower


def build_ultrawide():
    parts = []
    for i, turn in enumerate((14, 0, -14)):  # three panels make one curved screen
        parts += monitor(0.36, 0.36, x=(i - 1) * 0.35, y=0.03 + abs(i - 1) * 0.045, turn=turn)[:2]
    parts += [box((0.05, 0.03, 0.13), (0, 0.06, 0.07), "metal"),
              box((0.30, 0.16, 0.012), (0, 0.05, 0.006), "metal")]
    return parts + keyboard() + mouse(x=0.31) + [box((0.10, 0.10, 0.03), (-0.40, -0.20, 0.015), "secondary")]


def build_ai_panel():
    """Wall screen: the AI assistant's face, glowing on the office wall."""
    y = -0.15
    parts = [box((0.60, 0.04, 0.55), (0, y, 0), "primary"),
             box((0.54, 0.004, 0.42), (0, y - 0.022, 0.03), "screen"),
             box((0.50, 0.004, 0.02), (0, y - 0.022, -0.235), "glow")]
    parts.append(cyl(0.09, 0.006, (0, y - 0.026, 0.05), "glow", (90, 0, 0), verts=32))
    parts.append(cyl(0.06, 0.008, (0, y - 0.027, 0.05), "screen", (90, 0, 0), verts=32))
    return parts


def rack(width, height, depth, units, glow_every=1):
    parts = [box((width, depth, height), (0, 0, height / 2), "primary"),
             box((width - 0.06, 0.01, height - 0.08), (0, -depth / 2 - 0.004, height / 2), "black")]
    step = (height - 0.16) / units
    for i in range(units):
        z = 0.10 + step * (i + 0.5)
        parts.append(box((width - 0.12, 0.012, step * 0.7), (0, -depth / 2 - 0.01, z), "secondary"))
        if i % glow_every == 0:
            parts.append(box((0.04, 0.004, 0.012), (width / 2 - 0.12, -depth / 2 - 0.018, z), "glow"))
    return parts


def build_blade_server():
    return rack(0.90, 1.85, 0.95, 10)


def build_ai_cluster():
    parts = []
    for x in (-0.5, 0.5):
        for p in rack(0.95, 1.80, 0.95, 8):
            p.location.x += x
            parts.append(p)
    parts.append(box((1.96, 0.97, 0.03), (0, 0, 1.815), "glow"))  # light bar across the top
    return parts


def build_fab_printer():
    y = 0.11
    return [box((1.05, 1.80, 0.30), (0, y, 0.15), "secondary"),
            box((1.05, 1.80, 0.06), (0, y, 1.51), "primary"),
            box((0.06, 1.80, 1.20), (-0.50, y, 0.90), "primary"),
            box((0.06, 1.80, 1.20), (0.50, y, 0.90), "primary"),
            box((0.92, 1.70, 0.004), (0, y, 0.92), "glass"),
            box((0.30, 0.20, 0.10), (0, y, 1.20), "black"),
            box((0.98, 0.04, 0.03), (0, y, 1.25), "metal"),
            box((0.92, 0.01, 0.02), (0, y - 0.905, 0.32), "glow"),
            box((0.30, 0.02, 0.20), (0.30, y - 0.91, 1.30), "screen")]


def build_component_fab():
    return [box((0.95, 1.95, 0.80), (0, 0, 0.40), "primary"),
            box((0.95, 1.95, 0.05), (0, 0, 0.825), "secondary"),
            box((0.70, 1.60, 0.50), (0, 0, 1.10), "glass"),
            box((0.20, 0.20, 0.25), (0, 0.2, 1.00), "metal"),
            box((0.80, 0.01, 0.02), (0, -0.98, 0.70), "glow"),
            box((0.30, 0.02, 0.20), (0.25, -0.985, 0.55), "screen")]


def build_smart_fridge():
    y = 0.15
    return [box((0.74, 0.58, 1.48), (0, y, 0.74), "primary"),
            box((0.004, 0.012, 1.40), (0, y - 0.296, 0.75), "black"),
            box((0.30, 0.01, 0.40), (-0.18, y - 0.296, 1.05), "screen"),
            box((0.02, 0.03, 0.50), (0.04, y - 0.30, 0.95), "metal"),
            box((0.02, 0.03, 0.50), (-0.04, y - 0.30, 0.95), "metal"),
            box((0.10, 0.004, 0.01), (-0.18, y - 0.30, 0.82), "glow")]


def build_induction_stove():
    y = 0.10
    parts = [box((0.78, 0.78, 0.86), (0, y, 0.43), "primary"),
             box((0.78, 0.78, 0.02), (0, y, 0.87), "glass"),
             box((0.64, 0.01, 0.40), (0, y - 0.39, 0.40), "glass"),
             box((0.60, 0.012, 0.02), (0, y - 0.392, 0.70), "metal")]
    for x in (-0.19, 0.19):
        for dy in (-0.18, 0.18):
            parts.append(cyl(0.12, 0.004, (x, y + dy, 0.882), "glow"))
    return parts


def build_bean_coffee():
    y = -0.05
    return [box((0.40, 0.38, 0.44), (0, y + 0.02, 0.22), "primary"),
            box((0.40, 0.10, 0.06), (0, y - 0.14, 0.41), "secondary"),
            box((0.26, 0.012, 0.12), (0, y - 0.175, 0.30), "screen"),
            box((0.06, 0.06, 0.05), (0, y - 0.15, 0.35), "metal"),
            cyl(0.03, 0.08, (0, y - 0.13, 0.08), "secondary", verts=16),
            box((0.30, 0.16, 0.02), (0, y - 0.12, 0.01), "metal"),
            cyl(0.07, 0.10, (0.10, y + 0.08, 0.49), "glass", verts=16)]


def build_smart_vending():
    return [box((0.78, 0.76, 1.38), (0, 0, 0.69), "primary"),
            box((0.50, 0.01, 1.00), (-0.10, -0.385, 0.80), "glass"),
            box((0.14, 0.01, 0.30), (0.28, -0.385, 1.00), "screen"),
            box((0.50, 0.02, 0.12), (-0.10, -0.39, 0.15), "black"),
            box((0.004, 0.01, 1.00), (0.17, -0.39, 0.80), "glow")] + \
           [box((0.46, 0.30, 0.01), (-0.10, -0.20, 0.45 + i * 0.25), "secondary") for i in range(4)]


def build_heat_pump():
    return [box((0.44, 0.48, 0.84), (0, 0, 0.42), "primary"),
            cyl(0.16, 0.01, (0, -0.245, 0.50), "black", (90, 0, 0), verts=32),
            cyl(0.05, 0.015, (0, -0.25, 0.50), "secondary", (90, 0, 0)),
            box((0.30, 0.01, 0.06), (0, -0.245, 0.18), "screen"),
            box((0.06, 0.004, 0.01), (0.12, -0.25, 0.18), "glow")]


def build_power_wall():
    parts = [box((0.96, 1.96, 0.10), (0, 0, 0.05), "secondary")]
    for x in (-0.24, 0.24):
        for y in (-0.48, 0.48):
            parts.append(box((0.44, 0.90, 1.30), (x, y, 0.75), "primary"))
            parts.append(box((0.02, 0.60, 0.02), (x, y, 1.41), "glow"))
    return parts


def build_smart_vent():
    y, z = -0.15, 1.6
    parts = [box((0.40, 0.08, 0.40), (0, y, z), "primary"),
             cyl(0.15, 0.01, (0, y - 0.045, z), "black", (90, 0, 0), verts=32),
             cyl(0.04, 0.015, (0, y - 0.05, z), "secondary", (90, 0, 0)),
             cyl(0.17, 0.006, (0, y - 0.042, z), "glow", (90, 0, 0), verts=32)]
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


def build_vr():
    """VR headset seen from the front: visor, lenses, strap."""
    parts = [box((1.60, 0.90, 0.85), (0, 0, 0), "primary"),
             box((1.50, 0.02, 0.75), (0, -0.46, 0), "glass"),
             box((1.62, 0.20, 0.10), (0, 0.10, -0.47), "secondary"),
             box((0.10, 1.00, 0.30), (-0.85, 0.40, 0.05), "secondary"),
             box((0.10, 1.00, 0.30), (0.85, 0.40, 0.05), "secondary"),
             box((1.20, 0.02, 0.03), (0, -0.475, 0.30), "glow")]
    for x in (-0.42, 0.42):
        parts.append(cyl(0.12, 0.02, (x, -0.475, -0.05), "black", (90, 0, 0), verts=24))
    return parts


def build_watch():
    """Smartwatch lying face up: case, screen, crown, strap."""
    return [box((0.90, 1.05, 0.30), (0, 0, 0.10), "primary"),
            box((0.80, 0.95, 0.02), (0, 0, 0.26), "screen"),
            box((0.60, 1.90, 0.08), (0, 0, -0.10), "secondary"),
            cyl(0.07, 0.10, (0.50, 0.15, 0.12), "tertiary", (0, 90, 0), verts=16),
            box((0.50, 0.03, 0.005), (0, -0.30, 0.272), "glow")]


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


def render_thumbnail(objs, path, res=128, transparent=True):
    if not isinstance(objs, list):
        objs = [objs]
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.render.film_transparent = transparent
    scene.world = scene.world or bpy.data.worlds.new("bg")
    scene.world.color = (0.86, 0.88, 0.91)
    scene.render.resolution_x = scene.render.resolution_y = res
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    cam_data = bpy.data.cameras.new("thumb")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("thumb", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    corners = [o.matrix_world @ v.co for o in objs for v in o.data.vertices]
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
    "vrstation": build_vr_station,
    "ultrawide": build_ultrawide,
    "aipanel": build_ai_panel,
    "bladeserver": build_blade_server,
    "aicluster": build_ai_cluster,
    "fabprinter": build_fab_printer,
    "componentfab": build_component_fab,
    "smartfridge": build_smart_fridge,
    "inductionstove": build_induction_stove,
    "beancoffee": build_bean_coffee,
    "smartvending": build_smart_vending,
    "heatpump": build_heat_pump,
    "powerwall": build_power_wall,
    "smartvent": build_smart_vent,
}
DESIGNS = {"MT_GPU": build_gpu, "MT_CPU": build_cpu, "MT_VR": build_vr, "MT_Watch": build_watch}


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
    render_previews()
    print("ModernTech models built")


def render_previews():
    """Steam Workshop preview image (Thumbnail.png) for each of the three packages."""
    clear_scene()
    pcs = []
    for i, build in enumerate(FURNITURE.values()):
        pcs.append(join(build(), "pc%d" % i))
        pcs[-1].location = ((i % 6) * 2.3, (i // 6) * 2.3, 0)
    render_thumbnail(pcs, os.path.join(FURN_DIR, "Thumbnail.png"), res=512, transparent=False)

    clear_scene()
    gpu = join(build_gpu(), "gpu")
    gpu.rotation_euler.z = math.radians(-20)
    cpu = join(build_cpu(), "cpu")
    cpu.location = (2.6, 1.4, -0.4)
    laptop = join(build_ultrabook(), "laptop")
    laptop.scale = (4, 4, 4)
    laptop.location = (1.0, -1.8, -1.0)
    render_thumbnail([gpu, cpu, laptop], os.path.join(ROOT, "Thumbnail.png"), res=512, transparent=False)

    clear_scene()
    bars = [box((9 * 0.5, 1.0, 0.1), (2.0, 0, -0.05), "primary")]
    for i in range(9):  # demand growing from 25% to 100%, same curve as the code mod
        t = i / 8
        h = 3 * (0.25 + 0.75 * t * t * (3 - 2 * t))
        bars.append(box((0.35, 0.6, h), (i * 0.5, 0, h / 2), "glow"))
    chart = join(bars, "chart")
    render_thumbnail(chart, os.path.join(ROOT, "extras", "DLLMods", "ModernTechDemand", "Thumbnail.png"),
                     res=512, transparent=False)


main()
