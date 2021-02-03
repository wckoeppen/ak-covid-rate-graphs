#!/usr/bin/env python
# coding: utf-8

import textwrap
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

import os
cwd = os.getcwd()
print(cwd)

# ## Recent AK COVID-19 data
# - https://coronavirus-response-alaska-dhss.hub.arcgis.com/datasets/table-3-demographic-distribution-of-confirmed-cases/geoservice

query_url = (
    "https://services1.arcgis.com/"
    "WzFsmainVTuD5KML/arcgis/rest/services/"
    "Demographic_Distribution_of_Confirmed_Cases/"
    "FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
)

retrieval_date = datetime.now()

r = requests.get(query_url)
case_data = pd.json_normalize(r.json(), record_path="features")

case_data.columns = case_data.columns.str.lstrip("attributes.")
case_data.columns = case_data.columns.str.replace("_", " ")
case_data = case_data.drop(columns=["ObjectId"])
case_data = case_data.set_index("Demographic")
case_data.index.name = None

# convert percentage strings to floats
percent_columns = case_data.filter(regex="Percentage").columns
for percent_column in percent_columns:
    case_data[percent_column] = (
        case_data[percent_column].str.rstrip("%").astype("float")
    )

case_data = case_data.rename(
    index={
        "AI/AN": "Alaska Native or American Indian",
        "NHOPI": "Native Hawaiian or Other Pacific Islander",
        "Black": "Black or African American",
        "Multiple": "Multiple Races",
        "Other": "Other Race",
        "UI Race": "Race Under Investigation",
        "Hispanic": "Hispanic or Latino",
        "Non-Hispanic": "Non-Hispanic Ethnicity",
        "UI Ethnicity": "Ethnicity Under Investigation",
    }
)

# Race and ethnicity population data from AKDLWD
race_pop_est = pd.read_excel("resources/RaceHispAK.xls", header=3)
race_pop_est = race_pop_est.set_index("Unnamed: 0")
race_pop_est.index.name = ""
race_pop_est = race_pop_est.dropna(how="all")
race_pop_est = race_pop_est.drop(columns=["Unnamed: 1"])
race_pop_est = race_pop_est.rename(
    index={
        "White (alone)": "White",
        "Alaska Native or American Indian (alone)": "Alaska Native or American Indian",
        "Black or African American (alone)": "Black or African American",
        "Asian (alone)": "Asian",
        "Native Hawaiian or Other Pacific Islander (alone)": "Native Hawaiian or Other Pacific Islander",
        "Two or More Races": "Multiple Races",
        "Hispanic Origin (of any race)": "Hispanic or Latino",
    }
)
race_pop_est = race_pop_est[["July 2019"]]
race_pop_est = race_pop_est.rename(columns={"July 2019": "Population Estimate"})

# Formatting lists
include_race_list = [
    "Alaska Native or American Indian",
    "Asian",
    "Black or African American",
    "Hispanic or Latino",
    "Native Hawaiian or Other Pacific Islander",
    "White",
    "Multiple Races",
]
other_includes = ["Unknown Race", "Race Under Investigation"]
plot_order = [
    "American Indian and Alaska Native",
    "Asian",
    "Black or African American",
    "Hispanic or Latino",
    "Native Hawaiian and Other Pacific Islander",
    "White",
    #     'Other Race',
    "Multiple Races",
]

# Race data with population
race_pop_data = case_data.loc[include_race_list + other_includes]
race_pop_data = race_pop_data.join(race_pop_est.loc[include_race_list])
race_pop_data[
    [
        "All Cases",
        "All Cases Percentage",
        "Hospitalizations",
        "Hospitalizations Percentage",
        "Deaths",
        "Deaths Percentage",
        "Population Estimate",
    ]
]

# Rate data with population
rate_data = race_pop_data[["All Cases", "Hospitalizations", "Deaths"]].div(
    race_pop_data["Population Estimate"], axis=0
)
rate_data = rate_data.rename(
    columns={
        "All Cases": "Case Rate",
        "Hospitalizations": "Hospitalization Rate",
        "Deaths": "Death Rate",
    }
)


