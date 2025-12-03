# 🧩 Chess Project — Markdown Summary

## 1. 📦 Deliveries

* **Delivery date:** Undefined
* **Format:** Archive (`zip`, `tar.gz`, `tar.bz2`)
* **Name:** `firstname_lastname-chess.[ext]`
* **Send to:** `bastien.saltel@sucfin.com`
* **Programming language:** Any
* **OS/Architecture:** Any
* **Libraries:** No restrictions
* **Requirements:**

  * Clean and commented code
  * Full documentation
  * Include tests
  * Entirely personal work

---

## 2. 🎯 Aim of the Project

Build a **client/server chess game** over **TCP/IP**, delivering:

### ✔ `chess_server`

```
chess_server [-v] [-i 127.0.0.1] [-p 2000] [-h]
```

* `-v`: Verbose
* `-i`: Bind IP (default `127.0.0.1`)
* `-p`: Listening port (default `2000`)
* `-h`: Help + exit

### ✔ `chess_client`

```
chess_client [-v] [-i 127.0.0.1] [-p 2000] [-f ./gamefile] [-h]
```

* `-v`: Verbose
* `-i`: Server IP
* `-p`: Server port
* `-f`: Input game file
* `-h`: Help

### ✔ Input Game Format

```
a2-a4
h7-h5
// comments allowed
```

Invalid examples:

```
a4-_h
a2a3
a1-e
```

---

## 3. ♟ Interaction Logic

* When client connects → a **new game** starts.
* If `-f` is not provided → client enters **interactive mode**.
* Client sends *moves* to server; server validates and replies with a formatted message.

### Server Response Formats

#### ✓ Normal move

```
X. color piece moves from src to dest
```

#### ✓ Capture

```
X. color piece on src takes color piece on dest
```

#### ✓ Castling

```
X. color king does a [big|little] castling from src to dest
```

#### ✓ Invalid

```
Invalid move
```

#### ✓ Optional check suffix

```
42. white king does a little castling from e1 to g1. Check
```

---

## 4. 📺 Display Board Command

Client can send:

```
display_board
```

Server returns a pretty-printed ASCII chessboard, e.g.:

```
    a   b   c   d   e   f   g   h
  ---------------------------------
8 | r | c | b | q | k | b | c | r |
...
1 | R | C | B | Q | K | B | C | R |
  ---------------------------------
```

* **Uppercase** = white
* **Lowercase** = black
* P/p: Pawn
* C/c: Knight
* Q/q: Queen
* R/r: Rook
* K/k: King
* B/b: Bishop

---

## 5. 🧩 Protocol & Architecture

You are free to design:

* Serialization format (JSON, binary, custom…)
* Packet layout
* Logger design
* Parsers/scanners
* Error handling
* Server architecture

Document & justify your choices.

---

## 6. 🧪 Testing

Include test files under **`test/`** following expected format.

---

## 7. 👥 Multi-Client Extension

Later, add support for **multiple clients**.
You may design commands such as:

* `join_game`
* `start_game`
* `end_game`

Be creative.

---

## 8. 🧱 Project Structure

```
AUTHORS.md       # Your name
bin/             # Executables
conf/            # Config files
doc/             # Documentation
log/             # Log files
src/             # Source code
test/            # Test files
INSTALL.md       # Installation instructions
README.md        # How to run the project
```

---

## 9. 📚 References

* Chess rules: [https://www.chess.com/learn-how-to-play-chess](https://www.chess.com/learn-how-to-play-chess)
* PGN spec: [https://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm](https://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm)