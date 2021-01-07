# Pathfinding using A* Algorithm

A mini-game visualization of A* Algorithm in Python 3 using PyGame.
Requirement: Pygame, pygame-menu

#### Free Run
Visualization of A* algorithm. Start, Destination and obstacles can be manually created.  

- Clicking Left Mouse Button for the first time creates the starting grid.
- Clicking Left Mouse Button for the second time creates the destination grid.
- Clicking Left Mouse Button for the third time creates barrier grid.
- Right Mouse Button removes cells created.
- Escape button resets all grid.
- Press SPACEBAR after creating all the cells to draw the path

#### Google Map
A Sample visualization of Google Map. A section of map is created using [SnazzyMap](https://snazzymaps.com/editor). Then I have used my utility program [PathDrawer](https://github.com/akshayhari/Path_Drawer) to create paths in grid format. Then the A* algorithm is used to find the shortest path in the map.

How to Run:
- Clicking Left Mouse Button for the first time creates the starting grid.
- Clicking Left Mouse Button for the second time creates the destination grid.
- Escape button resets all grid.
- Press SPACEBAR to draw the path

Note:
- Requires pyGame and pygame-menu module.
- Paths can be straight line as well as diagonal. 
- Contains global variables which, I understand, are very bad. :/ 
- Beginner level code. Not in coding standards.  
- Might have some bugs. Haven't done any QA. Let me know if you find any.

Credits:
[PyGame](https://pypi.org/project/pygame/)
[pygame-menu](https://pypi.org/project/pygame-menu/)
Map data ©2019 Google
