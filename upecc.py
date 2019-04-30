import requests

url = 'http://ec2-34-212-54-152.us-west-2.compute.amazonaws.com' # server url
uid = '305108348' # your uid
resp = requests.post(url + '/session', data = {'uid':uid}) # start new session
body = resp.json()
access_token = body['token'] # retrieve access token from response body
print(access_token)

# while status is not GAME_OVER
# while result is not 1:
#
def explore(dir, cur_row, cur_col):
    global maze
    nextRow = [cur_row + 1, cur_row, cur_row - 1, cur_row]
    nextCol = [cur_col, cur_col - 1, cur_col, cur_col + 1]
    if nextRow[dir] < 0 or nextRow[dir] >= mazeRows:
        return -3
    elif nextCol[dir] < 0 or nextCol[dir] >= mazeColumns:
        return -3
    elif maze[nextRow[dir]][nextCol[dir]] != ' ':
        return -3

    resp = requests.post(url + '/game?token=' + access_token, data = {'action': nextDir[dir]})
    body = resp.json()
    res = body['result']
    if res == "EXPIRED":
        print("*******************EXPIRED")
        quit()

    if  res == 1:
        return 1
    elif res == -1:
        maze[nextRow[dir]][nextCol[dir]] = '*'
        return -1
    elif res == -2:
        return -2
    else:
        maze[nextRow[dir]][nextCol[dir]] = 'v'
        for i in range(4):
            result = explore(i, nextRow[dir], nextCol[dir])
            if result == 1:
                return 1

    # for i in range(len(maze)):
    #     print(maze[i])
    #     print()


    oppDir = (dir + 2) % 4
    resp = requests.post(url + '/game?token=' + access_token, data = {'action': nextDir[oppDir]})
    return 0

while True:
    resp = requests.get(url + '/game?token=' + access_token) # get maze information
    body = resp.json()
    if body['status'] != "PLAYING":
        print(body['status'])
        break
    print("*****************")
    print(body['levels_completed'])
    print("*****************")
    size = body['size']
    print(size)
    mazeRows = size[1]
    mazeColumns = size[0]
    maze = [[' '] * mazeColumns for i in range(mazeRows)]
    currLoc = body['cur_loc']
    currRow = currLoc[1]
    currCol = currLoc[0]
    maze[currRow][currCol] = 'v'
    # 2 arrays for the (r,c) coordinates of the places SOUTH, WEST, NORTH, EAST
    # in that order.
    nextDir = ["down", "left", "up", "right"]
    for i in range(4):
        result = explore(i, currRow, currCol)
        if result == 1:
            print("End reached. starting next level...")
            break
