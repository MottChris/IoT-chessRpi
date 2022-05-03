import helper_function as hf


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]



###### ALL CODE BELOW HERE IS USED TO CREATE THE DIRECTIONAL WEIGHTED GRAPH #####
# includes logic to avoid assigning weights to edge pieces
## Creat weighted directinal graph data strucure for dijstra
## This function is used parse the cleaned game string (output from cleaned_game_str function)
#       to initialize a weighted directional graph. That graph is then used to generate piece 
#       movements based on the eqeclidean distances. 
#  If there is a peice on a node of the graph, that weight is set to 100; this prevents pieces
#       generating paths that go through another piece.

########### STEP 1 ############
## Make new string with 17 x 17 to. 
## We are using 17 x 17 so that there are nodes in between squares for piece movement
###############################
#                           
#                           
#   This represents the 17 x 17 graph     
#   . . . . . . . . . . . . .  
#   . r . k . b . q . k . b .
#   . . . . . . . . . . . . .
#   . p . p . p . p . p . p .
#   . . . . . . . . . . . . .
#
#   given a spot X on the board with all its neighbor nodes...
#   x8      x1      x2  

#   x7      X       x3 
#   
#   x6      x5      x4
#
#   We need to assign the proper weights for each neighbor of X. But this becomes an issue
#       when trying to assign a weight to a neighbor that isn't there (i.e, when the node is on the edge of the board)
#
#   So we will check to make sure the current node is not on the edge of the board before assigning weights
#
#   i = n // 17
#   j = n % 17
#                                                     INVALID MOVED WHEN ON ONE OF THE FOLLOWING
#                                                     [top-rank (i == 0), bottom-rank (i == 17), file-a (j == 0), file-h (j == 17)]
#   X = (i,j)                 | n = n                 [                   ]
#   x8 = (i - 1 , j - 1)      | n = n - 17 - 1        [top-rank, file-a   ]
#   x1 = (i - 1 , j)          | n = n - 17            [top-rank           ]
#   x2 = (i - 1 , j + 1)      | n = n - 17 + 1        [top-rank,    file-h]
#   x3 = (i     , j + 1)      | n = n + 1             [             file-h]
#   x4 = (i + 1 , j + 1)      | n = n + 17 + 1        [bottom-rank, file-h]
#   x5 = (i + 1 , j)          | n = n + 17            [bottom-rank        ]
#   x6 = (i + 1 , j - 1)      | n = n + 17 - 1        [bottom-rank, file-a]
#   x7 = (i     , j - 1)      | n = n - 1             [             file-a]

# checks to see if the current node is on the top rank
def isTopRank(nodeNum):
  if(nodeNum // 17 == 16):
    return True
  else:
    return False

# checks to see if the current node is on the bottom rank
def isBottomRank(nodeNum):
  if(nodeNum // 17 == 0):
    return True
  else:
    return False

# checks to see if the current node is on the A file
def isFileA(nodeNum):
  if nodeNum % 17 == 0:
    return True
  else:
    return False

# Checks to see if the current node is on the H file
def isFileH(nodeNum):
  if nodeNum % 17 == 16:
    return True
  else:
    return False


def getPieceChar(nodeNum, cleaned_graph_str):
  return cleaned_graph_str[nodeNum]

def create_graph(graph, out, board):
  for node in range(288):

    # iterate through all neighbors
    # current_node = 289 - 17 * (node // 17 + 1) + (node % 17)
    current_node = node
    neighbor_node_num = current_node

    # Check to see if current node is on the edge of the board
    isTop = isTopRank(current_node)
    isBottom = isBottomRank(current_node)
    isA = isFileA(current_node)
    isH = isFileH(current_node)

    out = out[::-1]
    ## INDIVIDUALLY GO THROUGH THE 8 POSSIBLE NEIGHBOR SQUARES AND ASSIGN EDGES
    ## MUST CHECK IF THE NODE HAS A PEICE ON IT> IF IT DOES THEN MAKE THE EDGE HAVE MASSIVE WEIGHT
    # top rank : a file
    if(not (isTop or isA)):

      neighbor_node_num = current_node + 17 - 1
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.70716)
      else:
        if((neighbor_node_num // 17 % 2 == 0) ^ (neighbor_node_num % 17 % 2 == 0 )):
          graph.add_edge(current_node, neighbor_node_num, 10)
        else:
          graph.add_edge(current_node, neighbor_node_num, 0.707106)

        # is only top rank
    if(not isTop):
      neighbor_node_num = current_node + 17
      #print(f"Adding Edge top : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.5)
      else:
        graph.add_edge(current_node, neighbor_node_num, 0.5)

    # top rank : h file
    if(not (isTop or isH)):
      #if current_node !=16:
      neighbor_node_num = current_node + 17 + 1
      #print(f"Adding Edge topright : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.707106)
      else:
        if((neighbor_node_num // 17 % 2 == 0) ^ (neighbor_node_num % 17 % 2 == 0 )):
          graph.add_edge(current_node, neighbor_node_num, 10)
        else:
          graph.add_edge(current_node, neighbor_node_num, 0.707106)

    # h file
    if(not isH):
      neighbor_node_num = current_node + 1
      #print(f"Adding Edge right: [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.5)
      else:
        graph.add_edge(current_node, neighbor_node_num, 0.5)

    # h file : bottom
    if(not (isH or isBottom)):
      
      neighbor_node_num = current_node - 17 + 1
      #print(f"Adding Edge bottomright : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.707)
      else:
        if((neighbor_node_num // 17 % 2 == 0) ^ (neighbor_node_num % 17 % 2 == 0 )):
          graph.add_edge(current_node, neighbor_node_num, 10)
        else:
          graph.add_edge(current_node, neighbor_node_num, 0.707106)

    # bottom
    if(not isBottom):
      neighbor_node_num = current_node - 17
      #print(f"Adding Edge bottom : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.5)
      else:
        graph.add_edge(current_node, neighbor_node_num, 0.5)

    # isBottom : is A
    if(not (isBottom or isA)):
      neighbor_node_num = current_node - 17 - 1
      #print(f"Adding Edge bottomleft : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.707101)
      else:
        if((neighbor_node_num // 17 % 2 == 0) ^ (neighbor_node_num % 17 % 2 == 0) ):
          graph.add_edge(current_node, neighbor_node_num, 10)
        else:
          graph.add_edge(current_node, neighbor_node_num, 0.707106)

    # isA
    if(not isA):
      neighbor_node_num = current_node - 1
      #print(f"Adding Edge left : [{current_node}]-->[{neighbor_node_num}]")
      if(hf.node_hasPiece(neighbor_node_num, out, board) == True):
        graph.add_edge(current_node, neighbor_node_num, 100.5)
      else:
        graph.add_edge(current_node, neighbor_node_num, .5)

  return graph