#Othello Game

import pygame
import sys
from gymnasium.spaces import MultiDiscrete

pygame.init()

#Classes


#############################################################################################################################################

class OthelloDisplay():
    
    def __init__(self, display_width = 800, display_height = 600, fps=30):
        # Initialise the game.
        
        #Display the caption on top of the window.
        pygame.display.set_caption("Othello Game (an implementation of the popular game also known as Reversi)")

        #Set the window width and the window height.
        self.display_width = display_width
        self.display_height = display_height

        #Make the screen.
        self.Screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.Background = pygame.Surface(self.Screen.get_size())
        self.Background.fill((255, 255, 255))
        self.Background = self.Background.convert()
        self.Screen.blit(self.Background, (0,0))

        #Set the Clock.
        self.Clock = pygame.time.Clock()  
        self.fps = fps

        #Define the colors
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.cellgreen = (0,230,0)

    #Draw text on anew surface.
    def CreateText(self, text, Font):
        textSurface = Font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    #To display the welcome message and the heading.
    def WelcomeMessageDisplay(self, text):
        Font = pygame.font.SysFont('freesansbold.tiff',50)
        TextSurf, TextRect = self.CreateText(text, Font)
        TextRect.center = (430,30)
        self.Background.blit(TextSurf, TextRect)

    #To display the choices the user has.
    def ChoiceDisplay(self, text, xcenter, ycenter):
        Font = pygame.font.SysFont('timesnewroman',30)
        TextSurf, TextRect = self.CreateText(text, Font)
        TextRect.center = (xcenter, ycenter)
        self.Background.blit(TextSurf, TextRect)

    #To dislay the disc choice buttons in the welcome screen.
    def DiscChoiceButtons(self):
        
        MousePos = pygame.mouse.get_pos()

        #Create white button
        WhiteButton = pygame.Surface((100,100))
        
        if 250 < MousePos[0] < 350 and 350 < MousePos[1] < 450:
            WhiteButton.fill((0,0,200))
        else:
            WhiteButton.fill((0,200,0))
        
        WhiteButton = WhiteButton.convert()
        self.Background.blit(WhiteButton, (250, 350))
        self.ChoiceDisplay('White', 300,400)


        #Create black button
        
        BlackButton = pygame.Surface((100,100))
        

        if 500 < MousePos[0] < 550 and 350 < MousePos[1] < 450:
            BlackButton.fill((0,0,200))
        else:
            BlackButton.fill((0,200,0))
        
        BlackButton = BlackButton.convert()
        self.Background.blit(BlackButton, (500, 350))
        self.ChoiceDisplay('Black', 550,400)

    #To activate the disc choice buttons in the welcome screen.
    def  ActivateButton(self, x, y):
        #Activate white button
    
        if 250 < x < 350 and 350 < y < 450:
            return 'W'
  
        #Activate Black Button

        if 500 < x < 550 and 350 < y < 450:
            return 'B'
        
        return ' '

    #The welcome screen loop.       
    def WelcomeScreen(self):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Welcome to Othello')
            self.ChoiceDisplay('Please choose the color of your disc', 430,200)
            self.DiscChoiceButtons()
            
            

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT: #Player presses QUIT-button.
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos
                    PlayerDisc = ' '
                    PlayerDisc = self.ActivateButton(x,y)
                    
                    if (PlayerDisc == 'W') or (PlayerDisc == 'B'):
                        MainLoop = False
                        return PlayerDisc
                    else:
                        MainLoop = True


            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))

    #To create cells in the board.
    def CreateCell(self, radius, cellcolor, disccolor, x, y):

        MousePos = pygame.mouse.get_pos()
        
        Cell = pygame.Surface((2*radius,2*radius))
        
        if x < MousePos[0] < x + 2*radius and y < MousePos[1] < y + 2*radius:
            Cell.fill((0,0,200))
        else:
            Cell.fill(cellcolor)
            pygame.draw.rect(Cell, self.black, [0,0,2*radius, 2*radius], 3)
            pygame.draw.circle(Cell, disccolor, (radius, radius), radius-5)
        
        Cell = Cell.convert()
        self.Background.blit(Cell, ( x, y))
       

    #To create the game board.
    def CreateBoard(self, Board):

        for i in range(8):
            for j in range (8):
                if Board[i][j] == 'W':
                    self.CreateCell(20, self.cellgreen, self.white, x=15 + j*40, y=50 + i*40)
                elif Board[i][j] == 'B':
                    self.CreateCell(20, self.cellgreen, self.black, x=15 + j*40, y=50 + i*40)
                else:
                    self.CreateCell(20, self.cellgreen, self.cellgreen, x=15 + j*40, y=50 + i*40)


    #To display the game screen.
    def GameScreen(self, Board, Score):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Othello Game')
            self.ShowPoints(Score)
            self.DisplayMessage('Please make a move.')
            self.ExitButton()
            self.HintButton()
            self.CreateBoard(Board) 

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos

                    Move = [-1,-1]
                    self.CreateBoard(Board)
                    Move = self.ModifyBoard(x,y, Board)
                    i = Move[0]
                    j = Move[1]
                    if (i in range(8)) and (j in range(8)):
                        MainLoop = False
                        return Move
                    else:
                        MainLoop = True
                    
                    Exit = ' '
                    Exit = self.ActivateExitButton(x,y)
                    if Exit == 'Exit':
                        MainLoop = False
                        return 'Exit'
                    else:
                        MainLoop = True
                    
                    Hint = ' '
                    Hint = self.ActivateHintButton(x,y)
                    if Hint == 'Hint':
                        MainLoop = False
                        return 'Hint'
                    else:
                        MainLoop = True

            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))

    #To show the current points.
    def ShowPoints(self, Score):
        Font = pygame.font.SysFont('mono',19)
        TextSurf, TextRect = self.CreateText("WhiteScore: " + str(Score['W']) + " BlackScore: " + str(Score['B']), Font)
        TextRect.center = (570,60)
        self.Background.blit(TextSurf, TextRect)

    #To display the desired message.
    def DisplayMessage(self, text):
        Font = pygame.font.SysFont('mono',19)
        TextSurf, TextRect = self.CreateText(text, Font)
        TextRect.center = (450,80)
        self.Background.blit(TextSurf, TextRect)

    #To display the exit button.
    def ExitButton(self):
        
        MousePos = pygame.mouse.get_pos()
        
        ExitButton = pygame.Surface((150,50))
        
        if 400 < MousePos[0] < 550 and 100 < MousePos[1] < 150:
            ExitButton.fill((0,0,200))
        else:
            ExitButton.fill((0,200,0))
        
        ExitButton = ExitButton.convert()
        self.Background.blit(ExitButton, (400, 100))
        self.ChoiceDisplay('Exit Game', 475,125)

    #To activate the exit button.
    def  ActivateExitButton(self, x, y):
        if 400 < x < 550 and 100 < y < 150:
            return 'Exit'

    #To display the hint button.
    def HintButton(self):
        
        MousePos = pygame.mouse.get_pos()
        
        HintButton = pygame.Surface((150,50))
        
        if 600 < MousePos[0] < 750 and 100 < MousePos[1] < 150:
            HintButton.fill((0,0,200))
        else:
            HintButton.fill((0,200,0))
        
        HintButton = HintButton.convert()
        self.Background.blit(HintButton, (600, 100))
        self.ChoiceDisplay('Get Hint', 675,125)

    #To activate the hint button.
    def  ActivateHintButton(self, x, y):
        if 600 < x < 750 and 100 < y < 150:
            return 'Hint'

    #To display the continue button.
    def ContinuePlayingButton(self):
        
        MousePos = pygame.mouse.get_pos()
        
        ContinuePlayingButton = pygame.Surface((250,50))
        
        if 500 < MousePos[0] < 750 and 200 < MousePos[1] < 250:
            ContinuePlayingButton.fill((0,0,200))
        else:
            ContinuePlayingButton.fill((0,200,0))
        
        ContinuePlayingButton = ContinuePlayingButton.convert()
        self.Background.blit(ContinuePlayingButton, (500, 200))
        self.ChoiceDisplay('Continue Playing', 630,225)

    #To activate the continue button.
    def  ActivateContinuePlayingButton(self, x, y):
        if 500 < x < 750 and 200 < y < 250:
            return 'Continue Playing'    

    #To activate the board.
    def ModifyBoard(self,cx,cy, Board):
        radius = 20
        cellcolor = self.cellgreen
        disccolor = self.black
        for i in range(8):
            for j in range (8):
                Cell = pygame.Surface((2*radius,2*radius))
                Cell.fill(cellcolor)
                pygame.draw.rect(Cell, self.black, [0,0,2*radius, 2*radius], 3)
                pygame.draw.circle(Cell, disccolor, (radius, radius), radius-5)
                x=15 + j*40
                y=50 + i*40

                if x < cx < x + 2*radius and y < cy < y + 2*radius:

                    if Board[i][j] == ' ':
                        Cell = Cell.convert()
                        self.Background.blit(Cell, ( x, y))
                        return [i,j]
                        
        return [-1,-1]
                    
    #To display the intermediate screen for the hint.
    def IntermediateScreen(self, TemporaryBoard, LegalMoves, Score):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Othello Game')
            self.ShowPoints(Score)
            self.DisplayMessage('Please make a move.')
            self.ContinuePlayingButton()
            self.CreateHintBoard(TemporaryBoard, LegalMoves)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos
    
                    ContinuePlaying = ' '
                    ContinuePlaying = self.ActivateContinuePlayingButton(x,y)
                    if ContinuePlaying == 'Continue Playing':
                        MainLoop = False
                        return ContinuePlaying
                    else:
                        MainLoop = True
                    

            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))
        
    #To create the hint board.
    def CreateHintBoard(self,TemporaryBoard, LegalMoves):

        for i in range(8):
            for j in range (8):
                if TemporaryBoard[i][j] == 'W':
                    self.CreateCell(20, self.cellgreen, self.white, x=15 + j*40, y=50 + i*40)
                elif TemporaryBoard[i][j] == 'B':
                    self.CreateCell(20, self.cellgreen, self.black, x=15 + j*40, y=50 + i*40)
                elif [i,j] in LegalMoves:
                    self.CreateCell(20, self.cellgreen, (255,255,0), x=15 + j*40, y=50 + i*40)
                else:
                    self.CreateCell(20, self.cellgreen, self.cellgreen, x=15 + j*40, y=50 + i*40)


    #To display the illegal move screen
    def IllegalMoveScreen(self, TemporaryBoard, Score):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Othello Game')
            self.ShowPoints(Score)
            self.DisplayMessage('Illegal move.')
            self.ContinuePlayingButton()
            self.CreateBoard(TemporaryBoard)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos
    
                    ContinuePlaying = ' '
                    ContinuePlaying = self.ActivateContinuePlayingButton(x,y)
                    if ContinuePlaying == 'Continue Playing':
                        MainLoop = False
                        return ContinuePlaying
                    else:
                        MainLoop = True
                    

            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))


    #To display the final screen.
    def FinalScreen(self, TemporaryBoard, Score):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Othello Game')
            self.ShowPoints(Score)
            if Score['W'] > Score['B']:
                self.DisplayMessage('White Wins')
            elif Score['W'] < Score['B']:
                self.DisplayMessage('Black Wins')
            else:
                self.DisplayMessage('Game has Tied')
            self.ExitButton()
            self.CreateBoard(TemporaryBoard)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos

                    Exit = ' '
                    Exit = self.ActivateExitButton(x,y)
                    if Exit == 'Exit':
                        MainLoop = False
                        return Exit
                    else:
                        MainLoop = True
                    
            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))

    #To display the screen after the computer made a move.
    def SeeComputerMoveScreen(self, TemporaryBoard, Score):
        MainLoop = True #The mainloop

        while MainLoop:

            self.Clock.tick(self.fps)
            self.WelcomeMessageDisplay('Othello Game')
            self.ShowPoints(Score)
            self.DisplayMessage("Your Move is:")
            self.ContinuePlayingButton()
            self.CreateBoard(TemporaryBoard)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    MainLoop = False
                    return 'Exit'
                elif Event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = Event.pos

                    ContinuePlaying = ' '
                    ContinuePlaying = self.ActivateContinuePlayingButton(x,y)
                    if ContinuePlaying == 'Continue Playing':
                        MainLoop = False
                        return ContinuePlaying
                    else:
                        MainLoop = True
                    
            pygame.display.update()
            self.Screen.blit(self.Background, (0,0))


          
