import marimo

__generated_with = "0.11.26"
app = marimo.App(app_title="Plugin Tutorial")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from pathlib import Path
    return Path, mo


@app.cell(hide_code=True)
def _(mo):
    _tip = mo.accordion({
        "Dependencies...": mo.md("""
    The rest of this tutorial assumes you have read the attached README and have installed the required packages described therein. Although not foolproof, you can run the following command to check if at least AiiDA and the plugin are installed correctly.

    ```
    verdi plugin list aiida.calculations fans
    ```
    """)
    })
    mo.md(
        rf"""
        # Plugin Tutorial

        The goal of this tutorial is to give you an idea of how to utilise the `aiida-fans` plugin as well as an introduction to `AiiDA` and `FANS`.
        By the end of this tutorial, you should know how to:

        - Setup your AiiDA profile, computer, and code.
        - Define FANS options and prepare a parameter space study. 
        - Write a `submit.py` script to run your jobs.
        - Query and read the results.

        {_tip}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _note = mo.md(
        """
        **Note:** This section assumes you have not already set up an appropriate profile, computer, and code for using AiiDA and FANS. If you have already done this, you may skip to the next section.
        """
    ).callout("info")
    mo.md(
        rf"""
        ## AiiDA Setup

        Before we can truly begin, we must set up AiiDA on your machine. This means three things.

        1. Create a Profile
        2. Specify a Computer
        3. Define a Code

        AiiDA has multiple user interfaces but their CLI, `verdi`, is particularly well suited to these three steps since they need to be performed only rarely. Therefore, you will need access to the terminal to proceed.

        {_note}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1. Create a Profile

        By default, AiiDA stores app data at the user level. Even when AiiDA is installed in a virtual environment, it will still read and write to `.aiida` in your home directory. However, AiiDA provides users a way to seperate their data into "profiles". Let's create a profile for this tutorial.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    config_profile = (
        mo.md("""
        **Fill in the details below to generate your custom profile configuration.**

        - {profile_name}
        - {first_name}
        - {last_name}
        - {email}
        - {institution}
        """)
        .batch(
            profile_name=mo.ui.text("aiida-fans-tutorial", label="Profile Name:"),
            first_name=mo.ui.text("Max", label="First Name:"),
            last_name=mo.ui.text("Mustermann", label="Last Name:"),
            email=mo.ui.text("example@nomail.com", label="Email:"),
            institution=mo.ui.text("MIB", label="Institution:"),
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=False)
    ); config_profile
    return (config_profile,)


@app.cell(hide_code=True)
def _(config_profile, mo):
    mo.stop(config_profile.value is None, mo.md("*Awaiting input above...*"))

    setup_profile = rf"""profile: {config_profile.value["profile_name"]}
    first_name: {config_profile.value["first_name"]}
    last_name: {config_profile.value["last_name"]}
    email: {config_profile.value["email"]}
    institution: {config_profile.value["institution"]}
    use_rabbitmq: false
    set_as_default: true
    non_interactive: true
    """

    with open("setup_profile.yaml", "w") as _f:
        _f.write(setup_profile)

    mo.md(rf"""
    Below is your profile configuration. It has been automatically written to the file `setup_profile.yaml`.

    ```yaml
    {setup_profile}
    ```
    """
    )
    return (setup_profile,)


