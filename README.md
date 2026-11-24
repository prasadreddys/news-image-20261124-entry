[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/prasadreddys/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/prasadreddys/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in One Page — 24 November 2026

An entry for the [make.fun](https://make.fun) bounty
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124):
a program that writes one image summing up the world's news of
Tuesday 24 November 2026 to `/output/entry.png`.

The image is a newspaper front page, "THE WORLD IN ONE PAGE", drawn with
Pillow and shipped as `entry.png`:

- **Lead — Iran / Strait of Hormuz:** Iran's Revolutionary Guard says three
  oil tankers hit naval mines and caught fire, one off the south coast and
  two in the east, while under US air escort. The claims are unverified;
  US Central Command has not responded.
- **Korea / Ulleung Island:** five Russian jets enter the defence zone;
  Seoul sounds a 07:52 shelter alert, lifted in minutes. No breach of
  territorial airspace.
- **Markets / Wall Street:** S&P 500 +4.7%, Nasdaq +6.5% as Nvidia brings
  back Jensen Huang; Nvidia shares surge 31%.
- **Europe / Estonia:** Moscow accuses Tallinn of acts "on the verge of
  open war" as Estonia shuts its border from 1 Dec.
- **USA / Congress:** Rep. Jimmy Gomez resigns from 1 Dec after the House
  Ethics Committee finds "substantial evidence" of sexual misconduct.
- **Also today:** the Zaporizhzhia strike, NATO's vow to defend space,
  the Solomon Islands ending its China security pact, reported Russian war
  deaths near 500,000, Gukesh v Sindarov opening in Geneva, and the 2031
  Women's World Cup hosts.

## Run it

```sh
python3 draw_image.py   # redraw entry.png from the fixed design
python3 main.py          # validate entry.png and copy it to /output/entry.png
```

`main.py` (Python 3.13, standard library only) checks the bundled PNG —
signature, every chunk checksum, 1024x1024 size, whole file through IEND,
at most 1 MiB — then copies it unchanged. No network, no clock, no
randomness: two runs write the same bytes.

## Files

- `main.py` — the entry program
- `draw_image.py` — draws `entry.png` from the fixed design
- `entry.png` — the 1024x1024 image the program writes
- `LICENSE` — MIT
