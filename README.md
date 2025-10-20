# qosf_task

## Step 1 - Generate Circuits
For this task, I will need to have a Toffoli circuit and the circuit from the task with the two U3 gates set with provided parameters.

## Step 2 - Test Equivalency
The primary goal of the task is to find a decomposed circuit that matches the original Toffoli circuit. Therefore, it is critical to properly test equivalency.
https://quantumcomputing.stackexchange.com/questions/13723/test-equivalence-of-circuits-exactly-on-qiskit/13724?noredirect=1#comment18445_13724

Note: From these tests it is determined that `unitaries_allclose()` is the only test that consider global phase. The `operator_equiv()` is the next best equivalency test, but it does not consider global phase. Finally, `statevector_equiv()` is the least useful equivalency test as it will have a number of false positives and does not incorporate global phase.

## Step 3 - Cost Function
A cost function will be important to determine how close a circuit is to the ideal Toffoli circuit. This will allow the use of existing minimization functions to tune the parameters for the U3 gates.
From a search of cost function options for comparing unitary matrices, I found Frobenius Norm and Trace Norm which could both be run with [Numpy's norm functino](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html). Also, I used the shot equivalency found on the stackexchange answer above as another cost function.

Note: Ran into an interesting pytest and AerSimulator issue when using @pytest.mark.parametrize. Due to the way pytest runs all of the tests at once, the AerSimulator frequently hits an error due to duplicate keys. I added a label and extracted the unitary matrix differently in the Frobenius Norm cost function to adjust for this.

## Step 4 - Parameter Tuning
With the cost function in place, setup the parameter tuning to find the optimized parameters. I had planned to use scipy.optimize.minimize(), but Gemini recommended a global optimizer like scipy.optimize.differential_evolution. The global optimizer makes it less likely to get stuck in local minimums. 

## Step 5 - Check Optimized Parameters
It is important to check that the circuit with the optimized parameters is exactly equivalent.

## Step 6 - Clean Parameters (to fractions of pi)
Most "standard" angles that are used with the U3 gate tend to be fractions of pi. Therefore, the [fractions.Fraction() method](https://docs.python.org/3/library/fractions.html) was used to find cleaner parameter values. These values were then tested a final time to verify equivalency.