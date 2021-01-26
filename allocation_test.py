import unittest
import allocation

class TestGeneral(unittest.TestCase):
    def test_wrong_unit(self):
        with self.assertRaises(ValueError):
            allocation.Allocation(1, 128, 'ab', 'mb')
        with self.assertRaises(ValueError):
            allocation.Allocation(1, 128, 'kb', 'ab')

    def test_init_one_block(self):
        memory = allocation.Allocation(1, 1, 'kb', 'kb')
        self.assertEqual(memory.list_files(), {})
        self.assertEqual(memory.availability(), '0')

    def test_init(self):
        memory = allocation.Allocation(1, 128, 'mb', 'kb')
        self.assertEqual(memory.list_files(), {})
        self.assertEqual(memory.availability(), '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7')

class TestReadMethods(unittest.TestCase):
    def initialize_standard(self):
        return allocation.Allocation(1, 128, 'mb', 'kb', 'first')

    def test_read(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        self.assertEqual(memory.read('a'), [0])

    def test_read_non_existant(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        with self.assertRaises(ValueError):
            memory.read('b')

    def test_wrong_unit(self):
        memory = self.initialize_standard()
        with self.assertRaises(ValueError):
            memory.save('a', 120, 'cd')

class TestFirstFitSaveMethods(unittest.TestCase):
    def initialize_standard(self):
        return allocation.Allocation(1, 128, 'mb', 'kb', 'first')

    def save_full(self, memory):
        counter = 'a'
        for i in range(8):
            memory.save(counter, 128, 'kb')
            counter = chr(ord(counter[0]) + 1)

    def test_save_same(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        with self.assertRaises(ValueError):
            memory.save('a', 200, 'kb')

    def test_save_one_block(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        self.assertEqual(memory.read('a'), [0])

    def test_save_one_block_exact(self):
        memory = self.initialize_standard()
        memory.save('a', 128, 'kb')
        self.assertEqual(memory.read('a'), [0])

    def test_save_multi_block(self):
        memory = self.initialize_standard()
        memory.save('a', 130, 'kb')
        self.assertEqual(memory.read('a'), [0, 1])

    def test_save_multi_chunk(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        memory.save('b', 200, 'kb')
        self.assertEqual(memory.read('a'), [0])
        self.assertEqual(memory.read('b'), [1, 2])

    def test_save_to_full(self):
        memory = self.initialize_standard()
        memory.save('a', 1020, 'kb')
        with self.assertRaises(ValueError):
            memory.save('b', 100, 'kb')

    def test_save_last_block(self):
        memory = self.initialize_standard()
        memory.save('a', 896, 'kb')
        memory.save('b', 120, 'kb')
        self.assertEqual(memory.read('a'), [0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(memory.read('b'), [7])

    def test_save_fragmented_blocks_no_chunk_available(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('a')
        memory.delete('d')
        memory.delete('h')
        with self.assertRaises(ValueError):
            memory.save('z', 200, 'kb')

    def test_save_fragmented_blocks_front(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('a')
        memory.delete('b')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [0, 1])

    def test_save_fragmented_blocks_middle(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('c')
        memory.delete('d')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [2, 3])

    def test_save_fragmented_blocks_back(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('c')
        memory.delete('g')
        memory.delete('h')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [6, 7])

    def test_save_fragmented_blocks_oversized(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('b')
        memory.delete('c')
        memory.delete('d')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [1, 2])

class TestBestFitSaveMethods(unittest.TestCase):
    def initialize_standard(self):
        return allocation.Allocation(1, 128, 'mb', 'kb')

    def save_full(self, memory):
        counter = 'a'
        for i in range(8):
            memory.save(counter, 128, 'kb')
            counter = chr(ord(counter[0]) + 1)

    def test_save_same(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        with self.assertRaises(ValueError):
            memory.save('a', 200, 'kb')

    def test_save_one_block(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        self.assertEqual(memory.read('a'), [0])

    def test_save_one_block_exact(self):
        memory = self.initialize_standard()
        memory.save('a', 128, 'kb')
        self.assertEqual(memory.read('a'), [0])

    def test_save_multi_block(self):
        memory = self.initialize_standard()
        memory.save('a', 130, 'kb')
        self.assertEqual(memory.read('a'), [0, 1])

    def test_save_multi_chunk(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        memory.save('b', 200, 'kb')
        self.assertEqual(memory.read('a'), [0])
        self.assertEqual(memory.read('b'), [1, 2])

    def test_save_to_full(self):
        memory = self.initialize_standard()
        memory.save('a', 1020, 'kb')
        with self.assertRaises(ValueError):
            memory.save('b', 100, 'kb')

    def test_save_last_block(self):
        memory = self.initialize_standard()
        memory.save('a', 896, 'kb')
        memory.save('b', 120, 'kb')
        self.assertEqual(memory.read('a'), [0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(memory.read('b'), [7])

    def test_save_fragmented_blocks_no_chunk_available(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('a')
        memory.delete('d')
        memory.delete('h')
        with self.assertRaises(ValueError):
            memory.save('z', 200, 'kb')

    def test_save_fragmented_blocks_front(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('a')
        memory.delete('b')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [0, 1])

    def test_save_fragmented_blocks_middle(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('c')
        memory.delete('d')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [2, 3])

    def test_save_fragmented_blocks_back(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('c')
        memory.delete('g')
        memory.delete('h')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [6, 7])

    def test_save_fragmented_best_block(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('c')
        memory.delete('d')
        memory.delete('f')
        memory.save('z', 100, 'kb')
        self.assertEqual(memory.read('z'), [5])

    def test_save_fragmented_best_block_oversized(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('b')
        memory.delete('c')
        memory.delete('d')
        memory.delete('f')
        memory.delete('g')
        memory.save('z', 100, 'kb')
        self.assertEqual(memory.read('z'), [5])

    def test_save_fragmented_blocks_oversized(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('b')
        memory.delete('c')
        memory.delete('d')
        memory.save('z', 200, 'kb')
        self.assertEqual(memory.read('z'), [1, 2])

class TestDeleteMethods(unittest.TestCase):
    def initialize_standard(self):
        return allocation.Allocation(1, 128, 'mb', 'kb', 'first')

    def save_full(self, memory):
        counter = 'a'
        for i in range(8):
            memory.save(counter, 128, 'kb')
            counter = chr(ord(counter[0]) + 1)

    def test_delete_non_existant(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        with self.assertRaises(ValueError):
            memory.delete('z')

    def test_delete_generic(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('d')
        with self.assertRaises(ValueError):
            memory.read('d')
        self.assertEqual(memory.availability(), '3')
        memory.delete('b')
        with self.assertRaises(ValueError):
            memory.read('b')
        self.assertEqual(memory.availability(), '1 -> 3')
        memory.delete('f')
        with self.assertRaises(ValueError):
            memory.read('f')
            self.assertEqual(memory.availability(), '1 -> 3 -> 5')
        memory.delete('c')
        with self.assertRaises(ValueError):
            memory.read('c')
        self.assertEqual(memory.availability(), '1 -> 2 -> 3 -> 5')

    def test_delete_front(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('a')
        with self.assertRaises(ValueError):
            memory.read('a')
        self.assertEqual(memory.availability(), '0')

    def test_delete_last(self):
        memory = self.initialize_standard()
        self.save_full(memory)
        memory.delete('h')
        with self.assertRaises(ValueError):
            memory.read('h')
        self.assertEqual(memory.availability(), '7')

    def test_delete_front_2(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        memory.delete('a')
        with self.assertRaises(ValueError):
            memory.read('a')
        self.assertEqual(memory.availability(), '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7')

    def test_delete_middle_2(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        memory.save('b', 120, 'kb')
        memory.delete('a')
        with self.assertRaises(ValueError):
            memory.read('a')
        self.assertEqual(memory.availability(), '0 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7')
        memory.delete('b')
        with self.assertRaises(ValueError):
            memory.read('b')
        self.assertEqual(memory.availability(), '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7')

    def test_delete_last_2(self):
        memory = self.initialize_standard()
        memory.save('a', 896, 'kb')
        memory.save('b', 120, 'kb')
        memory.delete('a')
        memory.delete('b')
        self.assertEqual(memory.availability(), '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7')

    def test_delete_fragmented(self):
        memory = self.initialize_standard()
        memory.save('a', 120, 'kb')
        memory.save('b', 200, 'kb')
        memory.save('c', 120, 'kb')
        memory.save('d', 120, 'kb')
        memory.delete('a')
        memory.delete('c')
        memory.delete('d')
        self.assertEqual(memory.availability(), '0 -> 3 -> 4 -> 5 -> 6 -> 7')

if __name__ == '__main__':
    unittest.main()
