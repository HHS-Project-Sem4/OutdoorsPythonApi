import pandas as pd

from app.Machine_Learning.Analysis import AnalyzerBase
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


class FrequentItemSetAnalyzer(AnalyzerBase):

    def __init__(self, overrideData=None):
        super().__init__()

        if overrideData is not None:
            self.mergedData = overrideData

    def getFrequentItemSet(self, columns, group_by_column, item_column, min_support=0.2, min_threshold=0.1):
        dataframe = self.mergedData[columns]

        transactions = dataframe.groupby([group_by_column])[item_column].apply(list).values.tolist()

        te = TransactionEncoder()
        te_data = te.fit_transform(transactions)
        df = pd.DataFrame(te_data, columns=te.columns_)

        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)

        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

        final_set = rules[["antecedents", "consequents", "support", "confidence"]]
        final_set = final_set.sort_values('support', ascending=False)

        return final_set
