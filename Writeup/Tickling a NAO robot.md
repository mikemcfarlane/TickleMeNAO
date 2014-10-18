## Tickling a NAO robot ##

Why would I want to tickle a robot? It's fun for a start. And as far as I know a robot has never been tickled before. The TickleMeNAO app began life at the [2013 UK NAO Hackathon](http://www.uknao.com/2013-london-hackathon) hosted at [Queen Mary University London](http://www.qmul.ac.uk/) as a joint project between three developers who wanted to work on tickling a robot. During the hackathon we got a basic version working and came _second_ at the hackathon. 

I have continued working on TickleMeNAO to enhance the functionality. This is an overview of the key parts of the software.

## Software design ##

I wanted the robot to react to being tickled in a similar way to people being tickled. [YouTube tickling videos](https://www.youtube.com/results?search_query=tickle) provided the main inspiration! There is a high degree of randomness of movement, sounds and words when people are being tickled but there is also an underlying centring of that random movement around the area being tickled. For example, when a foot is tickled the whole body may respond but the main movement will be the foot. 

I would like to have run some form of [Video motion analysis](https://en.wikipedia.org/wiki/Video_motion_analysis) on the videos to gain a deeper understanding of any patterns within the tickle movements. At this early stage in the app I based my movement design on observations.

I also wanted the tickling to be part of a simple game to encourage people to tickle NAO more. 

## Introducing controlled randomness with Markov Chains ##

I love randomness and [probability theory within robotics](http://www.probabilistic-robotics.org/) and technology. I like the idea of robots acting without every move being programmed so they act in interesting and [emergent](https://en.wikipedia.org/wiki/Emergence) ways. Randomness, probability theory and machine learning allow this.

[Markov Chains](https://en.wikipedia.org/wiki/Markov_chain) are a simple but powerful method that uses a table of probabilities, called a [_transition matrix_](https://en.wikipedia.org/wiki/Transition_matrix), to calculate the probability of the next action the system should do based on the current action. It is possible for systems to learn their own transition matrix. I chose to hand code the transition matrices to keep the system simple. Video motion analysis could be used to create more _realistic_ transition matrices.

## Initial attempts ##

The first iteration of the software design tried to reflect the centring of the movement around the area being tickled with each robot body area being animated independently. I also tried to write the code as a framework that would allow the tickle behaviour to run with other behaviours and emotional models to create a full and natural robot behaviour. This would have worked by each behaviour and model independently calculating it's own motion, then using the data structure that I created, the motions could have been blended to create a single motion animation that the robot would follow. 

This got too complex, coupled with my inexperience as a developer, resulting in a halt! I scrapped the first version of the code and started again building the software one function at a time. A bit more [_agile_](https://en.wikipedia.org/wiki/Agile_software_development)! I also decided to remove the centring of the movement around the area being tickled for the first iteration. Each area of the robot system still acts independently and randomly but based of a single transition matrix so tickling the hand would be the same as tickling the foot.

## Markov Choice ##

The current markovChoice function looks like:

    def markovChoice(self, inMatrix):
        """ Chooses a value from a Markov transition matrix.

        """
        randNum = np.random.random()
        cum = 0
        sumMatrix = np.sum(inMatrix)


        if not abs(sumMatrix - 1.0) < 1e-10:
            raise ValueError("Not a p array")
        else:
            for index, probability in enumerate(inMatrix):
                cum += probability
                if cum > randNum:
                    return index

where inMatrix is a transition matrix. The function returns an index for the next state that the robot should do.

## Data design ##

I have used [numpy](http://www.numpy.org/) to hold and process data arrays for speed. Each system in the robot will typically have a transition matrix and a dictionary of _actions_. The index returned by _markovChoice()_ provides the index for the transition matrix and the dictionary key. For example, the tickle sounds:


        self.transitionMatrixWord = np.array([[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
                                            [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01]]
                                            )

        self.wordDictionary = {0 : 'ha',
                                1 : "ha ha",
                                2 : "he",
                                3 : "he he",
                                4 : "he he he",
                                5 : "ho",
                                6 : "ho ho",
                                7 : "Fookin hell that tickles me!"
                            }

Motion is handled slightly differently, see below, but an example transition matrix might be:

        self.transitionMatrixAction = np.array([[0.25, 0.25, 0.25, 0.25],
                                                [0.25, 0.25, 0.25, 0.25],
                                                [0.25, 0.25, 0.25, 0.25],
                                                [0.25, 0.25, 0.25, 0.25]]
                                                )

## Summary of choices made ##

+ self.currentStateWord = 0 # Word said when tickled.
+ self.currentStateActionLeftArm = 0    # Left arm movement when tickled.
+ self.currentStateActionRightArm = 0    # Right arm movement when tickled.
+ self.currentStateInvite = 0    # Phrases said when inviting user to tickle.
+ self.currentStateLEDs = 0    # Eye colour change when tickled.
+ self.currentStateWalk = 0    # Whether to walk and how to walk when tickled.
+ self.currentTickleTarget = 0    # NAOs current tickly spot.
+ self.currentStateTickleSuccessPre = 0    # First part of phrase when NAO successfully tickled.
+ self.currentStateTickleSuccessPost = 0    # Second part of phrase when NAO successfully tickled. 
+ self.currentStateTickleAgain = 0    # Phrases said to reinitiate tickling.
+ self.currentStateGameWinPraise = 0     # Phrases said when tickling game won.
+ self.currentStateGameWinAnimation = 0    # Animation motion to run when game won.    
+ self.currentStateGameLost = 0    # Phrases to say if game lost.

## Robot motion ##

There are three core ways I identified to move/animate the robot through the Python API:

+ [Joint control](https://community.aldebaran.com/doc/2-1/naoqi/motion/control-joint.html#control-joint)
+ [Cartesian control](https://community.aldebaran.com/doc/2-1/naoqi/motion/control-cartesian.html#control-cartesian)
+ [Whole body](https://community.aldebaran.com/doc/2-1/naoqi/motion/control-wholebody.html#control-wholebody)

I choose to use _joint control_ as I could record animations in Choregraph then export them as Python code to animate with angleInterpolation(). This gives good quality motions, dependent on the quality of the animations I record in Choregraph of course. It is also easy to manipulate the timing of this data to change the motion and to combine data from each independent system (e.g. right arm + left arm) to create a single set of motion data for the whole robot.

I would like to further investigate _whole body_ motion as this provides very fluid and natural movement at the expense of more complex maths and programming.

An example of the Python motion data exported from Choregraph after cleaning up for the arm might be:

    # Move left arm left right.
    leftArmMovementList0 = [

                ["LElbowRoll",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [-0.335904, -0.308292, -0.269942, -0.283748, -0.19631, -0.1733, -0.079726]],

                ["LElbowYaw",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [-1.19963, -1.20116, -1.18736, -1.08305, -1.12293, -1.11219, -1.11833]],

                ["LHand",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [0.2952, 0.2952, 0.2952, 0.2952, 0.2952, 0.2952, 0.2952]],

                ["LShoulderPitch",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [0.892746, 0.87127, 1.00933, 1.01393, 1.02927, 1.04615, 1.14125]],

                ["LShoulderRoll",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [0.110406, 0.478566, -0.0629361, -0.30991, 0.082794, 0.41107, -0.0798099]],

                ["LWristYaw",
                [0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2],
                [-0.377406, -1.30241, 0.191708, 0.960242, -0.599836, 0.582878, -0.314512]]
                ]

There are four potential states in the transitionMatrixAction transition matrix. So four sets of motion are needed. For the left arm example above, there are four such sets of data combined into a single list:

    leftArmMovementList = [leftArmMovementList0, leftArmMovementList1, leftArmMovementList2, leftArmMovementList3]

The index returned by _markovChoice()_ provides an index to this movement list. Each movement system has such a randomly chosen movement list. After all the markovChoices are made then the motion data is combined and executed with:

    id = robotMotionProxy.post.angleInterpolation()
    robotMotionProxy.wait(id, 0)

## Sound design ##

Sounds and phrases are randomly chosen each time they are needed using _markovChoice()_. naoqi 2.0 brings [_ALAnimatedSpeech_](https://community.aldebaran.com/doc/2-1/naoqi/audio/alanimatedspeech.html#alanimatedspeech) which adds contextual body language to any words spoken by the robot creating a more lifelike speech delivery. Here, any words or phrases coming from markovChoice() are chosen and combined as necessary then:

    sayPhrase = "thing to say"
    configuration = {"bodyLanguageMode":"contextual"}
    id = animatedSpeechProxy.post.say(sayPhrase, configuration)
    animatedSpeechProxy.wait(id, 0)

I really like the way that NAO delivers speech using _ALAnimatedSpeech_ but I have experienced problems with phrases stalling mid sentence. Documentation suggests _ALAnimatedSpeech_ requires a wait before use to ensure full control of robot resources.

## Game design ##

TickleMeNAO runs as a simple game to encourage engagement with the game and test memory. This could be more complex and engaging. As a first attempt the game is:

1. If NAO successfully tickled then give a code number.
2. When NAO successfully tickled three times ask the player to repeat the three digit code.
3. If code correctly said then play a success animation, sound and phrase.
4. Play again.

With thanks to Aldebaran Robotics for the current success animations from the animation library.

## The trouble with concurrency! ##

Running multiple processes trying to move the robot and say phrases quickly created concurrency problems in the game. And there are current issues with ALAnimatedSpeech stalling mid-sentence potentially due to this. I looked at a number of ways to deal with concurrency in TickleMeNAO. In short summary these are:

+ Mutexes.
+ Thread locks.
+ Thread library.
+ Multiprocessing library.
+ Writing better code that functions as a state machine.
+ Using queues e.g. a speech queue where each speech generating function submits the phrase to the queue and a single process deal with saying what is in the queue.

Clearly this was something I should have designed up front in the code design process. I tried a number of approaches which are detailed in my [Concurrency iPython notebook](http://nbviewer.ipython.org/github/mikemcfarlane/Code_sprints/blob/master/Concurrency_1/Concurrency_1.ipynb?create=1). Given much of the code was already written I chose to work with mutexes and the naoqi [_post_](https://community.aldebaran.com/doc/2-1/dev/naoqi/index.html?highlight=post) and [_wait_](https://community.aldebaran.com/doc/2-1/naoqi/core/almodule-api.html?highlight=wait#ALModule::wait__iCR.iCR) methods and this has solved many of the problems but not all.

## Next steps ##

It's taken me longer than expected to get the app to this point. I'm going to release the current version and get some feedback before making any other changes and improvements. Beyond the bug fixes, improvements to the app I would like to make are:

+ Improve the individual animations to be more exciting.
+ The app needs to flow a bit better.
+ Voice needs to be slower and more consistent.
+ Maintain position relative to user.
+ Better integration with Autonomous Life, currently disabled to run behavior.
+ Build into the ASK-NAO template for ASK-NAO community.
+ Use camera and ultrasound sensors to add in a _tummy_ tickle spot.
+ Use ear microphones to detect ear tickling.
+ Improve code to deal with concurreny/resource issues.
+ Use _whole body_ motion to create more fluid movements.
+ Re-introduce the centring of the being tickled animation around the area being tickled.
+ Add data logging to better understand how people tickle NAO. Maybe use this for online modification of the transition matrices.
+ Motion analysis of tickling videos to gain a better understanding of tickle movements and use this to redefine motion animations and initial tickle matrices.

## Want to tickle a robot? ##

Download TickleMeNAO from GitHub and give it a go.

## Resources ##

+ [TickleMeNAO idea development iPython notebook.](http://nbviewer.ipython.org/github/mikemcfarlane/TickleMeNAO/blob/master/Idea_Development/TickleMeNAO%20idea%20development.ipynb?create=1)
+ [TickleMeNAO on GitHub.](https://github.com/mikemcfarlane/TickleMeNAO)


[Email me](mailto:mike@mikemcfarlane.co.uk) if you want to be added to the repository.

 