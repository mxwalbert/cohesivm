# Contributing <a name="contributing"></a>

We welcome contributions from the community to make COHESIVM better! If you'd like to contribute an implementation 
of a {class}`~cohesivm.devices.Device`, an {class}`~cohesivm.interfaces.Interface`, 
a {class}`~cohesivm.measurements.Measurement` or an {class}`~cohesivm.analysis.Analysis`, please follow these steps:

1. Fork the repository to your own GitHub account.
2. Clone your forked repository to your local machine.
3. Create a new branch for your new component: git checkout -b my-new-component.
4. Make your changes and ensure the code passes existing tests.
5. Add new tests for your changes, if applicable.
6. Commit your changes with clear and concise messages.
7. Push your branch to your forked repository: git push origin my-new-feature.
8. Open a pull request to the main repository, describing the changes and why they should be merged.

Please make sure to follow the project's structure. The best way to start is to have a look at the tutorials given in 
the {doc}`/`. Also, don't forget to write tests for your newly implemented feature which may requires a new custom 
marker in the ``conftest.py`` (e.g., if you implement a physical device for which the tests will always fail if it is 
not connected).

You may also contribute by submitting feature requests, bugs and other issues over GitHub.

Thank you for your contributions!

