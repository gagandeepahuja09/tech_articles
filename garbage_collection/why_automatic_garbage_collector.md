// Arpit bhayani's video: https://www.youtube.com/watch?v=jcMxuLZCcqU

Memory Management Basics

Two possible places to allocate memory:
1) Stack => static memory
2) Heap => dynamic memory

* Stack is automatically garbage collected. Not the case with heap.

Stack
int a = 10;
* Allocates sizeof(int) on stack frame of the program.
* When the function returns, the variable looses its existence as it is popped from the stack. Hence we don't need explicit garbage collection for the variables allocated on stack.

Heap
* Everything that is non-stack and part of RAM.
* Allocating large memory on stack will make the program inefficient as it has a limited memory and passing through functions would be done by value(not address).
* C/C++ way of allocation is using malloc or new keyword.

*************************************************************************************

Why heaps
* Too long or too ineficient to be kept in stack. Eg: large struct or class objects.
* To have dynamically growing objects. Not sure at compile time how much space they'll take. eg: arrays, linkedlists, etc.
* To have multiple functions using the same instance of objects. The two functions could be running in seperate thread or goroutine.

* Objects allocated in the heap are always addressed by reference(pointer).

*************************************************************************************

Explicit Deallocation
* C++ -> free, delete functions.
* It's good that languages provide a method for memory deallocation but we cannot rely on engineers to always delete the memory that they allocated.
* Because
    * they might forget to do so.
    * the path in which deallocation is done might not get invoked due to some error or how the code is written.

*************************************************************************************

What happens if an unused object is not deleted? - Memory Leak
* Memory consumption will increase.
* Once the memory consumption reaches 100% and the process tries to allocate new memory, it crashes.

*************************************************************************************

What happens when an object is freed, but is still referenced(accessed, could be by another thread)?
* This scenario is called dangling pointer. 
* If we dereference a dangling pointer, the results are unpredictable.
* Hence, these scenarios are considered hard to debug.
* In this case, process crashing is a better scenario because unpredictable would be harder to debug.

*************************************************************************************

Advantages of garbage collection
* More reliable => reduces errors from engineering while doing garbage collection.
* Reduces human effort.
* Can have better ways of dealing with dangling pointers.
