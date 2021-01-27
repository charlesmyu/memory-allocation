# memory-allocation
This project is meant to simulate allocation of memory to files with a given ID and size (i.e. act as a file manager).
It manages allocation for storage, retrieval, and deletion of files on a storage device. This was created in response
to the File System Challenge provided by Capital One.

## Given Assumptions:
- Storage device has a set capacity, which is divided evenly into blocks of a constant size (e.g. 1 MB capacity split
  into 1024 1 KB blocks)
- Blocks must be written/read in whole (e.g. 1200 byte file requires two 1 KB blocks)

## My Assumptions:
- Blocks allocated for a given file must be adjacent, cannot assign non-adjacent blocks to a given file

## Design Choices
I decided to use a cache to store file locations in order to obtain optimal performance of reads. I also had to decide
between the linked list and bitmap approaches to track empty space, but ended up going with linked list approach despite
the worse deallocation performance as, on average, it saves on space and is more performant during allocation.  

I structured this such that an Allocation object represents a single file manager for a given heap, containing the
appropriate methods and instance variables to manage allocation and deallocation of memory in that heap. Capacity of the
heap and block size are determined during intialization of the Allocation object.

Allocation of memory can be done using two methods: best fit or first fit. First fit finds the first chunk large enough
to accommodate the file size requested. Best fit finds the smallest chunk available that accommodates the requested
file size. The algorithm can be specified using the `allocation_algorithm` parameter during creation of the Allocation
object.

## Testing
Testing script included, run by using `python allocation_test.py` in console. The suite of 40 tests across 5 categories
cover read, save, and delete functions, including testing of appropriate exceptions when conditions are met and testing
of both the first fit and best fit allocation algorithms.

## CLI
A CLI has been included for convenience of manual testing or other needed interactions with the file system manager. Run
`python allocation_cli.py` and follow the instructions given in the CLI.
