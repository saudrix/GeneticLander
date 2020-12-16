# :full_moon: Genetic Lander :new_moon: 
![Supported Python Versions](https://img.shields.io/badge/Python-3.9.0-blue.svg?logo=python&logoColor=white)  ![Made withPygame](https://img.shields.io/badge/Pygame-2.0.0-yellow.svg?logo=python&logoColor=white)  ![GitHub license](https://img.shields.io/badge/License-DTFW-green.svg?logo=GitHub%20Sponsors&logoColor=white)

------

The Genetic Lander repository is made to release the genetic algorithm project of my final year in engineering school. The goal of the project was to use genetics algorithm in some way. So I decided to apply a genetic algorithm at a quite simple problem, landing a lunar exploratory module. Indeed, I think it was a real challenge on one hand to  implement a simplified physics engine and on the other to use it as a base to make a genetic algorithm capable of landing the module in a specific spot.

## Getting started

To use the repository, its quite simple. The code is using python :snake: so you just need it on your machine, then clone the repository. Once it has download on your computer your can run the **LUNAR_LANDER.py**. It will automatically launch the  

## Implementing the physics engine of the Genetic Lander program

### Introduction

The first step in order to make this project was to find out how the heck you can mimic the behavior of  the Lem. To do so, I had to go back in my old physics bases to recall the gravity, speed, accelerations and other simple computations that applies to this problem. 

First, the Lem needed some simple properties, a **position** in the sky which is a vector of two components *($x$ and $y$)*, and so is **velocity**. The Lem also has a **weight** *($16437k$)* and three **engines** than can be turned _on_ or _off_ *(The main engine that allows you to go up and two on the side to direct you on the sides)*.

### Falling

First, I needed to implement gravity it's quite easy the equation states that gravity applies a downward force on a bodies according to the Newton's law:
$$
acc = \frac{G}{m} \Leftrightarrow acc = - g
$$
Where acceleration is a negative vector and g is the constant of gravitation of the planet considered. Here we consider the moon *(g = 1.625m/s²)* but it could easily be change to accommodate for other planets gravitational force. For the sake of this application, it's designed as a vector of two components $(0,-1.625)$ to be easily added to other force vectors that are not only downward but that consist of two components of the space.

### Global movement

#### acceleration

This simple formula can be extended according to the second law of movement that states that the sum of all forces applied to an object are equals to its mass times it's acceleration.  So we consider the sum of all forces applying to the module. The main is the gravity that we discussed earlier, then three forces can be added to the Lem one underneath, one on the left and the last on right if the respective engine is on. This give us:
$$
acc = \sum \overrightarrow F / m
$$
 With forces that can be either G,  or $Vector2(0,47000)$ for the main engine, or  $Vector2(-30000,0)$ and $Vector2(30000,0)$ respectively for the left and right thrusters. Here the effect of **Torque** is not applied and should be added in order to add difficulty to game and add realism to the model. But  rotations of the module implied more complex calculation of force vectors applied to decomposed them on their two axes components regarding the rotation angle. So because the core of the project was **genetic algorithms**, I chose to simplified the physics a bit.

#### velocity

Now that we got the acceleration vector on our two components of the plane, we need to transform it into a speed differential to compute the shift in speed regarding the previous speed at time $\Delta t-1$  and then use this shift in speed to compute the change of position of the module.

We know that acceleration is the derivative of speed and in the same way speed is the differential in position so with some simple :tired_face: computation, we can get to the following equations: 
$$
V_{t+1} = V_t + \overrightarrow{acc} * \Delta t \\
P_{t+1} = P_t + \Delta pos \\
avec\\
\Delta pos = V_t * \Delta t + \frac{\overrightarrow{acc} \times \Delta t ^2}{2}
$$
These three formulas allows us to compute the shift in speed and position. In the simulation, we use a 1 second $\Delta time$ synchronized with the frame-rate.

### Custom vectors 

Well finding out about all this math was fun bun I then realized in order to implement it easily, I needed to implement vectors and specifically vectors of two dimensions. So I designed the class **Vector 2** to accommodate for my vectorial calculations.

This class is designed as follow:

- It takes in two values its **x** and **y** component that if not given are defaulted to zero.
- It can be display with the use of its **\_\_repr\_\_** function

Then I've got a little crazy overriding operators to create custom operation of vectors:

- **\_\_add\_\_** : Allows us two add two vectors or a single float value to the two components of the vector
-  **\_\_sub\_\_** : Allows us to subtract two vectors or a single float value to the two components of the vector
- **\_\_mul\_\_** : Allows to compute either the dot product between two vector or a scalar vector multiplication
- **\_\_truediv\_\_** : Allows us to divide a vector by a floating component 

Adding to this the **\_\_gt\_\_**, **\_\_lt\_\_**, **\_\_eq\_\_**, **\_\_ne\_\_**, **\_\_le\_\_**, **\_\_le\_\_** also allows us to practically use this custom vector class in the physics math and collision detection comparison for exemple.

The **norm** method allows us to compute the norm of a vector and finally the **toTuple** method is used to easily transform a custom *Vector2* in a classic python *Tuple*. 

## Graphics

Then I needed to implement graphics in order to test out all the crazy maths I had done better than in my old console. I decided to use **pygame** because my teacher really loves it. And it was a first, it has been a long time since I had code in python and when I was back in the day I always would use **tkinter** (and hate it all the way). So I thought it was time for a change. I turned up my sleeves and start working on this new graphic engine. I think it went well, I fist designed a **gameWindow** class to encapsulate all my window logic, I also added a **gameObject** class to deal with all the sprite display.

Finally, I've created three main window, The main menu, the game window and the AI window. Due to lack of time and heavy workload, I had no time to really designed the game so I stole some artworks and I decided to go all the way with a retro style in the old Lunar Lander mood.

The result was the following:

![windows](C:\Users\Simon\Downloads\Présentation 1\windows.jpg)

In addition, two simple window have been designed for when a player loose or win.

## The genetics - Nature always finds a way :octopus:

Now that all this base was lay down, I could finally start to use all these bricks to create my genetic algorithm. The most important in genetic algorithms is the way you choose to describe the problem. This can determine whether or not your code will converge on a specific solution or not. After my research on-line, I finally come up with a method that I really liked. It was actually a really simple representation. My module could only do three things: **fire or not his engines**.

#### Genes 

So a **Gene** is simply describe like this:

```python
    def __init__(self, l=False,m=False,r=False):
        self.l = l
        self.m = m
        self.r = r
```

It contains three boolean parameters that describe the state of the Lem engines at any point in time. The Gene class contains a method that randomly create a Gene whit probability of **.5** that a side engine is turned on an a probability of **.4** that its main engine is turned on[^1].  The Gene also has a **mutate** function that allows it to mutate *(i.e. If an engine is turned on turns it off and the opposite)* with a given probability.

#### Chromosomes

Then the **Chromosome** class is really simple, it's only define as follows: 

```python
    def populateRandom(self):
        for i in range(0, self.size):
            g = Gene()
            g.randomize()
            self.genes.append(g)
```

 It contains a certain number of genes that define this specific chromosome. When a chromosome is create at random, it's filled with random genes. Now you can see that each chromosome actually represent a attempt at landing for the Lem, it's a serie of instruction defining what the Lem should do during time.

#### The algorithm

So the main body of the **genetic algorithm** is designed has follow. Its create an initial population of a given size *(actually 40)* that is filled with randomly generated chromosome. Then, we read every **chromosome** in the population. The reading process consist of a loop on every gene. For each gene, the Lem actions are turned on or off and the Lem physics are computed for a $\Delta t$ of one second. We range in every gene and at every step we check the status of the Lem. This status has four options witch each a color code:

- <span style="color:#E1431C">CRASHED ON MOON</span>
- <span style="color:#06498C">CRASHED ON BASE</span>
- <span style="color:#A0E11C">LANDED</span>
- <span style="background:#cccccc; color:white">WANDERED AWAY </span>

Based upon this status, a penalty score is compute. Two things are really important. If the lander **crashed on the moon** we consider the distance between the crash site and the base with a malus to penalize distance and crash. If it **wandered away** not going in the ground, we only consider the distance remaining to base to penalize distance. If the lander **crashed on base** we consider the norm of it's speed vector on landing. So we penalize both high vertical and horizontal speeds. If the module landed successfully then it's score is set to *-1* .

After every evaluation of the population, we order the chromosomes from best to worst and we execute three main actions to crate the next generation.

##### selection

We need to ensure perseverance of good genetic material as in the theory of evolution. I apply a method of elitism meaning each generation, I keep a certain amount of the previous population *(Here the best 40%)* to re-inject it in the new population.

So the first step selection consist on first keeping the best elements of the population. Then we need to choose individual to cross them and create children. For now, I choose the individuals at random with slows down the convergence of the program but is really fast to implement. I simply pick two different chromosome in the population and send them to be the parent of a new child until the population reaches it initial size.

Some other method could be consider to enhance the algorithm capabilities. First even with a simple selection, we should consider that better chromosome have better chance of survival *(meaning transferring their genes to a new generation)*. So in picking at random parents, we should chose with a higher probability the best genes and with fewer chances for the worst ones.

Another way could be to implement a **Roulette wheel** selection method. Where every score of chromosome for a run would be normalized. And the chromosome would be sorted by cumulative values of each chromosome. Then we would draw a random floating number between 0 and 1 and select the fist chromosome with a *cum-sum* superior to this number and we would repeat to select the second parent and so on.

##### Crossing

When two parents are selected, their are then merge or crossed to create a new child chromosome. Here each gene in the chromosome are only composed of boolean value so I couldn't implement a continuous genetic algorithm. In order to cross chromosome, I had two options:

- I could first select a random point to cut in half each chromosome and then swap the parts making two new chromosome one starting with the first parent and ending with the second and the other one doing the opposite.
- What I chose to do was to mix every genes of the two chromosome in a new gene in the child meaning that the new chromosome gene *i* is a mix of properties of the gene *i* of the first parent and the gene *i* of the second parent. This ways also slow the convergence of the algorithm but enhance the exploration capabilities meaning that the algorithm can more easily shift it's path to find the objective.

Here reside a way for improvement. Different crossing methodologies could be implemented in the future and metric must be compute on precision and time to find the best method for this problem and same goes with the mutation process.

##### mutation

When a child is constituted, we once more go through the genes, and every gene as a small chance to mutate. Then we add the mutated *(or not)* child to the new population. We continue these steps until the new population as reached the desired population size.

We repeat this global process until the first chromosome of our population $n$ reaches a score of one meaning the module successfully landed on the objective.

#### Showing results

Once I had done all this work, I had to display the population of chromosome in a way that make more sense than with sprite. So I decided to create a specific window to display the population. Each chromosome is then draw as a line representing all the successive positions of the module during the simulation of this specific genome. Each lined is colored accordingly to the result of the simulation run allowing us to easily see how the algorithm is going. Every population is draw in one go so you can see all chromosome of this specific generation.

## A structure disaster :spaghetti:

Before I end this document, I just want to apologize on behalf of all people that loves proper and clean code. Here because of lack of time, the final code *(for now)* is actually a mess. This mainly comes from the way the project grew in my mind. At first I only wanted to implement a simple genetic algorithm. Then I decided to apply it to moon landing problem. So I had to go about implementing physics and then displaying the result so the first window was born with a very specific structure. Then I started on an other branch of the code to create the genetic core and the display wasn't working anymore so here is an other one coming along. And then I wanted to bring it all together and didn't want to spend hour modifying the underlying structure of each part of the code. So this resulted in a wonderful plate of spaghetti :spaghetti: that I had no time to go back and order as linguine. 

This code organization that I might do at some point would need to be consider as a real game. All window functionalities should be bring together and smooth to accommodate fro every type of displays needs. The architecture of player controls should be centralized and a main game class should includes all the window and navigation logics. This class should contains a single window attribute to be dynamically changed  between the different windows according to the player selection. This wold resolves the actual looping in imports preventing the game from being totally functional and the navigation to loop between windows.

There is work that remains to be done. But the main core of the project is here and is enough regarding the genetic part that was asked. I might come back in the future and remodel the all architecture to clean the code and prevent some heart attacks :heart: to people who like me actually loves code.

[^1]:  This is done because the Lem goal is actually to go down so the main engine shouldn't be on even half the time. This value help the algorithm converge faster in our case.

<p align="center">
    <img src='https://ensc.bordeaux-inp.fr/sites/default/files/upload/page-edito/inp/img/logos/logo.ensc-bxinp.jpg' width=200px height=150px />
</p>

