#!/usr/bin/env python

from multiagent import *
from scenarios import *
import math
import Tkinter

# msec between updates
MAX_SPEED = 100
MIN_SPEED = 1000
# maximum iterations to run
MAX_ITERS = 1000

# some useful constants
AGENT_ARROW = [(0, -15), (-10, 15), (10, 15)]
#positive rotation is clockwise?
DIRECTION_ANGLE = {'n': 0, 'nw': 315, 'w': 270, 'sw': 225, 's': 180, 'se': 135,
				'e': 90, 'ne': 45}

scenarioList = [#GoalTestScenario(),
		#ObjSenseScenario1(),
		#ObjSenseScenario2(),
		#ObjSenseScenario3(),
		GoalSeekScenario1(),
		GoalSeekScenario2(),
		GoalSeekScenario3(),
                MazeScenario1(),
		AvoidScenario1(),
		AvoidScenario2(),
                AvoidScenario3(),
                AvoidScenario4(),
		HallwayScenario1()]

class RobotCanvas(Tkinter.Canvas):
	def __init__(self, master=None):
		Tkinter.Canvas.__init__(self, master)
		self.drawAgents = True
		self.drawGoals = True
		self.drawGoalBelief = True
		self.drawObjBelief = True
		self.drawMostLikelyExp = False
		self.cellSize = 100
	
	# Point the agent arrow in the correct directionf
	def compute_arrow(self, pose):
		d = pose[2]
		angle = math.radians(DIRECTION_ANGLE[d])
		pts = []
		for x,y in AGENT_ARROW:
			pts.append( (x * math.cos(angle) - y * math.sin(angle),
						y * math.cos(angle) + x * math.sin(angle)) )
		return pts
	
	def draw_agents(self, b):
		self.drawAgents = b
	
	def draw_goals(self, b):
		self.drawGoals = b
	
	def draw_goal_belief(self, b):
		self.drawGoalBelief = b
	
	def draw_obj_belief(self, b):
		self.drawObjBelief = b

	def draw_most_likely_exp(self, b):
		self.drawMostLikelyExp = b
	
	def draw_sim(self, sim, targetAgent):
		# work out position beliefs about other objects
		objs = sim.agents[targetAgent].currentBelief.b_objects
		objpos = {}
		# for each object...
		for obj in objs:
			objpos[obj] = {}
			# compute the sum over the different directions it faces
			#  for each location on the board
			for pose in objs[obj]:
				if pose[:2] not in objpos[obj]:
					objpos[obj][pose[:2]] = 0
				objpos[obj][pose[:2]] += objs[obj][pose]
			norm = max(objpos[obj][p] for p in objpos[obj])
			# this shouldn't happen
			if norm == 0:
				objpos[obj] = {}
			# normalize each location by the maximum over all locations
			for p in objpos[obj]:
				objpos[obj][p] /= norm

		# Draw the board!
		c=self.cellSize
		goalrad = c/10
		# "easterliness"
		for i in range(len(sim.map)):
			# "northerliness"
			for j in range(len(sim.map[i])):
				# If it's a believed goal, make it green
				if sim.agents[targetAgent].currentBelief.b_goal.get((i,j),0)!=0 \
						and self.drawGoalBelief:
					green = 'DE'
				else:
					green = 'BE'
				# Scale its redness by the belief in object positions
				red = 0xBE
				if self.drawObjBelief:
					for obj in objpos:
						if (i,j) in objpos[obj]:
							red += objpos[obj][(i,j)]*(0xFF-0xBE)
				red = min(0xFF, int(red))
				red = hex(red)[2:].upper()
				color = '#' + red + green + 'BE'
				if not sim.map[i][j]:
                                        color = 'black'
				# Draw this location
				self.create_rectangle((i*c, (len(sim.map[i])-j-1)*c,
						(i+1)*c, (len(sim.map[i])-j)*c), fill=color)
				
				# Draw a goal if appropriate
				if (i,j) == sim.agentGoals[targetAgent] and self.drawGoals:
					self.create_oval((i*c+c/2-goalrad, (len(sim.map[i])-j-1)*c+c/2-goalrad,
						i*c+c/2+goalrad, (len(sim.map[i])-j-1)*c+c/2+goalrad), fill='white')
		
		# Draw agents if box is checked
		if self.drawAgents:
			for a in sim.agents:
				pose = sim.currentState[a]
				xbase = pose[0]*c+c/2
				ybase = (len(sim.map[pose[0]])-pose[1]-1)*c+c/2
				pts = []
				for x,y in self.compute_arrow(pose):
					pts.append(x+xbase)
					pts.append(y+ybase)
				self.create_polygon(tuple(pts), fill='darkslategray')
				self.create_text(xbase,ybase+c/4,text=a,font='TkSmallCaptionFont')

                # Draw most likely explanations if checked
                if self.drawMostLikelyExp:
                        h = sim.histories[targetAgent]
                        if len(h) < 3: return
                        agentStates = [h[i][targetAgent] for i in xrange(0,len(h),4)]
                        for obj in sim.agents:
                                if obj == targetAgent: continue
                                objpercepts = [h[i].objectvisible[obj] for i in xrange(2,len(h),4)]
                                objstates = sim.agents[targetAgent].most_likely_trajectory(agentStates[:-1],obj,objpercepts)
                                for pose in objstates:
                                        xbase = pose[0]*c+c/2
                                        ybase = (len(sim.map[pose[0]])-pose[1]-1)*c+c/2
                                        pts = []
                                        for x,y in self.compute_arrow(pose):
                                                pts.append(x+xbase)
                                                pts.append(y+ybase)
                                        pts.append(pts[0])
                                        pts.append(pts[1])
                                        self.create_line(tuple(pts), fill='black')