#############################################################################################################################################

class OthelloBoardArray():
   
    def __init__ (self, Disc):

        '''
        Board is like:
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']                                
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        '''

        self.Board = [[' '] * 8 for i in range(8)]
        self.Board[3][3], self.Board[4][4] = 'W', 'W'
        self.Board[3][4], self.Board[4][3] = 'B', 'B'

        #Setting the player's disc.
        self.PlayerDisc = Disc
        
    #Creatin a temporary board.
    def MakeTempBoard(self, GivenBoard):
        TempBoard = [[' '] * 8 for i in range(8)]
        for i in range(8):
            for j in range(8):
                TempBoard[i][j] = GivenBoard[i][j]

        return TempBoard
                
            
    #Check if the move is legal and return the cells to be filled if it so.
    def isLegalMove(self, Disc, CellLocation, GivenBoard):

        # Setting the discs
        if Disc == 'W':
            OpponentDisc = 'B'
        else:
            OpponentDisc = 'W'

        # Creating the board directions
        EightDirections = []
        
        for i in range(-1,2):
            for j in range(-1,2):
                EightDirections.append([i,j])

        EightDirections.remove([0,0])

        #Creating an array to store the locations of cells to be flipped.
        CellsToBeFlipped = []

        #Checking all the Directions
        for Direction in EightDirections:
            
            XDirection = Direction[0]
            YDirection = Direction[1]
            x = CellLocation[0]
            y = CellLocation[1]

            x = x + XDirection
            y = y + YDirection

            TempCellStorage = []

            while(((x in range(8)) and (y in range(8))) and GivenBoard[x][y]==OpponentDisc):
                TempCellStorage.append([x,y])

                x = x + XDirection
                y = y + YDirection

                if not((x in range(8)) and (y in range(8))) or (GivenBoard[x][y]==' '):
                    TempCellStorage.clear()
                    break

                if (GivenBoard[x][y]==Disc):
                    break


            CellsToBeFlipped.extend(TempCellStorage)

        if len(CellsToBeFlipped) == 0:
            return 'False'
        else:
            return CellsToBeFlipped

    #Find all possible legal moves.
    def FindAllLegalMoves(self, Disc, GivenBoard):
        
        LegalMoves = []
        
        for i in range(8):
            for j in range(8):
                if (GivenBoard[i][j] == ' ') and (self.isLegalMove(Disc, [i,j], GivenBoard) != 'False'):
                    LegalMoves.append([i,j])

        return LegalMoves

    #Calculate the score.
    def CalculateScore(self, GivenBoard):

        WhiteScore, BlackScore = 0,0

        for i in range(8):
            for j in range(8):
                if (GivenBoard[i][j]=='W'):
                    WhiteScore += 1
                if(GivenBoard[i][j]=='B'):
                    BlackScore += 1

        return {'W': WhiteScore,'B': BlackScore}

    #Update the Board.
    def UpdateBoard(self, GivenBoard, CellsToBeFlipped):

        for Cell in CellsToBeFlipped:
            x = Cell[0]
            y = Cell[1]
            if GivenBoard[x][y] == 'W':
                GivenBoard[x][y] = 'B'
            else:
                GivenBoard[x][y] = 'W'

        return  GivenBoard

    #Check if the move is a corner move.
    def isCornerMove(self, x, y):
        return (x == 0 or x == 7) and (y == 0 or y == 7)


    #Choose the move for the computer.
    def ChooseComputerMove(self, Disc, GivenBoard):
        # Setting the discs
        if Disc == 'W':
            OpponentDisc = 'B'
        else:
            OpponentDisc = 'W'

        LegalMoves = self.FindAllLegalMoves(OpponentDisc, GivenBoard)

        MaxScore = 0
        MaxMove = [-1,-1]

        for Move in LegalMoves:
            x = Move[0]
            y = Move[1]

            if self.isCornerMove(x, y):
                MaxMove = [x,y]
                break

            TempBoard = self.MakeTempBoard(GivenBoard)
            TempBoard[x][y] = OpponentDisc
            CellsToBeFlipped = self.isLegalMove(OpponentDisc, Move, TempBoard)
            #print(CellsToBeFlipped)
            #return [-1,-1]
            TempBoard = self.UpdateBoard(TempBoard, CellsToBeFlipped)
            Score = self.CalculateScore(TempBoard)
            
            if Score[OpponentDisc] > MaxScore:
                MaxScore = Score[OpponentDisc]
                MaxMove = Move

        return MaxMove


