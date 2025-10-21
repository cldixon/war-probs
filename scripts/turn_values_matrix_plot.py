import matplotlib.pyplot as plt

from war_probs.metrics import turn_values_matrix_plot

PLOT_OUTPUT_FILEPATH: str = "img/turn_values_matrix_plot.png"


def main():
    ## -- get plot
    fig = turn_values_matrix_plot()

    ## -- save to disk
    fig.savefig(PLOT_OUTPUT_FILEPATH, dpi=300, bbox_inches="tight")

    print(f"> Saved plot to {PLOT_OUTPUT_FILEPATH}")

    plt.show()

    return


if __name__ == "__main__":
    main()
