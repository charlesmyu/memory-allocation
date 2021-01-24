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

Decided to use cache to obtain optimal performance of reads, as it only requires the location to be pulled from the
hashtable. Had to decide between linked list and bitmap approach to track empty space, went with linked list approach
despite worse deallocation performance as it saves on space and is more performant during allocation
