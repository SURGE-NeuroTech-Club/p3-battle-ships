

# p3-battle-ships 

This repository contains the source code for an **P300-based Battleship** game, built with Pygame.

-----

## Getting Started


### Prerequisites

You will need to have Python 3.10 or newer installed on your system.

  * [Python 3.13](https://www.python.org/)

### Installation

Follow these steps to set up your development environment.

1.  **Clone the repository** (replace with your own URL)

    ```sh
    git clone https://github.com/SURGE-NeuroTech-Club/p3-battle-ships.git
    cd p3-battle-ships
    ```

2.  **Create and activate a virtual environment**

      * On Windows:

        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```

      * On macOS & Linux:

        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages**

    The only package required is Pygame. You can install it using the provided `requirements.txt` file.

    **`requirements.txt`:**

    **Installation Command:**

    ```sh
    pip install -r requirements.txt
    ```


## Usage

To run the application, execute the `main.py` script from the root directory of the project:

```sh
python main.py
```

### Controls

The game accepts two forms of input for placing ships or disabling cells:

  * **Keyboard:**
      * **Arrow Keys:** Move the green cursor around the grid.
      * **Spacebar / Enter:** Place a ship at the cursor's current location.
  * **Mouse:**
      * **Left Click (on Buttons):** Click any of the "A1", "A2", etc. buttons at the bottom to disable the corresponding cell on the grid, preventing a ship from being placed there.