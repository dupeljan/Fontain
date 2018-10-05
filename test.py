#!/usr/bin/env python
import numpy as np
string = "123"

samples = np.fromstring(string, dtype=np.dtype( [ ( 'f' , 'i2' ) , ('l', 'i1')]))

print(samples)
res = np.int32( samples["f"] )

print(np.binary_repr(res[0], width=32)) 
res = res << 8
print(np.binary_repr(res[0], width=32))
res += samples["l"]
print(np.binary_repr(res[0], width=32))
