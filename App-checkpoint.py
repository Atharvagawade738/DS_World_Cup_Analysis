import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QTextEdit
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataScienceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.deliveries = None
        self.matches = None
        self.points = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Science Project: India World Cup Analysis')

        # Create widgets
        self.loadButton = QPushButton('Load Datasets', self)
        self.visualizeButton = QPushButton('Show Visualization', self)
        self.describeButton = QPushButton('Show Descriptive Stats', self)
        self.resultLabel = QLabel('Results will be displayed here', self)
        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        # Connect buttons to functions
        self.loadButton.clicked.connect(self.load_datasets)
        self.visualizeButton.clicked.connect(self.show_visualization)
        self.describeButton.clicked.connect(self.show_descriptive_stats)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.loadButton)
        layout.addWidget(self.visualizeButton)
        layout.addWidget(self.describeButton)
        layout.addWidget(self.resultLabel)
        layout.addWidget(self.resultTextEdit)

        # Set main widget
        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def load_datasets(self):
        # Ask for multiple files
        deliveries_path, _ = QFileDialog.getOpenFileName(self, 'Open Deliveries Dataset', '', 'CSV Files (*.csv)')
        matches_path, _ = QFileDialog.getOpenFileName(self, 'Open Matches Dataset', '', 'CSV Files (*.csv)')
        points_path, _ = QFileDialog.getOpenFileName(self, 'Open Points Dataset', '', 'CSV Files (*.csv)')

        if deliveries_path and matches_path and points_path:
            try:
                # Load datasets
                self.deliveries = pd.read_csv(deliveries_path)
                self.matches = pd.read_csv(matches_path)
                self.points = pd.read_csv(points_path)
                
                # Print columns to debug
                print("Deliveries columns:", self.deliveries.columns)
                print("Matches columns:", self.matches.columns)
                print("Points columns:", self.points.columns)
                
                self.resultLabel.setText('Datasets Loaded Successfully')
            except Exception as e:
                self.resultLabel.setText(f'Error loading datasets: {e}')
        else:
            self.resultLabel.setText('Please load all datasets')

    def show_visualization(self):
        if self.deliveries is None or self.matches is None or self.points is None:
            self.resultLabel.setText('Please load all datasets')
            return

        try:
            # Example visualizations
            plt.figure(figsize=(14, 7))

            # Visualization 1: Distribution of Runs Off Bat
            plt.subplot(1, 3, 1)
            sns.histplot(self.deliveries['runs_off_bat'], bins=20, kde=True)
            plt.title('Distribution of Runs Off Bat')
            plt.xlabel('Runs Off Bat')
            plt.ylabel('Frequency')

            # Visualization 2: Matches Count by Venue
            plt.subplot(1, 3, 2)
            sns.countplot(data=self.matches, x='venue')
            plt.title('Matches Count by Venue')
            plt.xlabel('Venue')
            plt.ylabel('Count')
            plt.xticks(rotation=45)

            # Visualization 3: Points Table
            plt.subplot(1, 3, 3)
            points_summary = self.points.groupby('Team').agg({'Points': 'sum'}).sort_values('Points', ascending=False)
            points_summary.plot(kind='bar', legend=False)
            plt.title('Points by Team')
            plt.xlabel('Team')
            plt.ylabel('Points')

            plt.tight_layout()
            plt.show()

            self.resultLabel.setText('Visualizations displayed successfully')
        except Exception as e:
            self.resultLabel.setText(f'Error: {e}')

    def show_descriptive_stats(self):
        if self.deliveries is None or self.matches is None or self.points is None:
            self.resultLabel.setText('Please load all datasets')
            return

        try:
            # Combine all datasets for descriptive stats
            combined_data = pd.concat([self.deliveries, self.matches, self.points], axis=1, join='inner')
            stats = combined_data.describe(include='all')
            self.resultTextEdit.setPlainText(stats.to_string())
            self.resultLabel.setText('Descriptive statistics displayed successfully')
        except Exception as e:
            self.resultLabel.setText(f'Error: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataScienceApp()
    ex.show()
    sys.exit(app.exec_())
