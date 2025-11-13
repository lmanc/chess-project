import socket
import chess
from src.validation import STRIKE, COMMENT

board = chess.Board()

HOST = '127.0.0.1'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn, conn.makefile('r', encoding='utf-8') as f:
        print(f'Connected by {addr}')
        for line in f:
            line = line.strip()
            if STRIKE.fullmatch(line):
                move = line.replace('-', '')
                move = chess.Move.from_uci(move)
                if board.is_legal(move):
                    print('legal move')
                    board.push(move)
                else:
                    print('illegal move')
            elif COMMENT.fullmatch(line):
                conn.sendall(b'comment')
            else:
                conn.sendall(b'scan error')