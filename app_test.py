import pandas as pd 

def main():
    print(pd.__version__)
    df = pd.read_csv("data/iris.csv")
    print(df)

if __name__ == "__main__":
    main()