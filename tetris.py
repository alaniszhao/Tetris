
from cmu_112_graphics import *

#Tetris

#draw functions
def drawFallingPiece(app,canvas): #draws current falling piece
    for row in range(len(app.fallingPiece)): #loops thru rows
        for col in range(len(app.fallingPiece[0])): #loops through cols
            if(app.fallingPiece[row][col]): #draws square if true
                drawCell(app,canvas,app.fallingPieceRow+row,
                app.fallingPieceCol+col,app.fallingPieceColor)

def drawScore(app,canvas): #draws curr score
    width=app.cols*app.cellSize+2*app.margin
    canvas.create_text(width/2, app.margin/2,text='Score: '+str(app.score))

def drawBoard(app, canvas): #draws board
    if(app.isGameOver):
        drawGameOver(app,canvas)
    height=app.rows*app.cellSize+2*app.margin
    width=app.cols*app.cellSize+2*app.margin
    canvas.create_rectangle(0,0,width,height,fill='orange')
    for currRow in range(len(app.board)): #goes cell by cell
        for currCol in range(len(app.board[0])):
            drawCell(app,canvas,currRow,currCol,app.board[currRow][currCol])

def drawGameOver(app,canvas): #draws game over sign
    height=app.rows*app.cellSize+2*app.margin
    width=app.cols*app.cellSize+2*app.margin
    canvas.create_rectangle(0,height/2.5,width,height/1.7,fill='white')
    canvas.create_text(width/2,height/2,text='Game Over',
                       fill='pink', font='Helvetica 26 bold underline')

def drawCell(app,canvas,row,col,color): #draws cell given parameters
    x1=app.margin+col*app.cellSize
    y1=app.margin+row*app.cellSize
    x2=x1+app.cellSize
    y2=y1+app.cellSize
    canvas.create_rectangle(x1,y1,x2,y2,fill=color,width=3)

def redrawAll(app,canvas): #draws all draw fxns
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    drawScore(app,canvas)
    if(app.isGameOver):
        drawGameOver(app,canvas)

#controller functions
def gameDimensions(): #sets size of game
    rows=15
    cols=10
    cellSize=20
    margin=25
    return rows,cols,cellSize,margin

def newFallingPiece(app): #creates random new falling piece
    import random
    randomIndex=random.randint(0,len(app.tetrisPieces)-1)
    app.fallingPiece=app.tetrisPieces[randomIndex]
    app.fallingPieceColor=app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow=0
    app.fallingPieceCol=app.cols//2-len(app.fallingPiece[0])//2

def placeFallingPiece(app): #draws falling piece in app
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col]):
                c=app.fallingPieceColor
                app.board[app.fallingPieceRow+row][app.fallingPieceCol+col]=c
    removeFullRows(app) #removes any full rows

def moveFallingPiece(app,drow,dcol): #moves falling piece L R or down
    app.fallingPieceRow+=drow
    app.fallingPieceCol+=dcol
    if(fallingPieceIsLegal(app)==False): #undo if illegal move
        app.fallingPieceRow-=drow
        app.fallingPieceCol-=dcol
        return False
    return True #returns if it was a legal move

def rotateFallingPiece(app): #rotates the falling piece
    oldPiece=copy.deepcopy(app.fallingPiece)
    oldRow=app.fallingPieceRow
    oldCol=app.fallingPieceCol
    newRows=len(oldPiece[0])
    newCols=len(oldPiece)
    new2D=[]
    for row in range(newRows): #creates new empty piece
        newRow=[]
        for col in range(newCols):
            newRow.append(None)
        new2D.append(newRow)
        newRow=[]
    currCol=0
    for row in range(newCols): #switches values of old piece to new one
        currRow=copy.copy(oldPiece[row])
        currRow.reverse()
        for newRow in range(newRows):
            new2D[newRow][currCol]=currRow[newRow]
        currCol+=1
    app.fallingPiece=new2D
    if(fallingPieceIsLegal(app)==False): #undo if move was illegal
        app.fallingPiece=oldPiece
        return
    newRow=oldRow+newCols//2-newRows//2
    newCol=oldCol+newRows//2-newCols//2
    app.fallingPieceRow=newRow #changes start row and col of piece
    app.fallingPieceCol=newCol
    if(fallingPieceIsLegal(app)==False): #undo if move was illegal
        app.fallingPieceRow=oldRow
        app.fallingPieceCol=oldCol
        app.fallingPiece=oldPiece
    
