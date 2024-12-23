# connect-4
Engine to play connect-4

![Codingame Ranking](./codingame.png)

## Usage

1. Make sure you have Python of version at least 3.11. Check your python version:

```bash
python --version
```

2. Clone this repository.

```bash
git clone https://github.com/nknguyenhc/connect-4.git
```

3. Redirect to the folder containing the cloned repository.

```bash
cd connect-4
```

4. Run the main programme.

```bash
python -m main
```

You can configure the game to your liking in `config.py`.

However, note that the unit tests only passes for the indicated config for `height`, `width`, `connect`, and `steal`.

If you play steal mode, as second player, you can steal the first move from the first player, only for your first move. Key in `0` to steal.
