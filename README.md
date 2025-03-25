# order book manager

### Data structure selection
- after api research we need to maintain to dicts, one for bids, one for asks
- in general the most efficient data structure to hold key(price) - value(supply) structure is hashmap aka dict
- we can use just dict because main focus is update speed, but sorting will make fast calculations on spread, so it seems a like cheating to use just dict :)
- now we need to select best way to create and update sorted, key-value structure 
  - option one - some kind of balanced tree(red-black(my favorite), AVL, etc)
    - main disadvantage is slow speed on updates
  - option two - sortedcontainers libs
    - main reason to choose is [better](https://grantjenks.com/docs/sortedcontainers/performance.html) performance in testing
    - it is well known and supported python library with great performance
- so i choose sortedcontainers for performance and simplicity of use

### Scheduler
- easiest and best way to implement scheduler is to use APScheduler
- but I fell that it can be better to do in manually in this case

### Some possible improvements
- I find my class structure a bit to heavy for such task
- It can be harder to use this code if we add additional subclasses for connectors and storages(calculation depends on storage) 
