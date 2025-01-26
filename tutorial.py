import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    tip = mo.accordion({
        "Dependencies...": mo.md("The rest of this tutorial assumes you have read the attached README and have installed the required packages described therein.")
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

        {tip}
        """
    )
    return (tip,)


@app.cell(hide_code=True)
def _(mo):
    note = mo.md(
        """
        **Note:** This section assumes you have not already set up a profile, computer, or code for AiiDA. If you have already done this, you may skip to the next section.
        """
    ).callout("info")
    mo.md(
        rf"""
        ## AiiDA

        Before we can truly begin, we must set up AiiDA on your machine. This means three things.

        1. Create a Profile
        2. Specify a Computer
        3. Define a Code
        
        {note}
        """
    )
    return (note,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1. Create a Profile

        By default, AiiDA stores app data at the user level. Even when AiiDA is installed in a virtual environment, it will still write and read to `.aiida` in your home directory. However, AiiDA provides users a way to seperate their data into "profiles". Let's create a profile for this tutorial.
        """
    )
    return


@app.cell
def _(mo):
    config = (
        mo.md('''
        **Fill in the details below to generate your profile configuration yaml.**

        {profile_name}

        {first_name}

        {last_name}

        {institution}
        ''')
        .batch(
            profile_name=mo.ui.text("aiida-fans-tutorial", label="Profile Name: "),
            first_name=mo.ui.text("John", label="First Name: "),
            last_name=mo.ui.text("Doe", label="Last Name: "),
            institution=mo.ui.text("MIB", label="Institution: "),
        )
        .form(show_clear_button=True, bordered=False)
    )
    config
    return (config,)


@app.cell
def _(config, mo):
    with open("setup-profile.yaml", "w") as f:
        f.write(rf"""profile_name: {config.value["profile_name"]}
    set_as_default: false
    first_name: {config.value["first_name"]}
    last_name: {config.value["last_name"]}
    institution: {config.value["institution"]}
    use_rabbitmq: false
    interactive: false
    """)

    mo.md(
        rf"""
        Here is your profile configuration.
        
        ```yaml
        profile_name: {config.value["profile_name"]}
        set_as_default: false
        first_name: {config.value["first_name"]}
        last_name: {config.value["last_name"]}
        institution: {config.value["institution"]}
        use_rabbitmq: false
        interactive: false
        ```
        
        In your terminal, navigate to this tutorial's directory and activate its environment.

        ```
        verdi profile setup core.sqlite_dos --config setup-profile.yaml
        ```
        """
    )
    return (f,)


@app.cell
def _():
    from aiida import load_profile, engine, orm, plugins
    return engine, load_profile, orm, plugins


if __name__ == "__main__":
    app.run()
