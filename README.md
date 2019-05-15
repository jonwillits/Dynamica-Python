# Dynamica-Python

Dynamica-python is a project designed to play around with a bunch of ideas related to artificial intelligence. It is an agent-based simulation involving recurrent neural networks, reinforcement learning, genetic algorithms, and all sorts of fun stuff. It all runs in pure python + numpy. So it is slow. But you can play with all sorts of parameters and see if you can evolve yourself a stable and happy population of animals that will learn to eat, have children, and not kill each other.

## Animal Actions
The animals have six action choices on any turn:
<ol>
<li>rest
<li>eat (if there is grass in their current square)
<li>attack (if there is another animal in the square they are facing)
<li>procreate (if there is another same-species, opposite-sex animal in the square they are facing)
<li>turn (rotate to face another square)
<li>move forward into the square they are facing
</ol>

## Animal Drives
Each of these actions have consequences for their three internal drives:
<ol>
  <li>health (which goes down if they are out of energy or are attacked, and heals back to max otherwise)
  <li>energy (which goes down when actions are taken, and goes up if they eat)
  <li>arousal (which goes down if they procreate, and ticks up otherwise)
</ol>

## Animal Learning (both prediction and reinforcement)
Each animal has a neural network inside it with the following architecture:

An input layer with 4 sub-components:
<ol>
  <li>a sensory array that encodes information about their current square, and squares in their field of vision
  <li>a drive array with their current values of health, energy, and arousal
  <li>a "previous action" array giving proprioceptive feedback on what action they took last turn
  <li>an "action argument" array giving information about entities that participated in their action on the previous turn
 </ol>

An output layer with 4 subcomponents:
<ol>
  <li>a sensory prediction array, where the network forcasts what its sensory state will be on the next turn
  <li>a drive prediction array, where the network forecasts what its drive state will be on the next turn
  <li>an action array, which the network uses to decide what action to take, given the current input
  <li>an action argument array, which the network uses as an argument modifying the action (such as how much to turn if turn is selected as the action, or what to eat if eat is selected as the action
</ol>
  
The input and output layers are connected by a a recurrent hidden layer (technically, the hidden state at time t-1 is an additional sub-component of the input layer, meaning that one of the inputs into the hidden layer is it's own state at the previous time step, like in a simple recurrent network (Elman, 1990).

The network learns in two different ways.

1. prediction learning: the network is trained through backpropogation by comparing each output state to a "target" output state, composed of 
<ol>
  <li>comparing it's prediction about its next sensory state to its actual next sensory state
  <li>comparing its prediction about its next drive state to its actual next drive state
  <li>comparing its action output activation to the actual action that it took (this has the effect of training the network not to try to perform actions that are illegal in the current context, such as attacking or procreating when no patient of that action is present).
  <li>comparing its action argument activation to the actual argument selected. This has the effect of creating attractors for the representation of actual objects that can be patients.
</ol>

2. reinforcement learning: the network is trained through backpropogation that certain outcomes are good or bad. As currently implemented, this all happens via a cost to the output unit for the action the agent just took. For each drive and for each drive delta, a score is computed for how far that drive state or drive delta was from a pre-defined target. That difference is considered the cost/error for that action output unit, and it's weight's are changed accordingly (as well as backpropogated through the hidden layer).

Thus, through the prediction learning in the network, the agents can get good at predicting what the consequences of their actions will be, in terms of changes to their internal and external state. The reinforcement learning teaches the agent that some of these changes are bad and should be punished so that they dont take the actions that led to those changes as often in the future.

## Animal Genotypes and Phenotypes
In addition to this learning via a neural network, there is also a wide range of genetic properties of each animal, including:
<ul> 
<li>sex, ie if the animal is a male or female
<li> size, where big size leads to greater attack strength, but makes actions cost more energy.
<li> appearance, so that animals can learn what their own species looks like, and sex and individual differences in appearance can evolve and participate in learning and behavior
<li> properties of its neural network, such as hidden layer size, learning rates, and weight initializations. This includes biases for certain actions, so that some animals may be predisposed to lovers, and others fights, others eaters, and others lazy bums that just like to rest.
<li> the reinforcement values are all genetically determined. In addition to separate learning rates for learning about prediction, health, energy, and arousal, each animal has a different genetically determined target rate for each drive state. Some animals "want" to have a target energy level of 1.0, others "want" to have a target energy level of 0.2. The former will be positively reinforced for eating almost all the time. The latter may often be punished for eating, if it makes the energy level go above 0.2, that moves it away from the target, and so generates a higher error signal in the learning function. Thus, the agents are not prewired to know that energy and health are good. The population has to evolve to figure out what the optimal level of energy, health, and arousal are.
</ul>
If you double-click on a species in the summary window, it will open a window telling you the initial and current population means for a bunch the variables. So this allow you to see how different traits are evolving in your popoulation.

## Parameters and Successful Ecologies
There are a large number of parameters that can be modified in src/config.py. Many of these are very sensitive and changing them can greatly affect the success of the animal populations. For example:
<ul>
<li>you can change the world size and starting population sizes. If you make the world too big, the zebras will never find each other, and so will probably all starve before they reproduce and the population will die out.
<li>You can change the amount of grass vs. desert vs. water, which obviously matters with regard to starvation.
<li>You can change the animal's metabolism costs (ie how much energy is consumed by each action). This can be set on an action-by-action and drive-by-drive basis in config.Animal.action_drive_change_dict, or more globally in config.Animal.metabolism.
<li>Some of these parameters don't do much yet, and are there as we get ready to add other animals. Some (like appearance size) have not be tested much at all. Play at your own risk. Or at least at your Zebras' risk.
</ul>

## Coming Soon
<ul>
<li>Performance issues. Everything was coded to be super transparent, and by a scientist, not a professional python programmer. Thus you will notice that with large populations, or with long simulations, speed really craters. This will be improved as we move out of alpha stage. 
<li>Load/save simulation. Obviously it would be useful to be able to do this and we need this functionality.
<li>More information diplays and graphs are coming to better understand what is happening in the simulation. But do remember  that you can double click on an an animal in the main window, or on the species in the summary display, and get more information on individuals or on the population.
<li>Right now the terrain is pretty much randomly generated. It should have a little structure and regularity.
</ul>
</ul>
