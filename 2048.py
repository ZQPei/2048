import os
import numpy as np
import cv2

class Game(object):
    def __init__(self):
        self.init_board()
        self.dirs = (56,53,52,54)
        self.funs = (self.up, self.down, self.left, self.right)
        # self.board = np.array([[  0, 64  , 8,  16],
        #                         [ 32  , 1024, 128 ,  4] ,
        #                         [  8 , 64 ,  4 ,  2],
        #                         [  1024,  8  , 2  , 4]])
        self.read_img()

    def init_board(self):
        self.board = np.zeros((4,4),dtype=int)
        self.board.ravel()[np.random.choice(16,2)] = np.random.choice((2,4))
        self.points = 0

    def generate(self):
        self.board.ravel()[np.random.choice(np.where(self.board.ravel()==0)[0])] = np.random.choice((2,4))

    def _merge_array(self,array,inverse=False):
        ori_array = array.copy()
        array = array[::-1] if inverse else array
        stack = []
        merge_flag = False
        for i in array:
            if i == 0:
                continue
            if merge_flag == False:
                stack.append(i)
                merge_flag = True
            elif i == stack[-1]:
                stack[-1] *= 2
                merge_flag = False
            else:
                stack.append(i)
        array.fill(0)
        array[:len(stack)] = stack
        array = array[::-1] if inverse else array
        #import pdb; pdb.set_trace()
        changed = False if np.sum(array == ori_array)==4 else True
        return changed
    
    def up(self):
        return True if True in [self._merge_array(self.board[:,i]) for i in range(4)] else False
    def down(self):
        return True if True in [self._merge_array(self.board[:,i],inverse=True) for i in range(4)] else False
    def left(self):
        return True if True in [self._merge_array(self.board[i]) for i in range(4)] else False
    def right(self):
        return True if True in [self._merge_array(self.board[i],inverse=True) for i in range(4)] else False

    def move(self,direction):
        assert direction in ('4','5','6','8'), "wrong direction"

    def is_dead(self):
        ret = False
        if np.sum(self.board>0)==16 and \
            np.sum((self.board.ravel('c')[np.array(range(0,16,2))]-self.board.ravel('c')[np.array(range(1,16,2))])==0)==0 and \
            np.sum((self.board.ravel('f')[np.array(range(0,16,2))]-self.board.ravel('f')[np.array(range(1,16,2))])==0)==0 and \
            np.sum((self.board.ravel('c')[np.array(range(1,16,4))]-self.board.ravel('c')[np.array(range(2,16,4))])==0)==0 and \
            np.sum((self.board.ravel('f')[np.array(range(1,16,4))]-self.board.ravel('f')[np.array(range(2,16,4))])==0)==0:
            ret = True
        return ret

    def read_img(self):
        self.imbase = {}
        self.imbase[0] = cv2.imread('img/0.jpg')
        for i in range(1,16):
            num = 2**i
            self.imbase[num] = cv2.imread('img/{}.jpg'.format(num))
        self.imbase['dead'] = cv2.imread('img/dead.jpg')

    def convert(self):
        self.imout = np.full((450,450,3),255,dtype=np.uint8)
        for i,row in enumerate(self.board):
            xmin = 10*(i+1) + i*100
            xmax = 110*(i+1)
            for j,val in enumerate(row):
                ymin = 10*(j+1) + j*100
                ymax = 110*(j+1)
                #import pdb; pdb.set_trace()
                self.imout[xmin:xmax,ymin:ymax] = self.imbase[val]

    def show(self):
        os.system("cls")
        print(self.board)    

        self.convert()
        cv2.imshow("2048",self.imout)
        self.key = cv2.waitKey(0)
        print(self.key)

    def show_dead(self):
        os.system("cls")
        print(self.board)    
        print("you are dead")

        idx = np.where(self.imbase['dead'][:,:,2]>100)
        self.imout[idx] = self.imbase['dead'][idx]
        #self.imout += self.imbase['dead']
        cv2.imshow("2048",self.imout)
        self.key = cv2.waitKey(0)
        print(self.key)
    
    def start(self):
        while True:
            if not self.is_dead():
                self.show()

                if self.key not in (52,53,54,56):
                    continue
                generate_flag = self.funs[self.dirs.index(self.key)]()
                if generate_flag:
                    self.generate()
            
            else:
                self.show_dead()
                self.init_board()

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()