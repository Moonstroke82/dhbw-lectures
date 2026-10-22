"""Draw the figures for session 15 (accessing data: files and APIs).

Run from the Lectures folder: python data-management/slides/img/make_api_figures.py
Needs matplotlib and pandas. Colours from tools/theme.py (DHBW corporate design).

api-call-anatomy.png: own illustration of one HTTP request and response, based on
Fielding (2000, Chapter 5) and RFC 9110 (Fielding et al., 2022); the example call is the
Bright Sky weather API (de Maeyer, n.d.).
api-weather-week.png: daily rain and maximum temperature in Mannheim, 5-11 October 2026,
computed from data-management/worksheets/data/brightsky-mannheim-2026-10-05.json
(Bright Sky response, data: Deutscher Wetterdienst, CC BY 4.0). Days in local time
(Europe/Berlin); the extra record at 2026-10-12 00:00 is left out.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
MONO = "DejaVu Sans Mono"

DATA = HERE.parents[1] / "worksheets" / "data" / "brightsky-mannheim-2026-10-05.json"


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, fill=LIGHT, edge=BORDER, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=fill, edgecolor=edge, lw=lw))


def api_call_anatomy():
    """Client and server with the parts of the request and of the response."""
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    # client and server
    box(ax, 0.1, 1.2, 1.9, 2.8, fill="white", edge=GREY, lw=1.6)
    ax.text(1.05, 3.55, "Client", ha="center", fontsize=13, weight="bold", color=GREY)
    ax.text(1.05, 2.6, "Python script\nor notebook\n(requests)", ha="center", va="center", fontsize=10.5, color=TEXT)
    box(ax, 9.0, 1.2, 1.9, 2.8, fill="white", edge=GREY, lw=1.6)
    ax.text(9.95, 3.55, "Server", ha="center", fontsize=13, weight="bold", color=GREY)
    ax.text(9.95, 2.6, "Web API\n(Bright Sky)\nreads DWD data", ha="center", va="center", fontsize=10.5, color=TEXT)

    # request
    ax.annotate("", xy=(8.95, 4.55), xytext=(2.05, 4.55),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2, mutation_scale=18))
    ax.text(2.2, 4.7, "1  Request", fontsize=12, weight="bold", color=RED)
    box(ax, 2.2, 3.15, 6.72, 1.2)
    ax.text(2.35, 4.08, "GET", fontsize=11, family=MONO, weight="bold", color=RED)
    ax.text(2.95, 4.08, "https://api.brightsky.dev/weather?lat=49.49&lon=8.47", fontsize=10, family=MONO, color=TEXT)
    ax.text(2.95, 3.8, "&date=2026-10-05&last_date=2026-10-12&tz=Europe/Berlin", fontsize=10, family=MONO, color=TEXT)
    ax.text(2.35, 3.35, "method  ·  base URL + endpoint  ·  query parameters  ·  headers (e.g. an API key)",
            fontsize=9.5, color=MUTED)

    # response
    ax.annotate("", xy=(2.05, 0.75), xytext=(8.95, 0.75),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2, mutation_scale=18))
    ax.text(8.8, 0.35, "2  Response", fontsize=12, weight="bold", color=GREY, ha="right")
    box(ax, 2.2, 1.0, 6.72, 1.9)
    ax.text(2.35, 2.6, "200 OK", fontsize=11, family=MONO, weight="bold", color=GREY)
    ax.text(3.6, 2.6, "status code: did it work?", fontsize=9.5, color=MUTED)
    ax.text(2.35, 2.25, "Content-Type: application/json", fontsize=10, family=MONO, color=TEXT)
    ax.text(6.0, 2.25, "headers: metadata", fontsize=9.5, color=MUTED)
    ax.text(2.35, 1.85, '{"weather": [{"timestamp": "2026-10-05T00:00:00+02:00",', fontsize=10, family=MONO, color=TEXT)
    ax.text(2.35, 1.57, '              "temperature": 13.1, ...}, ...],', fontsize=10, family=MONO, color=TEXT)
    ax.text(2.35, 1.29, ' "sources": [{"station_name": "Mannheim", ...}]}', fontsize=10, family=MONO, color=TEXT)
    ax.text(8.65, 1.12, "body: the data", fontsize=9.5, color=MUTED, ha="right")
    save(fig, "api-call-anatomy.png")


def weather_week():
    """Daily rain (bars) and maximum temperature (line) for the bike shop's week."""
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    w = pd.DataFrame(data["weather"])
    w["timestamp"] = pd.to_datetime(w["timestamp"])
    w["day"] = w["timestamp"].dt.date
    daily = w.groupby("day").agg(rain_mm=("precipitation", "sum"), t_max=("temperature", "max")).iloc[:7]
    labels = [pd.Timestamp(d).strftime("%a\n%d %b") for d in daily.index]
    x = range(len(daily))

    fig, ax = plt.subplots(figsize=(10, 3.9), dpi=200)
    bars = ax.bar(x, daily["rain_mm"], color=[RED if v >= 1 else GREY for v in daily["rain_mm"]], width=0.55, zorder=2)
    for xi, v in zip(x, daily["rain_mm"]):
        ax.text(xi, v + 0.25, f"{v:.1f} mm", ha="center", fontsize=10, color=TEXT)
    ax.set_ylim(0, 14)
    ax.set_ylabel("Rain per day (mm)", fontsize=10, color=TEXT)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=10, color=TEXT)
    ax.tick_params(axis="y", labelsize=9, colors=TEXT)
    ax2 = ax.twinx()
    ax2.plot(list(x), daily["t_max"], color=TEXT, marker="o", lw=1.6, zorder=3)
    for xi, v in zip(x, daily["t_max"]):
        ax2.text(xi, v + 1.3, f"{v:.1f} °C", ha="center", fontsize=9.5, color=TEXT,
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax2.set_ylim(0, 30)
    ax2.set_ylabel("Maximum temperature (°C)", fontsize=10, color=TEXT)
    ax2.tick_params(axis="y", labelsize=9, colors=TEXT)
    for a in (ax, ax2):
        a.spines["top"].set_visible(False)
        a.spines["left"].set_color(MUTED)
        a.spines["right"].set_color(MUTED)
        a.spines["bottom"].set_color(MUTED)
    ax.grid(axis="y", color=BORDER, lw=0.8, zorder=0)
    ax.text(6.4, 13.2, "red: at least 1 mm of rain", fontsize=9.5, color=RED, ha="right")
    save(fig, "api-weather-week.png")


if __name__ == "__main__":
    api_call_anatomy()
    weather_week()
