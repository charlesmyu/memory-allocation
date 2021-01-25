# memory-allocation
This project is used to simulate allocation of memory to files with a given ID and size. It manages allocation for
storage, retrieval, and deletion of files on a storage device. This was created in response to the File System Challenge
provided by Capital One.

## Given Assumptions:
- Storage device has a set capacity, which is divided evenly into blocks of a constant size (e.g. 1 MB capacity split
  into 1024 1 KB blocks)
- Blocks must be written/read in whole (e.g. 1200 byte file requires two 1 KB blocks)

## My Assumptions:
- Blocks allocated for a given file must be adjacent

## Design Choices
Decided to use cache to store file locations in order to obtain optimal performance of reads. Was deciding between
linked list and bitmap approach to track empty space, went with linked list approach despite worse deallocation
performance as, on average, it saves on space, and is more performant during allocation.  

Structured such that an Allocation object represents a single file manager for a given heap, containing the appropriate
methods and instance variables to manage allocation and deallocation of memory in that heap. Capacity of the heap and
block size are determined during intialization of the Allocation object.

Allocation of memory can be done using two methods: best fit or first fit. First fit finds the first chunk large enough
to accommodate the file size requested. Best fit finds the smallest chunk available that accommodates the requested
file size. The algorithm can be specified using the `allocation_algorithm` parameter during creation of the Allocation
object.

## Testing
Testing script included, run by using `python allocation_test.py` in console. Tests cover read, save, and delete
functions, including testing of appropriate exceptions when conditions are met.

## CLI
A CLI has been included for manual testing or other interaction with the file system manager. Run
`python allocation_cli.py` and follow the instructions to use.
