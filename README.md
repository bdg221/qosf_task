# QOSF Task 1
Brian Goldsmith

## Step 1 - Generate Circuits
For this task, I will need to have a Toffoli circuit and the circuit from the task with the two U3 gates set with provided parameters.
[generate._circuits.py](./generate_circuits.py)

## Step 2 - Test Equivalency
The primary goal of the task is to find a decomposed circuit that matches the original Toffoli circuit. Therefore, it is critical to properly test equivalency.
https://quantumcomputing.stackexchange.com/questions/13723/test-equivalence-of-circuits-exactly-on-qiskit/13724?noredirect=1#comment18445_13724

Note: From these tests it is determined that `unitaries_allclose()` is the only test that consider global phase. The `operator_equiv()` is the next best equivalency test, but it does not consider global phase. Finally, `statevector_equiv()` is the least useful equivalency test as it will have a number of false positives and does not incorporate global phase.

[equivalency.py](./equivalency.py)
[tests/test_equivalency.py](./tests/test_equivalency.py)

## Step 3 - Cost Function
A cost function will be important to determine how close a circuit is to the ideal Toffoli circuit. This will allow the use of existing minimization functions to tune the parameters for the U3 gates.
From a search of cost function options for comparing unitary matrices, I found Frobenius Norm and Trace Norm which could both be run with [Numpy's norm functino](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html). Also, I used the shot equivalency found on the stackexchange answer above as another cost function.

Note: Ran into an interesting pytest and AerSimulator issue when using @pytest.mark.parametrize. Due to the way pytest runs all of the tests at once, the AerSimulator frequently hits an error due to duplicate keys. I added a label and extracted the unitary matrix differently in the Frobenius Norm cost function to adjust for this.

Update: After not being able to find a solution from the existing cost functions, I searched for other way to compare matrices and added trace overlap (1-matix fidelity)

[cost.py](./cost.py)
[tests/test_cost.py](./tests/test_cost.py)

## Step 4 - Parameter Tuning
With the cost function in place, setup the parameter tuning to find the optimized parameters. I ended up using scipy.optimize.minimize() for the parameter optimization except for the optimization with the count comparison cost function. Gemini recommended a global optimizer like scipy.optimize.differential_evolution as the global optimizer makes it less likely to get stuck in local minimums. 

Update: Adjusting the scipy minimize's `method` parameters and tolerance allowed the other non-count based optimizations to work properly.

[parameter_tuning.py](./parameter_tuning.py)
[task1.ipynb](./task1.ipynb)

## Step 5 - Clean Parameters (to fractions of pi)
Most "standard" angles that are used with the U3 gate tend to be fractions of pi. Therefore, the [fractions.Fraction() method](https://docs.python.org/3/library/fractions.html) was used to find cleaner parameter values. These values were then tested a final time to verify equivalency.

[task1.ipynb](./task1.ipynb)

# Conclusion
In the final steps, I created [task1.ipynb](./task1.ipynb) that calls the optimization functions and show the results. The trace overlap (matrix fidelity) cost function worked well with `minimize` to provide the following answer:
U3(-1/2 pi, -pi, 0)
U3(0, -1/4 pi, 0)

This was confirmed in IBM Composer ([screenshot](./images/Trace_overlap_cost.png)) to be the correct parameters to create an accurate deomposition of a Toffoli gate..

Interestingly, the Frobenius norm and trace norm both gave results very close to the answer above.
Frobenius norm:
```
U3(-1/2 pi, -pi, 0)
U3(0, -2/11 pi, -2/29 pi)
```
and trace norm:
```
U3(-1/2 pi, -pi, 0)
U3(0, -2/11 pi, -1/15 pi)
```

Putting these values into IBM Composer shows that the circuits are very close with the table for Frobenius norm ([screenshot](./images/Frobenius_norm.png)) showing 99.99985% accuracy with the expected probability for a Toffoli gate. The trace norm ([screenshot](./images/Trace_norm.png)) results show a very similar 99.99943% accuracy.

Clearly, this is a matter of tolerance and additional adjusting in the optimization function and cost function could refine these solutions even more.

The `differential_evolution` optimizer did not seem to do well with the counts related cost function and took over 12 minutes. It never succesfuuly found the parameters for an equivolent Toffoli circuit, but putting the results into IBM Composer ([screenshot](./images/Count_comparison.png)), I see that it did reach 98.16148% accuracy.
U3(-49/31 pi, -23/16 pi, 46/31 pi)
U3(-pi, 16/11 pi, 4/23 pi)

To duplicate the results, perform a `git clone` of the repository. Navigate to the `qosf_task directory`. Make sure that `uv` is installed on the machine and run `uv sync`. Open the project in VS Code and open [task1.ipynb](task1.ipynb) selecting the virtual environment, `.venv`, (created during the `uv sync` command) as the Python interpretter. At this point, you should be able to run the notebook.