def fallingPieceIsLegal(app): #checks if piece in legal location
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col]!=False):
                if (app.fallingPieceRow+row<0 or app.fallingPieceRow+row>=
                    app.rows):
                    return False #if row is in bounds
                if (app.fallingPieceCol+col<0 or app.fallingPieceCol+col>=
                    app.cols):
                    return False #if col in bounds
                if(app.board[app.fallingPieceRow+row][app.fallingPieceCol+col]
                    !='blue'):
                    return False #if cell is taken
    return True    

def removeFullRows(app): #removes full rows
    fullRows=0
    newBoard=[]
    notBlues=0
    for row in range(len(app.board)): #checks all cell colors
        for col in range(len(app.board[0])):
            if(app.board[row][col]=='blue'):
                newBoard.append(app.board[row])
                break
            notBlues+=1
        if(notBlues==len(app.board[0])): #full row if all colors not blue
            fullRows+=1
        notBlues=0
    fullRow=[]
    for i in range(len(app.board[0])): #creates empty row
        fullRow+=['blue']
    for i in range(fullRows): #inserts correct num of empty rows
        newBoard.insert(0,fullRow)
    app.board=newBoard
    app.score+=fullRows**2 #adds to score

def appStarted(app): #initiates tetris
    app.timerDelay = 250
    app.score=0
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.board=[]
    app.isGameOver=False
    for row in range(app.rows): #creates empty board
        currRow = []
        for col in range(app.cols):
            currRow+=['blue']
        app.board.append(currRow)
        currRow=[]
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],[  True,  True,  True ]]
    lPiece = [[ False, False,  True ],[  True,  True,  True ]]
    oPiece = [[  True,  True ],[  True,  True ]]
    sPiece = [[ False,  True,  True ],[  True,  True, False ]]
    tPiece = [[ False,  True, False ],[  True,  True,  True ]]
    zPiece = [[  True,  True, False ],[ False,  True,  True ]]
    app.tetrisPieces=[iPiece,jPiece,lPiece,oPiece,sPiece,tPiece,zPiece]
    app.tetrisPieceColors=["red","yellow","magenta","pink","cyan","green"
                            ,"orange"]
    newFallingPiece(app) #starts new falling piece

def keyPressed(app, event): #controls
    if event.key=='r': #restarts
            appStarted(app)
    if(app.isGameOver!=True):
        if event.key=='Up': #rotates piece
            rotateFallingPiece(app)
        if event.key=='Down': #moves down 1 cell
            moveFallingPiece(app,1,0)
        if event.key=='Left': #moves left 1 cell
            moveFallingPiece(app,0,-1)
        if event.key=='Right': #moves right one cell
            moveFallingPiece(app,0,1) 
        if event.key=='Space': #hard drops piece
            hardDrop(app)

def hardDrop(app): #moves piece as far down as possible
    while (moveFallingPiece(app,1,0)==True):
        moveFallingPiece(app,1,0)

def timerFired(app): #runs timed fuctions
    if(app.isGameOver==False):
        if(moveFallingPiece(app,+1,0)==False): #moves and places legal piece
            placeFallingPiece(app)
            newFallingPiece(app)
            if(moveFallingPiece(app,+1,0)==False): #ends game if no legal moves
                app.isGameOver=True

def playTetris(): #runs tetris
    rows,cols,cellSize,margin=gameDimensions()
    w = cols*cellSize+2*margin
    h = rows*cellSize+2*margin
    runApp(width=w, height=h)

# main

def main():
    playTetris()

if __name__ == '__main__':
    main()
