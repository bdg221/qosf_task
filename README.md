# QOSF Task 1
Brian Goldsmith

## Step 1 - Generate Circuits
For this task, I will need to have a Toffoli circuit and the circuit from the task with the two U3 gates set with provided parameters.
[generate_circuits.py](./generate_circuits.py)

## Step 2 - Test Equivalency
The primary goal of the task is to find a decomposed circuit that matches the original Toffoli circuit. Therefore, it is critical to properly test equivalency.
https://quantumcomputing.stackexchange.com/questions/13723/test-equivalence-of-circuits-exactly-on-qiskit/13724?noredirect=1#comment18445_13724

Note: From these tests it is determined that `unitaries_allclose()` is the only test that consider global phase. The `operator_equiv()` is the next best equivalency test, but it does not consider global phase. Finally, `statevector_equiv()` is the least useful equivalency test as it will have a number of false positives and does not incorporate global phase.

[equivalency.py](./equivalency.py)
[tests/test_equivalency.py](./tests/test_equivalency.py)

## Step 3 - Cost Function
A cost function will be important to determine how close a circuit is to the ideal Toffoli circuit. This will allow the use of existing minimization functions to tune the parameters for the U3 gates.
From a search of cost function options for comparing unitary matrices, I found Frobenius Norm and Trace Norm which could both be run with [Numpy's norm function](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html). Also, I used the shot equivalency found on the stackexchange answer above as another cost function.

Note: Ran into an interesting pytest and AerSimulator issue when using @pytest.mark.parametrize. Due to the way pytest runs all of the tests at once, the AerSimulator frequently hits an error due to duplicate keys. I added a label and extracted the unitary matrix differently in the Frobenius Norm cost function to adjust for this.

Update: After not being able to find a solution from the existing cost functions, I searched for other way to compare matrices and added trace overlap (1-untiary matrix fidelity)

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
## First Attempt
In the final steps, I created [task1.ipynb](./task1.ipynb) that calls the optimization functions and show the results. The trace overlap (matrix fidelity) cost function worked well with `minimize` to provide the following answer:
Angles successfully found with trace_overlap_cost in 26.460007905960083 seconds!
U3(-1/2 pi, -pi, 0)
U3(0, -1/4 pi, 0)

This was confirmed in IBM Composer ([screenshot](./images/Trace_overlap_cost.png)) to be the correct parameters to create an accurate decomposition of a Toffoli gate..

Interestingly, the Frobenius norm and trace norm both gave results very close to the answer above.
Frobenius norm:
```
Angles successfully found with frobenius_norm in 95.35844302177429 seconds!
U3(-1/2 pi, -pi, 0)
U3(0, -2/11 pi, -2/29 pi)
```
and trace norm:
```
Angles successfully found with trace_norm in 85.04883122444153 seconds!
U3(-1/2 pi, -pi, 0)
U3(0, -2/11 pi, -1/15 pi)
```

Putting these values into IBM Composer shows that the circuits are very close with the table for Frobenius norm ([screenshot](./images/Frobenius_norm.png)) showing 99.99985% accuracy with the expected probability for a Toffoli gate. The trace norm ([screenshot](./images/Trace_norm.png)) results show a very similar 99.99943% accuracy.

Clearly, this is a matter of tolerance and additional adjusting in the optimization function and cost function could refine these solutions even more.

The `differential_evolution` optimizer did not seem to do well with the counts related cost function and took over 12 minutes. It never succesfuuly found the parameters for an equivalent Toffoli circuit, but putting the results into IBM Composer ([screenshot](./images/Count_comparison.png)), I see that it did reach 98.16148% accuracy.
U3(-49/31 pi, -23/16 pi, 46/31 pi)
U3(-pi, 16/11 pi, 4/23 pi)

## Second Attempt
The previous results provided by the different optimization functions all included a slight phase angle difference, seen in the IBM Composer screenshots. While these are passing the equivalency tests, I still wanted to at least try to address this. As I am not sure about manually manipulating the results to remove the phase differences, instead I decided to try to limit the bounds to be between zero and 2pi, instead of -2pi and 2pi. Using zero to 2pi should be sufficient because of the period should be 2pi. After making this slight change in [parameter_tuning](./parameter_tuning.py), I reran the different optimization functions in [task1.ipynb](./task1.ipynb) and received the following results.

The attempt using the `trace_overlap_cost` function, was unable to find a successful set of parameters, though it came very close as can be seen by both the fidelity and the [Composer screenshot](./images/Trace_overlap_cost_new.png):
The best angles found had a fidelity of 0.9999999999999951 were:
U3(3/2 pi, pi, 2 pi)
U3(0, 7/4 pi, 0)

The Frobenius norm cost function successfully found a set of parameters that passed all of the equivalency tests. However, the [Composer secreenshot](./images/Frobenius_norm_new.png) still show phase angles that are not all zero like a Toffoli gate.
Angles successfully found with frobenius_norm in 278.0414409637451 seconds!
U3(1/2 pi, 0, pi)
U3(0, 5/12 pi, 4/3 pi)

The attempt using the trace norm cost function found parameters that were pretty close. However, the [Composer screenshot](./images/Trace_norm_new.png) shows a small phase angel still appear.
The best angles found had a fidelity of 0.9690941253256485 were:
U3(1/2 pi, 0, pi)
U3(0, 0, 54/31 pi)

Finally, the use of the count comparison was again slow and unsuccessful at finding parameters that result appropriate Toffoli decomposition. The fidelity was the worst and phase angles were present for the computational base states as seen in the [Composer screenshot](./images/Count_comparison_new.png).
The best angles found had a fidelity of 0.911865234375 were:
U3(7/13 pi, 13/12 pi, 0)
U3(13/7 pi, 11/26 pi, 7/25 pi)

## Final Thoughts
It is very interesting that all of the times the parameters were successfully found, there was always a slight phase angle appearing in IBM Composer even though all equivalency tests passed. Also, I found it interesting that the `minimize` function consistently found parameters resulting in a high unitary matrix fidelity. Also, it was expected that the count comparison would be the most inefficient and least likely to be successful and both expectations proved true.


# How to Duplicate Results
To duplicate the results, perform a `git clone` of the repository. Navigate to the `qosf_task directory`. Make sure that `uv` is installed on the machine and run `uv sync`. Open the project in VS Code and open [task1.ipynb](task1.ipynb) selecting the virtual environment, `.venv`, (created during the `uv sync` command) as the Python interpreter. At this point, you should be able to run the notebook.