class RobotApp(Tkinter.Frame):
	def __init__(self, master=None):
		Tkinter.Frame.__init__(self, master)
		self.canvas = None
		self.iters = 0
		self.running = False
		self.step = False
		self.done = False
		self.alarm = None
		self.scenarios = dict((s.NAME,s) for s in scenarioList)
		# Scenario names in display order
		self.scenarioNames = [s.NAME for s in scenarioList]
		self.currentScenario = Tkinter.StringVar()
		self.currentScenario.set(self.scenarioNames[0])
		self.pack()
		# always make_sim(), make_canvas(), make_buttons() in order!
		self.make_sim()
		self.make_canvas()
		self.make_buttons()
		self.reset_buttons()
		self.redraw()
	
	def continue_check(self):
                if self.continue_cond==None: return True
                if isinstance(self.continue_cond,int): return self.iters < self.continue_cond
		return self.continue_cond(self.sim)
	
	def timeout(self):
		if (self.running or self.step) and self.iters < MAX_ITERS \
				and (self.continue_check() or not self.done):
			self.iters += 1
			self.sim.step()
			for a in self.agentRewards:
				if len(self.sim.histories[a]) > 3:
					self.agentRewards[a] += self.sim.histories[a][-3]
			self.rewardString.set('\n'.join(a+" reward accumulated : "+str(r) for a,r in self.agentRewards.iteritems()))
			if self.running:
				self.alarm = self.after(self.speed.get(), self.timeout)
			if not self.continue_check():
				self.done = True
		else:
			self.start()
		self.redraw()

	def redraw(self):
		self.canvas.draw_sim(self.sim, self.targetAgent.get())
	
	def step_one(self):
		self.step = True
		self.timeout()
		self.step = False
	
	def start(self):
		if self.running:
			self.playpause.config(text='Start')
			self.after_cancel(self.alarm)
			self.stepper.config(state='active')
			self.scenarioSelect.config(state='active')
		else:
			self.playpause.config(text='Pause')
			self.alarm = self.after(self.speed.get(), self.timeout)
			self.stepper.config(state='disabled')
			self.scenarioSelect.config(state='disabled')
		self.running = not self.running
	
	def reset(self):
                self.iters = 0
		if self.running:
			self.start()
		self.make_sim()
		self.make_canvas()
		self.reset_buttons()
		self.redraw()
	
	def agent_change(self):
                print "Changing agent to",self.targetAgent.get()
                self.rewardString.set('\n'.join(a+" reward accumulated : "+str(r) for a,r in self.agentRewards.iteritems()))
		self.reward.config(textvariable=self.rewardString)
		self.redraw()

        def give_omniscient_state(self):
                self.sim.give_omniscient_state(self.targetAgent.get())
                self.redraw()
	
	def call_with(self, fns, vals):
		for fn, val in zip(fns,vals):
			fn(*val)
			
	def reset_buttons(self):
		# Reset agent rewards
		self.agentRewards.clear()
		for a in self.sim.agents:
			self.agentRewards[a] = 0
                self.rewardString = Tkinter.StringVar()
		self.rewardString.set('\n'.join(a+" reward accumulated : "+str(r) for a,r in self.agentRewards.iteritems()))
		self.reward.config(textvariable=self.rewardString)
		
		# Fix the agents dropdown
		agents = self.sim.agents.keys()
		agents.sort()
		self.agents['menu'].delete(0,Tkinter.END)
		for a in agents:
			self.agents['menu'].insert('end', 'command', label=a, 
						command=lambda v=a: self.targetAgent.set(v))
		self.targetAgent.set(agents[0])
	
	def make_buttons(self):
		# Which scenario?
		self.scenarioFrame = Tkinter.Frame(self)
		self.scenarioLabel = Tkinter.Label(self.scenarioFrame, text="Scenario:")
		self.scenarioSelect = Tkinter.OptionMenu(self.scenarioFrame, self.currentScenario,
								*self.scenarioNames, command=lambda x: self.reset())
		
		# Control buttons
		self.playpause = Tkinter.Button(self, text='Start', command=self.start)
		self.stepper = Tkinter.Button(self, text='Step', command=self.step_one)
		self.resetter = Tkinter.Button(self, text='Reset', command=self.reset)
		
		# Which agent are we watching?
		self.targetAgent = Tkinter.StringVar()
		agents = self.sim.agents.keys()
		agents.sort()
		self.targetAgent.set(agents[0])
		self.agentFrame = Tkinter.Frame(self)
		self.agentLabel = Tkinter.Label(self.agentFrame, text="Agent's View:")
		self.agents = Tkinter.OptionMenu(self.agentFrame, self.targetAgent, *agents,
						command=lambda x: self.agent_change())
		
		# How much data are we observing?
		self.showFrame = Tkinter.Frame(self)
		self.showLabel = Tkinter.Label(self.showFrame, text="Show:")
		self.showAgentsVar = Tkinter.BooleanVar()
		self.showGoalsVar = Tkinter.BooleanVar()
		self.showGoalBeliefVar = Tkinter.BooleanVar()
		self.showObjBeliefVar = Tkinter.BooleanVar()
		self.showMostLikelyExpVar = Tkinter.BooleanVar()
		self.showAgents = Tkinter.Checkbutton(self.showFrame, text="Agents", 
						command=lambda: self.call_with([self.canvas.draw_agents, self.redraw],
											[(self.showAgentsVar.get(),), ()]),
						variable=self.showAgentsVar, onvalue=True, offvalue=False)
		self.showGoals = Tkinter.Checkbutton(self.showFrame, text="Goals",
						command=lambda: self.call_with([self.canvas.draw_goals, self.redraw],
											[(self.showGoalsVar.get(),), ()]),
						variable=self.showGoalsVar, onvalue=True, offvalue=False)
		self.showGoalBelief = Tkinter.Checkbutton(self.showFrame, text="Goal Beliefs",
						command=lambda: self.call_with([self.canvas.draw_goal_belief, self.redraw],
											[(self.showGoalBeliefVar.get(),), ()]),
						variable=self.showGoalBeliefVar, onvalue=True, offvalue=False)
		self.showObjBelief = Tkinter.Checkbutton(self.showFrame, text="Object Beliefs",
						command=lambda: self.call_with([self.canvas.draw_obj_belief, self.redraw],
											[(self.showObjBeliefVar.get(),), ()]),
						variable=self.showObjBeliefVar, onvalue=True, offvalue=False)
		self.showMostLikelyExp = Tkinter.Checkbutton(self.showFrame, text="Most Likely Explanations",
						command=lambda: self.call_with([self.canvas.draw_most_likely_exp, self.redraw],
											[(self.showMostLikelyExpVar.get(),), ()]),
						variable=self.showMostLikelyExpVar, onvalue=True, offvalue=False)
		self.showAgentsVar.set(True)
		self.showGoalsVar.set(True)
		self.showGoalBeliefVar.set(True)
		self.showObjBeliefVar.set(True)
		self.showMostLikelyExpVar.set(False)

		self.give_omniscient = Tkinter.Button(self, text='Give omniscient', command=self.give_omniscient_state)
		
		# How much reward has this agent accumulated?
		self.agentRewards = {}
		for a in self.sim.agents:
			self.agentRewards[a] = Tkinter.StringVar()
			self.agentRewards[a].set('Reward Accumulated: 0')
		self.reward = Tkinter.Label(self, textvariable=self.agentRewards[self.targetAgent.get()])
		
		# How fast are we going?
		self.speed = Tkinter.Scale(self, orient=Tkinter.HORIZONTAL, length=200,
						from_=MIN_SPEED, to=MAX_SPEED, label='Speed', showvalue=0)
		
		# Pack it all into subframes and then into the main frame's grid
		self.scenarioLabel.pack(side=Tkinter.LEFT)
		self.scenarioSelect.pack(side=Tkinter.LEFT)
		self.agentLabel.pack(side=Tkinter.LEFT)
		self.agents.pack(side=Tkinter.LEFT)
		self.showLabel.grid(column=0,row=0,rowspan=2)
		self.showAgents.grid(column=1,row=1)
		self.showGoals.grid(column=1,row=2)
		self.showObjBelief.grid(column=2,row=1)
		self.showGoalBelief.grid(column=2,row=2)
		self.showMostLikelyExp.grid(column=1,row=3,columnspan=2)
		i = 0
		for item in [self.scenarioFrame, self.playpause, self.stepper, self.resetter, 
					self.agentFrame, self.showFrame, self.give_omniscient, self.reward, self.speed]:
			item.grid(column=0,row=i)
			i+=1
	
	def make_canvas(self):
		pack = False
		if not self.canvas:
			self.canvas = RobotCanvas(self)
			self.canvas.grid(column=1,row=0,rowspan=8)
		w = len(self.map)
		h = max(len(m) for m in self.map)
                c = (100 if h <= 6 else 600/h)
                self.canvas.cellSize = c
		self.canvas.config(width=w*c,height=h*c)
	
	def make_sim(self):
		self.map,self.sim,self.continue_cond = self.scenarios[self.currentScenario.get()].make_sim()
		self.iters = 0

def main():
	root = Tkinter.Tk()
	app = RobotApp(root)
	root.mainloop()

if __name__ == "__main__":
	main()

