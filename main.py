##
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

##
def read_chat(path):
    '''
    :Path of the chat file, exported from android:
    :Returns the chat file as a pandas DataFrame:
    '''
    chat = open(r"data/HierNimmt.txt", "r", encoding= "UTF-8").read()
    date_format = re.compile(r"\d{2}/\d{2}/\d{4},\s\d{2}:\d{2}")
    dates = date_format.findall(chat)
    messages = date_format.split(chat)
    chat_df = pd.DataFrame()
    chat_df["datetime"] = dates
    chat_df["messages"] = messages[1:]
    return chat_df

def transform_chat(chat):
    #&& Testing
    chat["datetime"] = pd.to_datetime(chat["datetime"],
                                      format= "%d/%m/%Y, %H:%M")
    chat_df = pd.concat(
        [chat, chat["messages"].str.split(":", 1, True)], axis = 1
    )
    chat_df.rename(
        {"messages" : "unaltered_messages", 0 : "user", 1 : "message"},
        inplace = True, axis = 1
    )
    chat_df.user.replace(
        regex=True, inplace=True, to_replace=r"\s-\s", value=r""
    )
    return chat_df

##

chat_path = r"data/HierNimmt.txt"
chat = read_chat(chat_path)
chat_df = transform_chat(chat)

##

chat_df.to_excel("data/HierNimmt.xlsx", index = False)

##

chat_df["message_length"] = chat_df.message.str.len()
print(chat_df.loc[~chat_df["user"].str.contains("subject")]
      .groupby("user")["message_length"].sum().dropna()
      .sort_values(ascending = False).head(7))

##

chat_df["datetime"].sort_values(ascending = False).head(50)