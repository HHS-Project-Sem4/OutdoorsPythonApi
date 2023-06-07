import pandas as pd
import app.Tools.EtlUtil as etlUtil
import unittest


class TestSplitDataFrame(unittest.TestCase):
    def setUp(self):
        self.sourceFrame = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Name': ['John', 'Jane', 'Bob', 'Alice', 'Eve'],
            'Age': [25, 30, 35, 40, 45],
            'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
        })

    def test_splitDataFrame(self):
        idColumnName = 'ID'
        childColumns = ['Name', 'Age']

        result = etlUtil.splitDataFrame(self.sourceFrame, idColumnName, childColumns)

        # Check if originalFrame is correct
        expected_originalFrame = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
        })
        pd.testing.assert_frame_equal(result[0], expected_originalFrame)

        # Check if splitFrame is correct
        expected_splitFrame = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Name': ['John', 'Jane', 'Bob', 'Alice', 'Eve'],
            'Age': [25, 30, 35, 40, 45]
        })
        pd.testing.assert_frame_equal(result[1], expected_splitFrame)


class TestAddUniqueIntIdColumn(unittest.TestCase):
    def setUp(self):
        self.dataFrame = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Name': ['John', 'Jane', 'Bob', 'Alice', 'Eve'],
            'Age': [25, 30, 35, 40, 45],
            'City': ['New York', 'London', 'Paris', 'London', 'London']
        })

    def test_addUniqueIntIdColumn(self):
        columnName = 'City'
        newColumn = 'UniqueID'

        result = etlUtil.addUniqueIntIdColumn(self.dataFrame, columnName, newColumn)

        # Check if the new column is added
        self.assertTrue(newColumn in result.columns)

        # Check if the new column values are unique and incrementing
        expected_unique_ids = pd.Series([0, 1, 2, 1, 1], dtype='Int64', name='UniqueID')

        pd.testing.assert_series_equal(result[newColumn], expected_unique_ids)


class TestCreateDayDateDataframe(unittest.TestCase):
    def setUp(self):
        self.sourceFrame = pd.DataFrame({
            'DAY_date': ['2023-01-01', '2023-02-15', '2023-03-25', '2023-04-10', '2023-05-20'],
        })

    def test_createDayDateDataframe(self):
        sourceColumn = 'DAY_date'
        dateFormat = '%Y-%m-%d'

        result = etlUtil.createDayDateDataframe(self.sourceFrame, sourceColumn, dateFormat)

        # Check if the resulting DataFrame has the expected columns
        expected_columns = ['DAY_date', 'DAY_MONTH_nr', 'DAY_QUARTER_nr', 'DAY_YEAR_nr']
        self.assertListEqual(list(result.columns), expected_columns)

        # Check if the resulting DataFrame has the expected number of rows
        expected_rows = len(self.sourceFrame)
        self.assertEqual(len(result), expected_rows)

        # Check if the DAY_date column values are correct
        expected_dates = pd.to_datetime(self.sourceFrame[sourceColumn], format=dateFormat)
        pd.testing.assert_series_equal(result['DAY_date'], expected_dates)

        # Check if the DAY_MONTH_nr, DAY_QUARTER_nr, and DAY_YEAR_nr columns values are correct
        expected_month_nr = expected_dates.dt.month
        expected_quarter_nr = (expected_dates.dt.month - 1) // 3 + 1
        expected_year_nr = expected_dates.dt.year

        expected_month_nr.name = 'DAY_MONTH_nr'
        expected_quarter_nr.name = 'DAY_QUARTER_nr'
        expected_year_nr.name = 'DAY_YEAR_nr'

        pd.testing.assert_series_equal(result['DAY_MONTH_nr'], expected_month_nr)
        pd.testing.assert_series_equal(result['DAY_QUARTER_nr'], expected_quarter_nr)
        pd.testing.assert_series_equal(result['DAY_YEAR_nr'], expected_year_nr)


if __name__ == '__main__':
    unittest.main()
