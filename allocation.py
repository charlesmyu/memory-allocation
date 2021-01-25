from linked_list import Node, LinkedList
import math

class Allocation:
    def __init__(self, capacity: int, capacity_unit: str, block: int, allocation_algorithm: str = 'best') -> None:
        '''
        Initializes an object that represents a single file manager. Four private instance variables are created:
            capacity_used: amount of capacity used in Bytes
            capacity: amount of capacity available in Bytes
            block: size of block in Bytes
            available: linked list that tracks remaining empty space
            cache: hashmap (dict) that is used to store file_id -> list of assigned blocks for quick retrival

        :param capacity: Total capacity of memory
        :param capacity_unit: Unit used for capacity. Must be one of MB or GB
        :param block: Size of block of memory in KB
        :param allocation_algorithm: Algorithm used for allocation. Either 'best' or 'first'.
        '''
        self._allocation_algorithm = allocation_algorithm

        # Translate all amounts to bytes for standardization
        self._capacity_used = 0
        self._block = self._to_bytes(block, 'kb')
        self._capacity = self._to_bytes(capacity, capacity_unit)

        print('Block size: {}B'.format(str(self._block)))
        print('Capacity: {}B'.format(str(self._capacity)))
        print('Number of Blocks: {}'.format(str(int(self._capacity/self._block))))

        print('Creating block list...')
        self._available = LinkedList()
        self._available.fill(int(self._capacity/self._block))
        print('Creating cache...')
        self._cache = {}
        print('Done!')

    def save(self, file_id: str, size: int, size_unit: str) -> list:
        '''
        Takes file_id and saves it in a given location, returns list of block sets that is assigned to the file

        :param file_id: desired file_id as a string
        :param size: size of given file
        :param size_unit: unit of file size. Must be one of B, KB, MB, or GB
        :return: list of blocks that is assigned to the file given
        '''
        if self._cache.get(file_id):
            raise ValueError('file_id already exists')
        if size <= 0:
            raise ValueError('Size must be greater than 0')

        print('Saving file...')
        size = self._to_bytes(size, size_unit)

        if size > self.get_capacity_remaining():
            raise ValueError('Not enough capacity to store file')

        # First fit approach
        location = []
        if self._allocation_algorithm == 'best':
            location = self._allocate_best_location(size)
        else:
            location = self._allocate_first_location(size)
        self._cache_location(file_id, location)
        self._update_capacity_used(self._block * len(location))
        return location

    def delete(self, file_id: str) -> None:
        '''
        Removes allocation for provided file_id, and returns it's assigned blocks to the pool to be re-allocated.

        :param file_id: desired file_id as a string
        '''
        print('Deleting file...')
        location = self._cache.get(file_id)
        if location:
            del(self._cache[file_id])
            self._add_availability(location)
            self._update_capacity_used(-1 * self._block * len(location))
            print('File deleted, blocks ready to be reallocated!')
        else:
            raise ValueError('file_id does not exist')

    def read(self, file_id: str) -> list:
        '''
        Return blocks allocated to file in a list. Uses cache to look up location.

        :param file_id: desired file_id as a string
        :return: list of blocks allocated to the file
        '''
        print('Reading file...')
        location = self._cache.get(file_id)
        if location:
            print('Returning file location!')
            return location
        else:
            raise ValueError('file_id does not exist')

    # Setters and getters. All returned in Bytes
    def get_capacity(self) -> int:
        '''
        Capacity in bytes
        '''
        return self._capacity

    def get_capacity_used(self) -> int:
        '''
        Capacity used in bytes
        '''
        return self._capacity_used

    def get_capacity_remaining(self) -> int:
        '''
        Capacity remaining in bytes
        '''
        return self._capacity - self._capacity_used

    def availability(self) -> str:
        '''
        Blocks that have not been allocated
        '''
        curr = self._available.next
        string = str(curr.val)
        curr = curr.next
        while curr:
            string += ' -> ' + str(curr.val)
            curr = curr.next
        return string

    # Private support functions
    def _allocate_first_location(self, size: int) -> list:
        '''
        Finds first possible location to store file of given size, and allocates it for the file by removing assigned
        chunks from linked list of available nodes. Note: a chunk refers to a group of successive blocks.

        :param size: size of file in bytes
        :return: list of blocks to be allocated to file
        '''
        print('Allocating blocks using first fit...')

        no_error = False  # Cannot use chunk_postend as indicator of no error, as it may be None if last block assigned
        curr = self._available
        chunk_prestart = curr  # Node preceeding chunk
        chunk_postend = None  # Node succeeding chunk
        chunk_size = 0  # Size of current chunk
        while curr.next:
            if self._blocks_are_adjacent(curr.next.val, chunk_prestart.next.val, chunk_size):
                chunk_size += 1
                if chunk_size * self._block >= size:
                    chunk_postend = curr.next.next
                    no_error = True
                    break
            else:  # Nodes not adjacent
                chunk_prestart = curr
                chunk_size = 1
            curr = curr.next  # Update to next as last step so current pointer can be assigned as prestart if needed

        if no_error:  # Sufficient block was found
            first_block = chunk_prestart.next.val

            # Remove allocated blocks from linked list
            chunk_prestart.next = chunk_postend

            print('Blocks allocated!')
            return [x for x in range(first_block, first_block + chunk_size)]
        else:
            raise ValueError('No chunk large enough to be allocated for given size')

    def _allocate_best_location(self, size: int) -> list:
        '''
        Finds best possible location to store file of given size, and allocates it for the file by removing assigned
        chunks from linked list of available nodes. Note: a chunk refers to a group of successive blocks, and best
        location is defined as smallest existing chunk that can be allocated for given size

        :param size: size of file in bytes
        :return: list of blocks to be allocated to file
        '''
        print('Allocating blocks using best fit...')

        chunk_size_needed = math.ceil(size/self._block)

        curr = self._available
        best_chunk_prestart = None
        best_chunk_size = None
        chunk_prestart = curr  # Node preceeding chunk
        chunk_size = 0  # Size of current chunk
        while curr.next:
            if self._blocks_are_adjacent(curr.next.val, chunk_prestart.next.val, chunk_size):
                chunk_size += 1
            else:
                if self._chunk_is_valid_and_better(best_chunk_size, chunk_size, chunk_size_needed):
                    best_chunk_size = chunk_size
                    best_chunk_prestart = chunk_prestart
                if chunk_size == chunk_size_needed:  # Break if perfect size found, no need to keep searching
                    break
                chunk_prestart = curr
                chunk_size = 1
            curr = curr.next

        # Do checks for last chunk (not checked in loop)
        if self._chunk_is_valid_and_better(best_chunk_size, chunk_size, chunk_size_needed):
            best_chunk_size = chunk_size
            best_chunk_prestart = chunk_prestart

        if best_chunk_size and best_chunk_prestart:  # Sufficient block was found
            first_block = best_chunk_prestart.next.val

            # Remove allocated blocks from linked list
            best_chunk_postend = best_chunk_prestart
            for i in range(chunk_size_needed + 1):
                best_chunk_postend = best_chunk_postend.next
            best_chunk_prestart.next = best_chunk_postend

            print('Blocks allocated!')
            return [x for x in range(first_block, first_block + chunk_size_needed)]
        else:
            raise ValueError('No chunk large enough to be allocated for given size')

    def _blocks_are_adjacent(self, block_num: int, prestart_num: int, chunk_size: int):
        return block_num == prestart_num + chunk_size

    def _chunk_is_valid_and_better(self, best_chunk_size: int, chunk_size: int, chunk_size_needed: int):
        return (not best_chunk_size or chunk_size < best_chunk_size) and chunk_size >= chunk_size_needed

    def _cache_location(self, file_id: str, location: list) -> None:
        '''
        Caches file location in instance cache.
        '''
        print('Caching location...')
        self._cache[file_id] = location
        print('Location cached!')

    def _update_capacity_used(self, size: int) -> None:
        '''
        Updates capacity used (either positive or negative size)
        '''
        print('Updating capacity used...')
        self._capacity_used += size
        print('Updated capacity used!')

    def _to_bytes(self, size: int, unit: str) -> int:
        '''
        Translates size to bytes according to given unit
        '''
        conversion_unit = unit.lower()
        if (conversion_unit not in ['b', 'kb', 'mb', 'gb']):
            raise ValueError('Incorrect unit, must be one of b, kb, mb, or gb')

        converted_size = size
        if conversion_unit in ['kb', 'mb', 'gb']:
            converted_size *= 1024
            if conversion_unit in ['mb', 'gb']:
                converted_size *= 1024
                if conversion_unit == 'gb':
                    converted_size *= 1024

        return converted_size

    def _add_availability(self, blocks: list) -> None:
        '''
        Return availability of blocks to the availability linked list.

        :param location: sorted list of blocks to be returned and reallocated
        '''
        # Blocks used by one file always adjacent, so build a linked list
        blocks_linked = LinkedList()
        curr_chunk = blocks_linked
        for block in blocks:
            curr_chunk.next = Node(block)
            curr_chunk = curr_chunk.next

        # Search through availability to find the gap blocks to be returned to
        # Note assumption is linked list will always be sorted in ascending order
        chunk_prestart = self._available  # Node at which chunk should be inserted
        chunk_postend = None  # Sucessive node after chunk
        chunk_min = blocks[0]  # Lowest block in chunk
        chunk_max = blocks[len(blocks)-1]  # Highest block in chunk

        if self._available.next:
            curr = self._available.next
            while curr:
                if chunk_min > curr.val:
                    chunk_prestart = curr
                if chunk_max < curr.val:
                    chunk_postend = curr
                if chunk_prestart and chunk_postend:
                    break
                curr = curr.next

        chunk_prestart.next = blocks_linked.next
        curr_chunk.next = chunk_postend
