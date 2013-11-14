if obsvisible == (0,False):
			return self.predict_object_belief()
		
		else:

			for (x,y,d) in bobject.keys():
				if (x,y) != (mypose[0],mypose[1]):
					update = self.sensorModel.objectSensors[objname].probability_raw(mypose,(x,y),obsvisible)
					if update <= 0.5:
						bobject[(x,y,d)] = 0
					else:
						bobject[(x,y,d)] = update
			normalize(bobject) 
			return bobject.copy()