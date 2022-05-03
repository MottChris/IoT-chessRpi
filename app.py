#!/usr/bin/env python3
import chess
import time
import sys
import dijkstar as djk
import helper_function as hf
import Graph
from stockfish import Stockfish
import chess.engine
import serial
import time


## Firebase Config
import pyrebase

config = {
    "apiKey" : "AIzaSyA-aoU16El2xsvxKyctepp2lr6Yj6wmbKA",
    "authDomain" : "iot-final-project-7ea84.firebaseapp.com",
    "databaseURL" : "https://iot-final-project-7ea84-default-rtdb.firebaseio.com/",
    "storageBucket" : "iot-final-project-7ea84.appspot.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()

## FIREBASE DATA 

move_queue = []

def stream_handler(message):
    print(message)
    move_queue.append(message["data"])
    ## add message["data"] to move_queue

my_stream = db.child("move").stream(stream_handler)

# User sign in somehow #

engine = chess.engine.SimpleEngine.popen_uci("/home/pi/Documents/stockfish_15_android_armv8/stockfish_15_src/src/stockfish")
limit = chess.engine.Limit(time = 2.0)

# Arduino serial connection
if __name__ == '__main__':
 ser = serial.Serial('/dev/ttyACM0', 9600)
 ser.reset_input_buffer()

def getNodeCoordsStr(node):
    return f'{node % 17},{node // 17}'

board = chess.Board()

## Change this to While True:
while True:
  if(len(move_queue) != 0):
    
    move = move_queue.pop(0)
    print(board)
    legal_moves = str(board.legal_moves)
    print(str(board.legal_moves))
    # User Move
    #move = input("Make white move: ")
    print(f'WHITE MADE MOVE: {move}')
    board.push_san(move)

    # populate the graph with new game state
    dijk_graph = djk.Graph()
    cleaned_str = hf.clean_board_str(str(board))
    print(f"cleaned str{cleaned_str}")
    print(board)
    
    graph = Graph.create_graph(dijk_graph, board)
    #time.sleep(1)

    engine_move = str(engine.play(board, limit).move)
    print(f'engine UCI: {engine_move}')
    # e4e5
    # Determine if the move is attacking
    fromNode, tonNode =  hf.UCItoNodeNums(engine_move)
    parsed_square = chess.parse_square(engine_move[-2:])
    if(board.piece_at(parsed_square)):
        ## Ensure graph is up to date
        print("GOING INTO MOVE")
        ## Generate path for nonNode to jail zone
        path = djk.find_path(graph, tonNode, 119)
        ## call arduino serial commands to make the moves
        command_bytes = str.encode("M" + getNodeCoordsStr(path.nodes[0]))
        ser.write(command_bytes + b"\n")
        print("M" + getNodeCoordsStr(path.nodes[0]))
    
        # wait for response from serial comm.
        tdata = ser.read().decode("utf-8")  
        data_left = ser.inWaiting()  # Get the number of characters ready to be read
        tdata += ser.read(data_left).decode("utf-8")
        print(f'{tdata} received.')

        #ser.flush()
        tdata = ""
        # raise magnet up to the board
        command_bytes = str.encode("S1")
        ser.write(command_bytes + b"\n")
        print("S1")
        
        # wait for response
        tdata = ser.read().decode("utf-8")  
        data_left = ser.inWaiting()  # Get the number of characters ready to be read
        tdata += ser.read(data_left).decode("utf-8")
        print(f'{tdata} received.')
        tdata = ""
        #ser.flush()

        # loop through the rest of the moves
        for node in path.nodes[1:]:
            tdata = ""
            print("M" + getNodeCoordsStr(node))
            command_bytes = str.encode("M" + getNodeCoordsStr(node))
            ser.write(command_bytes + b"\n")

            tdata = ser.read().decode("utf-8")  
            data_left = ser.inWaiting()  # Get the number of characters ready to be read
            tdata += ser.read(data_left).decode("utf-8")
            print(f'{tdata} received.')
            #ser.flush()

        print("S0")
        command_bytes = str.encode("S0")
        ser.write(command_bytes + b"\n")

        tdata = ""
        tdata = ser.read().decode("utf-8")  
        data_left = ser.inWaiting()  # Get the number of characters ready to be read
        tdata += ser.read(data_left).decode("utf-8")
        print(f'{tdata} received.')



    board.push_uci(engine_move)

    print(board)
    #engine.quit()
    # get node nums for the move
    
    # get proper nodes from engine move
    fromNode, tonNode =  hf.UCItoNodeNums(engine_move)

    path = djk.find_path(graph, fromNode, tonNode)
    print("PATH INFO:")
    print(path)
    print(path.nodes)

    command_bytes = str.encode("M" + getNodeCoordsStr(path.nodes[0]))
    ser.write(command_bytes + b"\n")
    print("M" + getNodeCoordsStr(path.nodes[0]))
    
    # wait for response from serial comm.
    tdata = ser.read().decode("utf-8")  
    data_left = ser.inWaiting()  # Get the number of characters ready to be read
    tdata += ser.read(data_left).decode("utf-8")
    print(f'{tdata} received.')

    #ser.flush()
    tdata = ""
    # raise magnet up to the board
    command_bytes = str.encode("S1")
    ser.write(command_bytes + b"\n")
    print("S1")
    
    # wait for response
    tdata = ser.read().decode("utf-8")  
    data_left = ser.inWaiting()  # Get the number of characters ready to be read
    tdata += ser.read(data_left).decode("utf-8")
    print(f'{tdata} received.')
    tdata = ""
    #ser.flush()

    # loop through the rest of the moves
    for node in path.nodes[1:]:
        tdata = ""
        print("M" + getNodeCoordsStr(node))
        command_bytes = str.encode("M" + getNodeCoordsStr(node))
        ser.write(command_bytes + b"\n")

        tdata = ser.read().decode("utf-8")  
        data_left = ser.inWaiting()  # Get the number of characters ready to be read
        tdata += ser.read(data_left).decode("utf-8")
        print(f'{tdata} received.')
        #ser.flush()

    print("S0")
    command_bytes = str.encode("S0")
    ser.write(command_bytes + b"\n")

    tdata = ""
    tdata = ser.read().decode("utf-8")  
    data_left = ser.inWaiting()  # Get the number of characters ready to be read
    tdata += ser.read(data_left).decode("utf-8")
    print(f'{tdata} received.')
    #ser.flush()