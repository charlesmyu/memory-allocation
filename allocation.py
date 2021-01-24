from linked_list import Node, LinkedList

class Allocation:
    def __init__(self, capacity: int, capacity_unit: str, block: int):
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
        '''
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

    def save(self, file_id: str, size: int, size_unit: str) -> []:
        '''
        Takes file_id and saves it in a given location, returns list of block sets that is assigned to the file

        :param file_id: desired file_id as a string
        :param size: size of given file
        :param size_unit: unit of file size. Must be one of B, KB, MB, or GB
        :return: list of blocks that is assigned to the file given
        '''
        if size <= 0:
            raise ValueError('Size must be greater than 0')

        print('Saving file...')
        size = self._to_bytes(size, size_unit)

        if size > self.get_capacity_remaining():
            raise ValueError('Not enough capacity to store file')

        # First fit approach
        location = self._allocate_first_location(size)
        self._cache_location(file_id, location)
        self._update_capacity_used(self._block * len(location))
        return location

    def delete(self, file_id: str):
        '''
        Removes allocation for provided file_id, and returns it to the pool to allow it to be re-allocated.

        :param file_id: desired file_id as a string
        '''
        print('Deleting file...')


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

    # Private support functions
    def _allocate_first_location(self, size: int) -> list:
        '''
        Finds first possible location to store file of given size, and allocates it for the file by removing assigned
        chunks from linked list of available nodes. Note: a chunk refers to a group of successive blocks.

        :param size: size of file in bytes
        :return: list of blocks to be allocated to file
        '''
        print('Allocating blocks using first fit...')

        curr = self._available  # current node
        chunk_prestart = curr  # node preceeding node chunk starts on
        chunk_end = None  # node chunk ends on
        chunk_size = 0  # size of chunk currently being explored
        while curr.next:
            if curr.next.val == chunk_prestart.next.val + chunk_size:
                chunk_size += 1
                if chunk_size * self._block >= size:
                    chunk_end = curr.next.next
                    break
            else:
                chunk_prestart = curr
                chunk_size = 1
            curr = curr.next

        if chunk_end:  # sufficient block was found
            first_block = chunk_prestart.next.val
            chunk_prestart.next = chunk_end
            print('Blocks allocated!')
            return [x for x in range(first_block, first_block + chunk_size)]
        else:
            raise ValueError('No chunk large enough to be allocated for given size')

    def _cache_location(self, file_id: str, location: list):
        '''
        Caches file location in instance cache.
        '''
        print('Caching location...')
        self._cache[file_id] = location
        print('Location cached!')

    def _update_capacity_used(self, size: int):
        '''
        Updates capacity used (either positive or negative size)
        '''
        print('Updating capacity used...')
        self._capacity_used += size
        print('Updated capacity used!')

    def _to_bytes(self, size: int, unit: str) -> int:
        '''
        Translates unit to bytes
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

    def _print_availability(self):
        '''
        For debugging purposes
        '''
        curr = self._available.next
        while curr:
            print(curr.val)
            curr = curr.next
