from typer import Typer

from src.commands.dummy import dummy
from src.commands.assets import assets_app
from src.commands.packages import packages_app

app = Typer(help="Dotfiles configuration management CLI")

# Register command groups
app.add_typer(assets_app, name="assets")
app.add_typer(packages_app, name="packages")

# Register individual commands
app.command(help="A dummy command that prints a message")(dummy)


def main():
    app()


if __name__ == "__main__":
    main()
