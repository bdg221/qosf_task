# qosf_task

Environment Notes:
Latest version of Qiskit and numpy


## Step 1 - Generate Circuits
For this task, I will need to have a Tofolli circuit and the circuit from the task with the two U3 gates set with provided parameters.

## Step 2 - Test Equivalency
The primary goal of the task is to find a decomposed circuit that matches the original Tofolli circuit. Therefore, it is critical to properly test equivalency.

## Step 3 - Cost Function
A cost function will be important to determine how close a circuit is to the ideal Tofolli circuit. This will allow the use of existing minimization functions to tune the parameters for the U3 gates.

## Step 4 - Parameter Tuning
With the cost function in place, setup the parameter tuning to find the optimized parameters.

## Step 5 - Check Optimized Parameters
Check that the circuit with the optimized parameters is exactly equivalent. If so, try to change the parameters to be fractions of pi if possible. Save verified correct parameters for reporting.