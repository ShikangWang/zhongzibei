from req import ActionType
from map import AStar
from resp_anaylise import Info
import numpy as np

Dir2ActionType = [[ActionType.SILENT, ActionType.MOVE_RIGHT,ActionType.MOVE_LEFT],
                  [ActionType.MOVE_DOWN, ActionType.SILENT,ActionType.SILENT],
                  [ActionType.MOVE_UP, ActionType.SILENT,ActionType.SILENT]]
'''方向至ActionType的映射'''

def Get_Dir(routelist):
    dir_x = []
    dir_y = []

    dirlist = []
    for block in routelist:
        dir_x.append(block[0])
    for block in routelist:
        dir_y.append(block[1])
    
    dir_x = np.diff(dir_x)
    dir_y = np.diff(dir_y)

    for i in range(len(dir_x)):
        dirlist.append((dir_x[i],dir_y[i]))
        
    return dirlist
# tar_pos = (0,0)
def GetAction(info:Info) ->ActionType :
    # tar_pos = info.enemy_status['x'],info.enemy_status['y']
    danger_map = info.get_danger_map()
    tar_pos = info.get_worthest_pos(danger_map)
    myAstar = AStar(info, tar_pos)
    routelist = [] #记录搜索到的最优路径
    nextaction = ActionType.SILENT
    if tar_pos == (info.my_status['x'], info.my_status['y']) :
        FirstAction = ActionType.SILENT
        SecondAction = ActionType.PLACED
    elif myAstar.run() == 1:
        routelist = myAstar.get_minroute()
        dirlist = Get_Dir(routelist)
        if len(dirlist) == 1 :
            nextdir = dirlist[0]
            nextaction = Dir2ActionType[nextdir[0]][nextdir[1]]
            FirstAction = nextaction
            SecondAction = ActionType.PLACED
        else :
            nextdir = dirlist[0]
            nextaction = Dir2ActionType[nextdir[0]][nextdir[1]]
            FirstAction = nextaction

            nextdir = dirlist[1]
            nextaction = Dir2ActionType[nextdir[0]][nextdir[1]]
            SecondAction = nextaction
        # print(dirlist)

    else:
        FirstAction = ActionType.SILENT
        SecondAction = ActionType.SILENT


    return FirstAction,SecondAction
