# Imports all the necessary python packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Filename to import the analyzed stories from the previous task
filename = "data/trends_analyzed.csv"

# Python function to setup the environment and load the data
def setup(filename):
    # Loads the data from the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    print(df.head())

    if not os.path.exists("outputs"):
        os.mkdir("outputs")
    return df

def chart1(df):
    top10 = df.sort_values(by="score", ascending=False).head(10)
    plt.figure()
    plt.barh(top10["title"].str[:50], top10["score"], color="steelblue")
    plt.xlabel("Scores")
    plt.ylabel("Story Title")
    plt.title("Top 10 stories by score")
    plt.savefig("outputs/chart1_top_stories.png")
    plt.show()
    return top10


def chart2(df):
    category_counts = df["category"].value_counts()
    plt.figure()
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Number of stories per category")
    plt.xticks(rotation=45)
    plt.savefig("outputs/chart2_categories.png")
    plt.show()
    return category_counts

def chart3(df):
    plt.figure()
    sns.scatterplot(data=df,
        x="score",
        y="num_comments",
        hue="is_popular",
        palette={True: "green", False: "red"}
    )
    plt.xlabel("Score")
    plt.ylabel("Number of comments")
    plt.title("Score vs Comments (Green=Popular, Red=Not Popular)")
    plt.legend(title="Is Popular")
    plt.savefig("outputs/chart3_scatter.png")
    plt.show()

    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    return popular, not_popular



def dashboard(top10, cat_counts, popular, not_popular):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].barh(top10["title"], top10["score"])
    axs[0].set_title("Top Stories")

    axs[1].bar(cat_counts.index, cat_counts.values)
    axs[1].set_title("Categories")
    axs[1].tick_params(axis='x', rotation=45)

    axs[2].scatter(popular["score"], popular["num_comments"])
    axs[2].scatter(not_popular["score"], not_popular["num_comments"])
    axs[2].set_title("Scatter")

    fig.suptitle("TrendPulse Dashboard")
    plt.savefig("outputs/dashboard.png")
    plt.close()



def main():
    df = setup(filename)
    top10 = chart1(df)
    cat_counts = chart2(df)
    popular, not_popular = chart3(df)
    dashboard(top10, cat_counts, popular, not_popular)

if __name__ == "__main__":
    main()