def save_png(figure, png_path):
    """Save figures as PNG files.

    Args:
        figure (matplotlib.pyplot.figure): Matplotlib figure to be saved.
        png_path (string): Path to which to save the file.
    """
    print(f"Saving PNG {png_path}")
    figure.savefig(png_path, bbox_inches="tight", pad_inches=0.3, dpi=72, facecolor="w")
    plt.close(figure)  # comment out if you want outputs on the screen


# Infection, hospitalization, and deaths for each population
def count_plot(_series, _percents, color="#006B95", title="", width=0.9):
    """Plot a series of counts as a vertical bar chart.

    Args:
        _series (pandas.Series): The series of values to plot.
        _percents (pandas.Series): The series of percentages to add to the bars.
        color (str, optional): Color of the bars. Defaults to "#006B95".
        title (str, optional): Title of the plot. Defaults to "".
        width (float, optional): Width of the bars from 0 (non-existent) to 1 (touching). Defaults to 0.9.

    Returns:
        matplotlib.pyplot.figure: the generated figure
    """

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_axes([0, 0, 1, 1])

    x_labels = _series.index
    x_locs = np.arange(len(x_labels))  # the label locations
    y_values = _series.values
    y_percents = _percents.values

    rects1 = ax.bar(x_locs, y_values, width, color=color)

    ax.set_xticks(np.arange(len(x_locs)))
    x_labels = ["\n".join(textwrap.wrap(label, 13)) for label in x_labels]
    ax.set_xticklabels(x_labels, rotation=0, fontweight="normal", fontsize=10)
    ax.set_ylabel("Count", fontsize=16, labelpad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_linewidth(3)
    ax.spines["left"].set_linewidth(2)
    ax.tick_params(axis="x", labelsize=16, length=0)
    ax.tick_params(axis="x", pad=10)
    ax.tick_params(axis="y", labelsize=16, length=10)
    ax.set_title(title, fontsize=36, fontweight="bold", loc="left", pad=25)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height.

        Args:
            rects (matplotlib output): the barplot axes object.
        """
        for i in range(len(rects)):
            rect = rects[i]
            height = y_values[i]
            percent = y_percents[i]
            ax.annotate(
                f"{height:0.0f} ({percent:0.0f}%)",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 20),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="top",
                fontsize=18,
                fontweight="bold",
                color="#000000",
            )

    autolabel(rects1)

    plt.figtext(
        0.0,
        -0.14,
        "Sources:",
        ha="left",
        va="top",
        fontsize=16,
        fontweight="bold",
        linespacing=1.5,
        color="#555555",
    )
    sources_text = "COVID-19 case counts from AK DHSS: coronavirus-response-alaska-dhss.hub.arcgis.com. "
    plt.figtext(
        0.056,
        -0.14,
        sources_text,
        ha="left",
        va="top",
        fontsize=16,
        linespacing=1.5,
        color="#555555",
    )
    plt.figtext(
        0.0,
        -0.165,
        "Notes:",
        ha="left",
        va="top",
        fontsize=16,
        fontweight="bold",
        linespacing=1.5,
        color="#555555",
    )
    notes_text = (
        f"Hispanic or Latino ethnicity is not mutually exclusive of race. Percents are relative to total counts. "
        f"Data retrieved on {retrieval_date.strftime('%b %d, %Y at %-I:%M %p')}"
    )
    plt.figtext(
        0.044,
        -0.165,
        notes_text,
        ha="left",
        va="top",
        fontsize=16,
        linespacing=1.5,
        color="#555555",
    )

    return fig


case_count_plot = count_plot(
    race_pop_data["All Cases"],
    race_pop_data["All Cases Percentage"],
    title="Alaska: COVID-19-associated case counts by race / ethnicity",
)
hosp_count_plot = count_plot(
    race_pop_data["Hospitalizations"],
    race_pop_data["Hospitalizations Percentage"],
    title="Alaska: COVID-19-associated hospitalization counts by race / ethnicity",
    color="#33a02c",
)
deat_count_plot = count_plot(
    race_pop_data["Deaths"],
    race_pop_data["Deaths Percentage"],
    title="Alaska: COVID-19-associated death counts by race / ethnicity",
    color="#B85009",
)

save_png(
    case_count_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-case-count-by-race.png",
)
save_png(
    hosp_count_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-hospitalization-count-by-race.png",
)
save_png(
    deat_count_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-death-count-by-race.png",
)


def rate_plot(_series, color="#006B95", title="", width=0.9):

    # categories
    x_labels = _series.index
    x_labels = ["\n".join(textwrap.wrap(label, 18)) for label in x_labels]
    x_locs = np.arange(len(x_labels))  # the label locations
    # y-values
    y_values = _series.values * 100

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_axes([0, 0, 1, 1])

    rects1 = ax.bar(x_locs, y_values, width, color=color)

    #    xlabels = [re.sub("(.{10})", "\\1\n", label, 0, re.DOTALL) for label in xlabels]
    ax.set_xticks(np.arange(len(x_locs)))
    ax.set_xticklabels(x_labels, rotation=0)
    ax.set_ylabel("Rate per 100 population", fontsize=16, labelpad=12)
    # grid
    #     ax.grid(axis='y')
    #     ax.set_axisbelow(True)
    #     ax.yaxis.grid(color='lightgray', linestyle='dashed')

    # Hide stuff
    #     ax.yaxis.label.set_visible(False)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.spines["bottom"].set_linewidth(3)
    ax.spines["left"].set_linewidth(2)

    # Tick size
    ax.tick_params(axis="x", labelsize=16, length=0)
    ax.tick_params(axis="x", pad=10)

    ax.tick_params(axis="y", labelsize=16, length=10)

    ax.set_title(title, fontsize=29, fontweight="bold", loc="left", pad=25)

    def autolabel(rects):

        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:0.3f}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 20),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="top",
                fontsize=18,
                fontweight="bold",
                color="#000000",
            )

    autolabel(rects1)

    plt.figtext(
        0.0,
        -0.11,
        "Sources:",
        ha="left",
        va="top",
        fontsize=16,
        fontweight="bold",
        linespacing=1.5,
        color="#555555",
    )
    sources_text = (
        "(1) COVID-19 case counts from AK DHSS: coronavirus-response-alaska-dhss.hub.arcgis.com. "
        "(2) Population estimates from July 2019: live.laborstats.alaska.gov/pop/\n"
    )
    plt.figtext(
        0.056,
        -0.11,
        sources_text,
        ha="left",
        va="top",
        fontsize=16,
        linespacing=1.5,
        color="#555555",
    )
    plt.figtext(
        0.0,
        -0.14,
        "Notes:",
        ha="left",
        va="top",
        fontsize=16,
        fontweight="bold",
        linespacing=1.5,
        color="#555555",
    )
    notes_text = (
        f'"Unknown Race" or "Race Under Investigation" are not included. '
        f"Hispanic or Latino ethnicity is not mutually exclusive of race. "
        f"Data retrieved on {retrieval_date.strftime('%b %d, %Y at %-I:%M %p')}"
    )
    plt.figtext(
        0.044,
        -0.14,
        notes_text,
        ha="left",
        va="top",
        fontsize=16,
        linespacing=1.5,
        color="#555555",
    )
    return fig


to_plot = rate_data.drop(labels=["Unknown Race", "Race Under Investigation"])

case_rate_plot = rate_plot(
    to_plot["Case Rate"],
    title="Alaska: COVID-19-associated case rates per 100 people by race / ethnicity",
)
hosp_rate_plot = rate_plot(
    to_plot["Hospitalization Rate"],
    title="Alaska: COVID-19-associated hospitalization rates per 100 people by race / ethnicity",
    color="#33a02c",
)
deat_rate_plot = rate_plot(
    to_plot["Death Rate"],
    title="Alaska: COVID-19-associated death rates per 100 people by race / ethnicity",
    color="#B85009",
)

save_png(
    case_rate_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-case-rate-by-race.png",
)
save_png(
    hosp_rate_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-hospitalization-rate-by-race.png",
)
save_png(
    deat_rate_plot,
    f"outputs/archived/{retrieval_date.strftime('%Y%m%d')}-death-rate-by-race.png",
)

# Write currents out for Github README.md
save_png(case_count_plot, "outputs/latest-case-count-by-race.png")
save_png(hosp_count_plot, "outputs/latest-hospitalization-count-by-race.png")
save_png(deat_count_plot, "outputs/latest-death-count-by-race.png")
save_png(case_rate_plot, "outputs/latest-case-rate-by-race.png")
save_png(hosp_rate_plot, "outputs/latest-hospitalization-rate-by-race.png")
save_png(deat_rate_plot, "outputs/latest-death-rate-by-race.png")
