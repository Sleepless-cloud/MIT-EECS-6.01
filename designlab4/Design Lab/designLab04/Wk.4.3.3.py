import lib601.sm as sm
# Use sm.R, sm.Gain, sm.Cascade, sm.FeedbackAdd and sm.FeedbackSubtract
# to construct the state machines

def accumulator(init):
    return sm.FeedbackAdd(sm.Wire(), sm.R(init))

def accumulatorDelay(init):
    return sm.Cascade(sm.R(0), accumulator(init))

def accumulatorDelayScaled(s, init):
    return sm.Cascade(accumulatorDelay(init), sm.Gain(s))

if __name__ == '__main__':
    def test_accumulator():
        y = accumulator(0)
        print y.transduce(list(range(10)))

    def test_accumulatorDelay():
        y = accumulatorDelay(0)
        print y.transduce(list(range(10)))

    def test_accumulatorDelayScaled():
        y = accumulatorDelayScaled(0.5, 0)
        print y.transduce(list(range(10)))

    test_accumulator()
    test_accumulatorDelay()
    test_accumulatorDelayScaled()
