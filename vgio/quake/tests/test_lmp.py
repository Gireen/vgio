import unittest

from vgio.quake.tests.basecase import TestCase
from vgio.quake import lmp


class TestLmpReadWrite(TestCase):
    def test_lmp(self):
        l0 = lmp.Lmp.open('./test_data/test.lmp')
        l0.close()

        l0.save(self.buff)
        self.buff.seek(0)

        l1 = lmp.Lmp.open(self.buff)

        self.assertEqual(l0.width, l1.width, 'Image widths should be equal')
        self.assertEqual(l0.height, l1.height, 'Image heights should be equal')
        self.assertEqual(l0.pixels, l1.pixels, 'Image pixel data should be equal')

        self.assertFalse(l1.fp.closed, 'File should be open')
        fp = l1.fp
        l1.close()
        self.assertTrue(fp.closed, 'File should be closed')
        self.assertIsNone(l1.fp, 'File pointer should be cleaned up')

    def test_palette(self):
        l0 = lmp.Lmp()
        l0.palette = []

        for i in range(256):
            l0.palette.append((i, i, i))

        l0.save(self.buff)
        self.buff.seek(0)

        l1 = lmp.Lmp.open(self.buff)

        self.assertEqual(l0.palette, l1.palette, 'Palettes should be equal')

    def test_colormap(self):
        l0 = lmp.Lmp()
        l0.colormap = tuple(range(256)) * 64

        l0.save(self.buff)
        self.buff.seek(0)

        l1 = lmp.Lmp.open(self.buff)

        self.assertEqual(l0.colormap, l1.colormap, 'Color maps should be equal')


if __name__ == '__main__':
    unittest.main()
