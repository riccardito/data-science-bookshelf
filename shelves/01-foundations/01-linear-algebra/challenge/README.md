# Challenge · photo-compress

**An image is a matrix. How few singular values does it need -- and does that depend on what it shows?**

| Image | Full rank | Rank for 95 % energy | Rank for PSNR 30 dB | Numbers at that rank vs pixels |
|---|---|---|---|---|
| terrain (USGS elevation model) | 344 | 4 | **23** | 12 % |
| photograph (Grace Hopper, US Navy) | 512 | 15 | **88** | 32 % |
| document (an invented Swiss QR bill) | 620 | 2 | **101** | 24 % |

- **Smooth surfaces are low-rank; text is not.** The document holds 95 % of its energy in two
  components -- the white paper -- and still needs rank 101 for 30 dB. Energy and quality disagree by a
  factor of about 6 on the photograph and the terrain, and of 50 on the document.
- **The SVD explains compression but is not a good codec:** JPEG stores the same kind of document
  far smaller at higher quality, because it works on local blocks (book 27, chapter 1).
- **Data:** both images ship with matplotlib (public domain); the bill comes from `ds_toolbox.qrbills`.

Run it: `jupyter nbconvert --to notebook --execute photo-compress.ipynb` -- offline, a few seconds.
The numbers go to [`results.json`](results.json).
