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

## Step 4 - Parameter Tuning
With the cost function in place, setup the parameter tuning to find the optimized parameters.

## Step 5 - Check Optimized Parameters
Check that the circuit with the optimized parameters is exactly equivalent. If so, try to change the parameters to be fractions of pi if possible. Save verified correct parameters for reporting.