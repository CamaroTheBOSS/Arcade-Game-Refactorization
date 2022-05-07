# Arcade-Game-Refactorization

In this project I have fully rewritten my old code I wrote in 2021. After successful refactorization I decided to develop this game and create functional level editor.
Game and level editor has been presented here https://www.youtube.com/watch?v=dV-pDi8bhXI

GAME:
Gameplay is pretty simple. We control red square and we have to go to the green "win" area. In the meantime we should collect as much coins (yellow squares) as
possible and avoid enemies (blue squares). Orange area is the checkpoint. After achieving this area we will be respawning there after our death.

Collisions with walls and green, orange areas:
Collisions with these game elements are detected using image processing. After each move we are testing pixels color in front of our move direction. If pixels are black
its a wall; if green its a win area; if orange its a checkpoint area. This solution has pros and cons. The biggest advantage is simple level creation, we just need
a graphics with level layout and we can play on it. The biggest disadvantage is that we cant to use these colors in creating level background, because they are
interpreted as game objects. Now I think it would be better to create a mask for each level. It could be a great compromiss between simple level creation and
possible bugs due to wrong colors in level's layout png file.

Level editor:
In level editor we can create completely new level with low time cost. We just need to create level layout in pait where black color is wall, green
is win area and orange is checkpoint. Just use these colors in paint:

![image](https://user-images.githubusercontent.com/67116759/167271666-b7b74390-484d-4dd3-b45a-8cc9a0fa6272.png)

Its important to know that level layout size should be 1024x720, because game window is hardcoded, so it works only with this resolution.
After creating a layout we can import it directly in editor. With left mouse button we can drag and drop objects. Right mouse button click creates
selection of the object we clicked. With selected objects we can do more actions. We can delete or, for enemies, we can create a path enemy will
be travelling by adding orange path points. We can change type of the path as well. One type is path where after reaching last point of the path,
enemy back to the start position and continue traveling by this path since its start. Second path type is reverse type where after reaching last
point of the path, enemy go through this path again but reversed.
