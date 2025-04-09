# Importing necessary libraries
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()
X = iris.data  # Features (Petal and Sepal length and width)
y = iris.target  # Target labels (0, 1, 2 for the three Iris species)

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the model (Decision Tree Classifier)
model = DecisionTreeClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict using the test data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy of the model: {accuracy * 100:.2f}%')

# Optional: Visualize the decision tree (requires graphviz library)
# from sklearn.tree import export_graphviz
# import graphviz

# dot_data = export_graphviz(model, out_file=None, feature_names=iris.feature_names,
#                            class_names=iris.target_names, filled=True, rounded=True, special_characters=True)
# graph = graphviz.Source(dot_data)
# graph.render("iris_tree")

# Create a scatter plot, coloring by the actual labels in the test set
scatter = plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.Paired)

plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Iris Flower Species')

# Create a legend for the species
# Use iris.target_names to convert numeric labels to species names
species = iris.target_names

# Map numeric labels to species names and set the labels for the legend
plt.legend(handles=scatter.legend_elements()[0], labels=species.tolist())

plt.show()