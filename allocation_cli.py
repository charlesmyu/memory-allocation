import allocation

class AllocationCli():
    def run_cli(self):
        print()
        print('Welcome to the memory-allocation CLI!')
        print('Created by Charles Yu')
        print()

        size, unit = self.obtain_size_and_unit()
        print('Please enter block size in KB: ')
        block = input()
        print('Please select whether first fit or best fit allocation is to be used. Enter one of best or first: ')
        algorithm = input()
        print()

        memory = allocation.Allocation(size, unit, int(block), algorithm)
        exit = False

        print()
        while not exit:
            print('Please select an option using the corresponding number: ')
            print('1) Save file')
            print('2) Read file')
            print('3) Delete file')
            print('4) List files and locations')
            print('5) View unallocated blocks')
            print('6) Exit')

            choice = int(input())

            print()
            if choice == 1:
                file_id = self.obtain_file_id()
                size, unit = self.obtain_size_and_unit()
                print()
                try:
                    location = memory.save(file_id, size, unit)
                    print()
                    print('File located at ' + str(location))
                except ValueError as e:
                    print(e)
                print()
            elif choice == 2:
                file_id = self.obtain_file_id()
                print()
                try:
                    location = memory.read(file_id)
                    print()
                    print('File located at ' + str(location))
                except ValueError as e:
                    print(e)
                print()
            elif choice == 3:
                file_id = self.obtain_file_id()
                print()
                try:
                    memory.delete(file_id)
                except ValueError as e:
                    print(e)
            elif choice == 4:
                print(memory.list_files())
                print()
            elif choice == 5:
                print('Unallocated blocks: ' + memory.availability())
                print()
            elif choice == 6:
                exit = True
            else:
                print('Your choice was not recognized. Please try again.')

        print('Exiting CLI. Thank you!')

    def obtain_file_id(self):
        print('Please enter a file ID: ')
        file_id = input()
        return file_id

    def obtain_size_and_unit(self):
        print('Please enter size in B, KB, MB, or GB: ')
        size = input()
        size = int(size)
        print('Please enter unit used for size: ')
        unit = input()
        unit = unit.lower()
        while unit not in ['b', 'kb', 'mb', 'gb']:
            print('That unit is not valid, size must be one of B, KB, MB, or GB.')
            print('Please enter unit used for size: ')
            unit = input()
            unit = unit.lower()
        return size, unit

if __name__ == '__main__':
    AllocationCli().run_cli()
