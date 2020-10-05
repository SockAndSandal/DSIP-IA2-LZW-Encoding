# Implementing LZW compression for digital images
 

## test.py

File contains an 8->12 bit encoding. Uses buffers and serious bit manipulation to align and pack bits

## main.py

Does an 8->16 bit encoding. Significantly easier to implement while also achieveing higher compression ratio.


## Comparison between encodings 

rfc3530.txt (LZW really doesn't like working with images).
8->12 bit encoding compresses it from ~60K bytes to ~37K bytes [61.7% of original]
8->16 bit encoding compresses it from ~60k bytes to ~20k bytes [33% of original]

## Conclusion

Don't use python when doing low level bit manipulation or for significantly large programs. Thankfully streamIO can read a single byte at a time after which it's mostly easy to manipulate.

8->12 bit packing is annoying, but not hard. Small use of buffers i.e using a 3 byte buffer to store 2-12 bit codes and flushing buffers makes packing 12 bit codes into 8 manageable. However, it's significantly easier to encode 8 bits to 16 bits and you get the added bonus of increasing table size from 4096 -> 65,636. 4096 takes lesser space but for any file above a trivial size you'll end up doing multiple dictionary resets.
