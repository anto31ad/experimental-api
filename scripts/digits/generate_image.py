import random
from sklearn.datasets import load_digits
import json
import matplotlib.pyplot as plt

# Load the dataset
digits = load_digits()
X, y = digits.data, digits.target

# Choose a random index
i = random.randint(0, len(X) - 1)
sample_features = X[i].tolist()
sample_label = y[i]

# # Optionally: display the digit
# plt.imshow(digits.images[i], cmap='gray')
# plt.title(f"Label: {sample_label}")
# plt.axis('off')
# plt.show()

# Output the JSON-like structure
sample_json = {
    "features": ';'.join(str(x) for x in sample_features),
    "label": int(sample_label)
}

# Print it as JSON string
with open('data/digit_data.json', "w") as file:
    file.write(json.dumps(sample_json, indent=2))
