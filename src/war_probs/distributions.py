import matplotlib.pyplot as plt
import numpy as np


def turn_count_distribution_histogram(
    turn_counts, bins=50, figsize=(14, 8)
) -> plt.Figure:  # type: ignore
    """
    Create a histogram showing the distribution of turn counts across simulations.

    Parameters:
    -----------
    turn_counts : list or np.array
        Array of turn counts from each simulation
    bins : int or sequence
        Number of bins for the histogram (default=50)
    figsize : tuple
        Figure size as (width, height) in inches

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object containing the histogram
    """
    # Convert to numpy array for easier statistics
    turn_counts = np.array(turn_counts)

    # Calculate statistics
    mean = np.mean(turn_counts)
    median = np.median(turn_counts)
    std = np.std(turn_counts)
    q1 = np.percentile(turn_counts, 25)
    q3 = np.percentile(turn_counts, 75)
    minimum = np.min(turn_counts)
    maximum = np.max(turn_counts)
    iqr = q3 - q1

    # Create the figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create histogram
    n, bins_edges, patches = ax.hist(
        turn_counts,
        bins=bins,
        color="steelblue",
        edgecolor="black",
        alpha=0.7,
        label="Turn Count Distribution",
    )

    # Add vertical lines for key statistics
    ax.axvline(
        float(mean), color="red", linestyle="--", linewidth=2, label=f"Mean: {mean:.1f}"
    )
    ax.axvline(
        float(median),
        color="green",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median:.1f}",
    )
    ax.axvline(
        float(q1), color="orange", linestyle=":", linewidth=1.5, label=f"Q1: {q1:.1f}"
    )
    ax.axvline(
        float(q3), color="orange", linestyle=":", linewidth=1.5, label=f"Q3: {q3:.1f}"
    )

    # Shade the IQR region
    ax.axvspan(float(q1), float(q3), alpha=0.2, color="orange", label=f"IQR: {iqr:.1f}")

    # Labels and title
    ax.set_xlabel("Number of Turns", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Game Lengths in War Simulations", fontsize=14, pad=20)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")

    # Add text box with statistics
    stats_text = (
        f"Statistics (n={len(turn_counts):,} games):\n"
        f"Mean: {mean:.2f}\n"
        f"Median: {median:.2f}\n"
        f"Std Dev: {std:.2f}\n"
        f"Min: {minimum}\n"
        f"Max: {maximum}\n"
        f"Q1: {q1:.2f}\n"
        f"Q3: {q3:.2f}\n"
        f"IQR: {iqr:.2f}"
    )

    # Position text box in upper left
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
    ax.text(
        0.02,
        0.98,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=props,
    )

    fig.tight_layout()

    # Print statistics to console as well
    print("Turn Count Distribution Statistics:")
    print("=" * 40)
    print(f"Number of simulations: {len(turn_counts):,}")
    print(f"Mean turns: {mean:.2f}")
    print(f"Median turns: {median:.2f}")
    print(f"Standard deviation: {std:.2f}")
    print(f"Minimum turns: {minimum}")
    print(f"Maximum turns: {maximum}")
    print(f"Q1 (25th percentile): {q1:.2f}")
    print(f"Q3 (75th percentile): {q3:.2f}")
    print(f"IQR (Interquartile range): {iqr:.2f}")
    print(f"Coefficient of variation: {(std/mean)*100:.2f}%")

    return fig
