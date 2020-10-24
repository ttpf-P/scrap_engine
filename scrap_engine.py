#!/usr/bin/env python3
import time
import os

width, height = os.get_terminal_size()


class Map():
    def __init__(self, height=height-1, width=width, background="#", dynfps="on"):
        a="["+width*("'"+background+"',")+"],"
        self.height=height
        self.width=width
        self.dynfps=dynfps
        self.background=background
        exec("self.map=["+height*a+"]")
        self.obs=[]

    def blur_in(self, blurmap):
        for l in range(self.height):
            for i in range(self.width):
                if self.map[l][i] == self.background:
                    self.map[l][i]="\033[37m"+blurmap.map[l][i]+"\033[0m"

    def show(self, init=False):
        try:
            self.out_old
        except:
            self.out_old="test"
        self.out=""
        for arr in self.map:
            for i in arr:
                self.out+=i
            self.out+="\n"
        if self.out_old != self.out or self.dynfps == "off" or init == True:
            print(self.out, end="")
            self.out_old=self.out

class Object():
    def __init__(self, char, state="solid"):
        self.char=char
        self.state=state
        self.added=False

    def add(self, map, x, y):
        for ob in map.obs:
            if ob.x==x and ob.y==y and ob.state=="solid":
                return
        self.backup=map.map[y][x]
        self.x=x
        self.y=y
        map.map[y][x]=self.char
        map.obs.append(self)
        self.map=map
        self.added=True

    def set(self, x, y):
        if self.added == False:
            return
        for ob in self.map.obs:
            if ob.x==x and ob.y==y and ob.state=="solid":
                return
        if x > self.map.width-1 or x < 0:
            return
        if y > self.map.height-1 or y < 0:
            return
        self.map.map[self.y][self.x]=self.backup
        self.backup=self.map.map[y][x]
        self.x=x
        self.y=y
        self.map.map[y][x]=self.char
        for ob in self.map.obs:
            if ob.x==x and ob.y==y and ob.state=="float":
                ob.action()

    def action(self):
        return

    def remove(self):
        self.map.map[self.y][self.x]=self.backup
        for i in range(len(self.map.obs)):
            if self.map.obs[i] == self:
                del self.map.obs[i]
                break
        self.added=False

class ObjectGroup():
    def __init__(self, obs):
        self.obs=obs

    def add(self, ob):
        self.obs.append(ob)

    def move(self, x=0, y=0):
        for ob in self.obs:
            ob.set(ob.x+x, ob.y+y)

    def remove(self):
        for ob in self.obs:
            ob.remove()

class Text(ObjectGroup):
    def __init__(self, text, map, x, y, state="solid"):
        self.obs=[]
        self.x=x
        self.y=y
        for i, char in enumerate(text):
            exec("self.ob_"+str(i)+"=Object(char, state)")
            exec("self.ob_"+str(i)+".add(map, x+i, y)")
            exec("self.obs.append(self.ob_"+str(i)+")")


# map=Map(background=" ")
# ob=Object("i")
# ob2=Object("2")
# ob3=Object("3")
# ob4=Object("3")
# ob5=Object("3")
# ob6=Object("3")
# ob7=Object("3")
# group=ObjectGroup([ob3, ob4, ob5, ob6, ob7])
# ob3.add(map, 2, 2)
# ob4.add(map, 3, 2)
# ob5.add(map, 4, 2)
# ob6.add(map, 5, 2)
# ob7.add(map, 6, 2)
# ob.add(map, 1, 2)
# ob.set(1,2)
# ob2.add(map, 1, 2)
# map.show()
# for i in range(3):
#     time.sleep(1)
#     ob.set(ob.x, ob.y+1)
#     map.show()
# group.move(2,3)
# map.show()
# group.remove()
# map.show()
