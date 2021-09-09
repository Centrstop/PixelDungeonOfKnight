import random as rnd

class Cell:
    """Class Cell
    
    A helper class for generating a maze
    Stores cell coordinates
    
    """

    def __init__(self, x,y):
        """ Init cell coordinates (x, y) """
        self.x=x
        self.y=y


class Labirint:
    """

    Class for generating a maze
    Generating a maze using the depth-first search algorithm

    """

    wall = 0
    visitedCell = 1
    unvisitedCell = 2

    def __init__(self, size):
        """ init class

        Size parameter sets the size of the field
        
        """
        #size must be odd
        self.height = size[1] if size[1]%2 != 0 else size[1] + 1
        self.width = size[0] if size[0]%2 != 0 else size[0] + 1

        #fill map with initial values
        self._map =[[Labirint.wall for _ in range(self.height)] for _ in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                if i%2 != 0 and j%2 != 0 and i<self.height and j<self.width: 
                    self._map[i][j] = Labirint.unvisitedCell
        
        #choosing starting cell
        current_cell = Cell(1,1)

        #marking cell as visited
        self._map[current_cell.y][current_cell.x] = Labirint.visitedCell

        #create stack for visited cells
        stack = [] 
        while True:
            #find adjacent unvisited cells
            neighbours = self.get_neighbours(current_cell)

            if len(neighbours) != 0:
                #choose random neighboring cell
                next_cell = neighbours[rnd.randrange(0,len(neighbours))]
                stack.append(current_cell)
                #removing the wall between the cells
                self.destroy_wall(current_cell,next_cell)
                #marking cell as visited
                current_cell = next_cell
                self._map[current_cell.y][current_cell.x] = Labirint.visitedCell
            elif len(stack) != 0:
                #if there are no neighboring cells, checking the stack
                current_cell = stack.pop()
            else:
                break

    
    def get_neighbours(self, selectedCell):
        """ Method search neighboring cell """
        up = Cell(selectedCell.x,selectedCell.y-2)
        down =  Cell(selectedCell.x, selectedCell.y+2)
        left = Cell(selectedCell.x-2,selectedCell.y)
        right = Cell(selectedCell.x+2, selectedCell.y)
        all = [up, down, left, right]
        neighbours=[]
        
        for i in range(4):
            if all[i].x > 0 and all[i].x < self.width and all[i].y > 0 and all[i].y < self.height:
                if self._map[all[i].y][all[i].x] !=Labirint.visitedCell:
                    neighbours.append(all[i])
        
        return neighbours

    def destroy_wall(self, firstCell, lastCell):
        """ Method removing wall between cells """
        dx = firstCell.x - lastCell.x
        if dx == 2:
            self._map[firstCell.y][firstCell.x - 1] = Labirint.visitedCell
            return
        elif dx == -2: 
            self._map[firstCell.y][firstCell.x + 1] = Labirint.visitedCell
            return
        dy = firstCell.y - lastCell.y
        if dy == 2: 
            self._map[firstCell.y - 1][firstCell.x] = Labirint.visitedCell
            return
        elif dy == -2:
            self._map[firstCell.y + 1][firstCell.x] = Labirint.visitedCell
            return
    
    def get_labirint(self):
        """ Method get ready maze """
        return self._map

