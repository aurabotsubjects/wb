# How the handwriting reader was made
- Data: MNIST (public handwritten digits, 60k train / 10k held-out test), expanded with thick, slanted, wobbly variants and a "not a clean digit" class (scribbles, crossed-out, merged digits).
- Model: small CNN (~47k weights, int8) embedded in index.html. Trained with JAX (`train.py`), exported by `export.py`.
- Held-out results: 98.3% on original MNIST test digits; ~97% on the harder augmented test set (incl. scribble class).
- End-to-end test (`test_browser.py`): simulated 10x10 sheets run through the real in-app code. See the chat summary for numbers.
- Not tested on real students' writing.

> **Note:** the 5 Minute Frenzy is now answered by typing on an on-screen keypad and marked exactly, so this handwriting reader is no longer used by `index.html`. These files are kept only for reference (`test_browser.py` no longer runs against the current app).
