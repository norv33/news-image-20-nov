[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/norv33/news-image-20-nov/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/norv33/news-image-20-nov/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World — 20 November 2026

A single image that sums up Friday 20 November 2026 in world news:
a wire-desk poster with the day's six most consequential stories,
an also-today line, and a "by the numbers" strip.

Entry for the make.fun bounty
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — run it twice and compare sha256: identical.
```

To redraw the image from scratch (needs Python 3 + Pillow):

```sh
python3 draw.py   # writes entry.png (1024x1024, < 1 MiB)
```

## The six stories

1. **Trump pushes Iran war decision to 2027** — the US president
   says there is no rush and he will "see what happens" after
   1 January. (Reuters; The Times of India)
2. **Europe ready to talk to Russia on Ukraine** — European leaders
   say they are open to negotiations to end the war, after a summit
   in Berlin. (BBC News)
3. **Cyclone Akvan: 300,000 evacuated in India** — a severe storm
   bears down on the Odisha coast; 423 rescue teams deployed as
   landfall nears. (The Hindu)
4. **GTA 6 sales pass $1.8 billion** — Rockstar's blockbuster
   overtakes The Odyssey's global box-office run within days of
   launch. (Mezha and others)
5. **Van Gogh sells for a record $190.4m** — a painting with a
   disputed Nazi-era past fetches a record price at auction.
   (BBC News)
6. **Dozens missing as migrant boat sinks** — a boat carrying about
   100 people capsizes off Senegal; four bodies recovered so far.
   (BBC News)

Also today: India v New Zealand Test opens in Wellington; Haiti
police kill 34 gang members in a Port-au-Prince raid.

By the numbers: 300,000 evacuated ahead of Cyclone Akvan · $1.8bn
GTA 6 sales · $190.4m record Van Gogh · ~100 aboard the Senegal
boat · 2027, Trump's Iran decision.

## Design

A wire-desk poster on warm white paper: "THE WORLD IN ONE DAY"
in huge black type, the date "FRIDAY, 20 NOVEMBER 2026" in red
under a red rule, six white cards with thick black borders in a
2×3 grid — each with a coloured tag, a big coloured story number
and a two-line headline — then a black "BY THE NUMBERS" strip.
This design is original to this entry and deliberately different
from the 17 November entry (cream broadsheet, crimson serif
masthead), the 18 November entry (navy-and-amber world map,
breaking-news dark) and the 19 November entry (deep-green
storyboard cards, ivory broadsheet, navy timeline).

## How it works

`entry.png` (1024×1024, drawn with Python PIL and Liberation fonts
by `draw.py`, kept local) is the image. `main.ts` (Node 22, stdlib
only) validates it first — the first 8 bytes must match the PNG
signature, the file must be at most 1 MiB, and the IHDR dimensions
at most 1024×1024 — then writes it atomically to
`$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`: the bytes go
to a temporary file in the output directory, then rename over
`entry.png`, so a failed run never leaves a truncated image behind.
Running it twice produces byte-identical output.
