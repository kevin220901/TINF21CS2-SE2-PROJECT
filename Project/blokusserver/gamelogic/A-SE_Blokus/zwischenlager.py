feld = np.zeros([10, 20])

piece = np.array([[1,0,0],[1,0,0],[1,0,0]])

def place_piece(piece, start_x, start_y):
    for x in range(len(piece)):
        for y in range(len(piece[x])):
            feld[y+start_y,x+start_x] = piece[y,x]






test_p = np.array([[0,1,0],[0,1,1],[1,1,0]])

r_piece = pieces["5_9"]
r_piece.print()
r_piece.rotieren()
r_piece.print()
r_piece.rotieren()
r_piece.print()

i_piece = pieces["5_3"]
i_piece.print()
i_piece.rotieren()
i_piece.print()
'''
l_piece = pieces["4_3"]
l_piece.print()
rotated = list(zip(*test_p))[::-1]
print("90°: ",rotated)

rotated = list(zip(*rotated))[::-1]
print("180°: ",rotated)

rotated = list(zip(*rotated))[::-1]
print("270°: ",rotated)
'''