#############################################################################################################################################


OpeningScreen = OthelloDisplay()
PlayerDisc = OpeningScreen.WelcomeScreen()
if PlayerDisc == 'W':
    ComputerDisc = 'B'
else:
    ComputerDisc = 'W'

Turn = 'Player'

OthelloGame = OthelloBoardArray(PlayerDisc)
OthelloBoard = OthelloGame.Board


while True:
    if PlayerDisc == 'Exit':
        pygame.quit()
        break
    
    if Turn == 'Player':
        GameDisplay = OthelloDisplay()
        Score = OthelloGame.CalculateScore(OthelloBoard)
        Move = GameDisplay.GameScreen(OthelloBoard, Score) # update gamescreen(self, score)

        if Move == 'Exit':
            #print("Exit")
            pygame.quit()
            break
        elif Move == 'Hint':
            TemporaryBoard = OthelloBoard
            LegalMoves = OthelloGame.FindAllLegalMoves(PlayerDisc, TemporaryBoard)
            IntermediateDisplay = OthelloDisplay()
            Move = IntermediateDisplay.IntermediateScreen(TemporaryBoard, LegalMoves, Score)
            if Move == 'Continue Playing':
                #print ("Hello")
                continue
            if Move == 'Exit':
                pygame.quit()
                break
        else:
            CellsToBeFlipped = OthelloGame.isLegalMove(PlayerDisc, Move, OthelloBoard)
            if (CellsToBeFlipped == 'False'):
                IllegalMoveDisplay = OthelloDisplay()
                Move = IllegalMoveDisplay.IllegalMoveScreen(OthelloBoard, Score)
                if Move == 'Continue Playing':
                    #print ("Hello")
                    continue
                if Move == 'Exit':
                    pygame.quit()
                    break

            else:
                x = Move[0]
                y = Move[1]
                OthelloBoard[x][y] = PlayerDisc
                OthelloBoard = OthelloGame.UpdateBoard(OthelloBoard, CellsToBeFlipped)
                Score = OthelloGame.CalculateScore(OthelloBoard)
                
                LegalMoves = OthelloGame.FindAllLegalMoves(ComputerDisc, OthelloBoard)

                if len(LegalMoves) == 0:
                    FinalDisplay = OthelloDisplay()
                    Move = FinalDisplay.FinalScreen(OthelloBoard, Score)
                    if Move == 'Exit':
                        pygame.quit()
                        break
                else:
                    ToSeeComputerMove = OthelloDisplay()
                    Move = ToSeeComputerMove.SeeComputerMoveScreen(OthelloBoard, Score)
                    if Move == 'Continue Playing':
                        #print ("Hello")
                        Turn = 'Computer'
                        continue
                    if Move == 'Exit':
                        pygame.quit()
                        break

    else:
        ComputerMove = OthelloGame.ChooseComputerMove(PlayerDisc, OthelloBoard)
        #break
        x = ComputerMove[0]
        y = ComputerMove[1]
        OthelloBoard[x][y] = ComputerDisc
        CellsToBeFlipped = OthelloGame.isLegalMove(ComputerDisc, ComputerMove, OthelloBoard)
        #print(CellsToBeFlipped)
        OthelloBoard = OthelloGame.UpdateBoard(OthelloBoard, CellsToBeFlipped)

        LegalMoves = OthelloGame.FindAllLegalMoves(PlayerDisc, OthelloBoard)

        if len(LegalMoves) == 0:
            FinalDisplay = OthelloDisplay()
            Move = FinalDisplay.FinalScreen(OthelloBoard, Score)
            if Move == 'Exit':
                pygame.quit()
                break
        else:
            Turn = 'Player'
        

pygame.quit()
