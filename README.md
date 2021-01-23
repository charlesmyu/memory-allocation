# memory-allocation

This project is used to simulate allocation of memory to files with a given ID and size. It manages allocation for storage, retrieval, and deletion of files on a storage device. This was created in response to the File System Challenge provided by Capital One.

## Given Assumptions:
- Storage device has a set capacity, which is divided evenly into blocks of a constant size (e.g. 1 MB capacity split into 1024 1 KB blocks)
- Blocks must be written/read in whole (e.g. 1200 byte file requires two 1 KB blocks)

## My Assumptions:
- Memory is structured linearly
- Blocks allocated for a given file must be adjacent