@app.cell(hide_code=True)
def _(config_profile, mo):
    mo.stop(config_profile.value is None, None)

    _tip = mo.accordion({
            "On default profiles...": mo.md(rf"""
    We have made the new profile our default profile. This means that any further calls to `verdi` will implicitly use the {config_profile.value["profile_name"]} profile. You can change the profile on a per-call basis with the `-p/--profile` option. To change the default profile use:

    ```
    verdi profile set-default PROFILE
    ```
    """
    )
    })

    mo.md(rf"""
    To create your new profile from this file run:

    ```
    verdi profile setup core.sqlite_dos --config setup_profile.yaml
    ```

    Hopefully, that completed successfully. Using these commands, you should see your new profile listed (alone if this is your first profile) and a report on it also:

    ```
    verdi profile list
    verdi profile show {config_profile.value["profile_name"]}
    ```

    {_tip}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 2. Specify a Computer

        Before you proceed, ensure that your local computer satisfies the following requirements:

        - It runs a Unix-like operating system (Linux distros and MacOS should work fine)
        - It has `bash` installed

        AiiDA does not assume what computer you wish to run jobs on, so even if you are only using your local machine, you must tell it as much. That is what we will do here; specify the localhost computer.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    config_computer = (
        mo.md("""
        **Fill in the details below to generate your custom computer configuration.**

        - {label}
        - {mpiprocs}
        - {description}
        """)
        .batch(
            label=mo.ui.text("localhost", label="Computer Label:"),
            mpiprocs=mo.ui.text("2", label="MPI processes:"),
            description=mo.ui.text("This is my local machine.", label="Description:", full_width=True),
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=False)
    ); config_computer
    return (config_computer,)


@app.cell(hide_code=True)
def _(Path, config_computer, mo):
    mo.stop(config_computer.value is None, mo.md("*Awaiting input above...*"))

    setup_computer = rf"""label: {config_computer.value["label"]}
    description: {config_computer.value["description"]}
    hostname: localhost
    transport: core.local
    scheduler: core.direct
    shebang: #!/bin/bash
    work_dir: {Path.cwd()}/.aiida_run""" + r"""
    mpirun_command: mpiexec -n {tot_num_mpiprocs}""" + rf"""
    mpiprocs_per_machine: {config_computer.value["mpiprocs"]}
    default_memory_per_machine: null
    use_double_quotes: false
    prepend_text: ' '
    append_text: ' '
    non_interactive: true
    """

    with open("setup_computer.yaml", "w") as _f:
        _f.write(setup_computer)

    mo.md(rf"""
    Below is your computer configuration. It has been automatically written to the file `setup_computer.yaml`.

    ```yaml
    {setup_computer}
    ```
    """
    )
    return (setup_computer,)


@app.cell(hide_code=True)
def _(config_computer, mo):
    mo.stop(config_computer.value is None, None)

    mo.md(rf"""
    To specify your new computer from this file run:

    ```
    verdi computer setup --config setup_computer.yaml
    ```

    Then you must configure the computer with the following command:

    ```
    verdi computer configure core.local localhost
    ```

    The default options should be suitable.

    Hopefully, that completed successfully. Using this command, you should test that AiiDA can connect to the machine:

    ```
    verdi computer test {config_computer.value["label"]}
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 3. Define a Code

        The final step to setup AiiDA is to define the "code" you wish to utilise. Here, the "code" refers to FANS. This step is important as it tells AiiDA how to execute FANS and which plugin should handle its jobs. AiiDA provides many ways of handling the "code" of your project. Since we installed FANS in the environment, we can simply make use of it there.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    config_code = (
        mo.md("""
        **Fill in the details below to generate your custom code configuration.**

        - {label}
        - {description}
        - {environment}
        """)
        .batch(
            label=mo.ui.text("FANS", label="Code Label:"),
            description=mo.ui.text("The FANS executable.", label="Description:"),
            environment=mo.ui.text_area("""eval "$(conda shell.bash hook)"
    conda activate aiida-fans-tutorial""", label="Environment Activation Script:", full_width=True)
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=False)
    ); config_code
    return (config_code,)


@app.cell(hide_code=True)
def _(config_code, config_computer, mo):
    mo.stop(config_code.value is None, mo.md("*Awaiting input above...*"))

    setup_code = rf"""label: {config_code.value["label"]}
    description: {config_code.value["description"]}
    default_calc_job_plugin: fans
    use_double_quotes: false
    with_mpi: true
    computer: {config_computer.value["label"]}
    filepath_executable: FANS
    prepend_text: |
    {"\n".join([f"    {ln}" for ln in config_code.value["environment"].split("\n")])}
    append_text: ' '
    non_interactive: true
    """

    with open("setup_code.yaml", "w") as _f:
        _f.write(setup_code)

    mo.md(rf"""
    Below is your code configuration. It has been automatically written to the file `setup_code.yaml`.

    ```yaml
    {setup_code}
    ```
    """
    )
    return (setup_code,)


@app.cell(hide_code=True)
def _(config_code, mo):
    mo.stop(config_code.value is None, None)

    _tip = mo.accordion({
            "Your first node...": mo.md(rf"""
    You should also note that the code is saved by AiiDA as a node, and thus we have created our first node. Any calculation jobs we perform will be connected to this code node in the provenance graph.

    To list all the nodes stored in your profile, run:

    ```
    verdi node list
    ```
    """
    )
    })

    mo.md(rf"""
    To define your new code from this file run:

    ```
    verdi code create core.code.installed --config setup_code.yaml
    ```

    Hopefully, that completed successfully. Using these commands, you can show the details of your new code and verify that AiiDA can connect to it:

    ```
    verdi code show {config_code.value["label"]}
    verdi code test {config_code.value["label"]}
    ```

    {_tip}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## FANS Rundown

        FANS requires a JSON input file. The input file can be thought of in 5 sections, each specifying the various problem parameters as well as runtime settings. Each setting also notes the appropriate AiiDA datatype. This is the type of node that you must give AiiDA when running jobs, as we will see later.

        ### Microstructure Definition

        ```json
        "ms_filename": "microstructures/sphere32.h5",
        "ms_datasetname": "/sphere/32x32x32/ms",
        "ms_L": [1.0, 1.0, 1.0]
        ```

        - `ms_filename`: This specifies the path to the HDF5 file that contains the microstructure data. (AiiDA type: `SinglefileData`)
        - `ms_datasetname`: This is the path within the HDF5 file to the specific dataset that represents the microstructure. (AiiDA type: `Str`)
        - `ms_L`: Microstructure length defines the physical dimensions of the microstructure in the x, y, and z directions. (AiiDA type: `List`)

        ### Problem Type and Material Model

        ```json
        "problem_type": "mechanical",
        "matmodel": "LinearElasticIsotropic",
        "material_properties": {
            "bulk_modulus": [62.5000, 222.222],
            "shear_modulus": [28.8462, 166.6667]
        }
        ```

        - `problem_type`: This defines the type of physical problem you are solving. Common options include "thermal" problems and "mechanical" problems. (AiiDA type: `Str`)
        - `matmodel`: This specifies the material model to be used in the simulation. Examples include `LinearThermalIsotropic` for isotropic linear thermal problems, `LinearElasticIsotropic` for isotropic linear elastic mechanical problems, `PseudoPlasticLinearHardening`/`PseudoPlasticNonLinearHardening` for plasticity mimicking model with linear/nonlinear hardening, and `J2ViscoPlastic_LinearIsotropicHardening`/ `J2ViscoPlastic_NonLinearIsotropicHardening` for rate dependent J2 plasticity model with linear/nonlinear isotropic hardening. (AiiDA type: `Str`)
        - `material_properties`: This provides the necessary material parameters for the chosen material model. For thermal problems, you might specify `conductivity`, while mechanical problems might require `bulk_modulus`, `shear_modulus`, and more properties for advanced material models. These properties can be defined as arrays to represent multiple phases within the microstructure. (AiiDA type: `Dict`)

        ### Solver Settings

        ```json
        "method": "cg",
        "error_parameters":{
            "measure": "Linfinity",
            "type": "absolute",
            "tolerance": 1e-10
        },
        "n_it": 100
        ```

        - `method`: This indicates the numerical method to be used for solving the system of equations. `cg` stands for the Conjugate Gradient method, and `fp` stands for the Fixed Point method. (AiiDA type: `Str`)
        - `error_parameters`: This section defines the error parameters for the solver. Error control is applied on the finite element nodal residual of the problem.
            - `measure`: Specifies the norm used to measure the error. Options include `Linfinity`, `L1`, or `L2`. (AiiDA type: `Str`)
            - `type`: Defines the type of error measurement. Options are `absolute` or `relative`. (AiiDA type: `Str`)
            - `tolerance`: Sets the tolerance level for the solver, defining the convergence criterion based on the chosen error measure. The solver iterates until the solution meets this tolerance. (AiiDA type: `Float`)
        - `n_it`: Specifies the maximum number of iterations allowed for the FANS solver. (AiiDA type: `Int`)


        ### Macroscale Loading Conditions

        ```json
        "macroscale_loading":   [
                                    [
                                        [0.004, -0.002, -0.002, 0, 0, 0],
                                        [0.008, -0.004, -0.004, 0, 0, 0],
                                        [0.012, -0.006, -0.006, 0, 0, 0],
                                        [0.016, -0.008, -0.008, 0, 0, 0],
                                    ],
                                    [
                                        [0, 0, 0, 0.002, 0, 0],
                                        [0, 0, 0, 0.004, 0, 0],
                                        [0, 0, 0, 0.006, 0, 0],
                                        [0, 0, 0, 0.008, 0, 0],
                                    ]
                                ]
        ```

        - `macroscale_loading`: This defines the external loading applied to the microstructure. It is an array of arrays, where each sub-array represents a loading condition applied to the system. The format of the loading array depends on the problem type (AiiDA type: `ArrayData`):
            - For `thermal` problems, the array typically has 3 components, representing the temperature gradients in the x, y, and z directions.
            - For `mechanical` problems, the array must have 6 components, corresponding to the components of the strain tensor in Mandel notation (e.g., $[[ε_{11}, ε_{22}, ε_{33}, \sqrt{2} ε_{12}, \sqrt{2} ε_{13}, \sqrt{2} ε_{23}]]$).

        In the case of path/time-dependent loading as shown, for example as in plasticity problems, the `macroscale_loading` array can include multiple steps with corresponding loading conditions.

        ### Results Specification

        ```json
        "results": [
            "stress", "strain",
            "stress_average", "strain_average",
            "phase_stress_average", "phase_strain_average",
            "microstructure",
            "displacement",
            "absolute_error",
        ]
        ```

        - `results`: This array lists the quantities that should be stored into the results HDF5 file during the simulation. Each string in the array corresponds to a specific result (AiiDA type: `List`):
            - `stress` and `strain`: The stress and strain fields at each voxel in the microstructure.
            - `stress_average` and `strain_average`: Volume averaged- homogenized stress and strain over the entire microstructure.
            - `phase_stress_average` and `phase_strain_average`: Volume averaged- homogenized stress and strain for each phase within the microstructure.
            - `microstructure`: The original microstructure data.
            - `displacement`: The displacement fluctuation field (for mechanical problems) and temperature fluctuation field (for thermal problems).
            - `absolute_error`: The L-infinity error of finite element nodal residual at each iteration.

        Additional material model specific results can be included depending on the problem type and material model.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Submitting Jobs

        Now that AiiDA is suitably prepared and we're familiar with the FANS parameter specifications, its time to get to work. We will conduct a mock experiment to demonstrate the simplicity and flexibility that using the plugin offers. Breaking down the submission of jobs into two steps makes for a clean workflow.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    load_profile_button = mo.ui.run_button()

    mo.md(
        rf"""
        ### Creating Input Parameters

        We will create all the input parameters we wish to study today at once. To begin, we import everything that will be needed and call the `load_profile()` command to activate the default profile within this script.

        Press this button only after you have created a default profile as described above.

        {load_profile_button}
        """
    )
    return (load_profile_button,)


@app.cell
def imports():
    from aiida.engine import run
    from aiida.plugins import CalculationFactory
    from aiida.orm import (
        Group,
        QueryBuilder,
        SinglefileData,
        Str,
        Float,
        Int,
        List,
        Dict,
        ArrayData,
        CalcJobNode,
        load_node,
        load_code,
    )
    from numpy import array
    from itertools import product
    from random import uniform
    return (
        ArrayData,
        CalcJobNode,
        CalculationFactory,
        Dict,
        Float,
        Group,
        Int,
        List,
        QueryBuilder,
        SinglefileData,
        Str,
        array,
        load_code,
        load_node,
        product,
        run,
        uniform,
    )


@app.cell
def _(load_profile_button, mo):
    mo.stop(not load_profile_button.value)  # run on click
    from aiida import load_profile
    load_profile()
    return (load_profile,)


@app.cell(hide_code=True)
def _(mo):
    mk_group_button = mo.ui.run_button()

    mo.md(
        rf"""
        Next, we will create a "group". This is purely an organisational tool that AiiDA provides. It may come in handy later to see what nodes belong to the inputs we are creating today.

        We use the `QueryBuilder` to find all groups with label "inputs". If none exist, we create one and provide it a short description.

        {mk_group_button}
        """
    )
    return (mk_group_button,)


@app.cell
def group(Group, QueryBuilder, mk_group_button, mo):
    mo.stop(not mk_group_button.value)  # run on click

    groups = QueryBuilder(
    ).append(
        Group, filters={
            Group.fields.label: "inputs"
        }
    ).all(
        flat=True
    )

    if len(groups) == 0:
        inputs = Group(
            label="inputs",
            description="Herein are all the manually defined inputs for FANS."
        ).store()
    elif len(groups) == 1:
        inputs = groups.pop()
    else:
        raise
    return groups, inputs


@app.cell(hide_code=True)
def _(mo):
    mk_microstructure_button = mo.ui.run_button(); mk_microstructure_button

    abs_path = mo.ui.text(placeholder="/path/to/microstructure.h5", label="Absolute Path to Microsturcture:", full_width=True)

    mo.md(rf"""
    Next, we store the microstructure file in the database. Using a similar strategy as with the group definition, the `QueryBuilder` first searches for an existing microstructure. If none are found, we define a new one in the form of a `SinglefileData`. This built-in AiiDA datatype points to a file via a path. Finally, the microstructure node is included with our "inputs" group.

    {abs_path}

    As an added precaution, you must click this button to run the following cell. A few more buttons like this appear throughout this tutorial.

    {mk_microstructure_button}
    """)
    return abs_path, mk_microstructure_button


@app.cell
def microstructure(
    Path,
    QueryBuilder,
    SinglefileData,
    abs_path,
    inputs,
    mk_microstructure_button,
    mo,
):
    mo.stop(not mk_microstructure_button.value)  # run on click

    microstructurequery = QueryBuilder(
    ).append(
        SinglefileData, filters={
            SinglefileData.fields.label: "microstructure"
        }
    ).all(flat=True)

    if len(microstructurequery) == 0:
        microstructurefile = SinglefileData(
            Path(abs_path.value),
            label="microstructure"
        ).store()
    elif len(microstructurequery) == 1:
        microstructurefile = microstructurequery.pop()
    else:
        raise

    inputs.add_nodes(microstructurefile)
    return microstructurefile, microstructurequery


@app.cell(hide_code=True)
def _(mo):
    def_nodes_button = mo.ui.run_button()

    mo.md(
        rf"""
        Now, we will define the rest of our parameters. This is mostly straightforward, but we treat `material_properties` and `macroscale_loading` a little differently.

        - `material_properties`: A mock parameter space study is realised by randomly picking bulk and shear moduli from within a range.
        - `macroscale_loading`: Three distinct loading conditions are explicitly written out.

        When it comes time to run our calculations, we will run the "product" of all these parameters.

        {def_nodes_button}
        """
    )
    return (def_nodes_button,)


@app.cell
def node_definition(
    ArrayData,
    Dict,
    Float,
    Int,
    List,
    Str,
    array,
    def_nodes_button,
    mo,
    product,
    uniform,
):
    mo.stop(not def_nodes_button.value)  # run on click

    nodes = [

    # Microstructure Definition
    Str("/sphere/32x32x32/ms", label="ms_datasetname"),
    List([1.0, 1.0, 1.0], label="ms_L"),

    # Problem Type and Material Model
    Str("mechanical", label="problem_type"),
    Str("LinearElasticIsotropic", label="matmodel")
    ] + [
    Dict({"bulk_modulus": bulk, "shear_modulus": shear}, label="material_properties")
     for bulk, shear in product(
        [[uniform(50, 75), uniform(200, 250)] for _ in range(2)],
        [[uniform(25, 50), uniform(150, 200)] for _ in range(2)]
    )] + [

    # Solver Settings
    Str("cg", label="method"),
    Str("Linfinity", label="error_parameters.measure"),
    Str("absolute", label="error_parameters.type"),
    Float(1e-10, label="error_parameters.tolerance"),
    Int(100, label="n_it"),
    Int(200, label="n_it"),

    # Macroscale Loading Conditions
    ArrayData({
        "0": array([[1,0,0,0,0,0]]),
        "1": array([[0,1,0,0,0,0]]),
        "2": array([[0,0,1,0,0,0]]),
        "3": array([[0,0,0,1,0,0]]),
        "4": array([[0,0,0,0,1,0]]),
        "5": array([[0,0,0,0,0,1]])
    }, label="macroscale_loading"),
    ArrayData({
        "0": array([[1,0,0,0,0,0]]),
        "1": array([[1,0,0,0,0,0]]),
        "2": array([[1,0,0,0,0,0]]),
        "3": array([[1,0,0,0,0,0]]),
        "4": array([[1,0,0,0,0,0]]),
        "5": array([[1,0,0,0,0,0]])
    }, label="macroscale_loading"),
    ArrayData({
        "0": array([[0,0,0,0,0,1]]),
        "1": array([[0,0,0,0,0,1]]),
        "2": array([[0,0,0,0,0,1]]),
        "3": array([[0,0,0,0,0,1]]),
        "4": array([[0,0,0,0,0,1]]),
        "5": array([[0,0,0,0,0,1]])
    }, label="macroscale_loading"),

    # Results Specification
    List(["stress_average", "strain_average", "absolute_error", "phase_stress_average", "phase_strain_average", "microstructure", "displacement", "stress", "strain"], label="results")
    ]
    return (nodes,)


@app.cell(hide_code=True)
def _(mo):
    mk_nodes_button = mo.ui.run_button()

    mo.md(rf"""
    While the cell above defined all the parameters, they still need to be stored in the database. Otherwise, they will be lost when the session ends. AiiDA automatically stores nodes when submitting them to a job, but it is good practice to handle this yourself. Moreover, you get to see your database grow step by step. After clicking the button below, try running `verdi node list` to see all the new additions we've made so far, and `verdi node show <id>` for more information about specific nodes.

    It is important to note that this time we did not make any checks through the QueryBuilder to ensure that indentical nodes don't already exist. This means that if you click the button below repeatedly, you *may* trigger duplicate nodes to be created. Since these are some the first nodes we're making, it is not so critical, but in practice you would want to first fetch existing nodes you want to reuse before creating the remainder of the nodes you wish to study.

    {mk_nodes_button}
    """)
    return (mk_nodes_button,)


@app.cell
def node_storage(inputs, mk_nodes_button, mo, nodes):
    mo.stop(not mk_nodes_button.value)

    for node in nodes:
        node.store()
        inputs.add_nodes(node)
    return (node,)


@app.cell(hide_code=True)
def _():
    # # Microstructure Definition
    # microstructure_definition = [
    #     {
    #         "ms_datasetname": Str("/sphere/32x32x32/ms"),
    #         "ms_L": List([1.0, 1.0, 1.0])
    #     }
    # ]

    # # Problem Type and Material Model
    # problem_type_and_material_model = []
    # some = {
    #     "problem_type": Str("mechanical"),
    #     "matmodel": Str("LinearElasticIsotropic")
    # }
    # bulks = [[uniform(50, 75), uniform(200, 250)] for _ in range(2)]
    # shears = [[uniform(25, 50), uniform(150, 200)] for _ in range(2)]
    # for _bulk, _shear in product(bulks, shears):
    #     material_properties = {"material_properties": Dict(
    #             {
    #                 "bulk_modulus": _bulk,
    #                 "shear_modulus": _shear
    #             }
    #     )}
    #     problem_type_and_material_model.append(some | material_properties)

    # # Solver Settings
    # solver_settings = [
    #     {
    #         "method": Str("cg"),
    #         "error_parameters.measure": Str("Linfinity"),
    #         "error_parameters.type": Str("absolute"),
    #         "error_parameters.tolerance": Float(1e-10),
    #         "n_it": Int(100)
    #     }
    # ]

    # # Macroscale Loading Conditions
    # macroscale_loading_conditions = [
    #     {
    #         "macroscale_loading": ArrayData({
    #             "0": array([[1,0,0,0,0,0]]),
    #             "1": array([[0,1,0,0,0,0]]),
    #             "2": array([[0,0,1,0,0,0]]),
    #             "3": array([[0,0,0,1,0,0]]),
    #             "4": array([[0,0,0,0,1,0]]),
    #             "5": array([[0,0,0,0,0,1]])
    #         })
    #     },
    #     {
    #         "macroscale_loading": ArrayData({
    #             "0": array([[1,0,0,0,0,0]]),
    #             "1": array([[1,0,0,0,0,0]]),
    #             "2": array([[1,0,0,0,0,0]]),
    #             "3": array([[1,0,0,0,0,0]]),
    #             "4": array([[1,0,0,0,0,0]]),
    #             "5": array([[1,0,0,0,0,0]])
    #         })
    #     },
    #     {
    #         "macroscale_loading": ArrayData({
    #             "0": array([[0,0,0,0,0,1]]),
    #             "1": array([[0,0,0,0,0,1]]),
    #             "2": array([[0,0,0,0,0,1]]),
    #             "3": array([[0,0,0,0,0,1]]),
    #             "4": array([[0,0,0,0,0,1]]),
    #             "5": array([[0,0,0,0,0,1]])
    #         })
    #     }
    # ]

    # # Results Specification
    # results_specification = [
    #     {
    #         "results": List(["stress_average", "strain_average", "absolute_error", "phase_stress_average", "phase_strain_average", "microstructure", "displacement", "stress", "strain"])
    #     }
    # ]
    return


@app.cell(hide_code=True)
def _():
    # mo.stop(not mk_params_button.value)

    # for ms, pt, ss, lc, rs in product(
    #     microstructure_definition,
    #     problem_type_and_material_model,
    #     solver_settings,
    #     macroscale_loading_conditions,
    #     results_specification
    # ):
    #     nodes = ms | pt | ss | lc | rs
    #     for label, node in nodes.items():
    #         node.label = label
    #         node.store()
    #         inputs.add_nodes(node)
    return


@app.cell(hide_code=True)
def _(mo):
    mk_params_button = mo.ui.run_button()

    mo.md(
        rf"""
        ### Executing Calculations

        Now that all the input parameters have been specified, it it time to run some calculations. We create lists of dictionaries for each set of paramaters we wish to vary. In our case, the `material_properties` need a list, as does the `macroscale_loading`. Everything else falls into a list of length one. The keys of the dictionaries here are important and are specified by the plugin. More information is available on the documentation, but efforts are being made to synchronise these with the FANS parameter specification.

        Below, the nodes are fetched using a helper function (see Appendix A) which essentially queries the database for a single node with a particular label and value. You could also use the nodes we created above instead, passing them forward as variables, but here we demonstrate how you might run calculations using a either new or old nodes at once.

        Click the button bellow when you are sure that all the nodes above have been successfully created and stored. Try `verdi node list` to see them all.

        {mk_params_button}
        """
    )
    return (mk_params_button,)


@app.cell
def parameter_definition(
    ArrayData,
    Dict,
    QueryBuilder,
    SinglefileData,
    fetch,
    mk_params_button,
    mo,
):
    mo.stop(not mk_params_button.value)

    some_params = [{
        "microstructure": {
            "file": QueryBuilder().append(
                SinglefileData, filters={
                    SinglefileData.fields.label: "microstructure"
                }
            ).first(flat=True),
            "datasetname": fetch("ms_datasetname", "/sphere/32x32x32/ms"),
            "L": fetch("ms_L", [1.0, 1.0, 1.0])
        },
        "problem_type": fetch("problem_type", "mechanical"),
        "matmodel": fetch("matmodel", "LinearElasticIsotropic"),
        "method": fetch("method", "cg"),
        "error_parameters": {
            "measure": fetch("error_parameters.measure", "Linfinity"),
            "type": fetch("error_parameters.type", "absolute"),
            "tolerance": fetch("error_parameters.tolerance", 1e-10)
        },
        # "n_it": fetch("n_it", 100),
        "results": fetch("results", ["stress_average", "strain_average", "absolute_error", "phase_stress_average", "phase_strain_average", "microstructure", "displacement", "stress", "strain"])
    }]

    n_it_params = [
        {"n_it": fetch("n_it", 100)},
        {"n_it": fetch("n_it", 200)}
    ]

    material_properties_params = [
        {"material_properties": mp.pop()}
        for mp in QueryBuilder().append(
            Dict, filters={
                Dict.fields.label: "material_properties"
            }
        ).iterall()
    ]

    macroscale_loading_params = [
        {"macroscale_loading": ml.pop()}
        for ml in QueryBuilder().append(
            ArrayData, filters={
                ArrayData.fields.label: "macroscale_loading"
            }
        ).iterall()
    ]
    return (
        macroscale_loading_params,
        material_properties_params,
        n_it_params,
        some_params,
    )


@app.cell(hide_code=True)
def _(mo):
    calculate_button = mo.ui.run_button()

    mo.md(rf"""
    Once these lists are defined, we use the `product` function to explore every permutation of their contents. Each permutation is coupled with the code node, defined earlier, and given to the `run` function with the plugin specific `FANSCalculation` process class.

    Much like last time, we aren't checking if these calculations have already been run. so clicking the button below repeatedly will request duplicate calulations to be run and duplicate results will be generated.

    {calculate_button}
    """)
    return (calculate_button,)


@app.cell
def calculations(
    CalculationFactory,
    calculate_button,
    config_code,
    load_code,
    macroscale_loading_params,
    material_properties_params,
    mo,
    n_it_params,
    product,
    run,
    some_params,
):
    mo.stop(not calculate_button.value)

    FANSCalculation = CalculationFactory("fans")
    code = {"code": load_code(config_code.value["label"])}

    for sp, nit, mpp, mlp in product(some_params, n_it_params, material_properties_params, macroscale_loading_params):
        all_params = sp | nit | mpp | mlp

        run(FANSCalculation, all_params | code)
    return FANSCalculation, all_params, code, mlp, mpp, nit, sp


@app.cell
def _(mo):
    query_button = mo.ui.run_button()

    mo.md(
        rf"""
        ## Analysing the Results

        Now that our calculations are complete, we can make use of the QueryBuilder again to find and analyse the results.

        {query_button}
        """
    )
    return (query_button,)


@app.cell
def _(CalcJobNode, Int, QueryBuilder, mo, query_button):
    mo.stop(not query_button.value)  # run on click

    calcs = QueryBuilder().append(CalcJobNode).all(flat=True)

    calc = calcs[0]

    print("For a Single Calculation with the Following Inputs...")
    print()
    print("Number of Iterations:")
    print(calc.inputs.n_it.value)

    print()
    print("Material Properties:")
    for k, v in calc.inputs.material_properties.items():
        print(f"{k}\t{v}")

    print()
    print("Macroscale Loading:")
    for arr in calc.inputs.macroscale_loading.get_iterarrays():
        print(arr)


    print()
    print(f"The Available Outputs: {list(calc.outputs._get_keys())}")
    print()
    calc.outputs.results # h5 output

    log = calc.outputs.retrieved.get_object_content("input.json.log").split("\n")

    stresses = []
    strains = []
    for ln in log:
        if "Effective Stress" in ln:
            stresses.append(ln.lstrip("# Effective Stress .. "))
        if "Effective Strain" in ln:
            strains.append(ln.lstrip("# Effective Strain .. "))
    stress_strains = [{"Effective Stress": stress, "Effective Strain": strain} for stress, strain in zip(stresses, strains)]

    print("Effective Stress and Strain per Loading Condition:")
    print(*stress_strains, sep="\n")

    filtered_calcs = QueryBuilder().append(
        Int,
        filters={
            Int.fields.label: "n_it",
            Int.fields.value: {"==": 200}
        },
        tag="n_it"
    ).append(
        CalcJobNode,
        with_incoming="n_it"
    ).all(flat=True)

    print()
    print("Calculation Jobs with n_it = 200:")
    print(*filtered_calcs, sep="\n")
    return (
        arr,
        calc,
        calcs,
        filtered_calcs,
        k,
        ln,
        log,
        strains,
        stress_strains,
        stresses,
        v,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Appendix""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## A. `fetch()`

        This is a helper function to simplify the querying of individual nodes when the label and value are known.
        """
    )
    return


@app.cell
def _(Dict, Float, Int, List, QueryBuilder, Str):
    def fetch(label : str, value):
        """Helper function to return a node whose label and value are known.

        Returns an error if more or less than 1 suitable node is found.
        """
        match value:
            case str():
                datatype = Str
            case int():
                datatype = Int
            case float():
                datatype = Float
            case list():
                datatype = List
            case dict():
                datatype = Dict
            case _:
                raise NotImplementedError

        bone = QueryBuilder().append(
            datatype,
            filters={
                datatype.fields.label: label,
                "attributes.value": value
            } if datatype is not List else {
                datatype.fields.label: label,
                "attributes.list": value
            },
        ).all(flat=True)

        if len(bone) != 1:
            raise RuntimeError

        return bone.pop()
    return (fetch,)


if __name__ == "__main__":
    app.run()
