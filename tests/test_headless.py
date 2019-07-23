from pathlib import Path

import moderngl
from headless import HeadlessTestCase
from moderngl_window.context.headless import Keys
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
from moderngl_window import geometry

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class HeadlessWindowTestCase(HeadlessTestCase):
    """Basic property and method testing"""
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_properties(self):
        self.assertEqual(self.window.keys, Keys)
        self.assertEqual(self.window.title, 'ModernGL Window')
        self.assertIsInstance(self.window.ctx, moderngl.Context)
        self.assertIsInstance(self.window.fbo, moderngl.Framebuffer)
        self.assertEqual(self.window.gl_version, (3, 3))
        self.assertEqual(self.window.width, self.window_size[0])
        self.assertEqual(self.window.height, self.window_size[1])
        self.assertEqual(self.window.size, self.window_size)
        self.assertEqual(self.window.buffer_size, self.window_size)
        self.assertEqual(self.window.viewport, (0, 0, self.window_size[0], self.window_size[1]))
        self.assertIsInstance(self.window.frames, int)
        self.assertEqual(self.window.resizable, False)
        self.assertEqual(self.window.fullscreen, False)
        self.assertEqual(self.window.config, None)
        self.assertEqual(self.window.vsync, False)
        self.assertEqual(self.window.samples, 0)
        self.assertEqual(self.window.cursor, False)

    def test_frames(self):
        """Ensure frame counter increases"""
        frame = self.window.frames
        self.window.swap_buffers()
        self.assertEqual(self.window.frames, frame + 1)

    def test_functions(self):
        """Ensure the basic functions do not cause crashes"""
        self.window.swap_buffers()
        self.window.clear()
        self.window.render(0, 0)

    def test_render(self):
        """Render something simple to the framebuffer"""
        self.window.use()
        prog = resources.programs.load(ProgramDescription(path="programs/white.glsl"))
        quad = geometry.quad_fs()
        quad.render(prog)

        # Ensure all fragments (rgba) values are white
        data = self.window.fbo.read(components=4)
        self.assertEqual(data, b'\xff' * (self.window_size[0] * self.window_size[1] * 4))
