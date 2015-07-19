# wot-replay
World of Tanks replay parser

# Usage

## Read data
```
import replay
rep = replay.load('test.wotreplay')
vehicles = rep.blocks[0]['vehicles']
```

## Append new chunk
```
import replay
rep = replay.load('test.wotreplay')
rep.add_block({'user-data': 'hello world'})
rep.save('new.wotreplay')  # or rep.to_file('new.wotreplay') or rep.to_string()
```
