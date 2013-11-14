
import numpy

from PyML.classifiers.baseClassifiers import Classifier
from PyML.classifiers.svm import modelDispatcher

class RidgeRegression (Classifier) :
    """
    A kernel ridge regression classifier

    :Keywords:
      - `ridge` -- the ridge parameter [default: 1.0]
      - `kernel` -- a kernel object [default: Linear]

    """

    attributes = {'ridge' : 1.0,
		  'kernel' : None}

    def __init__(self, arg = None, **args) :
    
        Classifier.__init__(self, arg, **args)

    def __repr__(self) :
        
        rep = '<' + self.__class__.__name__ + ' instance>\n'
        rep += 'ridge: %f\n' % self.ridge
            
        return rep
                    
        
    def train(self, data, **args) :

        Classifier.train(self, data, **args)
        self.data = data
        if self.kernel is not None :
            self.data.attachKernel(self.kernel)
        Y = numpy.array(data.labels.Y)
        Y = Y * 2 - 1
        K = data.getKernelMatrix()
        K = K + self.ridge * numpy.eye(len(data))
        self.alpha = numpy.dot(Y, numpy.linalg.inv(K))
        self.model = modelDispatcher(data, svID=range(len(data)), alpha=self.alpha)
        self.log.trainingTime = self.getTrainingTime()
        
    classify = Classifier.twoClassClassify

    def decisionFunc(self, data, i) :

        return self.model.decisionFunc(data, i)


