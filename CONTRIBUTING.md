# Guidelines for contributing to COHESIVM

We welcome contributions from the community to make COHESIVM better! If you'd like to contribute an implementation 
of a [``Device``](https://cohesivm.readthedocs.io/en/latest/reference/devices.html#cohesivm.devices.Device), 
an [``Interface``](https://cohesivm.readthedocs.io/en/latest/reference/interfaces.html#cohesivm.interfaces.Interface), 
a [``Measurement``](https://cohesivm.readthedocs.io/en/latest/reference/measurements.html#cohesivm.measurements.Measurement) 
or an [``Analysis``](https://cohesivm.readthedocs.io/en/latest/reference/analysis.html#cohesivm.analysis.Analysis), 
please follow these steps:

1. [Fork the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository) to your own GitHub account.
2. [Clone your forked repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#cloning-your-forked-repository) to your local machine.
3. Create a new branch for your new component: 
    ```console
    git checkout -b my-new-component
    ```
4. Make your changes and ensure the code passes existing tests.
    ```console
    python -m pytest
    ```
5. Add new tests for your changes, if applicable.  
   *⚠ This may require a new custom marker in the [``conftest.py``](test/conftest.py). E.g., if you implement new hardware which should only
   be tested if it is physically connected.*
   
7. Commit your changes with clear and concise messages.
8. Push your branch to your forked repository:
    ```console
    git push origin my-new-component
    ```
9. [Open a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) to the main repository, describing the changes and why they should be merged.

Please make sure to follow the project's structure. The best way to start is to have a look at the tutorials given in 
the [documentation](https://cohesivm.readthedocs.io/en/latest/).

You may also contribute by submitting feature requests, bugs and other issues over GitHub.

Thank you for your contributions!
