# Importing necessary packages
import pandas as pd
import numpy as np

# Filename to import the cleaned stories from the previous task
filename = r"data\trends_clean.csv"

# Python function to load data from CSV file
def load_and_explore_data(filename):
    
    # Load the cleaned data from CSV file into pandas DataFrame
    df = pd.read_csv(filename)
    # Drops the unnecessary column "Unnamed: 0"
    df.drop("Unnamed: 0", axis=1, inplace=True)
    # df.shape give the number of rows and columns in the dataframe.
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    # head() method prints the first 5 rows of the dataframe
    print(df.head())

    # Calculates the mean score and average number of comments for the stories
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score: {avg_score}")
    print(f"Average comments: {avg_comments}")

    # Finally returns the DataFrame
    return df


def basic_analysis(df):

    # Calculates the mean, median, and standard deviation of the scores of the stories using built-in numpy functions.
    mean = np.mean(df["score"])
    median = np.median(df["score"])
    std = np.std(df["score"])

    max_score = np.max(df["score"])
    min_score = np.min(df["score"])

    most_stories = df["category"].value_counts().idxmax()
    count_category = df["category"].value_counts().max()

    most_commented_story = df.iloc[df["num_comments"].idxmax()]
    print(most_commented_story['title'], most_commented_story['num_comments'])
    
    print("\n--- NumPy Stats ---")
    print("Mean score   :", round(mean))
    print("Median score :", round(median))
    print("Std deviation:", round(std))
    print("Max score    :", max_score)
    print("Min score    :", min_score)
    print(f"\nMost stories in category: {most_stories} ({count_category} stories)")
    print(f"Most commented story: {most_commented_story['title']} — {most_commented_story['num_comments']} comments")
    

def add_new_columns(df):    
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    avg_score = df["score"].mean()
    df["is_popular"] = df["score"] > avg_score
    
    return df

def save_updated_data(df, filename):
    df.to_csv(filename, index=False)
    print(f"\nSaved to {filename}")


def main():
    df = load_and_explore_data(filename)
    basic_analysis(df)
    updated_df = add_new_columns(df)
    save_updated_data(updated_df, r"data\trends_updated.csv")


if __name__ == "__main__":
    main()



"""--- NumPy Stats ---
Mean score   : 12,450
Median score : 8,200
Std deviation: 9,870
Max score    : 87,432
Min score    : 5

Most stories in: technology (22 stories)

Most commented story: "AI model beats humans at coding"  — 4,891 comments

Saved to data/trends_analysed.csv"""
